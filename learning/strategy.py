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

def conform(G, beliefs, **kwargs):
    '''For all nodes in G, choose the most popular list of beliefs among neighbors 

    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    
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
        try:
            popular_val = mode(temp_val[v])
        except StatisticsError: 
            popular_val = current_beliefs[v]
        new_beliefs[v] = tuple(popular_val)
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


def best_neighbor(G, beliefs, true_value, **kwargs):
    '''For node v, chose the neighbor with bit string closest to the true value and copy it. 
    
    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    
    true_value: The list of true values. Each nodes needs to look at all its neighbors and see
    which one has the closest list to the true value 
    
    #Return
     A list of belief chosen among v's neighbors closest to the true value
    '''
    new_beliefs = {} #empty dict for new beliefs
    
    current_beliefs = dict(beliefs) #starts a dict of nodes and their list of beliefs//argument beliefs
    # Ensure tuples
    for k, v in current_beliefs.items():
        current_beliefs[k] = tuple(v)
    
    #determine number of bit
    num_bit = len(next(iter(beliefs.values())))
        
    for v in G.nodes(): #iterates through each node
        
        current_equal_bits = len([
            i for i, vi in enumerate(current_beliefs[v])
            if current_beliefs[v][i] == true_value[i]])
        
        list_winners = [] #keeps the neighbors with the highest num of equal value to the true value
        key_val_equal = {} #keeps num of neigh of node v with equal num of bits to true value
        for w in G.neighbors(v):
            num_equal_bits = 0 #records num of bits in each neigh that have same val as true_val.
        
            for bit in range(num_bit):
                if current_beliefs[w][bit] == true_value[bit]: 
                    num_equal_bits += 1
            key_val_equal[w] = num_equal_bits
        
        #finds neighbors with max vals

        max_value = max(key_val_equal.values()) 
        max_neigh = [k for k, v in key_val_equal.items() if v == max_value]# getting all keys containing the `maximum`
  
        # Only select a new balue if it beats current
        if max_value <= current_equal_bits:
            new_beliefs[v] = current_beliefs[v]
        else:    
          #when there is multiple neighbors with max values choose the best neighbor randomly 
          best_neigh = random.choice(max_neigh)
          new_beliefs[v] = current_beliefs[best_neigh]
        
    return new_beliefs

learning_step_best_neighbor = best_neighbor

def local_majority(G, beliefs, **kwargs):
    '''Update each node's beliefs based on its neighbors' beliefs
    # Params
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: Added for consistency (Not use)
    
    # Return value
    Dict of new beliefs for v
    '''

    new_beliefs = {}
    for v in G.nodes():
        num_beliefs = []
        #call function 
        for bit in range(len(beliefs[v])):
            new_belief = find_neighbor_bit_mode(G, v, beliefs, bit)
            num_beliefs.append(new_belief)
        new_beliefs[v] = tuple(num_beliefs)
    return new_beliefs

learning_step_bit_majority = local_majority