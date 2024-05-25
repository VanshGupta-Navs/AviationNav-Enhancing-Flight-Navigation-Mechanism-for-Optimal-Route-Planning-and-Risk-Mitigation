import numpy as np
import ofApp

class Nodes:
    def __init__(self, x_=0.0, y_=0.0, cost_to_start_=0.0, p_=None):
        self.location = np.array([x_, y_])
        self.parent = p_
        self.prev_parent = None
        self.alive = True
        self.color = (10, 12, 160)
        self.cost_to_start = cost_to_start_
        self.children = []

    def __repr__(self):
        return f"Nodes(location={self.location}, parent={self.parent}, cost_to_start={self.cost_to_start})"

    def add_child(self, child_node):
        self.children.append(child_node)
