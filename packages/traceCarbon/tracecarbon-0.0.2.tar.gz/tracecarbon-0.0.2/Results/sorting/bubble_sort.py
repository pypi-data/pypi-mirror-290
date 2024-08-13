import random

def bubble_sort(arr):
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


if __name__ == "__main__":
    import sys
    input_size = int(sys.argv[-1])
    print(input_size)
    arr = [random.random() for _ in range(input_size)]
    bubble_sort(arr)

