from abc import ABC, abstractmethod

class UnionFind (ABC):
    def __init__(self,n):
        self.nodes = [x for x in range(n)]
    def Union(self,x,y):
        pass
    def Find(self,x,y):
        pass

class QuickFind(UnionFind):
    def __init__(self,n):
        super.__init__(n)
    def Union(self,x,y):
        for i in range(len(self.nodes)):
            if self.nodes[i] == x:
                self.nodes[i] = y
    def Find(self,x,y):
        return True if self.nodes[x] == self.nodes[y] else False

class QuickUnion(UnionFind):
    def __init__(self,n):
        super.__init(n)
    def GetRoot(self,x):
        while self.nodes[x] != x:
            x = self.nodes[x]
        return x
    def Find(self,x,y):
        return True if self.GetRoot(x) == self.GetRoot(y) else False
    def Union(self,x,y):
        p = self.GetRoot(x)
        q = self.GetRoot(y)
        self.nodes[p] = q

class WeightedQuickUnion(UnionFind):
    def __init__(self,n):
        super.__init(n)
        self.sizes = [1 for x in self.nodes]
    def GetRoot(self,x):
        while self.nodes[x] != x:
            x = self.nodes[x]
        return x
    def Find(self,x,y):
        return True if self.GetRoot(x) == self.GetRoot(y) else False
    def Union(self,x,y):
        p = self.GetRoot(x)
        q = self.GetRoot(y)
        if self.sizes[p] < self.sizes[q]:
            self.nodes[p] = self.nodes[q]
            self.sizes[q] += self.sizes[p]
        else:
            self.nodes[q] = self.nodes[p]
            self.sizes[p] += self.sizes[q]
        self.nodes[p] = q

class WeightedQuickUnionWithCompression(UnionFind):
    def __init__(self,n):
        super.__init(n)
        self.sizes = [1 for x in self.nodes]
    def GetRoot(self,x):
        while self.nodes[x] != x:
            self.nodes[x] = self.nodes[self.nodes[x]]   #make every other node point to its grandparent
            x = self.nodes[x]
        return x
    def Find(self,x,y):
        return True if self.GetRoot(x) == self.GetRoot(y) else False
    def Union(self,x,y):
        p = self.GetRoot(x)
        q = self.GetRoot(y)
        if self.sizes[p] < self.sizes[q]:
            self.nodes[p] = self.nodes[q]
            self.sizes[q] += self.sizes[p]
        else:
            self.nodes[q] = self.nodes[p]
            self.sizes[p] += self.sizes[q]
        self.nodes[p] = q
