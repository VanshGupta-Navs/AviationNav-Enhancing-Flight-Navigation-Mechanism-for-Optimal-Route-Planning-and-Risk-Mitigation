from queue import PriorityQueue
from typing import List, Set
import Robot2

class Nodes:
    def __init__(self, location):
        self.location = location

class Obstacles:
    pass

class Robot:
    pass

class NodesCompare:
    def __call__(self, lhs: Nodes, rhs: Nodes) -> bool:
        if lhs.location.x != rhs.location.x:
            return lhs.location.x < rhs.location.x
        else:
            return lhs.location.y < rhs.location.y

class InformedRRTstar:
    pass

class RTRRTstar(InformedRRTstar):
    visited_set: Set[Nodes] = set()
    goalDefined: bool = False

    def __init__(self):
        self.currPath: List[Nodes] = []
        self.rewireRand: List[Nodes] = []
        self.rewireRoot: List[Nodes] = []
        self.closestNeighbours: List[Nodes] = []
        self.pushedToRewireRoot: List[Nodes] = []
        self.timeKeeper: float = 0.0

    def nextIter(self, nodes: List[Nodes], obst: List[Obstacles], agent: Robot):
        pass

    def expandAndRewire(self, nodes: List[Nodes], obst: List[Obstacles]):
        pass

    def updateNextBestPath(self):
        pass

    def sample(self) -> Nodes:
        pass

    def getClosestNeighbour(self, u: Nodes, nodes: List[Nodes]) -> Nodes:
        pass

    def addNode(self, n: Nodes, closest: Nodes, nodes: List[Nodes], obst: List[Obstacles]):
        pass

    def rewireRandomNode(self, obst: List[Obstacles], nodes: List[Nodes]):
        pass

    def rewireFromRoot(self, obst: List[Obstacles], nodes: List[Nodes]):
        pass

    def cost(self, node: Nodes) -> float:
        pass

    def getHeuristic(self, u: Nodes) -> float:
        pass

    def changeRoot(self, nextPoint: Nodes, nodes: List[Nodes]):
        pass

    def isPathToGoalAvailable(self) -> bool:
        pass


