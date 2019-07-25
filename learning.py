# Configure plotting in Jupyter
from matplotlib import pyplot as plt
plt.rcParams.update({
    'figure.figsize': (7.5, 7.5),
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.top': False,
    'axes.spines.bottom': False})
# Seed random number generator
import random
from numpy import random as nprand


# Import NetworkX
import networkx as nx
import numpy as np

#to handle stats error in learning step // need to be more specific 
from statistics import mode
from statistics import StatisticsError



def get_random_belief_bit (p):
    """Return a 1 with probability p and a 0 with probability (p - 1).
    
    # Params
    p: The probability of returning a 1

    # Return value
    1 with probability p, 0 otherwise.
    """
    
    val = np.random.uniform(low=0, high=1, size = 1)
    
    if val < p:
        x = 1
    else: 
        x = 0
    return x

def get_random_belief (p1):
    """Get a random belief for a single agent.
    
    # Params
    p1: A list of numbers between 0 and 1. Each element of p1 represents 
    the probability the corresponding element of the belief list should be 1.
    
    # Return
    A list of length len(p1), with each element equal to 0 or 1.
    """
    
    list_bits = []

    for p in p1:
        bit = get_random_belief_bit(p)
        list_bits.append(bit)
    return list_bits

def initial_beliefs(G, p1):
    
    """Generate the initial beliefs for each node in graph G.
    The number of bits is determined by len(p1). 
    If there are 5 bits, p1 should have 5 elements.

    # Params
    G: A graph
    p1: an array of real numbers between 0 and 1. p1[i] is the 
    probability that the belief of bit i is 1.

    # Return
    A dict mapping nodes in G to lists of length len(p1).
    """
    beliefs = {}
    for v in G.nodes():
        l_beliefs = []
        list_bits = get_random_belief (p1) 
        l_beliefs = list_bits
        beliefs[v] = l_beliefs
    return beliefs
    
    
def initial_beliefs_noisy(G, true_value, p_error):
    '''Generates a list of beliefs with a probability error 
    #Params 
    true_value: A list of true bits
    p_error: probability an error 
    
    #Return 
    A dict of beliefs with a noise (p_error)
    '''
    
    p1 = []
    
    for bit in true_value:
        
        if bit == 1:
            x =  1 - p_error
            p1.append(x)
            
        else:
            x = p_error
            p1.append(x)
    
    beliefs = initial_beliefs(G, p1)
    return beliefs


def get_belief_bit_fraction(G, beliefs, bit):
    '''Get the fraction of nodes that have 1 in given bit
    #HELPER FUNCTION
    #Params 
    G: graph
    beliefs: set of beliefs for each node
    bit = given index
    
    #Returns 
    fraction of nodes that have a 1 in given bit. 
    '''
    #fraction of nodes with 1 in given bit
    
    node_bit_value = []
    for v in G.node():
        #print(beliefs[v][bit])
        node_bit_value.append(beliefs[v][bit]) 
        #print(beliefs, beliefs[v][bit])
    #print(node_bit_value)
    frac_nodes_one = sum(node_bit_value) / len(node_bit_value)
    return frac_nodes_one

def find_neighbor_bit_mode(G, v, beliefs, true_value, bit):
    '''Among node v and its neighbors, find the most common belief in the specified bit.
    
    # Params
    G: a Graph
    v: a node in G
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: it was for consistency with other learning strategies (Not use)
    bit: An integer >= 0 corresponding an index of the belief lists.
    
    # Return value
    The most common belief (at the specified bit) among v and its neighbors or beliefs[v][bit] if there is a tie.
    '''
    true_value = 0
    #for test
    neighbors_bit_value = []
    #include bit value of v in mode calculation
    node_belief = beliefs[v]
    try:
        neighbors_bit_value.append(node_belief[bit])
    except TypeError:
        print(node_belief)
    for w in G.neighbors(v):
        neighbors_bit_value.append(beliefs[w][bit])
        try:
            popular_val = mode(neighbors_bit_value)
        except StatisticsError: 
            popular_val = beliefs[v][bit]
    return popular_val

