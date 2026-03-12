def normalize_nums(nums):
    if isinstance(nums, str):
        nums = nums.split()
    if not isinstance(nums, list):
        return None
    if len(nums) < 1:
        return None
    for i in range(len(nums)):
        if isinstance(nums[i], float) and nums[i].is_integer():
            nums[i] = int(nums[i])
        if isinstance(nums[i], str) and (nums[i].isdigit() or (nums[i].startswith("-") and nums[i][1:].isdigit())):
            nums[i] = int(nums[i])
        if not isinstance(nums[i], int):
            return None
    return nums


def normalize_target(target):
    if isinstance(target, list) and len(target) == 1:
        target = target[0]
    if isinstance(target, str) and (target.isdigit() or (target.startswith("-") and target[1:].isdigit())):
        target = int(target)
    if not isinstance(target, int):
        return None
    return target


def two_sum(nums, target):
    nums = normalize_nums(nums)
    target = normalize_target(target)
    if nums is None:
        return "List format error"
    if target is None:
        return "Target format error"

    ans = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                ans.append([i, j])

    if len(ans) > 1:
        return "More than one answer"
    elif len(ans) == 1:
        return ans[0]
    else:
        return "No answer"
