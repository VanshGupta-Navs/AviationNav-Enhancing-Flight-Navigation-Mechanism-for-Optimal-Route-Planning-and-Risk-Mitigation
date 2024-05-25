import SMP
import RRTstar
import InformedRRTstar
import simulationParam
import RTRRTstar


class SMP:
    goalFound = False
    sampledInGoalRegion = False
    moveNow = False
    usingInformedRRTstar = False
    goalDefined = False
    goal = None
    start = None
    target = None
    nextTarget = None
    root = None
    visited_set = set()

    def __init__(self):
        pass

    @staticmethod
    def addNode(n, nodes):
        nodes.append(n)
        if n.location.distance(SMP.goal) < converge:
            SMP.goalFound = True
            SMP.sampledInGoalRegion = True
            SMP.target = nodes[-1]

    @staticmethod
    def nearestNode(n, nodes):
        min_dist = n.location.squareDistance(nodes[0].location)
        near_node = nodes[0]
        if nodes:
            for node in nodes:
                if n.location.squareDistance(node.location) < min_dist:
                    min_dist = n.location.squareDistance(node.location)
                    near_node = node
            return near_node
        else:
            return None

    @staticmethod
    def nearestNode(n, nodes):
        min_dist = n.location.squareDistance(nodes[0].location)
        near_node = nodes[0]
        if nodes:
            for node in nodes:
                if n.location.squareDistance(node.location) < min_dist:
                    min_dist = n.location.squareDistance(node.location)
                    near_node = node
            return near_node
        else:
            return None

    @staticmethod
    def sampler():
        x = random.uniform(0, ofGetWindowWidth())
        y = random.uniform(0, ofGetWindowHeight())
        new_node = Nodes()
        new_node.location.x = x
        new_node.location.y = y
        return new_node

    @staticmethod
    def checkCollision(n1, n2, obst):
        for i in obst:
            if i.isCollide(n1.location, n2.location):
                return False
        return True

    @staticmethod
    def checkSample(n, obst):
        for i in obst:
            if i.isInside(n.location):
                return False
        return True


class RRTstar:
    @staticmethod
    def nextIter(nodes, obst, u_=None):
        if u_ is None:
            u = SMP.sampler()
        else:
            u = u_

        v = SMP.nearestNode(u, nodes)
        dist = u.location.distance(v.location)

        if dist > epsilon:
            x_n = v.location.x + (u.location.x - v.location.x) * epsilon / dist
            y_n = v.location.y + (u.location.y - v.location.y) * epsilon / dist
            u.location.x = x_n
            u.location.y = y_n

        if not SMP.checkSample(u, obst):
            return

        closestNeighbours = RRTstar.findClosestNeighbours(u, nodes)

        if not closestNeighbours:
            return

        safeNeighbours = []
        for neighbour in closestNeighbours:
            if SMP.checkCollision(u, neighbour, obst):
                safeNeighbours.append(neighbour)

        if not safeNeighbours:
            return

        minDist = safeNeighbours[0].costToStart + u.location.distance(safeNeighbours[0].location)
        index = 0

        for i in range(1, len(safeNeighbours)):
            dist = safeNeighbours[i].costToStart + u.location.distance(safeNeighbours[i].location)
            if dist < minDist:
                minDist = dist
                index = i

        u.parent = safeNeighbours[index]
        u.costToStart = minDist

        SMP.addNode(u, nodes)

        safeNeighbours.remove(safeNeighbours[index])

        for neighbour in safeNeighbours:
            dist = u.costToStart + u.location.distance(neighbour.location)
            if neighbour.costToStart > dist:
                neighbour.prevParent = neighbour.parent
                neighbour.parent = nodes[-1]
                neighbour.costToStart = dist

    @staticmethod
    def findClosestNeighbours(u, nodes):
        closestNeighbours = []
        for node in nodes:
            f = u.location.distance(node.location)
            if f < rrtstarradius and f > 0.0001:
                closestNeighbours.append(node)
        return closestNeighbours


