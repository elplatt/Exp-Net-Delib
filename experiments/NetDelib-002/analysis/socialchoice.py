import numpy.random as nprand
import scipy.stats as spstats

class Preference(object):
    """
    Represents a rank-ordered preference.
    
    Parameters
    ----------
    ranked : ranked list of alternatives
    
    """
    
    def __new__(cls, ranked, _cache={}):
        """Load existing object or create new if necessary"""
        try:
            return _cache[ranked]
        except KeyError:
            obj = super(Preference, cls).__new__(cls)
            obj.__init__(ranked)
            _cache[ranked] = obj
            return obj
        
    def __init__ (self, ranked):
        self.ranked = tuple(ranked)
    
    def __hash__ (self):
        return hash(self.ranked)
    
    def __repr__ (self):
        return repr(self.ranked)
    
    def __str__ (self):
        return str(self.ranked)
    
    def __len__ (self):
        return len(self.ranked)
    
    def __getitem__ (self, key):
        return self.ranked[key]
    
    def alternatives (self):
        """
        Return a set of all ranked alternatives.
        """
        return set(self.ranked)
    
    def ranks (self):
        alternatives = sorted(self.alternatives())
        rank_alt = [(rank, alt) for rank, alt in enumerate(self.ranked)]
        rank_alt = sorted(rank_alt, key=lambda x: x[1])
        ranks = [rank for rank, alt in rank_alt]
        return ranks

    
class Profile(object):
    """
    Represents a social preference profile. The profile counts the number ballots expressing
    each `Preference`.
    """
    
    def __init__ (self):
        self.preference_counts = {}
        
    def add(self, preference):
        self.preference_counts[preference] = self.preference_counts.get(preference, 0) + 1
        
    def alternatives (self):
        preference_alternatives = [p.alternatives() for p in self.preference_counts.keys()]
        return set().union(*preference_alternatives)
        
    def counts (self):
        return self.preference_counts.items()
    
    @classmethod
    def from_score(cls, df):
        """Create a profile from a score dataframe.

        Parameters
        ----------
        df: Pandas dataframe with columns: "treatment", "stage", "participant_id", "prop1_score", "prop2_score", ...

        Returns
        -------
        A new Profile instance.
        """
        participant_ids = sorted(set(df.participant_id))
        participant_preferences = {}
        proposals = df.columns[3:]

        # Get preference tuples for each participant
        for pid in participant_ids:
            participant_df = df[df.participant_id == pid]
            try:
                prop_scores = [
                    (p, participant_df[p].to_numpy()[0])
                    for p in proposals]
            except IndexError:
                # Participant did not participate in this round
                continue
            # Sort in order of decreasing score
            
            prop_rank = reversed(sorted(prop_scores, key=lambda x: x[1]))
            ranked = tuple([prop[0:-6] for prop, rank in prop_rank])
            participant_preferences[pid] = Preference(ranked)
            
        # Add preferences to profile
        profile = Profile()
        for pid, preference in participant_preferences.items():
            profile.add(preference)
            
        return profile

    def ballot_count(self):
        return sum([count for preference, count in self.counts()], 0)
    
    def sample_bootstrap(self):
        n = self.ballot_count()
        preferences = list(self.preference_counts.keys())
        # Sampling probabilities for each preference
        p = [self.preference_counts[pref] / n for pref in preferences]
        # Initialize new profile
        bootstrap = Profile()
        # Take n samples with replacement
        count = len(preferences)
        for i in range(n):
            bootstrap.add(preferences[nprand.choice(count, p=p)])
        return bootstrap
            
    def agreement_spearman(self):
        total = 0
        count = 0
        for pref_a, count_a in self.counts():
            for pref_b, count_b in self.counts():
                if pref_a == pref_b:
                    continue
                r, p = spstats.spearmanr(pref_a.ranks(), pref_b.ranks())
                total += count_a * count_b * r
                count += count_a * count_b
        return total / count
    
    def agreement_kendall(self):
        total = 0
        count = 0
        for pref_a, count_a in self.counts():
            for pref_b, count_b in self.counts():
                if pref_a == pref_b:
                    continue
                r, p = spstats.kendalltau(pref_a.ranks(), pref_b.ranks())
                total += count_a * count_b * r
                count += count_a * count_b
        return total / count
    
