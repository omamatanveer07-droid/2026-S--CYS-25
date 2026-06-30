height = 4
for current_row in range(1, height + 1):
    leading_spaces = height - current_row
    row_stars = (current_row * 2) - 1
    print(("\t" * leading_spaces) + ("*\t" * row_stars))
for current_row in range(height - 1, 0, -1):
    leading_spaces = height - current_row
    row_stars = (current_row * 2) - 1
    print(("\t" * leading_spaces) + ("*\t" * row_stars))