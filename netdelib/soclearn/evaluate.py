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

