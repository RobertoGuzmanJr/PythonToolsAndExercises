import Node

class Graph:
    def __init__(self,nodes,adjMatrix):
        self.nodes = [Node(x) for x in nodes]
        [x.adj.append() for x in self.nodes]
            for node in nodes:
                x = Node(node)
                for row in range(len(adjMatrix)):
                    if adjMatrix[row]
                self.nodes.append(Node(node))