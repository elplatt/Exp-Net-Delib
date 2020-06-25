import random
import networkx as nx
import numpy as np
from numpy import random as nprand
from statistics import mode, StatisticsError

def find_neighbor_bit_mode(G, v, beliefs, bit):
    '''Among node v and its neighbors, find the most common belief in the specified bit.
    
    # Params
    G: a Graph
    v: a node in G
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    bit: An integer >= 0 corresponding an index of the belief lists.
    
    # Return value
    The most common belief (at the specified bit) among v and its neighbors or beliefs[v][bit] if there is a tie.
    '''
    neighbor_values = [beliefs[v][bit]]
    next_belief = beliefs[v][bit]
    neighbor_values += [beliefs[w][bit] for w in G.neighbors(v)]
    try:
        next_belief = mode(neighbor_values)
    except StatisticsError: 
        pass
    return next_belief

def conform(G, beliefs, sample=None, **kwargs):
    '''For all nodes in G, choose the most popular list of beliefs among neighbors 

    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    sample: None (default) or the number of neighbors to random
    
    # Return value
    A dictionary mapping nodes to their new beliefs.
    '''
    true_value = 0
    
    new_beliefs = {}
    current_beliefs = dict(beliefs) #dict of beliefs
    
    # Ensure tuples
    for k, v in current_beliefs.items():
        current_beliefs[k] = tuple(v)
    
    new_lists = dict((v, [current_beliefs[v]]) for v in G.nodes()) #a dict: intiates a list for each node v. 
    
    for v in new_lists:
        for w in G.neighbors(v):
            new_lists[v].append(current_beliefs[w]) #appends the vals of all neighbors of v in new list[v]
    
    temp_val = new_lists #assing new lists to temp_val. For testing purposes.
    
    for v in temp_val.keys(): #for each node v in temp_val find the mode using the try/except block. if there's more than one mode, keep the original list of beliefs
        # Sample neighbors if specified
        candidates = temp_val[v]
        if sample is not None and len(candidates) > sample:
            candidates = random.sample(temp_val[v], sample)
        try:
            next_belief = mode(candidates)
        except StatisticsError: 
            next_belief = current_beliefs[v]
        new_beliefs[v] = tuple(next_belief)
    return new_beliefs

most_popular_list = conform


def random_neighbor_bit(G, beliefs, **kwargs):
    '''For each node in v, create a new belief by choosing each bit randomly
    from the beliefs of the node and its neighbors.
    # Params
    G: a Graph
    beliefs: a dict. mapping nodes of graph G to a list of beliefs. each lists has 1s and 0s.
    true_value: added for consistency with other learning strategies (Not use)
    
    # Return value
    A dict mapping nodes to their new belief list.
    '''
    
    # Ensure tuples
    for k, v in beliefs.items():
        beliefs[k] = tuple(v)
    
    new_beliefs = {}

    for v in sorted(G.nodes()):
        num_bit = len(beliefs[v])
        rand_beliefs = [] #temp list to hold new rand vals
        
        for bit in range(num_bit):
            bit_val = [beliefs[v][bit]] #append all the neighs val at position bit
            
            for w in sorted(G.neighbors(v)):
                vals_pos_bit = beliefs[w][bit] #first find the val at pos bit of each neigh, safe it in temp var
                bit_val.append(vals_pos_bit) #add all the vals at position bit
                
            new_rand_val = random.choice(bit_val) # randomly select one of the vals      
            rand_beliefs.append(new_rand_val) #add the randomly selected val to a temp list called rand_beliefs        
            
        new_beliefs[v] = tuple(rand_beliefs) #assing the new rand vals to new beliefs 
    return new_beliefs

def random_neighbor_list(G, beliefs, **kwargs):
    '''For a given node, choose a neighboor randomly an adopt all its belief
    
    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: added for consistency with other learning strategies (Not use)
    
    # Return value
    A list of belief where each bit is randomly chosen among v's neighbors
    
    '''
    
    new_beliefs = {}
    
    current_beliefs = dict(beliefs)# a dict of beliefs 
    # Ensure tuples
    for k, v in current_beliefs.items():
        current_beliefs[k] = tuple(v)
        
    for v in sorted(G.nodes()):
        neighboors_keys = [v] #hold v's neighboors keys
        
        for w in sorted(G.neighbors(v)):
            neighboors_keys.append(w)
            
        one_neigh = random.choice(neighboors_keys)        
        vals_rand = current_beliefs[one_neigh]# here's i solved it.         
        new_beliefs[v] = vals_rand
    return new_beliefs

