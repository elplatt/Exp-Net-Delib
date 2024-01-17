import netdelib.soclearn as slearn
import netdelib.soclearn.models.interpreted as slint

def run_nk_trial(
    factory,
    learning_strategy,
    model,
    N,
    M,
    stages,
    steps
):
    """Run a single trial
    
    Parameters:
    factory: network factory
    learning strategy: learning strategy to simulate in topology
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
            beliefs = slint.initial_beliefs(N, model.N, model.get_value)
            beliefs_stages.append(beliefs)
        else:
            # At later stages, only create new network if factory.stage_graphs is True
            if factory.stage_graphs:
                G = factory.create(stage)

        # Run several learning steps and add beliefs at each step to beliefs_stages
        # The first element of the result is just the initial belief, which is already in beliefs_stages
        beliefs_list = slearn.learn(G, beliefs_stages[-1], learning_strategy, model.get_value, steps)
        beliefs_stages += beliefs_list[1:]
    return beliefs_stages
