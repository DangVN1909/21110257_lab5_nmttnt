from treelib import Node, Tree
import sys

class TreeNode(object): 
    def __init__(self, c_no, c_id, f_value, h_value, parent_id):
        self.c_no = c_no
        self.c_id =  c_id
        self.f_value = f_value
        self.h_value = h_value
        self.parent_id = parent_id

class FringeNode(object):
    def __init__(self, c_no, f_value):
        self.f_value = f_value
        self.c_no = c_no

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def printMST(self, parent, d_temp, t):
        sum_weight = 0
        min1 = 10000
        min2 = 10000
        r_temp = {}
        for k in d_temp:
            r_temp[d_temp[k]] = k
        for i in range(1, self.V):
            if parent[i] is not None:
                sum_weight = sum_weight + self.graph[i][parent[i]]
                if self.graph[0][r_temp[i]] < min1:
                    min1 = self.graph[0][r_temp[i]]

                if parent[i] is not None and self.graph[0][r_temp[parent[i]]] < min1:
                    min1 = self.graph[0][r_temp[parent[i]]]
                if self.graph[t][r_temp[i]] < min2:
                    min2 = self.graph[t][r_temp[i]]

                if parent[i] is not None and self.graph[t][r_temp[parent[i]]] < min2:
                    min2 = self.graph[t][r_temp[parent[i]]]

        return (sum_weight + min1 + min2) % 10000

    def minKey(self, key, mstSet):
        min = sys.maxsize
        min_index = None
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
        return min_index

    def primMST(self, d_temp, t):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V
        sum_weight = 10000
        parent[0] = -1

        for c in range(self.V):
            u = self.minKey(key, mstSet)
            if u is None:
                break
            mstSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

        return self.printMST(parent, d_temp, t)

def heuristic(tree, p_id, t, V, graph):
    visited = set()
    visited.add(0)
    visited.add(t)

    if p_id is not None:
        tnode = tree.get_node(str(p_id))
    else:
        tnode = None

    while tnode is not None and tnode.data.c_id != 1:
        visited.add(tnode.data.c_no)
        tnode = tree.get_node(str(tnode.data.parent_id))

    l = len(visited)
    num = V - 1
    if num != 0:
        g = Graph(V)
        d_temp = {}
        key = 0
        for i in range(V):
            if i not in visited:
                d_temp[i] = key
                key = key + 1
        i = 0

        for i in range(V):
            for j in range(V):
                if i not in visited and j not in visited:
                    g.graph[d_temp[i]][d_temp[j]] = graph[i][j]

        mst_weight = g.primMST(d_temp, t)

        return mst_weight
    else:
        return graph[t][0]

def checkPath(tree, toExpand, V):
    tnode = tree.get_node(str(toExpand.c_id))
    list1 = list()

    if tnode is not None and tnode.data is not None and tnode.data.c_id == 0:
        return 0
    else:
        depth = tree.depth(tnode)
        s = set()
        while tnode is not None and tnode.data is not None and tnode.data.c_id != 0:
            s.add(tnode.data.c_no)
            list1.append(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))

        list1.append(0)
        if depth == V and len(s) == V and list1[0] == 0:
            print("Path complete")
            print(list1)
            return 1
        else:
            return 0

def startTSP(graph, tree, V):
    goalState = 0
    times = 0
    toExpand = TreeNode(0, 0, 0, 0, -1)
    key = 1
    heu = heuristic(tree, -1, 0, V, graph)
    tree.create_node("0", "0", data=TreeNode(0, 0, heu, heu, -1))
    fringe_list = {key: FringeNode(0, heu)}
    key += 1

    cost = 0  

    while goalState == 0:
        minf = sys.maxsize
        toExpand.c_id = None 
        for i in fringe_list.keys():
            if fringe_list[i].f_value < minf:
                toExpand.f_value = fringe_list[i].f_value
                toExpand.c_no = fringe_list[i].c_no
                toExpand.c_id = i
                minf = fringe_list[i].f_value

        if toExpand.c_id is None: 
            break

        node = tree.get_node(str(toExpand.c_id))
        if node and node.data:
            h = node.data.h_value
            val = toExpand.f_value - h
            path = checkPath(tree, toExpand, V)

            if toExpand.c_no == 0 and path == 1:
                goalState = 1
                cost = toExpand.f_value
            else:
                del fringe_list[toExpand.c_id]
                j = 0
                while (j < V):
                    if j != toExpand.c_no:
                        h = heuristic(tree, toExpand.c_id, j, V, graph)
                        f_val = val + graph[j][toExpand.c_no] + h  # Define f_val here

                        parent_id = str(toExpand.c_id) if tree.get_node(
                            str(toExpand.c_id)) else "0"

                        if tree.contains(parent_id):
                            fringe_list[key] = FringeNode(j, f_val)
                            tree.create_node(
                                str(toExpand.c_no), str(key), parent=parent_id, data=TreeNode(j, key, f_val, h, toExpand.c_id))
                            key += 1
                    j += 1
        else:
            break  

    return cost


if __name__ == '__main__':
    V = 4
    graph = [[0, 5, 2, 3], [5, 0, 6, 3], [2, 6, 0, 4], [3, 3, 4, 0]]
    tree = Tree()
    ans = startTSP(graph, tree, V)
    print("Ans is " + str(ans))
