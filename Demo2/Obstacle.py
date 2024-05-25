import random
import math
from collections import namedtuple
import Obstacle2

# Define a simple 2D vector class
class Vec2f:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2f(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2f(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2f(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vec2f(self.x / scalar, self.y / scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        l = self.length()
        if l != 0:
            return self / l
        return Vec2f()

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"Vec2f({self.x}, {self.y})"

# Define a simple Rectangle class
Rectangle = namedtuple('Rectangle', ['x', 'y', 'width', 'height'])

class Obstacles:
    def __init__(self, loc=None):
        if loc is None:
            x = random.uniform(0, 800)  # Assuming window width is 800
            y = random.uniform(0, 600)  # Assuming window height is 600
            self.location = Vec2f(x, y)
        else:
            self.location = loc
        self.radius = random.uniform(10, 20)
        self.color = (200, 50, 10)
        self.mass = 3.14 * self.radius * self.radius

    def render(self):
        # Placeholder for rendering logic
        pass

    def is_collide(self, n1, n2):
        x1, y1 = n1.x, n1.y
        x2, y2 = n2.x, n2.y
        xo, yo = self.location.x, self.location.y
        lambda_ = (x1 - x2)**2 + (y1 - y2)**2
        t = (x1**2 + x2 * xo - x1 * (x2 + xo) - (yo - y1) * (y1 - y2)) / lambda_
        if 0 <= t <= 1:
            shortest_dist = abs((x2 * (y1 - yo) + x1 * (yo - y2) + xo * (y2 - y1)) / math.sqrt(lambda_))
        else:
            d1 = math.sqrt((x1 - xo)**2 + (y1 - yo)**2)
            d2 = math.sqrt((x2 - xo)**2 + (y2 - yo)**2)
            shortest_dist = min(d1, d2)
        return shortest_dist < self.radius

    def is_inside(self, n):
        return self.location.distance(n) <= self.radius

class MovingObst(Obstacles):
    def __init__(self):
        super().__init__()
        self.max_val = 5  # Assuming some max velocity
        self.radius = 25
        self.mass = 3.14 * self.radius * self.radius
        self.color = (200, 100, 20)
        self.velocity = Vec2f(random.uniform(-1, 1) * self.max_val, random.uniform(-1, 1) * self.max_val)

    def render(self):
        # Placeholder for rendering logic
        pass

    def move(self, key=None):
        if key == 'w':
            self.location.y -= self.max_val
        elif key == 's':
            self.location.y += self.max_val
        elif key == 'a':
            self.location.x -= self.max_val
        elif key == 'd':
            self.location.x += self.max_val

class Maze:
    def __init__(self, loc, width=20, height=240):
        self.location = loc
        self.color = (10, 10, 50)
        self.rect = Rectangle(loc.x, loc.y, width, height)
        self.mass = 1000

    def render(self):
        # Placeholder for rendering logic
        pass

    def loc(self):
        return Vec2f(self.rect.x + self.rect.width, self.rect.y + self.rect.height)

    def is_collide(self, p1, p2):
        return self.rect.x <= p1.x <= self.rect.x + self.rect.width and self.rect.y <= p1.y <= self.rect.y + self.rect.height

    def is_inside(self, p):
        return self.rect.x <= p.x <= self.rect.x + self.rect.width and self.rect.y <= p.y <= self.rect.y + self.rect.height


