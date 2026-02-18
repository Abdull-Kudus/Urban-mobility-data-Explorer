from typing import List, Dict


def _merge(left: List[Dict], right: List[Dict], key: str) -> List[Dict]:
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i][key] >= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(data: List[Dict], key: str) -> List[Dict]:
    if len(data) <= 1:
        return data

    mid   = len(data) // 2
    left  = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)

    return _merge(left, right, key)


def rank_zones_by_revenue(zone_revenue_list: List[Dict]) -> List[Dict]:
    return merge_sort(zone_revenue_list, key="total_revenue")