def learn(G, initial_beliefs, learning_step, objective, steps=10):
    '''Runs the simulation, takes the list of inital beliefs and updates each bit based on the learning strategy.

    # Parameters 
    - inital_beliefs: The inital beliefs of each agent before the simulation
    - learning step: The learning strategy agents will follow (see learning section above for options)
    - step: number of iterations 
    
    #Returns 
    A list of agent's beliefs over time
    '''
    
    current_beliefs = dict(initial_beliefs) #starts a dict of nodes and their list of beliefs//
    
    beliefs = [current_beliefs]  #makes the dict into a list. 
    
    nodes = list(current_beliefs.keys())
    num_bit = len(current_beliefs[nodes[0]])
  
    #update the belief after each step
    for i in range(steps + 1):
        if i < steps:
            current_beliefs = learning_step(G, current_beliefs, objective=objective) 
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
    
    