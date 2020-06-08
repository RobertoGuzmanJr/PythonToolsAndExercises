class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        m = len(nums1)
        n = len(nums2)
        
        p1 = p2 = 0
        mids = []
        s = 0
        
        #even case
        if (m + n) % 2 == 0:
            while s <= (m+n)/2:
                val = 0
                if p1 == m:
                    val = nums2[p2]
                    p2 += 1
                elif p2 == n:
                    val = nums1[p1]
                    p1 += 1
                elif nums1[p1] <= nums2[p2]:
                    val = nums1[p1]
                    p1 += 1
                else:
                    val = nums2[p2]
                    p2 += 1
                if s in [((m+n)/2),((m+n)/2)-1]:
                    mids.append(val)
                s += 1                    
        #odd case
        else:
            while s <= (m+n)/2:
                val = 0
                if p1 == m:
                    val = nums2[p2]
                    p2 += 1
                elif p2 == n:
                    val = nums1[p1]
                    p1 += 1
                elif nums1[p1] <= nums2[p2]:
                    val = nums1[p1]
                    p1 += 1
                else:
                    val = nums2[p2]
                    p2 += 1
                if s in [(m+n-1)/2]:
                    mids.append(val)
                s += 1
        return mean(mids)
