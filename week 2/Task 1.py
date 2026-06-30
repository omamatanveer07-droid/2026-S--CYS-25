
bin_str = input("Enter a binary number: ")
dec_val = 0
n = len(bin_str)
for i in range(n):
    bit = bin_str[n - 1 - i]
    if bit == '1':
        dec_val += 2 ** i
print("Decimal equivalent is:", dec_val)