rand_neighbor_list = random_neighbor_list


def best_neighbor(G, beliefs, objective, sample=None, **kwargs):
    '''For each node, chose the belief among neighbors that maximizes objective.
    
    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    objective: a function mapping a belief to a number.
    sample: None (default) or the number of neighbors to random
    
    #Return
     A list of beliefs chosen among v's neighbors 
    '''
    # Dict to contain new beliefs
    new_beliefs = {}
    
    # Create a copy of current beliefs and ensure tuples
    current_beliefs = dict(
        (k, tuple(v))
        for k, v in beliefs.items())
    
    # Iterates through each node
    for v in G.nodes():
        
        # Sample
        neighbors = list(G.neighbors(v))
        if sample is not None and len(neighbors) > sample:
            neighbors = random.sample(neighbors, sample)
        
        # Evaluate objective function for all neighbors and current node
        neighbor_values = dict(
            (current_beliefs[w], objective(current_beliefs[w]))
            for w in neighbors)
        node_value = objective(current_beliefs[v])
        neighbor_values[v] = node_value

        # Find belief that maximizes the objective function
        # Create a list in case there are ties
        max_value = max(neighbor_values.values())
        best_beliefs = [belief for belief, value in neighbor_values.items() if value == max_value]
        
        # Only change belief if it can be improved
        if max_value == node_value:
            new_beliefs[v] = current_beliefs[v]
            continue
        
        # Select one value randomly from the winners
        new_beliefs[v] = random.choice(best_beliefs)
        
    return new_beliefs

def local_majority(G, beliefs, sample=None, **kwargs):
    '''Update each node's belief by taking a majority vote among neighbors
    for each bit of the belief. In the case of a tie, the bit remains unchnaged.
    
    # Params
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    sample: None (default) or the number of neighbors to randomly sample.
    
    # Return value
    Dict of new beliefs for v
    '''

    new_beliefs = {}
    # Find new belief for each node
    for v in G.nodes():
        # Sample
        neighbors = list(G.neighbors(v))
        if sample is not None and len(neighbors) > sample:
            neighbors = random.sample(neighbors, sample)
        # Initialize bit
        new_bits = []
        for bit in range(len(beliefs[v])):
            neighbor_bits = [beliefs[v][bit]]
            neighbor_bits += [beliefs[w][bit] for w in neighbors]
            try:
                next_bit = mode(neighbor_bits)
            except StatisticsError:
                next_bit = beliefs[v][bit]
            new_bits.append(next_bit)
        new_beliefs[v] = tuple(new_bits)
    return new_beliefs

learning_step_bit_majority = local_majority

def individual(G, beliefs, objective, **kwargs):
    '''For each node, perform a single step of hill-climbing to find new belief.
    
    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    objective: a function mapping a belief to a number.
    
    #Return
     A list of beliefs chosen among v's neighbors 
    '''
    # Dict to contain new beliefs
    new_beliefs = {}
    
    # Create a copy of current beliefs and ensure tuples
    current_beliefs =dict(
        (k, tuple(v))
        for k, v in beliefs.items())
    
    # Iterates through each node
    for v in G.nodes():

        # Find current value
        belief = current_beliefs[v]
        current_value = objective(belief)
        
        # Try improving belief by hill-climbing
        trial_values = {}
        for bit in range(len(belief)):
            trial_belief = tuple(
                belief[i] if i != bit
                else 1 - belief[i]
                for i in range(len(belief)))
            trial_values[tuple(trial_belief)] = objective(trial_belief)

        # Find beliefs that maximize the objective function
        # Create a list in case there are ties
        max_value = max(trial_values.values())
        best_beliefs = [belief for belief, value in trial_values.items() if value == max_value]
        
        # Only change belief if it can be improved
        if max_value <= current_value:
            new_beliefs[v] = current_beliefs[v]
            continue
        
        # Select one value randomly from the winners
        if len(best_beliefs) == 1:
            new_beliefs[v] = best_beliefs[0]
        else:
            new_beliefs[v] = random.choice(best_beliefs)
        
    return new_beliefs
