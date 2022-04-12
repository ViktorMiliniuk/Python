def merge_two_list(left, right):
    collect = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            collect.append(left[i])
            i += 1
        else:
            collect.append(right[j])
            j += 1

    if i < len(left):
        collect += left[i:]
    elif j < len(right):
        collect += right[j:]
    return collect


def merge_sort(array):
    if len(array) == 1:
        return array
    else:
        left = merge_sort(s[:len(s) // 2])
        right = merge_sort(s[len(s) // 2:])

        return merge_two_list(left, right)
