class Node:
    def __init__(self,value):
        self.value = value
        self.adj = []
    def addToAdj(self,node):
        self.adj.append(node)