def most_popular_list(G, beliefs, true_value):
    '''For a given node, choose the most popular list of beliefs among neighbors 

    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: added for consistency with other learning strategies (Not use)
    
    # Return value
    The most popular list of beliefs among v's neighbors
    '''
    true_value = 0
    
    new_beliefs = {}
    #print(new_beliefs)
    
    current_beliefs = dict(beliefs) #dict of beliefs 
    #print(current_beliefs)

    
    new_lists = dict((v, list()) for v in G.nodes()) #a dict: intiates a list for each node v. 
    #print(new_lists)

    
    for v in new_lists:
        #print(v)
        #print(current_beliefs[v])
        
        for w in G.neighbors(v):
            #print(v, current_beliefs[w]) #print the beliefs of the neighboors
            
            new_lists[v].append(tuple(current_beliefs[w])) #appends the vals of all neighbors of v in new list[v]
    
    #print(new_lists) #to verify if each node has a list (compose of lists of beliefs) 
    
    temp_val = new_lists #assing new lists to temp_val. For testing purposes.
    #print("Temp vals", temp_val)
    
    for v in temp_val: #for each node v in temp_val find the mode using the try/except block. if there's more than one mode, keep the original list of beliefs
        #print("List", v, temp_val[v])
        try:
            popular_val = tuple(mode(temp_val[v]))
        except StatisticsError: 
            popular_val = current_beliefs[v]
        new_beliefs[v] = popular_val
    return new_beliefs


def random_neighbor_bit(G, beliefs, true_value):
    '''For a given bit, choose a neighbor randomly an adopt its belief at given position
    # Params
    G: a Graph
    beliefs: a dict. mapping nodes of graph G to a list of beliefs. each lists has 1s and 0s.
    true_value: added for consistency with other learning strategies (Not use)
    
    # Return value
    A list of belief where each bit is randomly chosen among v's neighbors
    '''
    new_beliefs = {}
    true_value = 0

    for v in G.nodes():
        #print(beliefs[v])
        num_bit = len(beliefs[v])
        rand_beliefs = [] #temp list to hold new rand vals
        
        for bit in range(num_bit):
            bit_val = [] #append all the neighs val at position bit
            
            for w in G.neighbors(v):
                
                vals_pos_bit = beliefs[w][bit] #first find the val at pos bit of each neigh, safe it in temp var
                bit_val.append(vals_pos_bit) #add all the vals at position bit
    
        #print (bit_val)
    
            new_rand_val = random.choice(bit_val) # randomly select one of the vals      
            rand_beliefs.append(new_rand_val) #add the randomly selected val to a temp list called rand_beliefs        
        #print(rand_beliefs)
            
        new_beliefs[v] = rand_beliefs#assing the new rand vals to new beliefs 
        #print(new_beliefs)
    return new_beliefs

def rand_neighbor_list(G, beliefs, true_value):
    '''For a given node, choose a neighboor randomly an adopt all its belief
    
    #Params 
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: added for consistency with other learning strategies (Not use)
    
    # Return value
    A list of belief where each bit is randomly chosen among v's neighbors
    
    '''
    true_value=0
    
    new_beliefs = {}
    
    current_beliefs = dict(beliefs)# a dict of beliefs 
    #print(current_beliefs)

    beliefs = [current_beliefs]#makes a list that contains a dict. Dict contains 34 nodes, each with a list of bits
    #print(beliefs)
        
    nodes = list(current_beliefs.keys()) #makes a list with 34 keys. no longer vals with it.
    #print(nodes)
    
    
    for v in G.nodes():
        #print(v) # prints 34 nodes without values. just keys.
        neighboors_keys = [] #hold v's neighboors keys
        
        for w in G.neighbors(v):
            
            neighboors_keys.append(w)
            
        one_neigh = random.choice(neighboors_keys)
        
        #vals_rand = beliefs[one_neigh] #here's the problem. it doesn't have the vals of neigh. only has the key
        
        vals_rand = current_beliefs[one_neigh]# here's i solved it. 
        
        #print(vals_rand)
        
        new_beliefs[v] = vals_rand
        #print(new_beliefs[v])
    return new_beliefs


