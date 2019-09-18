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

    
    