class InformedRRTstar:
    @staticmethod
    def nextIter(nodes, obst):
        if sol_nodes:
            min_cost = sol_nodes[0].costToStart
            for node in sol_nodes:
                if node.costToStart < min_cost:
                    min_cost = node.costToStart
                    SMP.target = node

            RRTstar.nextIter(nodes, obst, InformedRRTstar.sample(min_cost))
        else:
            if SMP.goalFound:
                RRTstar.nextIter(nodes, obst)
        if SMP.sampledInGoalRegion:
            sol_nodes.append(nodes[-1])

    @staticmethod
    def sample(c_max):
        c_min = SMP.goal.distance(SMP.start)

        if abs(c_max - c_min) < 100 and usingInformedRRTstar:
            SMP.moveNow = True

        x_centre = (SMP.start + SMP.goal) / 2
        dir = SMP.goal - SMP.start
        dir = dir.getNormalized()
        angle = math.atan2(-dir.y, dir.x)
        r1 = c_max / 2
        r2 = math.sqrt(math.pow(c_max, 2) - math.pow(c_min, 2)) / 2

        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        x2 = x * r1 * math.cos(angle) + y * r2 * math.sin(angle)
        y2 = -x * r1 * math.sin(angle) + y * r2 * math.cos(angle)

        rot_sample = ofVec2f(x2, y2)
        rot_trans_sample = rot_sample + x_centre

        n = Nodes()
        n.location.x = rot_trans_sample.x
        n.location.y = rot_trans_sample.y

        return n


