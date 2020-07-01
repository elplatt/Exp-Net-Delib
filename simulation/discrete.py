import netdelib.soclearn as slearn
import netdelib.soclearn.models.generated as slgen

def run_discrete_trial(
    factory,
    learning_strategy,
    initial_beliefs,
    objective,
    N,
    M,
    stages,
    steps,
    individual=False,
    individual_all_bits=True,
    individual_mode=slearn.MODE_ALL,
    sample=None
):
    """Run a single trial
    
    Parameters:
    factory: network factory
    learning strategy: learning strategy to simulate in topology
    intial beliefs: dict of initial beliefs for each agent
    objective: objective function to be maximized 
    stages: the number of stages in each trial
    steps: the number of learning steps per stage
    individual: whether to perform individual learning before each stage
    individaul_all_bits: If True (default), apply individual learning to each
        bit of a solution, one bit at a time. Otherwise, chose a single bit at
        random.
    
    Returns
    A list of dictionaries, one for each time step.
    Each dictionary maps collaborator ids to belief states.
    """
    beliefs_stages = []
    for stage in range(stages):
        if stage == 0:
            # Create new network and initial beliefs at stage 0
            G = factory.create(stage)
            beliefs = initial_beliefs
            beliefs_stages.append(beliefs)
        else:
            # At later stages, only create new network if factory.stage_graphs is True
            if factory.stage_graphs:
                G = factory.create(stage)

        # Run several learning steps and add beliefs at each step to beliefs_stages
        # The first element of the result is just the initial belief, which is already in beliefs_stages
        beliefs_list = slearn.learn(
            G,
            beliefs_stages[-1],
            learning_strategy,
            objective,
            steps,
            individual=individual,
            individual_all_bits=individual_all_bits,
            individual_mode=individual_mode,
            sample=sample)
        beliefs_stages += beliefs_list[1:]
    return beliefs_stages
