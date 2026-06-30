def make_uppercase(text_in):
    return text_in.upper()

def reverse_and_display(string_val):
    reversed_str = "".join(reversed(string_val))
    print("Reversed string:", reversed_str)

user_input = input("Enter a string: ")
capitalized = make_uppercase(user_input)

print("Uppercase:", capitalized)
reverse_and_display(capitalized)