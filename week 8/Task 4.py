rows = 4
for r in range(1, rows + 1):
    spaces = rows + 1 - r
    stars = 2 * r - 1
    for _ in range(spaces):
        print(" ", end="\t")
    for _ in range(stars):
        print("*", end="\t")
    print()