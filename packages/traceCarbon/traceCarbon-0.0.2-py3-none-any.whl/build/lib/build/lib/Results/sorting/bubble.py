import random

def bubble_sort(arr):
    for i in range(len(arr)):
        if i % 10000 == 0:
            print(i)
        swapped = False
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


if __name__ == "__main__":
    arr = [random.random() for _ in range(285996)]
    sorted_arr = bubble_sort(arr)
    print("Sorted array is:", sorted_arr)
    
