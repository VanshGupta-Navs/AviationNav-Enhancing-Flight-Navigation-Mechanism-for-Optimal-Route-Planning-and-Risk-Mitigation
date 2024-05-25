import simulationParam
import nodeStruct
import Obstacle2


class Robot:
    def __init__(self, loc=None):
        if loc is None:
            self.setup()
        else:
            self.setup(loc)

    def setup(self, loc=None):
        # Initialize variables
        self.alive = True
        self.scanRadius = 0.0
        self.mass = 0.0
        self.accuracy = 0.0
        self.color = None
        self.HOME = loc if loc else (0, 0)
        self.location = loc if loc else (0, 0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.maxVelocity = (0, 0)
        self.maxForce = (0, 0)
        self.line = []
        self.pt = (0, 0)

    def update(self):
        # Update logic here
        pass

    def render(self):
        # Render logic here
        pass

    def addForce(self, force):
        # Add force logic here
        pass

    def controller(self, target):
        # Controller logic here
        pass

    def isAlive(self):
        return self.alive

    def x(self):
        return self.location[0]

    def y(self):
        return self.location[1]

    def accu(self):
        return self.accuracy

    def getScanRadius(self):
        return self.scanRadius

    def getLocation(self):
        return self.location

    def getColor(self):
        return self.color

    def fillEnviroment(self, obst, node):
        # Fill environment logic here
        pass

    def updateEnviroment(self, node, obst):
        # Update environment logic here
        pass


