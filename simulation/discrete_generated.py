import netdelib.soclearn as slearn
import netdelib.soclearn.models.generated as slgen

def run_discgen_trial(
    factory,
    p_error,
    learning_strategy,
    true_value,
    N,
    M,
    stages,
    steps
):
    """Run a single trial
    
    Parameters:
    factory: network factory
    learning strategy: learning strategy to simulate in topology
    intial beliefs are generated inside the topology: prarms (G, true_value, p_error)
    true_value: the ground truth 
    stages: the number of stages in each trial
    steps: the number of learning steps per stage
    
    Returns
    A list of dictionaries, one for each time step.
    Each dictionary maps collaborator ids to belief states.
    """
    beliefs_stages = []
    for stage in range(stages):
        if stage == 0:
            # Create new network and initial beliefs at stage 0
            G = factory.create(stage)
            beliefs = slgen.initial_beliefs_noisy(G, true_value, p_error=p_error)
            beliefs_stages.append(beliefs)
        else:
            # At later stages, only create new network if factory.stage_graphs is True
            if factory.stage_graphs:
                G = factory.create(stage)

        # Run several learning steps and add beliefs at each step to beliefs_stages
        # The first element of the result is just the initial belief, which is already in beliefs_stages
        beliefs_list = slearn.learn(G, beliefs_stages[-1], learning_strategy, true_value, steps)
        beliefs_stages += beliefs_list[1:]
    return beliefs_stages
