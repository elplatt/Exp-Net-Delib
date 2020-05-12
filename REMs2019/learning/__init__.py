def learn(G, initial_beliefs, learning_step, true_value, steps=10):
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
            current_beliefs = learning_step(G, current_beliefs, true_value=true_value) 
            #need to pass a param that will call diff strategies
            beliefs.append(current_beliefs)
    return beliefs
