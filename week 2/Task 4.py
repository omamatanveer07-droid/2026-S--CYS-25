import random
import string

pwd_len = int(input("Eter length of password: "))
use_upper = input("Include uppercase letters? (yes/no): ").lower() == "yes"
use_lower = input("Include lowercase letters? (yes/no): ").lower() == "yes"
use_digits = input("Include digits? (yes/no): ").lower() == "yes"
use_special = input("Include special characters? (yes/no): ").lower() == "yes"

pool = ""
if use_upper:
    pool += string.ascii_uppercase
if use_lower:
    pool += string.ascii_lowercase
if use_digits:
    pool += string.digits
if use_special:
    pool += string.punctuation

if not pool:
    print("You must select at least one character type!")
else:
    result = "".join(random.choice(pool) for _ in range(pwd_len))
    print("Your password is:", result)