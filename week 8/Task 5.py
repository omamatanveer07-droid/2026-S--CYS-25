n = 4
for x in range(n):
    for y in range(n - x - 1):
        print(" ", end="\t")

    for z in range(2 * x + 1):
        print("*", end="\t")
    print()