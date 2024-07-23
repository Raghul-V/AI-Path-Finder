class DFS_Frontier:
    """ Depth First Search Algorithm """
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        for i in self.frontier:
            if i.state == state:
                return True
        return False

    def is_empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(-1)


class BFS_Frontier(DFS_Frontier):
    """ Depth First Search Algorithm """
    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(0)


class GBFS_Frontier(DFS_Frontier):
    """ Greedy Best-First Search Algorithm """
    def __init__(self, end):
        self.frontier = []
        self.end = end

    def add(self, node):
        i, j = node.state
        i1, j1 = self.end
        node.h_cost = abs(i-i1) + abs(j-j1)
        self.frontier.append(node)

    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty")
        index, h_cost = None, -1
        for i in range(len(self.frontier)):
            if h_cost == -1 or self.frontier[i].h_cost < h_cost:
                index, h_cost = i, self.frontier[i].h_cost
        return self.frontier.pop(index)


class A_star_Frontier(GBFS_Frontier):
    """ A* Search Algorithm """
    def add(self, node, g_cost):
        i, j = node.state
        i1, j1 = self.end
        node.g_cost = g_cost
        node.h_cost = abs(i-i1) + abs(j-j1)
        node.f_cost = node.g_cost + node.h_cost
        self.frontier.append(node)

    def remove(self):
        if self.is_empty():
            raise Exception("Frontier is empty")
        index, f_cost = None, -1
        for i in range(len(self.frontier)):
            if f_cost == -1 or self.frontier[i].f_cost < f_cost:
                index, f_cost = i, self.frontier[i].f_cost
        return self.frontier.pop(index)


