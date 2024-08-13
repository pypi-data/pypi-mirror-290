import random

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key

if __name__ == "__main__":
    import sys
    input_size = int(sys.argv[-1])
    print(input_size)
    arr = [random.random() for _ in range(input_size)]
    insertion_sort(arr)

