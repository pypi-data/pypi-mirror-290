import random
def loop(a,sum1):
    for j in range(size):
        for i in range(size):
            sum1 = sum1 + a[i][j]
    return sum1

if __name__ == "__main__":
    import sys
    size = int(sys.argv[1])
    a = [[random.random() for i in range(size)] for j in range(size)]
    loop(a, 0)

