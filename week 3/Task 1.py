def get_factorial(num):
    result = 1
    current = 1
    while current <= num:
        result *= current
        current += 1
    return result

def calc_p(n, r):
    return get_factorial(n) // get_factorial(n - r)

def calc_c(n, r):
    return calc_p(n, r) // get_factorial(r)

total_items = int(input("Enter value of n: "))
chosen_items = int(input("Enter value of r: "))

print("Permutation (nPr) =", calc_p(total_items, chosen_items))
print("Combination (nCr) =", calc_c(total_items, chosen_items))