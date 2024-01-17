from . import strategy as slstrat
from .result import RunResult

MODE_ALL = 1
MODE_FALLBACK = 2
MODE_BEST = 3

def learn(
        G,
        initial_beliefs,
        learning_step,
        objective=None,
        steps=10,
        individual=False,
        individual_all_bits=True,
        individual_mode=MODE_ALL,
        critical=False,
        sample=None):
    '''Runs the simulation, takes the list of inital beliefs and updates each bit based on the learning strategy.

    # Parameters 
    - inital_beliefs: The inital beliefs of each agent before the simulation
    - learning step: The learning strategy agents will follow (see learning section above for options)
    - step: number of iterations
    - individual: If True, apply individual learning at each step
    - individaul_all_bits: If True (default), apply individual learning to each
        bit of a solution, one bit at a time. Otherwise, chose a single bit at
        random.
    - individual_mode: When to perform individual learning:
        MODE_ALL - (default) before each social learning step
        MODE_FALLBACK - only when social learning fails to improve objective
        MODE_BEST - chose best between individual and social
    - critical: If True, only keep social solutions that improve objective
    - sample: The number of neighbors to sample
    
    # Returns 
    A soclearn.result.RunResult
    '''
    
    # Select the function for individual learning if necessary
    if individual:
        if individual_all_bits:
            individual_step = slstrat.individual
        else:
            individual_step = slstrat.individual_bit
    
    # Initialize current belief dict with initial beliefs
    current_beliefs = dict((k, tuple(v)) for k, v in initial_beliefs.items())
    
    # Create lists of belief dicts over time
    beliefs = [current_beliefs]
    individual_candidates = [None]
    social_candidates = [None]
    neighbor_beliefs = [None]

    
    nodes = list(current_beliefs.keys())
    num_bit = len(current_beliefs[nodes[0]])
  
    # Repeatedly update beliefs
    for i in range(steps):

        # Perform individual learning on all nodes, if necessary
        if individual:
            individual_beliefs = individual_step(G, current_beliefs, objective=objective)
            individual_candidates.append(individual_beliefs)

        # For MODE_ALL individual learning, update all nodes
        if individual and individual_mode == MODE_ALL:
            # Adopt individual learning results for all nodes
            current_beliefs = individual_beliefs
            
        # Create dict of each node's neighbors' beliefs
        step_neighbors = dict()
        for v, belief in current_beliefs.items():
            step_neighbors[v] = [current_beliefs[w] for w in G.neighbors(v)]
        neighbor_beliefs.append(step_neighbors)
        
        # Perform social learning
        social_beliefs = learning_step(G, current_beliefs, objective=objective, sample=sample)
        social_candidates.append(social_beliefs)

        # Adopt new beliefs based on social and individual learning
        if individual and individual_mode == MODE_FALLBACK:
            # Only fall back to individual belief if social learning yields previous belief
            next_beliefs = dict()
            for v in social_beliefs.keys():
                if social_beliefs[v] == current_beliefs[v]:
                    # No change from social learning, fall back to individual
                    next_beliefs[v] = individual_beliefs[v]
                else:
                    next_beliefs[v] = social_beliefs[v]
        elif individual and individual_mode == MODE_BEST:
            # Choose best between social and individual
            next_beliefs = dict()
            for v in social_beliefs.keys():
                if objective(social_beliefs[v]) > objective(individual_beliefs[v]):
                    next_beliefs[v] = social_beliefs[v]
                else:
                    next_beliefs[v] = individual_beliefs[v]                
        else:
            # Adopt all beliefs generated from social learning
            next_beliefs = social_beliefs
            
        # If critical learning is enabled, only keep improvements
        if critical:
            for v in next_beliefs.keys():
                if objective(next_beliefs[v]) <= objective(current_beliefs[v]):
                        next_beliefs[v] = current_beliefs[v]
        
        current_beliefs = next_beliefs
        beliefs.append(current_beliefs)
    
    result = RunResult(beliefs, individual_candidates, social_candidates, neighbor_beliefs)
    return result

def find_local_maximum(state, objective):
    """Repeatedly change one bit at a time until a local maximum of objective is achieved.
    
    Return
    The local maximum state
    """
    num_bits = len(state)
    current_value = objective(state)
    
    # Initialize best_value and best_state to starting state/value
    best_value = current_value
    best_state = state
    
    # Iterate until local max is reached
    while True:
        
        # Calculate objective value for each possible single bit flip
        step_values = {}
        step_state = tuple(best_state)
        for bit in range(num_bits):
            bit_state = list(step_state)
            bit_state[bit] = 1 - bit_state[bit]
            step_values[tuple(bit_state)] = objective(bit_state)
            
        # If best bit flip improves score, adopt it, otherwise end
        step_state, step_value = max(step_values.items(), key=lambda x: x[1])
        if step_value > best_value:
            best_state = step_state
            best_value = step_value
        else:
            return best_state
    