def learning_step_best_neighbor(G, beliefs, true_value):
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
    #print("new_beliefs", new_beliefs)
    
    current_beliefs = dict(beliefs) #starts a dict of nodes and their list of beliefs//argument beliefs
    #print("Current beliefs", current_beliefs)
    
    beliefs = [current_beliefs]  #makes the dict into a list. #to determine num of keys, and num of bits
    #print("List of dict", beliefs)
    
    #determine number of bit
    nodes = list(beliefs[0].keys()) #puts number keys in a list
    #print("num of keys", nodes)
    num_bit = len(beliefs[0][nodes[0]]) #determines the num of bits in a list of beliefs
    #print("num_bit in each list", num_bit)
    
    
    for v in G.node(): #iterates through each node
        list_winners = [] #keeps the neighbors with the highest num of equal value to the true value
        key_val_equal = {} #keeps num of neigh of node v with equal num of bits to true value
        for w in G.neighbors(v):
            num_equal_bits = 0 #records num of bits in each neigh that have same val as true_val.
        
            for bit in range(num_bit):
                if current_beliefs[w][bit] == true_value[bit]: 
                    num_equal_bits += 1
            #key_val_equal[w]     
            key_val_equal[w] = num_equal_bits
            #print("Node", v, "Neigh", w, "num bits equal to true value", key_val_equal)
        #print("node", v, key_val_equal) #to verify if dict is working correctly
        
        #finds neighbors with max vals

        max_value = max(key_val_equal.values()) 
        max_neigh = [k for k, v in key_val_equal.items() if v == max_value] # getting all keys containing the `maximum`
  
        #print(max_value, max_neigh)
        
        #when there is multiple neighbors with max values choose the best neighbor randomly 
        best_neigh = random.choice(max_neigh)   
        #print("The best neighor randomly selected", best_neigh)
        
        new_beliefs[v] = current_beliefs[best_neigh]
        #print("New beliefs of node", v, "are", new_beliefs[v])
    return new_beliefs


def learning_step_bit_majority(G, beliefs, true_value):
    '''Update each node's beliefs based on its neighbors' beliefs
    # Params
    G: a Graph
    beliefs: a dict mapping nodes of G to lists of 1s and 0s.
    true_value: Added for consistency (Not use)
    
    # Return value
    Dict of new beliefs for v
    '''
    true_value = 0
    new_beliefs = {}
    for v in G.nodes():
        num_beliefs = []
        #call function 
        for bit in range(len(beliefs[v])):
            new_belief = find_neighbor_bit_mode(G, v, beliefs, true_value, bit)
            num_beliefs.append(new_belief)
            #print(num_beliefs)
        new_beliefs[v] = num_beliefs
    return new_beliefs



def learn(G, ini_beliefs, learning_step, true_value, steps = 10):
    '''Runs the simulation, takes the list of inital beliefs and updates each bit based on the learning strategy
    #Parameters 
    inital_beliefs: The inital beliefs of each agent before the simulation
    #learning step: The learning strategy agents will follow (see learning section above for options)
    step: number of iterations 
    
    #Returns 
    A list of agent's beliefs over time
    '''
    
    current_beliefs = dict(ini_beliefs) #starts a dict of nodes and their list of beliefs//
    #print("Current beliefs", current_beliefs)
    
    beliefs = [current_beliefs]  #makes the dict into a list. 
    #print("Made current beliefs of a list of dict", beliefs)
    
    #nodes && num_bit are use to iterate through each bit 
    nodes = list(current_beliefs.keys())
    num_bit = len(current_beliefs[nodes[0]])
  
    #update the belief after each step
    for i in range(steps + 1):
        if i < steps:
            current_beliefs = learning_step(G, current_beliefs, true_value) 
            #need to pass a param that will call diff strategies
            beliefs.append(current_beliefs)
    return beliefs


def plot_beliefs_bits(beliefs_list):
    '''Plots the change of beliefs over time
    #Params
    beliefs_list: a list, each element is a dict of beliefs at one time [{}]
    
    plots the fraction of nodes that have a one in a given bit
    '''
    
    current_beliefs = beliefs_list #a list of dict. each key:value pair is a node, and a LIST of beliefs.
    
    #determine number of bits 
    nodes = list(current_beliefs[0].keys()) 
    num_bit = len(current_beliefs[0][nodes[0]])
    
    y = dict((bit, list()) for bit in range(num_bit))

    #takes the list of beliefs in each iteration. Then for each bit, takes the fraction that 
    #have a 1 and adds them to y (the plotting varaible)
    for steps_beliefs in current_beliefs:
        for bit in range(num_bit):
            bit_avg = get_belief_bit_fraction(G, steps_beliefs, bit) 
            y[bit].append(bit_avg) 
        
    #plot the fract of nodes in bit that have a one
    for bit in y:
        plt.plot(y[bit], '-', alpha=0.4, linewidth=2, label  = str(bit))

    #add spines to plot
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
    #plt.xlim([0, steps]) 
    #plt.ylim([0, 1])
    plt.legend()
    
