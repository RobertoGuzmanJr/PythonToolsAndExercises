import random

class Graph:
    def __init__(self,nodes,edges):
        self.nodes = nodes
        self.edges = edges
    def numNodes(self):
        return len(self.nodes)

def createRandomGraph(n,directed):
    nodes = [x+1 for x in range(n)]
    edges = []
    for i in nodes:
        for j in [y for y in nodes if y > i]:
            r1 = random.random()
            r2 = random.random()
            if r1 > .005 + r2:
                weight = random.randint(-20,50)
                edges.append((i,j,weight))
    if not directed:
        add = []
        for e in edges:
            add.append((e[1],e[0],e[2]))
    edges.extend(add)
    g = Graph(nodes,edges)
    return g

def BellmanFord(g,src):
    distances = [float("inf") if x != src else 0 for x in g.nodes]
    for i in range(g.numNodes()-1):
        for edge in g.edges:
            if distances[edge[0]-1] != float("inf") and distances[edge[0]-1] + edge[2] < distances[edge[1]-1]:
                distances[edge[1]-1] = distances[edge[0]-1] + edge[2]
    for edge in g.edges:
        if distances[edge[0]-1] != float("inf") and distances[edge[0] - 1] + edge[2] < distances[edge[1] - 1]:
            print("The graph contains a negative cycle.")
    return distances

if __name__ == '__main__':
    g = createRandomGraph(5,False)
    print("Here is the graph: {0} {1}".format(g.nodes,g.edges))
    print(BellmanFord(g,4))
