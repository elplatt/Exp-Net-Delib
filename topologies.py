import random

def get_long_path_stage_groups(N, M, stage):
    """Find groups for a particular stage using long-path network.
    
    # Params
    N: Number of participants (integer, must be > 0).
    M: Group size (integer, must be >= 2).
    stage: Stage of deliberation (integer, must be >= 0).
    
    # Returns
    A list, with each element a set of participant ids corresponding to a group.
    Participants are given integer ids in [0, N-1].
    
    """
    primes = [2, 3, 5, 7, 11, 13, 17]
    p = primes[stage]
    partition = []
    for j in range(p):
        # Generate 
        residue_class = [n for n in range(N) if n % p == j]
        chunks = [
            set(residue_class[k:k+M]) 
            for k in range(0, len(residue_class), M)]
        partition += chunks
    return partition

def get_long_path_stages(N, M, D):
    """Find groups all stages using long-path network.
    
    # Params
    N: Number of participants (integer, must be > 0).
    M: Group size (integer, must be >= 2).
    D: Number of stages (integer, must be > 0).
    
    # Returns
    A list of D elements.
    Each element is a list as returned by get_long_path_stage_groups().
    
    """
    stages = []
    for i in range(D):
        groups = get_long_path_stage_groups(N, M, i)
        stages.append(groups)
    return stages

def get_random_stage_groups(N, M, i):
    """Find groups for a particular stage using random network.
    
    # Params
    N: Number of participants (integer, must be > 0).
    M: Group size (integer, must be >= 2).
    stage: Stage of deliberation (integer, must be >= 0).
    
    # Returns
    A list, with each element a set of participant ids corresponding to a group.
    Participants are given integer ids in [0, N-1].
    
    """
    nodes = list(range(N))
    random.shuffle(nodes)
    groups = [set(nodes[k:k+M]) for k in range(0, N, M)]
    return groups

def get_random_groups(N, M, D):
    """Find groups all stages using long-path network.
    
    # Params
    N: Number of participants (integer, must be > 0).
    M: Group size (integer, must be >= 2).
    D: Number of stages (integer, must be > 0).
    
    # Returns
    A list of D elements.
    Each element is a list as returned by get_random_stage_groups().
    
    """
    groups = sum([get_random_stage_groups(N, M, i) for i in range(D)], [])
    return groups