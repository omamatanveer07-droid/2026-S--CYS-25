def find_max(x, y):
    if x > y:
        return x
    return y

def display_multiplication(base, limit):
    print(f"Multiplication Table of {base} up to {limit}")
    count = 1
    while count <= limit:
        print(f"{base} x {count} = {base * count}")
        count += 1

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

max_val = find_max(num1, num2)
print("Largest number is:", max_val)

table_limit = int(input("Enter range for table: "))
display_multiplication(max_val, table_limit)