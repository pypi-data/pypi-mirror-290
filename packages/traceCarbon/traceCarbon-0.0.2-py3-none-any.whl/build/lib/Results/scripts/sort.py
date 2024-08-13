import random
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplCoreDomain, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter
from pyJoules.handler.csv_handler import CSVHandler

domains = [RaplPackageDomain(0), RaplPackageDomain(1), RaplDramDomain(0), RaplDramDomain(1)]
devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)

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

def insertion_sort(a):
    for i in range(1, len(a)):
        value = a[i]
        j = i-1
        while j>=0 and value<a[j]:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = value
    return a

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

def merge_sort(arr):
    if len(arr) > 1:
        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements into 2 halves
        L = arr[:mid]
        R = arr[mid:]

        # Sorting the first half
        merge_sort(L)

        # Sorting the second half
        merge_sort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Python3 implementation of QuickSort


# Function to find the partition position
def partition(array, low, high):

    # Choose the rightmost element as pivot
    pivot = array[high]

    # Pointer for greater element
    i = low - 1

    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1

def quicksort(array, low, high):
    if low < high:

        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # Recursive call on the left of pivot
        quicksort(array, low, pi - 1)

        # Recursive call on the right of pivot
        quicksort(array, pi + 1, high)


meter.start()
for n in range(1, 25000, 1000):
    meter.record(tag = 'array creation')
    a = [random.random() for i in range(n)]
    meter.record(tag = 'quicksort')
    quicksort(a, 0, len(a) - 1)
    meter.record(tag = 'merge')
    merge_sort(a)
    meter.record(tag = 'selection')
    selection_sort(a)
    meter.record(tag = 'bubble')
    bubble_sort(a)
    meter.record(tag = 'insertion')
    insertion_sort(a)
    print("iteration done")
meter.stop()

csv_handler = CSVHandler('/home/dermot/sorting/sort-results.csv')
trace = meter.get_trace()
idles = meter.gen_idle(trace)
trace.remove_idle(idles)
csv_handler.process(trace)
csv_handler.save_data()
