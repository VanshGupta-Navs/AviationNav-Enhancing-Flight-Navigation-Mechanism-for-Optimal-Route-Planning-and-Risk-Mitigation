import numpy as np

# Macros
M = lambda e: np.interp(e, [-1, 1], [0, 1])
inf = float('inf')

# Constants
numberOfobst = 20
NODE_RADIUS = 3
sensorRadius = 200
mVal = 4
mForce = 1
accur = 1.0
startx = 500
starty = 500
goalx = 250
goaly = 200
converge = 50.0
epsilon = 25
rrtstarradius = 50
allowedTimeRewiring = 0.5
maxNeighbours = 50
minDistClosestNode = 5
alpha = 0.1
beta = 1.4
