def display(num):
    if num == 0:
        return
    print(num)
    display(num - 1)
display(5)