def sort(arr):
    if not arr:
        return arr

    mn = min(arr)
    offset = 0
    if mn < 0:
        offset = -mn
        arr = [x + offset for x in arr]

    mx = max(arr)
    range_size = mx + 1
    if range_size > 1_000_000:
        raise ValueError(f"Range too large for counting sort: {range_size}")

    count = [0] * (mx + 1)
    for num in arr:
        count[num] += 1

    out = []
    for num, c in enumerate(count):
        if c:
            out.extend([num] * c)

    if offset:
        out = [x - offset for x in out]

    return out
