import pandas as pd

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
