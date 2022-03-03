import pandas as pd
from socialchoice import Preference, PreferenceSequenceCollection, PreferenceSequence

def get_proposal_map(df):
    """Map proposal names to generic names."""
    proposals = df.columns[3:]
    proposal_map = dict([(proposal, 'prop{}'.format(i + 1)) for i, proposal in enumerate(proposals)])
    proposal_rev_map = dict([('prop{}'.format(i + 1), proposal) for i, proposal in enumerate(proposals)])
    return proposal_map, proposal_rev_map

def load_loomio_score(filename):
    """
    Load results from netdelib:export_results rake task.
    
    Parameters
    ----------
    filename: filename of a TSV of the rake output.
    
    Returns
    -------
    (df, proposal_map, proposal_rev_map)
    df: Pandas dataframe containing stage, participant_id, and proposal scores
    proposal_map: dict mapping original proposal names to generic names, e.g. "prop1"
    proposal_rev_map: dict mapping generic names back to original proposal names
    """
    df = pd.read_csv(filename, delimiter='\t')
    df['participant_id'] = pd.to_numeric(df.participant_id)
    proposal_map, proposal_rev_map = get_proposal_map(df)
    score_map = dict((k, '{}_score'.format(v)) for k, v in proposal_map.items())
    df = df.rename(mapper=score_map, axis='columns')
    return df, proposal_map, proposal_rev_map

def score_to_ranked(df):
    """Return tuple of proposals in rank order from highest to lowest."""
    
    if len(df) != 1:
        raise ValueError("Requires DataFrame with one row")
    
    # Get proposal names
    proposals = df.columns[3:]
    
    # Get proposal scores
    prop_scores = [
        (p, df[p].to_numpy()[0])
        for p in proposals]

    # Sort by rank
    prop_rank = reversed(sorted(prop_scores, key=lambda x: x[1]))
    
    # Return tuple of proposal names with "_score" removed
    ranked = tuple([prop[0:-6] for prop, rank in prop_rank])
    
    return ranked

def make_preference_sequence_collection(df_score):

    # Get participant ids, stages, and proposal names
    participant_ids = sorted(set(df_score.participant_id))
    participant_preferences = {}
    proposals = df_score.columns[3:]
    stages = len(set(df_score.stage))

    # Create collection
    collection = PreferenceSequenceCollection()

    # Add preference sequences
    for participant_id in participant_ids:

        # Build a preference sequence for this participant
        df_participant = df_score[df_score.participant_id == participant_id]
        sequence = PreferenceSequence()
        collection.add(participant_id, sequence)

        for stage in range(stages):
            try:
                df = df_participant[df_participant.stage == stage]
                ranked = score_to_ranked(df)
                preference = Preference(ranked)
                sequence.add(preference)
            except ValueError:
                # Missing data from participant
                break
    return collection
        
        
