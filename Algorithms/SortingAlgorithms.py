# Import the heap functions from python library
from heapq import heappush, heappop
import timeit
import random

"""
In this script, we will test the following sorting algorithms:
    -InsertionSort
    -SelectionSort
    -QuickSort
    -MergeSort
    -BubbleSort
    -HeapSort
    -GnomeSort
"""
def insertionSort(arr):
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[j] >= arr[i]:
                arr[j], arr[i] = arr[i], arr[j]

def selectionSort(arr):
    for i in range(len(arr)):
        for j in range(i,len(arr)):
            if arr[j] < arr[i]:
                arr[j],arr[i] = arr[i],arr[j]

def partition (arr,lo,hi):
    pivot = arr[lo]
    i = lo
    for j in range(i+1,hi+1):
        if arr[j] < pivot:
            i += 1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i],arr[lo] = arr[lo],arr[i]
    return i

def quickSort(arr,lo,hi):
    if lo < hi:
        p = partition(arr,lo,hi)
        quickSort(arr, lo, p - 1)
        quickSort(arr, p+1, hi)

def merge(arr, l, m, r):
    # create temporary lists
    L = arr[l:m + 1]
    R = arr[m + 1:r + 1]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there are any.
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there are any.
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1

# l is for left index and r is right index of the sub-array of arr to be sorted.
def mergeSort(arr, l, r):
    if l < r:
        # Same as (l+r)/2, but avoids overflow for large l and h.
        m = int((l + r) / 2)

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)

def bubbleSort(arr):
    numSwaps = 1
    while numSwaps > 0:
        numSwaps = 0
        for j in range(1,len(arr)):
            if arr[j] < arr[j-1]:
                arr[j],arr[j-1] = arr[j-1],arr[j]
                numSwaps += 1

# heappop - pop and return the smallest element from heap
# heappush - push the value item onto the heap, maintaining
#             heap invarient
# heapify - transform list into heap, in place, in linear time

# A class for Min Heap
class MinHeap:

    # Constructor to initialize a heap
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) / 2

    # Inserts a new key 'k'
    def insertKey(self, k):
        heappush(self.heap, k)

        # Decrease value of key at index 'i' to new_val

    # It is assumed that new_val is smaller than heap[i]
    def decreaseKey(self, i, new_val):
        self.heap[i] = new_val
        while (i != 0 and self.heap[self.parent(i)] > self.heap[i]):
            # Swap heap[i] with heap[parent(i)]
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)], self.heap[i])

            # Method to remove minium element from min heap

    def extractMin(self):
        return heappop(self.heap)

        # This functon deletes key at index i. It first reduces

    # value to minus infinite and then calls extractMin()
    def deleteKey(self, i):
        self.decreaseKey(i, float("-inf"))
        self.extractMin()

        # Get the minimum element from the heap

    def getMin(self):
        return self.heap[0]

def heapSort(arr):
    heap = MinHeap()
    for i in arr:
        heap.insertKey(i)
    for j in range(len(arr)):
        arr[j] = heap.extractMin()

def gnomeSort(arr):
    numElements = len(arr)
    i = 0
    while i <= numElements-1:
        if i == 0 or arr[i-1] <= arr[i]:
            i += 1
        else:
            arr[i-1],arr[i] = arr[i],arr[i-1]
            i -= 1

def mergeSortWrapper(arr):
    mergeSort(arr,0,len(arr)-1)

def quickSortWrapper(arr):
    quickSort(arr,0,len(arr)-1)

def sortTest(sortMethod,list,rep,num):
    SETUP_CODE = '''from __main__ import {0}'''.format(sortMethod)
    TEST_CODE = '''{0}({1})'''.format(sortMethod,list)

    # timeit.repeat statement
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=rep,
                          number=num)
    print('{0} time: {1}'.format(sortMethod,min(times)))

if __name__ == '__main__':
    #Random case
    L = [random.randrange(1, 100, 1) for i in range(500)]

    #Already sorted case.
    M = [i for i in range(500)]

    #Reverse-sorted case.
    N = [500-i for i in range(500)]

    inputs_random = {
        "selectionSort": L.copy(),
        "insertionSort": L.copy(),
        "quickSortWrapper": L.copy(),
        "mergeSortWrapper": L.copy(),
        "heapSort": L.copy(),
        "gnomeSort": L.copy(),
        "bubbleSort": L.copy()
    }

    inputs_sorted = {
        "selectionSort": M.copy(),
        "insertionSort": M.copy(),
        "quickSortWrapper": M.copy(),
        "mergeSortWrapper": M.copy(),
        "heapSort": M.copy(),
        "gnomeSort": M.copy(),
        "bubbleSort": M.copy()
    }

    inputs_reverse = {
        "selectionSort": N.copy(),
        "insertionSort": N.copy(),
        "quickSortWrapper": N.copy(),
        "mergeSortWrapper": N.copy(),
        "heapSort": N.copy(),
        "gnomeSort": N.copy(),
        "bubbleSort": N.copy()
    }

    print("Random Cases")
    for key in inputs_random.keys():
        sortTest(key,inputs_random[key],3,50)

    print("Sorted Cases")
    for key in inputs_sorted.keys():
        sortTest(key,inputs_sorted[key],3,50)

    print("Reverse Cases")
    for key in inputs_reverse.keys():
        sortTest(key,inputs_reverse[key],3,50)
