grid_size = 4

for current_row in range(1, grid_size + 1):
    leading_spaces = grid_size - current_row
    row_stars = (current_row * 2) - 1
    print(("\t" * leading_spaces) + ("*\t" * row_stars))