import math as m

def BinarySearch(L,k):
    if len(L) == 0:
        return False
    if L[0] == k:
        return True
    n = len(L)

    if n % 2 == 0:
        s1 = int((n-2)/2)
        s2 = int(n/2)
        if k >= L[0] and k <= L[s1]:
            return BinarySearch(L[0:(s1+1)],k)
        elif k >= L[s2] and k <= L[n-1]:
            return BinarySearch(L[s2:n],k)
        else:
            return False
    else:
        if L[int((n-1)/2)] == k:
            return True
        s1 = int((n-3)/2)
        s2 = int((n+1)/2)
        if k >= L[0] and k <= L[s1]:
            return BinarySearch(L[0:(s1+1)],k)
        elif k >= L[s2] and k <= L[n-1]:
            return BinarySearch(L[s2:n],k)
        else:
            return False

def circularlySortedBinarySearch(L,k):
    pivot = -1

    #first, locate the pivot point
    for i in range(1,len(L)):
        if L[i] - L[i-1] < 0:
            pivot = i
            break
    #now we call the binary search on the appropriate pivoted list.
    if pivot > 0:
        L1 = L[pivot:len(L)]
        L1.extend(L[0:pivot])
        return BinarySearch(L1,k)
    else:
        return BinarySearch(L,k)

if __name__ == '__main__':
    import random as rand

    N = 500
    L = []
    for i in range(rand.randint(0,N)):
        L.append(rand.randint(0,N))
    L.sort()
    p = rand.randint(0,len(L))
    N = L[p:len(L)]
    N.extend(L[0:p])
    print(L)
    print(N)
    print(p)
    for j in range(rand.randint(0,20)):
        h = rand.randint(0,500)
        print("Here is iteration: {0}, checking {1}".format(j,h))
        print(BinarySearch(L,h))
        print(circularlySortedBinarySearch(N,h))
