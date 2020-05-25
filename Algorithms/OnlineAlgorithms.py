import heapq

class OnlineStatus:
    def __init__(self):
        self.leftSize = 0
        self.rightSize = 0
        self.leftHeap = []
        self.rightHeap = []
        self.mean = None
        self.median = None
        self.max = None
        self.min = None
        heapq.heapify(self.leftHeap)
        heapq.heapify(self.rightHeap)
    def updateMax(self,v):
        if self.max is None or self.max < v:
            self.max = v
    def updateMin(self,v):
        if self.min is None or self.min > v:
            self.min = v
    def updateMean(self,v):
        if self.mean is None:
            self.mean = v
        else:
            self.mean = (1/(self.rightSize+self.leftSize))*((self.leftSize + self.rightSize - 1)*self.mean + v)
    def updateMedian(self,v):
        #just starting out...pretty simple.
        if self.median is None:
            self.median = v
            heapq.heappush(self.leftHeap,-1*v)
            self.leftSize += 1
        #standard run
        else:
            #first determine whether we are going left or right.
            #to do this, we need to find effective median.
            effectiveMedian = 0
            if self.leftSize == self.rightSize:
                effectiveMedian += ((-1)*self.leftHeap[0] + self.rightHeap[0])/2
            elif self.leftSize > self.rightSize:
                effectiveMedian += (-1)*self.leftHeap[0]
            else:
                effectiveMedian += self.rightHeap[0]
            #Going right
            if v >= effectiveMedian:
                #they are equal sizes, or left is bigger..so push right.
                if self.leftSize >= self.rightSize:
                    heapq.heappush(self.rightHeap,v)
                    self.rightSize += 1
                #right is heavy, so we need to move an item to the left and then push right.
                elif self.rightSize > self.leftSize:
                    m = heapq.heappop(self.rightHeap)
                    heapq.heappush(self.rightHeap,v)
                    heapq.heappush(self.leftHeap,-1*m)
                    self.leftSize += 1
            #Going left
            else:
                #they are equal sizes or right is bigger...push left
                if self.leftSize <= self.rightSize:
                    heapq.heappush(self.leftHeap,-1*v)
                    self.leftSize += 1
                #left is heavy, so we need to move an item to the right and then push left.
                elif self.leftSize > self.rightSize:
                    m = -1*heapq.heappop(self.leftHeap)
                    heapq.heappush(self.leftHeap,-1*v)
                    heapq.heappush(self.rightHeap,m)
                    self.rightSize += 1
            #Now we set the median
            if self.leftSize == self.rightSize:
                self.median = (1/2)*(-1*self.leftHeap[0] + self.rightHeap[0])
            elif self.leftSize > self.rightSize:
                self.median = -1*self.leftHeap[0]
            else:
                self.median = self.rightHeap[0]
    def addElement(self,v):
        self.updateMax(v)
        self.updateMin(v)
        self.updateMedian(v)
        self.updateMean(v)
    def printStatus(self):
        print("avg = {0}, median = {1}, max = {2}, min = {3}".format(
            self.mean,self.median,self.max,self.min))
        print("left heap is: {0}".format(self.leftHeap))
        print("right heap is: {0}".format(self.rightHeap))

if __name__ == "__main__":
    o = OnlineStatus()
    o.printStatus()
    o.addElement(1)
    o.printStatus()
    o.addElement(2)
    o.printStatus()
    o.addElement(3)
    o.printStatus()
    o.addElement(4)
    o.printStatus()
    o.addElement(5)
    o.printStatus()
    o.addElement(6)
    o.printStatus()
    o.addElement(7)
    o.printStatus()
