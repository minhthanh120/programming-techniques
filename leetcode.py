from typing import List
def searchRange(nums: List[int], target: int) -> List[int]:
    start = end = -1
    left = 0
    right = len(nums)-1
    while left <= right:
        mid = (right + left) // 2
        if (nums[mid] == target):
            if (start == -1):
                start = mid
            step = 1
            if (mid > 0 and nums[mid] == nums[mid - 1]):
                step = -1
            while mid<= right and mid >= left and nums[mid] == target:
                end = mid
                mid +=step
            break
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return [start, end] if start<end else [end,start]

print(searchRange(nums = [8,8,8], target = 8))