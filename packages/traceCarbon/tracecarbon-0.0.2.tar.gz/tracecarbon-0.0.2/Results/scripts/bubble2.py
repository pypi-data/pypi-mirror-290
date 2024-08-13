import random
def bubble_sort(a):
    for i in range(len(a)):
        swapped = False
        for j in range(len(a)-1-i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if swapped == False:
            break
    return 

a = [random.random() for i in range(1000000)]
bubble_sort(a)