class RTRRTstar:
    timeKeeper = 0
    closestNeighbours = []
    rewireRand = []
    rewireRoot = []
    pushedToRewireRoot = []

    @staticmethod
    def nextIter(nodes, obst, agent):
        timeKeeper = ofGetElapsedTimef()
        expandAndRewire(nodes, obst)
        if SMP.goalFound:
            updateNextBestPath()
        if len(currPath) > 1 and agent.getLocation().distance(SMP.root.location) < 0.1:
            nextPoint = currPath[1]
            changeRoot(nextPoint, nodes)

            visited_set.clear()
            pushedToRewireRoot.clear()
            rewireRoot.clear()
        closestNeighbours.clear()

    @staticmethod
    def changeRoot(nextPoint, nodes):
        nextPoint.children.append(SMP.root)
        nextPoint.parent = None
        nextPoint.prevParent = None
        nextPoint.costToStart = 0

        SMP.root.parent = nextPoint
        SMP.root.costToStart = SMP.root.location.distance(nextPoint.location)
        SMP.root = nextPoint

    @staticmethod
    def expandAndRewire(nodes, obst):
        u = sample()
        v = RTRRTstar.getClosestNeighbour(u, nodes)
        dist = u.location.distance(v.location)

        if dist > epsilon:
            x_n = v.location.x + (u.location.x - v.location.x) * epsilon / dist
            y_n = v.location.y + (u.location.y - v.location.y) * epsilon / dist
            u.location.x = x_n
            u.location.y = y_n

        if not SMP.checkSample(u, obst):
            return
        if SMP.checkCollision(u, v, obst):
            if len(closestNeighbours) < maxNeighbours:
                addNode(u, v, nodes, obst)
            else:
                rewireRand.insert(0, v)
        rewireRandomNode(obst, nodes)
        rewireFromRoot(obst, nodes)

    @staticmethod
    def updateNextBestPath():
        updatedPath = []
        pathNode = target
        if SMP.goalFound:
            while pathNode:
                currPath.append(pathNode)
                pathNode = pathNode.parent
            currPath.reverse()
            return
        else:
            if not goalDefined:
                return
            curr_node = SMP.root
            while curr_node.children:
                tempNode = curr_node.children[0]
                cost_ = cost(tempNode)
                minCost = cost_ + getHeuristic(curr_node.children[0])
                for child in curr_node.children:
                    cost_ = cost(child)
                    cost_new = cost_ + getHeuristic(child)
                    if cost_new < minCost:
                        minCost = cost_new
                        tempNode = child
                updatedPath.append(tempNode)
                if not tempNode.children or cost(tempNode) == inf:
                    visited_set.add(tempNode)
                    break
                curr_node = tempNode
            if not currPath:
                currPath.append(SMP.root)
            if updatedPath[-1].location.distance(SMP.goal) < currPath[-1].location.distance(SMP.goal):
                currPath = updatedPath

    @staticmethod
    def sample():
        rand_num = random.uniform(0, 1)

        if rand_num > 1 - alpha and SMP.target:
            x = random.uniform(SMP.root.location.x, SMP.target.location.x)
            y = random.uniform(SMP.root.location.y, SMP.target.location.y)
            new_node = Nodes()
            new_node.location.x = x
            new_node.location.y = y
            return new_node
        elif rand_num >= (1 - alpha) / beta and SMP.goalFound:
            return InformedRRTstar.sample(cost(SMP.target))
        else:
            return SMP.sampler()

    @staticmethod
    def getClosestNeighbour(u, nodes):
        min_dist = u.location.squareDistance(nodes[0].location)
        near_node = nodes[0]
        for node in nodes:
            dist = u.location.squareDistance(node.location)
            if dist < min_dist:
                min_dist = dist
                near_node = node
            if u.location.distance(node.location) < rrtstarradius:
                closestNeighbours.append(node)
        return near_node

    @staticmethod
    def addNode(n, closest, nodes, obst):
        parent = closest
        c_min = cost(closest) + n.location.distance(closest.location)
        for neighbour in closestNeighbours:
            c_new = cost(neighbour) + n.location.distance(neighbour.location)
            if c_new < c_min and SMP.checkCollision(n, neighbour, obst):
                c_min = c_new
                parent = neighbour
                n.costToStart = c_min
        n.parent = parent
        nodes.append(n)
        parent.children.append(nodes[-1])

        if n.location.distance(SMP.goal) < converge:
            if SMP.target is None or (SMP.target is not None and SMP.target.costToStart > n.costToStart):
                SMP.target = nodes[-1]
            SMP.goalFound = True

    @staticmethod
    def cost(node):
        badNode = False
        cost_ = 0
        curr = node
        while curr.parent:
            if curr.parent.costToStart == inf:
                node.costToStart = inf
                badNode = True
                break
            cost_ += curr.location.distance(curr.parent.location)
            curr = curr.parent
        if badNode:
            return inf
        else:
            node.costToStart = cost_
            return cost_

    @staticmethod
    def rewireRandomNode(obst, nodes):
        while rewireRand and (ofGetElapsedTimef() - timeKeeper) < 0.5 * allowedTimeRewiring:
            Xr = rewireRand.pop(0)
            nearNodes = RRTstar.findClosestNeighbours(Xr, nodes)
            safeNeighbours = []
            for neighbour in nearNodes:
                if SMP.checkCollision(Xr, neighbour, obst):
                    safeNeighbours.append(neighbour)
            if not safeNeighbours:
                continue
            for neighbour in safeNeighbours:
                oldCost = cost(neighbour)
                newCost = cost(Xr) + Xr.location.distance(neighbour.location)
                if newCost < oldCost:
                    neighbour.prevParent = neighbour.parent
                    neighbour.parent.children.remove(neighbour)
                    neighbour.parent = Xr
                    neighbour.costToStart = newCost
                    Xr.children.append(neighbour)
                    rewireRand.append(neighbour)

    @staticmethod
    def rewireFromRoot(obst, nodes):
        if not rewireRoot:
            rewireRoot.append(SMP.root)
        while rewireRoot and (ofGetElapsedTimef() - timeKeeper) < allowedTimeRewiring:
            Xs = rewireRoot.pop(0)
            nearNeighbours = RRTstar.findClosestNeighbours(Xs, nodes)
            safeNeighbours = []
            for neighbour in nearNeighbours:
                if SMP.checkCollision(Xs, neighbour, obst):
                    safeNeighbours.append(neighbour)
            if not safeNeighbours:
                continue
            safeNeighbours.remove(Xs.parent)
            for neighbour in safeNeighbours:
                oldCost = cost(neighbour)
                newCost = cost(Xs) + Xs.location.distance(neighbour.location)
                if newCost < oldCost:
                    neighbour.prevParent = neighbour.parent
                    neighbour.parent.children.remove(neighbour)
                    neighbour.parent = Xs
                    neighbour.costToStart = newCost
                    Xs.children.append(neighbour)
                found = neighbour in pushedToRewireRoot
                if not found:
                    rewireRoot.append(neighbour)
                    pushedToRewireRoot.append(neighbour)

    @staticmethod
    def getHeuristic(u):
        if u in visited_set:
            return inf
        else:
            return u.location.distance(SMP.goal)

