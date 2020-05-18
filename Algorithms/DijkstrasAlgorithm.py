from Algorithms import DataStructures as ds

"""
This is a class for storing a weighted graph, with E edges and V vertices. To do this, we store the nodes
in a dictionary where the keys are the node names and the values are an adjacency list. Each element in the adjacency
list stores tuples, where the first element is the adjoining vertex and the second element is the cost of the edge.
We also store a third argument indicating whether or not the graph is directed. If it is, then we will assume that the
pairs in edges are of the form [source, sink, cost].
"""
class Graph:
    #nodes is a list of names, and edges is a list of tuples with the following form: [node1, node2, value for edge]
    def __init__(self,nodes,edges,directed = True):
        if directed:
            self._adj = {y: [(x[1],x[2]) for x in set(edges) if y == x[0]] for y in set(nodes)}
        else:
            self._adj = {y: [(x[0],x[2]) if x[1] == y else (x[1],x[2]) for x in set(edges) if y in (x[0],x[1])] for y in set(nodes)}

    def numVertices(self):
        return len(self._adj.keys())

    def printGraph(self):
        for a in self._adj.keys():
            for b in  self._adj[a]:
                print('{0} -> {1} with edge weight = {2}'.format(a,b[0],b[1]))

    def dijkstra(self,v0):
        visited = {v0:0}
        while len(visited) < self.numVertices():
            candidates = [] #list to determine future additions to visited
            for v in visited.keys(): #check each visited node
                candidates.extend([(x[0],x[1] + visited[v]) for x in self._adj[v] if x[0] not in visited.keys()])
            if len(candidates) == 0:
                return None
            d_min = candidates[0][1]
            d = candidates[0][0]
            if len(candidates) > 1:
                for c in candidates[1:]:
                    if c[1] < d_min:
                        d_min = c[1]
                        d = c[0]
            visited[d] = d_min
        return visited
