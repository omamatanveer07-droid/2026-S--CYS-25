rows = 4
for level in range(1, rows + 1):
    spaces = rows - level
    stars = (2 * level) - 1
    print("  " * spaces, end="")
    for symbol in range(stars):
        print("* ", end="")

    print()