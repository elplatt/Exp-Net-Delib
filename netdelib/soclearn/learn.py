from . import strategy as slstrat

MODE_ALL = 1
MODE_FALLBACK = 2

def learn(
        G,
        initial_beliefs,
        learning_step,
        objective=None,
        steps=10,
        individual=False,
        individual_mode=MODE_ALL,
        sample=None):
    '''Runs the simulation, takes the list of inital beliefs and updates each bit based on the learning strategy.

    # Parameters 
    - inital_beliefs: The inital beliefs of each agent before the simulation
    - learning step: The learning strategy agents will follow (see learning section above for options)
    - step: number of iterations
    - individual: If True, apply individual learning before each step
    - individual_mode: When to perform individual learning:
      MODE_ALL - (default) before each social learning step
      MODE_FALLBACK - only when social learning fails to improve objective 
    - sample: The number of neighbors to sample
    
    #Returns 
    A list of agent's beliefs over time
    '''
    
    # Initialize current belief dict with initial beliefs
    current_beliefs = dict((k, tuple(v)) for k, v in initial_beliefs.items())
    
    # Create a list of belief dicts over time
    beliefs = [current_beliefs]
    
    nodes = list(current_beliefs.keys())
    num_bit = len(current_beliefs[nodes[0]])
  
    # Repeatedly update beliefs
    for i in range(steps):
        if individual:
            # Perform individual learning on all nodes
            individual_beliefs = slstrat.individual(G, current_beliefs, objective=objective)
        if individual and individual_mode == MODE_ALL:
            # Adopt individual learning results for all nodes
            current_beliefs = individual_beliefs
            beliefs.append(current_beliefs)
        # Perform social learning
        social_beliefs = learning_step(G, current_beliefs, objective=objective, sample=sample)
        if individual and individual_mode == MODE_FALLBACK:
            # Only fall back to individual belief if social learning is not an improvement
            next_beliefs = dict()
            for v in social_beliefs.keys():
                if social_beliefs[v] == current_beliefs[v]:
                    # No change from social learning, fall back to individual
                    next_beliefs[v] = individual_beliefs[v]
                else:
                    next_beliefs[v] = social_beliefs[v]
            current_beliefs = next_beliefs
        else:
            # Adopt all beliefs generated from social learning
            current_beliefs = social_beliefs
        #need to pass a param that will call diff strategies
        beliefs.append(current_beliefs)
    return beliefs

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
    