import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from collections import deque
from typing import List
import simulationParam
import nodeStruct
import Obstacle2
import SMP
import Robot2
import RRTstar
import InformedRRTstar
import RTRRTstar
import ofxGui
import time

from typing import List
from ofVec2f import ofVec2f
from ofxGui import ofxFloatSlider, ofxPanel
from RRTstar import RRTstar
from InformedRRTstar import InformedRRTstar
from RTRRTstar import RTRRTstar
from Nodes import Nodes
from Robot import Robot
from obstacle import obstacles

class Enviroment:
    def __init__(self):
        self.setup()
        # Variables
        self.grid = False
        self.goalin = False
        self.guiRad = ofxFloatSlider()
        self.guiEpsilon = ofxFloatSlider()
        self.gui = ofxPanel()
        self.nodes: List[Nodes] = []  # List of Nodes objects
        self.path: List[Nodes] = []   # List of Nodes pointers
        self.rrtstar = RRTstar()
        self.irrtstar = InformedRRTstar()
        self.rtrrtstar = RTRRTstar()
        self.rrtFlag = True
        self.planner = True
        self.goal = ofVec2f()
        self.home = ofVec2f()
        # self.car = None  # You can uncomment this line if you have a class named Robot

    def setup(self, _start: ofVec2f = None):
        if _start:
            self.home = _start
        self.gui.setup()
        self.gui.add(self.guiRad.setup("Radius", rrtstarradius, 10, 200))
        self.gui.add(self.guiEpsilon.setup("Epsilon", epsilon, 5, 150))
        self.nodes.append(Nodes(self.home.x, self.home.y, 0))
        self.rrtstar.root = self.nodes[0]
        self.goal = ofVec2f(goalx, goaly)

    def update(self, car: Robot = None, obst: List[obstacles] = None):
        if car:
            self.update_with_car(car, obst)
        else:
            self.update_without_car()

    def update_with_car(self, car: Robot, obst: List[obstacles]):
        if car.getLocation().distance(self.goal) < converge:
            self.planner = False

        if self.planner:
            car.fillEnviroment(obst, self.nodes)
            car.controller(self.nodes[0].location)
            car.update()

        self.rtrrtstar.nextIter(self.nodes, obst, car)

        if self.planner and self.rrtstar.target:
            self.path = self.rtrrtstar.currPath
            self.rtrrtstar.currPath.clear()

    def update_without_car(self):
        # Update without car
        pass

    def targetSet(self, loc: ofVec2f):
        self.goal = loc
        self.rtrrtstar.goalDefined = True
        self.planner = True
        for node in self.nodes:
            if node.location.distance(loc) < converge:
                self.rtrrtstar.target = node
                return
        self.goalFound = False
        self.rtrrtstar.target = None
        self.path.clear()
        self.goalin = True

    def render(self):
        # Render nodes
        pass

    def numofnode(self):
        return len(self.nodes)

    def renderGrid(self):
        # Render grid
        pass

class Enviroment:
    def __init__(self, _start=None):
        self.grid = False
        self.goalin = False
        self.guiRad = 0
        self.guiEpsilon = 0
        self.nodes = []
        self.path = deque()
        self.rrtstar = None
        self.irrtstar = None
        self.rtrrtstar = None
        self.rrtFlag = True
        self.planner = True
        self.goal = np.array([0, 0])
        self.home = np.array([0, 0])
        if _start is not None:
            self.setup(_start)
        else:
            self.setup()

    def setup(self, _start=None):
        if _start is not None:
            self.home = np.array(_start)
            start = Nodes(self.home[0], self.home[1], 0)
            self.nodes.append(start)
            SMP.root = self.nodes[0]
            self.goal = np.array([goalx, goaly])
            SMP.start = np.array([startx, starty])
            SMP.goalFound = False
        else:
            self.home = np.array([startx, starty])
            start = Nodes(startx, starty, 0)
            self.nodes.append(start)
            SMP.start = np.array([startx, starty])
            SMP.goalFound = False

    def update(self, car, obst):
        if np.linalg.norm(car.getLocation() - SMP.goal) < converge:
            self.planner = False

        if self.planner:
            car.fillEnviroment(obst, self.nodes)
            car.controller(SMP.root.location)
            car.update()

        self.rtrrtstar.nextIter(self.nodes, obst, car)

        if self.planner and SMP.target is not None:
            self.path = self.rtrrtstar.currPath
            self.rtrrtstar.currPath.clear()

    def targetSet(self, loc):
        self.goal = np.array(loc)
        SMP.goal = self.goal
        RTRRTstar.goalDefined = True
        self.planner = True
        for node in self.nodes:
            if np.linalg.norm(node.location - loc) < converge:
                SMP.target = node
                return
        SMP.goalFound = False
        SMP.target = None
        self.path.clear()
        self.goalin = True

    def render(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        if self.goalin:
            goal_circle = Circle(self.goal, NODE_RADIUS + 2, color='purple', alpha=0.5)
            ax.add_patch(goal_circle)
            converge_circle = Circle(self.goal, converge, color='purple', fill=False, linewidth=2)
            ax.add_patch(converge_circle)

        for node in self.nodes:
            color = 'black' if node.costToStart != inf else 'red'
            alpha = 0.6 if node.costToStart != inf else 0.5
            if node.parent is not None:
                ax.plot([node.location[0], node.parent.location[0]], [node.location[1], node.parent.location[1]], color=color, alpha=alpha)

        if self.path:
            for node in self.path:
                if node.parent is not None:
                    ax.plot([node.location[0], node.parent.location[0]], [node.location[1], node.parent.location[1]], color='green', linewidth=2)

        plt.show()

    def renderGrid(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        for i in range(0, 100, 5):
            ax.axvline(i, color='green', alpha=0.2)
        for j in range(0, 100, 5):
            ax.axhline(j, color='green', alpha=0.2)

        plt.show()


