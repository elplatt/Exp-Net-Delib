import random
import networkx as nx
import numpy as np
from numpy import random as nprand
from statistics import mode, StatisticsError


def initial_beliefs(N, true_value, p_error):
    '''Generates a list of beliefs with a probability error 
    #Params
    N: The number of agents
    true_value: A list of true bits
    p_error: probability an error 
    
    #Return 
    A dict of beliefs with a noise (p_error)
    '''
    
    beliefs = {}
    # Loop through nodes, (sorted guarantees same order, helps testing)
    for v in range(N):
        # Calculate which bits have errors for this node
        errors = [
            1 if nprand.uniform() < p_error
            else 0
            for true in true_value]
        # Create a belief by flipping bits with errors
        beliefs[v] = [
            (true + errors[i]) % 2
            for i, true in enumerate(true_value)]
    
    return beliefs

initial_beliefs_noisy = initial_beliefs
