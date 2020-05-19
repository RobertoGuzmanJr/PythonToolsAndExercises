"""
This is a problem from an interview. Here is the issue: you have a square matrix that is nxn, and within there are
numbers. These numbers represent elevations. Water flows from a higher elevation to its lowest neighbor (a neighbor is
defined as being in one of the four cardinal directions from the source). If water flows from one node in the matrix
to another adjoining one, these are said to be in the same "watershed." The challenge is twofold:

How do I label all nodes with the appropriate watershed (their exact names are irrelevant, but we want them to have
the same name if they are in the same watershed).

I want to also know how many watersheds there are, altogether.

EXAMPLE:

    0 1 2 2
    1 2 4 2
    1 2 0 3
    1 2 0 5

The coloring would be as follows:

    A A A B
    A A C D
    E C C C
    F G G G

SOLUTION:
This is ultimately a dynamic connectivity problem. The idea is that we can model each location as a node in a graph,
and there is a question as to whether or not there is a connection between adjoining nodes. We ultimately want the
connected components for this graph. To arrive at this, we will use the basic union find operation. To implement this,
it makes sense to use a one-D array since it is easier for bookkeeping. We will have a one to one correspondence between
this one-D array and the input, which is 2-D. Thus, we need a way to initialize this one-D array and the some methods
that allow us to convert coordinates.

The meat of this is in three different methods, though. The first is give a node and a 2D array from the input, we
need a method to identify its connected neighbors. The logic there is that we need to look in all 4 directions, only
if that direction exists. Then we find the min value and add those neighbors to the output.

Once we have the coordinates for the neighbors, we need to convert them to the corresponding 1D representation and then
update the entries in the array so that a node is pointing at its parents. We need a helper function to identify the
ultimate parents. Once we have all of this, we collect the entries into a dictionary and that gives us the connected
components.
"""
def findLowestNeighborRowAndColumn(mat,r,c):
    neighbors = []
    myValue = mat[r][c]
    minValue = float("inf")
    if r > 0:
        v = mat[r-1][c]
        if v < myValue:
            neighbors.append(("North",v,[r-1,c]))
            minValue = v if v < minValue else minValue
    if r < len(mat)-1:
        v = mat[r+1][c]
        if v < myValue:
            neighbors.append(("South",v,[r+1,c]))
            minValue = v if v < minValue else minValue
    if c > 0:
        v = mat[r][c-1]
        if v < myValue:
            neighbors.append(("West",v,[r,c-1]))
            minValue = v if v < minValue else minValue
    if c < len(mat)-1:
        v = mat[r][c+1]
        if v < myValue:
            neighbors.append(("East",v,[r,c+1]))
            minValue = v if v < minValue else minValue
    return None if len(neighbors) == 0 else list(filter(lambda x: x[1] == minValue,neighbors))

def convert2Dto1D(r,c,n):
    return n*r + c

def convert1Dto2D(k,n):
    r = k % n
    c = k - (n*r)
    return (r,c)

def initializeLabels(n):
    res = [x for x in range(n**2)]
    return res

def findParent(arr,n):
    while True:
        if arr[n] == n:
            return n
        else:
            n = arr[n]

def findWatersheds(input):
    arr = initializeLabels(len(input))
    for r in range(len(input)):
        for c in range(len(input[r])):
            k = convert2Dto1D(r,c,len(input))
            x = findLowestNeighborRowAndColumn(input,r,c)
            if x is not None:
                for parent in x:
                    j = convert2Dto1D(parent[2][0],parent[2][1],len(input))
                    arr[k] = j
    d = {}
    for a in range(len(arr)):
        p = findParent(arr,a)
        if d.get(p,"NA") == "NA":
            d[p] = [a]
        else:
            d[p].append(a)
    print("There are {0} different watersheds.".format(len(d.keys())))
    print("The watersheds are distributed as follows: {0}".format(d))

input = [ [0, 1, 2, 2],[1, 2, 4, 2],[1, 2, 0, 3],[1, 2, 0, 5]]
findWatersheds(input)