def plot_beliefs_correct(list_of_beliefs, true_value):
    '''Plots the fraction of nones that have the correct string of bits over time.
    #Params 
    list_of_beliefs: a list of dict, each element is a dict of beliefs at one step [{}]
    true_value: the true string of bits
    
    #Return value
    A plot with the fraction of nodes with the correct string of values
    '''
    
    current_beliefs = list_of_beliefs #gives me a list of all the beliefs in all steps
    
    y = []
    #print(y)
    
    for steps_beliefs in current_beliefs: #gives me a dict of all beliefs in all steps 
        #print(steps_beliefs) #steps_beliefs gives me the keys
        total = 0
        for v in steps_beliefs.keys():
            #print(v, steps_beliefs[v])
            if steps_beliefs[v] == true_value:
                #print ("The list are equal") 
                total += 1
            #else:
             #   print ("The list aren't equal")
        frac_nodes_one = (total) / (len(steps_beliefs))
         #append the fraction of nodes that have same string
        y.append(frac_nodes_one) 
        #print(y)
            
    plt.plot(y, 'y-', alpha=0.4, linewidth=2)

    #add spines to plot
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
    #plt.xlim([0, steps]) 
    plt.ylim([0, 1])
    plt.legend()
        
        
def fraction_correct_bit(G, steps_beliefs, true_value, bit):
    '''Get the fraction of nodes that have same value in given bit
    ##Helper function to plot_belief_bits_correct
    
    NOTE: difference between this and orginal get fraction of nodes that have one in given bit is that
    in this one it gets the fraction of nodes that have the same value in given bit. regardless if it is 0 or 1
    
    #Params 
    G: graph
    beliefs: set of beliefs for each node
    bit = given index
    
    #Returns
    fraction of nodes that have same value in given bit 
    '''
    #get fraction of nodes that have same val in given bit in one step
    
    total = 0 #records bits that have same val.
    for v in G.node(): #iterates through each node
        if steps_beliefs[v][bit] == true_value[bit]: 
            #print("F", steps_beliefs[v][bit], "TV", true_value[val])
            total += 1
        #else: 
        #    print("not same")
    frac_nodes_one = (total) / (len(G)) 
    return frac_nodes_one 


def plot_belief_bits_correct(beliefs_list, true_value):
    ''' Plot  line for each bit with the correct value
    #Params 
    beliefs_list =  a list of dict, each element is a dict of beliefs at one step. Sintax [{}]
    true_value = list of bits that represent the true value.
    
    NOTE: This function no plot the fraction that has a 1 in a given bit, instead plots the fraction 
    of nodes that have the same value in a given bit (0 or 1).
    #Return
    Plot of fraction of nodes that have the SAME value in each individual bit. 
    '''
    
    current_beliefs = beliefs_list #a list of dict. each key:value pair is a node, and a LIST of beliefs.
    #print(current_beliefs)
    
    #determine number of bits 
    nodes = list(current_beliefs[0].keys()) #list of 34 keys
    #print(nodes)
    num_bit = len(current_beliefs[0][nodes[0]]) #gets the num of bits
    #print(num_bit)
    
    #dict to hold the fraction with same value in given bit
    y = dict((bit, list()) for bit in range(num_bit)) #for each bit creates an empty list. 
    

    for steps_beliefs in current_beliefs:
        for bit in range(num_bit):
            bit_avg = fraction_correct_bit(G, steps_beliefs, true_value, bit) #frac of v that have smae in given bit
            y[bit].append(bit_avg) 
    
    #plot the fract of nodes in bit that have a one
    for bit in y:
        plt.plot(y[bit], '-', alpha=0.4, linewidth=2, label  = str(bit))

    #add spines to plot
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
    #plt.xlim([0, steps]) 
    #plt.ylim([0, 1])
    plt.legend()
    
    
    
