size = 5

for row in range(size):
    spaces = size - row
    stars = 2 * row + 1

    print(" " * spaces + "*" * stars)