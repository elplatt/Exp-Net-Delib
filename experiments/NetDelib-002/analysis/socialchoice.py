import itertools
import math
import numpy.random as nprand
import scipy.stats as spstats

class Preference(object):
    """
    Represents a rank-ordered preference.
    
    Parameters
    ----------
    ranked : ranked list of alternatives (0 is highest rank)
    
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

    def kendall_tau (self, other):
        """Kendall tau distance between this preference and `other`
        
        Parameters
        ----------
        other: a Preference or tuple of alternatives
        
        Returns
        -------
        The integer kendall tau distance.
        
        Notes
        -----
        This implementation uses the naive algorithm. Faster algorithms exist.
        """
        
        # Calculate pairwise contests
        alts = self.ranked
        self_pairs = set()
        for i, alt_i in enumerate(self.ranked):
            # alt_i beats any elements that come after it
            for j, alt_j in enumerate(self.ranked[i + 1:]):
                self_pairs.add( (alt_i, alt_j) )

        other_pairs = set()
        for i, alt_i in enumerate(other):
            for j, alt_j in enumerate(other[i + 1:]):
                other_pairs.add( (alt_i, alt_j) )
            
        # Calculate number of discordant pairs
        return len(self_pairs - other_pairs)
    
    def forward_swap_vector (self, other):
        """Returns a vector representing the number of forward swaps (i -> i+1) at
        index i over the course of bubble sorting `other` to match `self`.
        
        The sum of this vector is the kendall tau distance.
        """
        # Convert other to list
        if other.__class__ == Preference:
            other = list(other.ranked)
        else:
            other = list(other)
        # Initialize results and iterate through indexes
        v = [0] * (len(self.ranked) - 1)
        for i, alt in enumerate(self.ranked):
            # Swap all pairs between indexes of alt
            other_i = other.index(alt)
            other = other[0:i] + [alt] + other[i:other_i] + other[other_i + 1:]
            # Create swap vector
            # Only pairs between current index and other index are swapped
            swap_count = other_i - i
            vi = [0] * i + [1] * swap_count
            vi += [0] * (len(self.ranked) - len(vi) - 1)
            # Add vi to v
            for j, vij in enumerate(vi):
                v[j] += vij
        return tuple(v)
    
    def weighted_swap_distance (self, other, weight=0.5):
        v = reversed(self.forward_swap_vector(other))
        distance = 0
        for i, vi in enumerate(v):
            fraction = vi / (i + 1)
            distance = weight * fraction + (1 - weight) * distance
        return distance
        
                    
    
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
    
    def agreement_weighted_swap(self, weight=0.5):
        total = 0
        count = 0
        for pref_a, count_a in self.counts():
            for pref_b, count_b in self.counts():
                if pref_a == pref_b:
                    continue
                r = 1 - 2 * pref_a.weighted_swap_distance(pref_b, weight)
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
                    margins[(pref[lose], pref[win])] -= count
        return margins
    
    
class Condorcet(SocialWelfare):
    """Social welfare utilities for the Condorcet method"""
    
    def social_preference (self):
        """Calculate the social preference ranking according to the Condorcet method.
        If a cycle is encountered, the social preference ranking will be truncated.
        """

        # Get alternatives and contest win/loss margins
        alts_remaining = self.profile.alternatives()
        margins = self.pairwise_margin()
        
        # Find and remove condorcet winner until out of alternatives
        result = []
        while len(alts_remaining) > 0:
            
            winner = set()
            for a in alts_remaining:
                lost = False
                for b in alts_remaining:
                    if a == b:
                        # Skip self
                        continue
                    if margins[(a, b)] < 0:
                        lost = True
                        break
                if not lost and not a in winner:
                    # Add winner, avoiding double-counting
                    winner.add(a)

            # If no winner was found, a cycle exists, so exit
            if len(winner) == 0:
                break
            # Otherwise remove winners(s) from alts, append to result, and continue
            alts_remaining = alts_remaining - winner
            result.append(winner)
            
        return result

    
class KemenyYoung(SocialWelfare):
    
    def social_preference_set(self):
        # Iterate through every possible ordering
        counts = self.profile.counts()
        alts = sorted(self.profile.alternatives())
        preferences = itertools.permutations(alts)
        best_total = None
        best = set()
        for pref in preferences:
            tau_total = sum([
                count * p.kendall_tau(pref)
                for p, count in counts])
            if best_total == None or tau_total < best_total:
                best_total = tau_total
                best = set()
                best.add(pref)
            elif tau_total == best_total:
                best.add(pref)
        return best
        
        
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

class PreferenceSequence():

    def __init__(self):
        self.preferences = []
        
    def __getitem__(self, key):
        return self.preferences[key]
    
    def __repr__(self):
        return repr(self.preferences)
    
    def add(self, preference):
        self.preferences.append(preference)
        
class PreferenceSequenceCollection():
    
    def __init__(self):
        self.participant_sequences = {}
    
    def __repr__(self):
        return repr(list(self.items()))
    
    def __getitem__(self, key):
        return self.participant_sequences[key]
    
    def add(self, participant_id, sequence):
        self.participant_sequences[participant_id] = sequence
    
    def items(self):
        participant_ids = sorted(set(self.participant_sequences.keys()))
        for participant_id in participant_ids:
            yield (participant_id, self.participant_sequences[participant_id])
            
    def sequences(self):
        participant_ids = sorted(set(self.participant_sequences.keys()))
        for participant_id in participant_ids:
            yield self.participant_sequences[participant_id]
            
    def participant_ids(self):
        return sorted(set(self.participant_sequences.keys()))
