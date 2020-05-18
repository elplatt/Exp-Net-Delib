def beliefs_correct(belief_list, true_value):
    '''Calculates the fraction of agents with a correct value over time.
    #Params 
    beief_list: a list beliefs, each element is a dict of beliefs at one step [{}]
    true_value: the value a belief must match to be considered correct
    
    #Return value
    A list of numbers representing the fraction of correct agents at a given time.
    '''
    y = []
    for beliefs in belief_list: #gives me a dict of all beliefs in all steps 
        total = 0
        for v in beliefs.keys():
            if tuple(beliefs[v]) == tuple(true_value):
                total += 1
        frac_correct = total / (len(beliefs))
        y.append(frac_correct)
    return y    

def belief_distance(belief_list, true_value):
    '''Calculates the mean distance between agent beliefs and the true value.
    #Params 
    beief_list: a list beliefs, each element is a dict of beliefs at one step [{}]
    true_value: the value a belief must match to be considered correct
    
    #Return value
    A list of numbers in [0,1] representing the mean distance to the correct belief
    normalized by the number of bits.
    '''
    y = []
    for beliefs in belief_list: #gives me a dict of all beliefs in all steps
        num_bits = len(belief_list[0][0])
        total = 0
        for v in beliefs.keys():
            total += sum([1 for index, bit in enumerate(beliefs[v]) if true_value[index] == bit])
        mean = total / len(beliefs) / num_bits
        y.append(mean)
    return y    
