obtained = int(input("Enter obtained Marks: "))
total_pts = int(input("Enter total number: "))

final_ratio = (obtained * 100) / total_pts
print(final_ratio)

if final_ratio <= 0 or obtained > total_pts:
    print("Invalid")
elif final_ratio >= 90:
    print("Your grade is A")
elif final_ratio >= 85:
    print("Your grade is A-")
elif final_ratio >= 80:
    print("Your grade is B+")
elif final_ratio >= 75:
    print("Your grade is B")
elif final_ratio >= 70:
    print("Your grade is B-")
elif final_ratio >= 65:
    print("Your grade is C+")
elif final_ratio >= 60:
    print("Your grade is C")
elif final_ratio >= 55:
    print("Your grade is C-")
elif final_ratio >= 50:
    print("Your grade is D")
else:
    print("Fail")