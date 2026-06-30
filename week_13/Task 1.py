try:
    number = int(input("Enter your number: "))
    print(number)
except ValueError:
    print("Invalid")
finally:
    print("Hello World")