score_obtained = int(input("Enter obtained Marks: "))
score_total = int(input("Enter total Marks: "))

if score_total <= 0 or score_obtained < 0 or score_obtained > score_total:
    print("Invalid")
else:
    percentage = (score_obtained / score_total) * 100

    if percentage >= 90:
        grade_letter = "A"
    elif percentage >= 85:
        grade_letter = "A-"
    elif percentage >= 80:
        grade_letter = "B+"
    elif percentage >= 75:
        grade_letter = "B"
    elif percentage >= 70:
        grade_letter = "B-"
    elif percentage >= 65:
        grade_letter = "C+"
    elif percentage >= 60:
        grade_letter = "C"
    elif percentage >= 55:
        grade_letter = "C-"
    elif percentage >= 50:
        grade_letter = "D"
    else:
        grade_letter = "Fail"

    if grade_letter == "Fail":
        print(grade_letter)
    else:
        print(f"Your grade is {grade_letter}")