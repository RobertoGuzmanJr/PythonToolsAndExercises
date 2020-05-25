"""
This is an interview question. Suppose you have a list of integers and you want to return the kth largest. That is,
if k is 0, you want to return the largest element in the list. If k is the length of the list minus 1, it means that
you want to return the smallest element.

In this exercise, we want to do this in less than quadratic time (O(n^2)).

Our first approach will sort the data and then select the index of the kth largest. This is O(n*lg(n)) since it involves
a sort and that is known to done in O(n*lg(n)) time with mergeSort or QuickSort.

Our second approach will solve the same problem, but will do so using a specified amount of extra space, S.
"""
import heapq
import math

def kthLargest_SortApproach(arr,k):
    if k >= len(arr):
        return None
    arr.sort()
    return arr[len(arr)-1-k]

def kthLargest_FixedSpace(arr,k):
    if k > len(arr):
        return None
    heap = arr[0:k+1]
    heapq.heapify(heap)

    for i in range(k+1,len(arr)):
        if arr[i] >= heap[0]:
            heap[0] = arr[i]
            heapq.heapify(heap)
    return heap[0]



arr = [6,3,0,3,2,7,5,6,78,12,21]

print(kthLargest_FixedSpace(arr,6))
print(kthLargest_FixedSpace(arr,0))
print(kthLargest_FixedSpace(arr,10))

print(kthLargest_SortApproach(arr,6))
print(kthLargest_SortApproach(arr,0))
print(kthLargest_SortApproach(arr,10))
