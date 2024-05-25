import math
from random import randint
from collections import namedtuple
import Robot2

Vector2f = namedtuple('Vector2f', ['x', 'y'])

class Robot:
    def __init__(self, sensorRadius, accur, mVal, mForce, converge, inf):
        self.alive = True
        self.mass = 5.0
        self.scanRadius = sensorRadius
        self.accuracy = accur
        self.location = Vector2f(0.0, 0.0)
        self.HOME = self.location
        self.velocity = Vector2f(0.0, 0.0)
        self.acceleration = Vector2f(0.0, 0.0)
        self.maxVelocity = Vector2f(mVal, mVal)
        self.maxForce = Vector2f(mForce, mForce)
        self.color = (50, 145, 80)
        self.converge = converge
        self.inf = inf
        self.line = []  # Placeholder for line drawing

    def setup(self):
        self.alive = True
        self.mass = 5.0
        self.scanRadius = self.sensorRadius
        self.accuracy = self.accur
        self.location = Vector2f(0.0, 0.0)
        self.HOME = self.location
        self.velocity = Vector2f(0.0, 0.0)
        self.acceleration = Vector2f(0.0, 0.0)
        self.maxVelocity = Vector2f(self.mVal, self.mVal)
        self.maxForce = Vector2f(self.mForce, self.mForce)
        self.color = (50, 145, 80)

    def setup_with_location(self, loc):
        self.alive = True
        self.mass = 5.0
        self.scanRadius = self.sensorRadius
        self.accuracy = self.accur
        self.location = loc
        self.HOME = self.location
        self.velocity = Vector2f(0.0, 0.0)
        self.acceleration = Vector2f(0.0, 0.0)
        self.maxVelocity = Vector2f(self.mVal, self.mVal)
        self.maxForce = Vector2f(self.mForce, self.mForce)
        self.color = (50, 145, 80)

    def update(self):
        self.velocity = Vector2f(self.velocity.x + self.acceleration.x, self.velocity.y + self.acceleration.y)
        if math.sqrt(self.velocity.x**2 + self.velocity.y**2) > math.sqrt(self.maxVelocity.x**2 + self.maxVelocity.y**2):
            norm = math.sqrt(self.velocity.x**2 + self.velocity.y**2)
            self.velocity = Vector2f((self.velocity.x / norm) * self.mVal, (self.velocity.y / norm) * self.mVal)
        self.location = Vector2f(self.location.x + self.velocity.x, self.location.y + self.velocity.y)
        self.acceleration = Vector2f(0.0, 0.0)
        self.line.append(self.location)

    def render(self):
        r = 6
        # Placeholder for rendering logic
        # This would typically involve a graphics library like Pygame or similar
        pass

    def addForce(self, force):
        self.acceleration = Vector2f(self.acceleration.x + force.x / self.mass, self.acceleration.y + force.y / self.mass)

    def controller(self, target):
        error = Vector2f(target.x - self.location.x, target.y - self.location.y)
        m = self.mVal if math.sqrt(error.x**2 + error.y**2) >= self.converge else self.mVal * (math.sqrt(error.x**2 + error.y**2) / self.converge)
        temp = Vector2f((error.x / math.sqrt(error.x**2 + error.y**2)) * m, (error.y / math.sqrt(error.x**2 + error.y**2)) * m)
        steer = Vector2f(temp.x - self.velocity.x, temp.y - self.velocity.y)
        if math.sqrt(steer.x**2 + steer.y**2) > math.sqrt(self.maxForce.x**2 + self.maxForce.y**2):
            norm = math.sqrt(steer.x**2 + steer.y**2)
            steer = Vector2f((steer.x / norm) * self.mForce, (steer.y / norm) * self.mForce)
        self.addForce(steer)

    def fillEnvironment(self, obstacles, nodes):
        for obst in obstacles:
            dist = math.sqrt((self.location.x - obst.loc().x)**2 + (self.location.y - obst.loc().y)**2)
            if dist <= self.scanRadius + obst.rad():
                self.updateEnvironment(nodes, obst)

    def updateEnvironment(self, nodes, obst):
        for node in nodes:
            dist = math.sqrt((node.location.x - obst.loc().x)**2 + (node.location.y - obst.loc().y)**2)
            if dist <= obst.rad():
                node.costToStart = self.inf
                node.alive = False

# Placeholder classes for obstacles and nodes
class Obstacle:
    def __init__(self, loc, rad):
        self._loc = loc
        self._rad = rad

    def loc(self):
        return self._loc

    def rad(self):
        return self._rad

class Node:
    def __init__(self, location):
        self.location = location
        self.costToStart = 0
        self.alive = True


