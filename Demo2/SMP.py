from nodeStruct import Nodes
import ofApp
import Obstacle2
import random

class SMP:
    goalFound = False
    sampledInGoalRegion = False
    moveNow = False
    start = ofVec2f()
    goal = ofVec2f()
    root = None
    target = None
    nextTarget = None

    def __init__(self):
        pass

    @staticmethod
    def addNode(n, nodes):
        nodes.append(n)

    @staticmethod
    def nearestNode(n, nodes):
        return min(nodes, key=lambda node: (node.position - n.position).length())

    @staticmethod
    def nearestNodePtr(n, nodes):
        return min(nodes, key=lambda node: (node.position - n.position).length())

    @staticmethod
    def checkCollision(n1, n2, obst):
        for ob in obst:
            if ob.intersects(n1.position, n2.position):
                return True
        return False

    @staticmethod
    def checkSample(n, obst):
        for ob in obst:
            if ob.contains(n.position):
                return False
        return True

    @staticmethod
    def sampler():
        return Nodes(random.uniform(0, 1), random.uniform(0, 1))


