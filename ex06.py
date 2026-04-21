def median_of_three(arr: list, left: int, right: int) -> int:
    mid = (left + right) // 2
    a, b, c = arr[left], arr[mid], arr[right]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    if (b <= a <= c) or (c <= a <= b):
        return left
    return right

def partition(arr: list, left: int, right: int) -> int:
    pivot_index = median_of_three(arr, left, right)
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quickselect(arr: list, k: int) -> int:
    arr = arr[:]
    left, right = 0, len(arr) - 1
    target = k - 1
    def qs(left: int, right: int) -> int:
        pivot_index = partition(arr, left, right)
        if target == pivot_index:
            return arr[pivot_index]
        if target < pivot_index:
            return qs(left, pivot_index - 1)
        return qs(pivot_index + 1, right)
    return qs(left, right)


tests = [
    ([3, 1, 4, 1, 5, 9, 2, 6], 3),
    ([7, 2, 5, 1, 8, 3], 1),
    ([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 7),
]

for array, k_smallest in tests:
    resultado = quickselect(array, k_smallest)
    esperado = sorted(array)[k_smallest - 1]
    print(f"arr={array}")
    print(f"k={k_smallest} -> {k_smallest}-ésimo menor = {resultado} (esperado={esperado})")
