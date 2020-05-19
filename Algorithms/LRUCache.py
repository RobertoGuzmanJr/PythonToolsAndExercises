"""
This is a question from an interview. In this question, what we want to do is implement an API for an LRU cache.
The LRU stands for "Least Recently Used." In this problem, we want to support two operations: put and get.

Put should add an element to the LRU Cache. Get should return an element from the LRU cache. After we execute the get
 operation, we should ensure that we update its timestamp, so that we know it has been most-recently used.
 Both of these operations should have constant-time performance (O(1)).

Further, the LRU cache has a capacity. If we exceed this capacity, then we will evict the least-recently used entity.
"""

class Node:
    def __init__(self,d):
        self.data = d
        self.Next = None
        self.Previous = None

class LRUCache:
    def __init__(self,c):
        self.head = None
        self.tail = None
        self.capacity = c
        self.cache = {}
    def get(self,v):
        result = self.cache.get(v,None)
        #Key is missing.
        if not result:
            return None
        #Key is present.
        else:
            #check if the head is pointing at it.
            if self.head == result:
                self.head = result.Next
            #add it to the tail, so we know we used it.
            self.tail.Next = result
            result.Previous.Next = result.Next
            result.Next.Previous = result.Previous
            result.Previous = self.tail
            result.Next = None
            self.tail = result
            return result
    def put(self,v):
        n = Node(v)
        if len(self.cache) == self.capacity:
            del self.cache[self.head.data]
            self.head = self.head.Next
        self.cache[v] = n

        if len(self.cache.keys()) == 1:
            self.tail = n
            self.head = n
        else:
            self.tail.Next = n
            n.Previous = self.tail
            self.tail = n
    def printCache(self):
        printer = self.head
        print("Printing from oldest to newest:")
        s = ""
        while printer:
            s += "{0} -> ".format(printer.data)
            printer = printer.Next
        print(s)
        print("We reached the end! Just to check, the tail is pointed at {0}".format(self.tail.data))

c = LRUCache(10)

for i in range(10):
    c.put(i)

c.printCache()

print("We are getting 5: {0}".format(c.get(5).data))
c.printCache()
print("We are getting 5: {0}".format(c.get(5).data))
c.printCache()
print("We will put 11!")
c.put(11)
c.printCache()
print("We will put 12!")
c.put(12)
c.printCache()
print("We will get 7!")
c.get(7)
c.printCache()