class SocialWelfare(object):
    """
    Base class for social welfare and social choice calculations.
    
    Parameters
    ----------
    profile : ranked-choice voting profile
    """
    
    def __init__(self, profile):
        self.profile = profile
    
    def welfare_score (self):
        """Calculate a social welfare score for each alternative present in profile.
        
        returns a dict mapping alternatives to their scores according to the provided profile.
        """
        raise NotImplemented
    
    def social_preference (self):
        """Calculate the social preference ranking of the alternatives in profile.
        
        returns a tuple of sets listing alternatives in order of decreasing social preference,
            possibly inluding ties.
        """
        score = self.welfare_score()
        ordered_scores = sorted(score.items(), reverse=True, key=lambda x: x[1])
        social_preference = []
        last_score = ordered_scores[0][1]
        current_set = set()
        for alternative, score in ordered_scores:
            # If the score has changed, create a new set of alternatives
            if score == last_score:
                current_set.add(alternative)
            else:
                social_preference.append(current_set)
                current_set = set([alternative])
            last_score = score
        social_preference.append(current_set)
        return social_preference      
    
    def social_choice (self):
        """Calculate the social preference ranking of the alternatives in profile.
        
        returns a set containing the alternative(s) with the highest social welfare score.
        """
        social_preference = self.social_preference()
        return social_preference[0]
    
class Majority(SocialWelfare):
    """Social welfare function for majority vote. An alternative's score is the number
    of preferences in the profile that place the alternative in first place.
    """
    
    def welfare_score (self):
        profile = self.profile
        score = {}
        for pref, count in profile.counts():
            top = pref[0]
            try:
                score[top] += count
            except KeyError:
                score[top] = count
        return score

    
class Borda(SocialWelfare):
    
    def welfare_score (self):
        profile = self.profile
        borda = {}
        for pref, count in profile.counts():
            for i, alternative in enumerate(reversed(pref)):
                try:
                    borda[alternative] += i * count
                except KeyError:
                    borda[alternative] = i * count
        return borda
    
    
import itertools
import networkx as nx

class Tideman(SocialWelfare):
    
    def pairwise_margin (self):
        """Find the win/loss margin for each pair of alternatives.
        
        Returns
        -------
        A dict mapping (a,b) to <prefers(a) - prefers(b)>
        """
        # Create a list of distinct pairs
        alternatives = self.profile.alternatives()
        pairs = set(itertools.product(alternatives, alternatives))
        for alt in alternatives:
            pairs.remove((alt, alt))
        # Initialize margins
        margins = dict((contest, 0) for contest in pairs)
        # Update margins for each preference in the profile
        for pref, count in self.profile.counts():
            # Each element wins relative to those that come after it
            for win in range(len(pref)):
                for lose in range(win + 1, len(pref)):
                    margins[(pref[win], pref[lose])] += count
        return margins
        
    def social_preference_graph (self):
        profile = self.profile
        margins = self.pairwise_margin()
        ordered_margins = sorted(margins.items(), key=lambda x: x[1], reverse=True)
        G = nx.DiGraph()
        counted = 0
        skipped = 0
        for contest, margin in ordered_margins:
            if margin <= 0:
                # Only count winning margins
                continue
            s, t = contest
            try:
                if nx.has_path(G, t, s):
                    # Skip contest, would create cycle
                    skipped += margin
                    continue
            except nx.NodeNotFound:
                pass
            # Add node to graph
            G.add_edge(s, t)
            counted += margin
        return G, counted, skipped

    def social_preference (self):
        G, counted, skipped = self.social_preference_graph()
        root = next(nx.topological_sort(G))
        result = []
        done = set()
        shell = set([root])
        while len(shell) > 0:
            next_shell = set()
            # Remove alternatives ranked lower than others in shell
            for s in list(shell):
                for t in list(shell):
                    if G.has_edge(s, t):
                        shell.remove(t)
            # Update list of completed alternatives
            done = done | shell
            # Build next shell
            for s in shell:
                next_shell = (next_shell | set(G.successors(s))) - done
            # Add current shell to preference
            result.append(shell)
            shell = next_shell
        return result

    def agreement_tideman (self):
        G, counted, skipped = self.social_preference_graph()
        return counted / (counted + skipped)
    