import time
import random

questions = []
subjects = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology"]
Backgrounds = ["ICS", "Pre-Engineering", "Pre-Medical"]
# ============ Subject: Computer Science ============
questions.append({
    "subject": "Computer Science",
    "question": "What does CPU stand for?",
    "choices": {
        "A": "Central Processing Unit",
        "B": "Computer Personal Unit",
        "C": "Central Program Unit",
        "D": "Central Processor Unit"
    },
    "answer": "A"
})
questions.append({
    "subject": "Computer Science",
    "question": "What is the main function of an operating system?",
    "choices": {
        "A": "To manage computer hardware and software resources",
        "B": "To create new software applications",
        "C": "To connect to the internet",
        "D": "To design computer networks"
    },
    "answer": "A"
})

# ============ Subject: Mathematics ============
questions.append({
    "subject": "Mathematics",
    "question": "What is the value of π (pi) approximately?",
    "choices": {
        "A": "2.14",
        "B": "3.14",
        "C": "4.14",
        "D": "5.14"
    },
    "answer": "B"
})
questions.append({
    "subject": "Mathematics",
    "question": "What is the derivative of sin(x)?",
    "choices": {
        "A": "cos(x)",
        "B": "-cos(x)",
        "C": "-sin(x)",
        "D": "tan(x)"
    },
    "answer": "A"
})

# ============ Subject: Physics ============
questions.append({
    "subject": "Physics",
    "question": "What is the speed of light in a vacuum?",
    "choices": {
        "A": "3 x 10^8 m/s",
        "B": "3 x 10^6 m/s",
        "C": "3 x 10^4 m/s",
        "D": "3 x 10^2 m/s"
    },
    "answer": "A"
})
questions.append({
    "subject": "Physics",
    "question": "What is Newton's second law of motion?",
    "choices": {
        "A": "F = m * a",
        "B": "E = mc^2",
        "C": "V = IR",
        "D": "P = IV"
    },
    "answer": "A"
})

# ============ Subject: Chemistry ============
questions.append({
    "subject": "Chemistry",
    "question": "What is the chemical symbol for water?",
    "choices": {
        "A": "H2O",
        "B": "O2",
        "C": "CO2",
        "D": "NaCl"
    },
    "answer": "A"
})
questions.append({
    "subject": "Chemistry",
    "question": "What is the pH of a neutral solution?",
    "choices": {
        "A": "0",
        "B": "7",
        "C": "14",
        "D": "1"
    },
    "answer": "B"
})

# ============ Subject: Biology ============
questions.append({
    "subject": "Biology",
    "question": "What is the basic unit of life?",
    "choices": {
        "A": "Atom",
        "B": "Molecule",
        "C": "Cell",
        "D": "Organ"
    },
    "answer": "C"
})
questions.append({
    "subject": "Biology",
    "question": "What is the process by which plants make their food?",
    "choices": {
        "A": "Respiration",
        "B": "Photosynthesis",
        "C": "Transpiration",
        "D": "Germination"
    },
    "answer": "B"
})

# Shuffle the questions to randomize the order
random.shuffle(questions)

# ============ Exam State ============
answered_questions = {}
skipped_questions = []
deleted_questions = []
# ======== Student Marks and Results ============
student_mark = {}
student_results = {}

# ========== Credentials for Admin and Students ===========
admin_name = "ecat_admin"
admin_pass = "ecat@2026"

student_name = "student"
student_pass = "student123"


# =========== Shared Functions ===========
def auth_users(username, password, user_type):
    if user_type == "admin":
        return username == admin_name and password == admin_pass
    elif user_type == "student":
        return username == student_name and password == student_pass
    return False


def view_results():
    print("========== View Results ==========")
    if student_name in student_results:
        result = student_results[student_name]
        print(f"Student: {student_name}, Score: {result['score']}, Total Questions: {result['total']}")
    else:
        print("No results available for this student.")
    print("================================")


# ================= Admin Functions ================
def view_all_questions():
    print("========== All Questions ==========")
    for index, q in enumerate(questions):
        print(f"{index + 1}. [{q['subject']}] {q['question']}")
        for choice_key, choice_value in q['choices'].items():
            print(f"   {choice_key}. {choice_value}")
        print(f"   Correct Answer: {q['answer']}", end="\n")
    print("=================================")


