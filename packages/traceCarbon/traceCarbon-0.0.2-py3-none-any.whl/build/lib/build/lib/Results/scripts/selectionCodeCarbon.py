import random
from codecarbon import EmissionsTracker

def selection_sort(arr):
    # Traverse through all array elements
    for i in range(len(arr)):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

tracker = EmissionsTracker()
for n in range(1, 25000, 1000):
    tracker.start_task("create array")
    a = [random.random() for _ in range(n)]
    array_creation = tracker.stop_task()
    tracker.start_task(f"Selection n = {n}")
    selection_sort(a)
    selection_emissions = tracker.stop_task()

tracker.stop()
