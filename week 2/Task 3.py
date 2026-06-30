low = int(input("Enter starting number: "))
high = int(input("Enter ending number: "))
prime_list = []
prime_sum = 0
for val in range(low, high + 1):
    if val < 2:
        continue
    check = True
    for factor in range(2, int(val ** 0.5) + 1):
        if val % factor == 0:
            check = False
            break
    if check:
        prime_list.append(val)
        prime_sum += val
print("Prime numbers:", prime_list)
print("Sum of primes:", prime_sum)