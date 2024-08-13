import random
from codecarbon import EmissionsTracker


def insertion_sort(a):
    for i in range(1, len(a)):
        value = a[i]
        j = i-1
        while j>=0 and value<a[j]:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = value
    return a

tracker = EmissionsTracker()


for n in range(1, 25000, 1000):
    tracker.start_task("create array")
    a = [random.random() for _ in range(n)]
    array_creation = tracker.stop_task()
    tracker.start_task(f"Insertion n = {n}")
    insertion_sort(a)
    insertion_emissions = tracker.stop_task()

tracker.stop()


