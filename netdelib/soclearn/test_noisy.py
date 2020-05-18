import random

import unittest
import unittest.mock as mock

import networkx as nx

from models.generated import *

random_stub_index = 0
random_stub = [
    0.96142941, 0.20502207, 0.66953651, 0.44347763, 0.37082018,
    0.07533418, 0.81284394, 0.7320698 , 0.07155423, 0.09899788,
    0.09235606, 0.41511193, 0.2770485 , 0.68106939, 0.59625876,
    0.40823466, 0.63636044, 0.94410994, 0.16732805, 0.7151281 ,
    0.6274388 , 0.01699715, 0.15425404, 0.5690837 , 0.15544658,
    0.2937884 , 0.30919701, 0.44319367, 0.26233105, 0.59357598,
    0.69613934, 0.51785046, 0.43888461, 0.81046437, 0.96231795,
    0.78515283, 0.34346711, 0.85057948, 0.51339207, 0.41246771,
    0.82852677, 0.52785513, 0.23477266, 0.17540865, 0.93986785,
    0.08590314, 0.91543178, 0.94752169, 0.49639202, 0.31466992,
    0.29640989, 0.85787491, 0.0312848 , 0.85598481, 0.54614915,
    0.83201951, 0.62069739, 0.76449931, 0.31284561, 0.22789747,
    0.63842785, 0.57349069, 0.34380815, 0.77812847, 0.46424859,
    0.51168076, 0.8952304 , 0.59434738, 0.91616106, 0.94713365,
    0.63493068, 0.81467663, 0.04513869, 0.7030862 , 0.53539591,
    0.63593792, 0.05446999, 0.06053487, 0.18460238, 0.15254257,
    0.59822027, 0.57241993, 0.96549058, 0.91109005, 0.23572616,
    0.25006779, 0.56236473, 0.78677969, 0.46174007, 0.02297526,
    0.19252083, 0.0024075 , 0.79403319, 0.59557104, 0.13826026,
    0.68459786, 0.02798459, 0.33419036, 0.53432999, 0.28558709]

def mock_uniform(low=0, high=1, size=1):
    global random_stub_index
    next = random_stub[random_stub_index]
    random_stub_index += 1
    return next

noisy_beliefs = {
    0: [1, 1, 1, 1, 0],
    1: [0, 0, 1, 1, 0],
    2: [0, 1, 0, 0, 1]
    }

class TestLearning(unittest.TestCase):
    
    def setUp(self):
        global random_stub_index
        random_stub_index = 0
    
    def test_random(self):
        with mock.patch('random.uniform', mock_uniform):
            self.assertEqual(random.uniform(), 0.96142941)
            
    def test_initial_beliefs(self):
        G = nx.Graph()
        G.add_nodes_from([0, 1, 2])
        true_value = [1, 0, 1, 0, 1]
        p_error = 0.5
        with mock.patch('models.generated.nprand.uniform', mock_uniform):
            beliefs = initial_beliefs_noisy(G, true_value, p_error)
        self.assertEqual(beliefs, noisy_beliefs)
            
        
    
if __name__ == '__main__':
    unittest.main()
