class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        results = []
        
        for i in range(len(nums)-2):
            if i == 0 or nums[i] > nums[i-1]:
                j = i+1
                k = len(nums)-1
                while j < k:
                    s = nums[i] + nums[j] + nums[k]
                    if s == 0:
                        results.append([nums[i],nums[j],nums[k]])
                    if s < 0:
                        current_j = j
                        while nums[current_j] == nums[j] and j < k:
                            j += 1
                    else:
                        current_k = k
                        while nums[current_k] == nums[k] and j < k:
                            k -= 1
        return results
