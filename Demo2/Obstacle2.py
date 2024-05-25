import numpy as np
import matplotlib.pyplot as plt
import simulationParam

class Obstacles:
    def __init__(self, loc=None):
        if loc is None:
            loc = np.array([0.0, 0.0])
        self.location = loc
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.radius = 0.0
        self.color = 'black'
        self.mass = 1.0

    def render(self):
        circle = plt.Circle(self.location, self.radius, color=self.color)
        plt.gca().add_patch(circle)

    def loc(self):
        return self.location

    def rad(self):
        return self.radius

    def getX(self):
        return self.location[0]

    def getY(self):
        return self.location[1]

    def isCircle(self):
        return True

    def isCollide(self, p1, p2):
        # Implement collision detection logic
        pass

    def isInside(self, p):
        # Implement inside check logic
        pass

class MovingObst(Obstacles):
    def __init__(self):
        super().__init__()
        self.maxVal = 0.0
        self.velocity = np.array([0.0, 0.0])

    def render(self):
        super().render()

    def move(self, key=None):
        if key is not None:
            # Implement manual move logic based on key
            pass
        else:
            # Implement automatic move logic
            pass

    def applyForce(self, force):
        self.acceleration += force / self.mass

    def update(self):
        self.velocity += self.acceleration
        self.location += self.velocity
        self.acceleration = np.array([0.0, 0.0])

    def repulsive(self, obst):
        # Implement repulsive force logic
        pass

class Maze(Obstacles):
    def __init__(self, loc, width=0.0, height=0.0):
        super().__init__(loc)
        self.width = width
        self.height = height
        self.rect = plt.Rectangle(self.location, self.width, self.height, color=self.color)

    def render(self):
        plt.gca().add_patch(self.rect)

    def isCircle(self):
        return False

    def isCollide(self, p1, p2):
        # Implement collision detection logic
        pass

    def isInside(self, p):
        # Implement inside check logic
        pass


