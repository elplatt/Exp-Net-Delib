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
    primes = [
        2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97,101,103,107,109,113,
        127,131,137,139,149,151,157,163,167,173,
        179,181,191,193,197,199,211,223,227,229,
        233,239,241,251,257,263,269,271,277,281,
        283,293,307,311,313,317,331,337,347,349,
        353,359,367,373,379,383,389,397,401,409,
        419,421,431,433,439,443,449,457,461,463,
        467,479,487,491,499,503,509,521,523,541,
        547,557,563,569,571,577,587,593,599,601,
        607,613,617,619,631,641,643,647,653,659,
        661,673,677,683,691,701,709,719,727,733,
        739,743,751,757,761,769,773,787,797,809,
        811,821,823,827,829,839,853,857,859,863,
        877,881,883,887,907,911,919,929,937,941,
        947,953,967,971,977,983,991,997,1009,1013 
    ]
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

