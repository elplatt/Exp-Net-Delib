import random
import numpy as np
from numpy import random as nprand
from ... import soclearn as slearn


def initial_beliefs(N, num_bits, objective):
    '''
    
    #Params
    N: Number of agents
    num_bits: The number of bits in states
    objective: a function mapping states to objective values
    
    #Return 
    A dict of beliefs with a noise (p_error)
    '''
    
    beliefs = {}
    # Generate a belief for each agent
    
    for v in range(N):
        # Start with random belief
        belief = [random.getrandbits(1) for bit in range(num_bits)]
        
        # Find local maximum
        beliefs[v] = slearn.find_local_maximum(belief, objective)
    
    return beliefs
