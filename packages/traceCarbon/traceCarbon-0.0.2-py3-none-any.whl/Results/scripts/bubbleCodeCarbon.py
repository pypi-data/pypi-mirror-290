import random
from codecarbon import EmissionsTracker
def bubble_sort(a):
    for i in range(len(a)):
        swapped = False
        for j in range(len(a)-1-i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if swapped == False:
            break
    return a

tracker = EmissionsTracker()

for n in range(1, 25000, 1000):
    tracker.start_task("create array")
    a = [random.random() for _ in range(n)]
    array_creation = tracker.stop_task()
    tracker.start_task(f"Bubble n = {n}")
    bubble_sort(a)
    bubble_emissions = tracker.stop_task()
    
tracker.stop()
