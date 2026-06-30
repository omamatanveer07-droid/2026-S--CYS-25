total_students = int(input("Enter Total Number of Students: "))

while total_students > 0:
    student_name = input("Enter Student Name : ")
    roll_id = input("Enter Student Roll Number : ")
    marks_earned = int(input("Enter Obtained marks : "))

    score_percentage = (marks_earned * 100) / 300

    print(f"Name is {student_name}")
    print(f"Rollnumber is {roll_id}")
    print(f"Percentage is {score_percentage:.2f}")

    if score_percentage >= 90:
        assigned_grade = "A"
    elif score_percentage >= 85:
        assigned_grade = "A-"
    elif score_percentage >= 80:
        assigned_grade = "B+"
    elif score_percentage >= 75:
        assigned_grade = "B"
    elif score_percentage >= 70:
        assigned_grade = "B-"
    elif score_percentage >= 65:
        assigned_grade = "C+"
    elif score_percentage >= 60:
        assigned_grade = "C"
    elif score_percentage >= 55:
        assigned_grade = "C-"
    elif score_percentage >= 50:
        assigned_grade = "D"
    else:
        assigned_grade = "Fail"

    if assigned_grade == "Fail":
        print(assigned_grade)
    else:
        print(f"Your grade is {assigned_grade}")
    total_students -= 1