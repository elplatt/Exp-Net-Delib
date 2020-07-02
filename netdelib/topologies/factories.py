import networkx as nx
from . import topologies as topo

class NetworkFactory(object):
    """Base class for network factories.
    
    Constructor paramteters
    N: Number of participants
    M: Number of participants per group
    stage_graphs: Whether to regenerate network at each stage
    """

    def __init__(self, N, M, stage_graphs=True):
        self.N = N
        self.M = M
        self.stage_graphs = stage_graphs
    
    def create(self, stage):
        """Create a networkx Graph with a particular topology.
        
        Parameters
        stage: The deliberation stage
        
        Returns
        A networkx Graph.
        """
        return nx.Graph()

class LongPathFactory(NetworkFactory):
    '''Factory class for long-path networks.'''
    def create(self, stage):
        groups = topo.get_long_path_stage_groups(self.N, self.M, stage)
        G = nx.Graph()
        for group in groups:
            g = nx.complete_graph(group) #clique network
            G = nx.union(G, g)
        return G
    
class RandomGroupFactory(NetworkFactory):
    """Factory class for random group networks."""
    def create(self, stage):
        groups = topo.get_random_stage_groups(self.N, self.M, stage)
        G = nx.Graph()
        for group in groups:
            g = nx.complete_graph(group) #clique network
            G = nx.union(G, g)
        return G

class CompleteFactory(NetworkFactory):
    """Factory class for deliberation network with random group assignments."""

    def __init__(self, N, M):
        super(CompleteFactory, self).__init__(N, M, False)
        
    def create(self, stage):
        return nx.complete_graph(self.N)

class PreferentialFactory(NetworkFactory):
    """Factory class for preferential attachment networks.
    
    Constructor Params
    N: Number of participants
    M: Number of participants per group (unused)
    m: Number of edges per node"""
    
    def __init__(self, N, M, m):
        super(PreferentialFactory, self).__init__(N, M, False)
        self.m = m
        
    def create(self, stage):
        return nx.barabasi_albert_graph(self.N, self.m)
    
class SmallWorldFactory(NetworkFactory):
    """Factory class for small-world networks.
    
    Constructor Params
    N: Number of participants
    M: Number of participants per group (unused)
    k: Number of edges per node
    a: probability of rewiring
    """
    
    def __init__(self, N, M, k, a):
        super(SmallWorldFactory, self).__init__(N, M, False)
        self.k = k
        self.a = a
        
    def create(self, stage):
        return nx.watts_strogatz_graph(self.N, self.k, self.a)
    
class RandomFactory(NetworkFactory):
    """Factory class for Erdos-Renyi random networks.
    
    Constructor Params
    N: Number of participants
    M: Number of participants per group (unused)
    p: Probability of edge existing between two nodes
    """
    
    def __init__(self, N, M, p):
        super(RandomFactory, self).__init__(N, M, False)
        self.p = p
        
    def create(self, stage):
        return nx.erdos_renyi_graph(N, self.p)

class LFRFactory(NetworkFactory):
    """Factory class for LFR networks.
    
    Constructor Params
    N: Number of participants
    M: Number of participants per group
    tau1: Power law exponent for the degree distribution of the created graph. This value must be strictly greater than one.
    tau2: Power law exponent for the community size distribution in the created graph. This value must be strictly greater than one.
    mu: (0<=mu<=1) mixing parameter.
    """
    
    def __init__(self, N, M, tau1, tau2, mu):
        super(LFRFactory, self).__init__(N, M, False)
        self.tau1 = tau1
        self.tau2 = tau2
        self.mu = mu
        
    def create(self, stage):
        degree = self.M - 1
        return nx.LFR_benchmark_graph(
            self.N, self.tau1, self.tau2, self.mu, average_degree=degree)
    
class StochasticBlockFactory(NetworkFactory):
    """Factory class for stochastic block model networks.
    
    Constructor Params
    N: Number of participants
    M: Number of participants per group
    """
    
    def __init__(self, N, M):
        super(StochasticBlockFactory, self).__init__(N, M, False)
    
    def create(self, stage):
        num_blocks = int(self.N / self.M)
        within_density = (self.M - 2) / self.M
        between_density = 1 / (self.N - self.M)
        sizes = [self.M for i in range(num_blocks)]
        density = [[
                within_density if s == r else between_density
                for s in range(num_blocks)]
            for r in range(num_blocks)
        ]
        return nx.stochastic_block_model(sizes, density)
    
    