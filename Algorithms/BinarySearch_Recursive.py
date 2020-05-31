    def binarySearch(self,arr,i,low,high):
        if abs(high-low) <= 1 and arr[low] != i and arr[high] != i:
            return -1
        mid = int((low+high)/2) if (low + high)%2 == 0 else int(math.floor((low+high)/2))
        if arr[mid] == i:
            return mid
        elif arr[mid] < i:
            return self.binarySearch(arr,i,mid,high)
        else:
            return self.binarySearch(arr,i,low,mid)
