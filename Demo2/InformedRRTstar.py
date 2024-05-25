from RRTstar import RRTstar
from typing import List

class InformedRRTstar(RRTstar):
    usingInformedRRTstar = False

    def next_iter(self, nodes: List['Nodes'], obst: List['obstacles']):
        pass

    @staticmethod
    def sample(c_max: float) -> 'Nodes':
        pass

    def __init__(self):
        self.sol_nodes = []


