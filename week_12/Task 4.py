def fibonacci(num):
    if num <= 1:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)
n = 6
result = fibonacci(n)
print("Fibonacci number at position", n, "is:", result)