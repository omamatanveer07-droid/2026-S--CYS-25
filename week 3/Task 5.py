def compute_semester_gpa():
    num_courses = int(input("Enter number of subjects: "))
    weighted_sum = 0
    hours_sum = 0
    idx = 0
    while idx < num_courses:
        print(f"\nSubject {idx + 1}")
        points = float(input("Enter Grade Point: "))
        hours = int(input("Enter Credit Hours: "))

        weighted_sum += (points * hours)
        hours_sum += hours
        idx += 1
    if hours_sum > 0:
        final_gpa = weighted_sum / hours_sum
        print(f"\nYour GPA for this semester is: {final_gpa:.2f}")
    else:
        print("Total credits cannot be zero!")
compute_semester_gpa()