def add_new_question():
    print("========== Add a New Question ==========")
    subject = input("Enter the subject: ")
    question_text = input("Enter the question: ")
    choices = {}
    for option in ['A', 'B', 'C', 'D']:
        choice_text = input(f"Enter choice {option}: ")
        choices[option] = choice_text
    correct_answer = input("Enter the correct answer (A/B/C/D): ").upper()
    if correct_answer not in ['A', 'B', 'C', 'D']:
        print("Invalid answer choice. Question not added.")
        return
    # New Questions Addition
    questions.append({
        "subject": subject,
        "question": question_text,
        "choices": choices,
        "answer": correct_answer
    })
    print("Question added successfully!")


def edit_question():
    print("========== Edit a Question ==========")
    view_all_questions()
    try:
        question_number = int(input("Enter the question number to edit: "))
        if 1 <= question_number <= len(questions):
            question = questions[question_number - 1]
            print(f"Editing Question {question_number}: [{question['subject']}] {question['question']}")
            for choice_key, choice_value in question['choices'].items():
                print(f"   {choice_key}. {choice_value}")
                correct_answer = question['answer']
            new_subject = input(f"Enter new subject (leave blank to keep '{question['subject']}'): ")
            new_question_text = input(f"Enter new question (leave blank to keep current): ")
            new_choices = {}
            for option in ['A', 'B', 'C', 'D']:
                new_choice_text = input(
                    f"Enter new choice {option} (leave blank to keep '{question['choices'][option]}'): ")
                new_choices[option] = new_choice_text if new_choice_text else question['choices'][option]
            new_correct_answer = input(
                f"Enter new correct answer (A/B/C/D) (leave blank to keep '{question['answer']}'): ").upper()
            new_correct_answer = new_correct_answer if new_correct_answer in ['A', 'B', 'C', 'D'] else question[
                'answer']
            # Update the question
            question['subject'] = new_subject if new_subject else question['subject']
            question['question'] = new_question_text if new_question_text else question['question']
            question['choices'] = new_choices
            question['answer'] = new_correct_answer
            print("Question updated successfully!")
        else:
            print("Invalid question number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_question():
    print("========== Delete a Question ==========")
    view_all_questions()
    try:
        question_number = int(input("Enter the question number to delete: "))
        if 1 <= question_number <= len(questions):
            delete_confirm = input(f"Are you sure you want to delete question {question_number}? (yes/no): ").lower()
            if delete_confirm == "yes":
                deleted_questions.append(questions.pop(question_number - 1))
                print("Question deleted successfully!")
            else:
                print("Deletion cancelled.")
    except ValueError:
        print("Please enter a valid number.")


def view_student_results():
    print("========== Student Results ==========")
    if not student_results:
        print("No student results available.")
    else:
        for student, result in student_results.items():
            print(f"Student: {student}, Score: {result['score']}, Total Questions: {result['total']}")
    print("===================================")


def questions_bank_statistics():
    print("========== Questions Bank Statistics ==========")
    subject_count = {}
    for q in questions:
        subject = q['subject']
        if subject in subject_count:
            subject_count[subject] += 1
        else:
            subject_count[subject] = 1
    for subject, count in subject_count.items():
        print(f"{subject}: {count} questions")
    print("===================================")


# =========== Student Functions ===========
def exam_rules():
    print("========== Exam Rules ==========")
    print("1. The exam consists of multiple-choice questions.")
    print("2. Each question has four options: A, B, C, and D.")
    print("3. Only one option is correct for each question.")
    print("4. You will receive 4 marks for each correct answer.")
    print("5. Wrong answer will deduct 1 mark.")
    print("6. You can skip questions, Enter S to skip a question and it will be marked as skipped.")
    print("7. You can view your results at the end of the exam.")
    print("8. Enter submit to finish the exam.")


def skipped_questions_report():
    if skipped_questions:
        print("========== Skipped Questions Report ==========")
        for index, q in enumerate(skipped_questions):
            print(f"{index + 1}. [{q['subject']}] {q['question']}")
            for choice_key, choice_value in q['choices'].items():
                print(f"   {choice_key}. {choice_value}")
        print("=============================================")
    else:
        print("No questions were skipped.")


def start_exam():
    name = input("Enter your name: ")
    roll_no = input("Enter your roll number: ")
    background = input("Enter your background (ICS/Pre-Engineering/Pre-Medical): ")
    if background not in Backgrounds:
        print("Invalid background. Please enter one of the following: ICS, Pre-Engineering, Pre-Medical.")
        return
    score = 0
    total_questions = len(questions)
    for index, q in enumerate(questions):
        print(f"Question {index + 1}/{total_questions}: [{q['subject']}] {q['question']}")
        for choice_key, choice_value in q['choices'].items():
            print(f"   {choice_key}. {choice_value}")
        answer = input("Your answer (A/B/C/D/S to skip): ").upper()
        if answer == "S":
            skipped_questions.append(q)
            print("Question skipped.")
        elif answer == q['answer']:
            score += 4
            answered_questions[q['question']] = "Correct"
        else:
            score -= 1
            answered_questions[q['question']] = "Wrong"
        time.sleep(1)  # Pause for a moment before the next question
    student_results[student_name] = {"score": score, "total": total_questions}
    skip_questions = input("Do you want to see the skipped questions report? (yes/no): ").lower()
    if skip_questions == "yes":
        skipped_questions_report()
    else:
        print(f"Exam finished!")
    student_results[student_name] = {"score": score, "total": total_questions}
    student_mark[student_name] = score


def take_exam():
    print("========== Take the Exam ==========")
    exam_rules()
    press_enter = input("Press Enter to start the exam...")
    start_exam()


# =========== Main body ===========
while True:
    print("Welcome to the ECAT Exam System")
    print("1. Admin Login")
    print("2. Student Login")
    print("3. Exit")
    choice = input("Please select an option: ")
    attempts = 0
    if choice == "1":
        while attempts < 3:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if auth_users(username, password, "admin"):
                print("Admin login successful!")
                while True:
                    # ====== Admin Menu =======
                    print("========== Admin Menu ==========")
                    print("1. View all questions")
                    print("2. Add a new question")
                    print("3. Edit an existing question")
                    print("4. Delete a question")
                    print("5. view student results")
                    print("6. Questions bank statistics")
                    print("7. Logout")
                    print("================================")
                    adminn_choice = input("Please select an option: ")
                    if adminn_choice == "1":
                        # View all questions
                        view_all_questions()
                    elif adminn_choice == "2":
                        # Add a new question
                        add_new_question()
                    elif adminn_choice == "3":
                        # Edit an existing question
                        edit_question()
                    elif adminn_choice == "4":
                        # Delete a question
                        delete_question()
                    elif adminn_choice == "5":
                        # View student results
                        view_student_results()
                    elif adminn_choice == "6":
                        # Questions bank statistics
                        questions_bank_statistics()
                    elif adminn_choice == "7":
                        # Logout
                        break
            else:
                print("Invalid credentials. Please try again.")
                attempts += 1
        if attempts == 3:
            print("Too many failed attempts. Returning to main menu.")
    elif choice == "2":
        while attempts < 3:
            username = input("Enter student username: ")
            password = input("Enter student password: ")
            if auth_users(username, password, "student"):
                print("Student login successful!")
                while True:
                    # ====== Student Menu =======
                    print("========== Student Menu ==========")
                    print("1. Take the exam")
                    print("2. View Results")
                    print("3. Logout")
                    print("================================")
                    student_choice = input("Please select an option: ")
                    if student_choice == "1":
                        # start the exam
                        take_exam()
                    elif student_choice == "2":
                        # View results
                        view_results()
                    elif student_choice == "3":
                        # Logout
                        break
            else:
                print("Invalid credentials. Please try again.")
                attempts += 1
        if attempts == 3:
            print("Too many failed attempts. Returning to main menu.")
    elif choice == "3":
        print("Exiting the system. Goodbye!")
        break