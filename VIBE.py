#Meloney Mattison
#CIS261
#WK10 VIBE Coding

import os

GRADE_FILE = "student_grades.txt"


def is_esc_input(s: str) -> bool:
    """Return True if the user's input represents an ESC keypress or the string 'ESC'.

    Some terminals deliver the actual ESC character (ASCII 27) when the user
    presses the Escape key. Detect both textual "ESC" and the raw escape
    character so pressing the key works the same as typing ESC.
    """
    if s is None:
        return False
    if not isinstance(s, str):
        return False
    if s.strip().upper() == "ESC":
        return True
    if s and ord(s[0]) == 27:
        return True
    return False


def calculate_letter_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def calculate_average(test1: float, test2: float, test3: float) -> float:
    return round((test1 + test2 + test3) / 3, 2)


def load_student_records(filename: str):
    students = []
    if not os.path.exists(filename):
        print(f"No existing record file found. A new file will be created at '{filename}'.")
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                record = line.strip()
                if not record:
                    continue
                parts = record.split("|")
                if len(parts) != 7:
                    print(f"Skipping invalid record on line {line_number}: wrong field count")
                    continue
                name, student_id, test1, test2, test3, average, grade = [part.strip() for part in parts]
                try:
                    test1_value = float(test1)
                    test2_value = float(test2)
                    test3_value = float(test3)
                except ValueError:
                    print(f"Skipping invalid scores on line {line_number}.")
                    continue
                calculated_average = calculate_average(test1_value, test2_value, test3_value)
                calculated_grade = calculate_letter_grade(calculated_average)
                students.append({
                    "name": name,
                    "id": student_id,
                    "test1": test1_value,
                    "test2": test2_value,
                    "test3": test3_value,
                    "average": calculated_average,
                    "grade": calculated_grade,
                })
    except IOError as error:
        print(f"Error reading '{filename}': {error}")
    return students


def save_student_records(filename: str, students):
    try:
        print("Saving records...")
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student['name']}|{student['id']}|{student['test1']:.2f}|{student['test2']:.2f}|{student['test3']:.2f}|{student['average']:.2f}|{student['grade']}\n"
                )
        print(f"√ Saved {len(students)} student record(s) to file.")
    except IOError as error:
        print(f"Error saving records to '{filename}': {error}")


def get_float_input(prompt: str):
    while True:
        raw = input(prompt)
        value = raw.strip()
        if is_esc_input(raw):
            return None
        try:
            score = float(value)
            if score < 0:
                print("Score cannot be negative. Please enter a non-negative value.")
                continue
            return score
        except ValueError:
            print("Invalid input. Enter a numeric score or type ESC to cancel.")


def add_student(students):
    print("\nAdd New Student Record")
    name_raw = input("Student name: ")
    name = name_raw.strip()
    if is_esc_input(name_raw) or not name:
        print("Student entry canceled.")
        return

    student_id_raw = input("Student ID: ")
    student_id = student_id_raw.strip()
    if is_esc_input(student_id_raw) or not student_id:
        print("Student entry canceled.")
        return

    scores = []
    for i in range(1, 4):
        score = get_float_input(f"Test {i} score: ")
        if score is None:
            print("Student entry canceled.")
            return
        scores.append(score)

    average = calculate_average(scores[0], scores[1], scores[2])
    grade = calculate_letter_grade(average)
    students.append({
        "name": name,
        "id": student_id,
        "test1": scores[0],
        "test2": scores[1],
        "test3": scores[2],
        "average": average,
        "grade": grade,
    })
    delineate("STUDENT ADDED")
    print(f"✓ Added student: {name} (ID: {student_id})")
    print(f"Average: {average:.2f} | Grade: {grade}")


def display_all_students(students):
    if not students:
        print("\nNo student records to display.")
        return

    print("\nStudent Records")
    print("{:<20} {:<12} {:>8} {:>8} {:>8} {:>10} {:>6}".format(
        "Name", "ID", "Test1", "Test2", "Test3", "Average", "Grade"
    ))
    print("-" * 74)
    for student in students:
        print("{:<20} {:<12} {:>8.2f} {:>8.2f} {:>8.2f} {:>10.2f} {:>6}".format(
            student["name"],
            student["id"],
            student["test1"],
            student["test2"],
            student["test3"],
            student["average"],
            student["grade"],
        ))


def delineate(title: str):
    """Display a professional delineated header."""
    width = 64
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def display_grade_distribution(students):
    """Print the grade distribution (letter grade -> count)."""
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        g = s.get("grade", "F")
        counts[g] = counts.get(g, 0) + 1

    print()
    print("Grade Distribution:")
    sorted_grades = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    sorted_grades = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    for grade, cnt in sorted_grades:
        if cnt > 0:
            print(f"  {grade}: {cnt} student(s)")


def calculate_class_statistics(students):
    if not students:
        print("\nNo student records available for statistics.")
        return
    averages = [student["average"] for student in students]
    highest_avg = max(averages)
    lowest_avg = min(averages)

    highest_students = [student for student in students if student["average"] == highest_avg]
    lowest_students = [student for student in students if student["average"] == lowest_avg]

    print()
    delineate("CLASS STATISTICS")

    highest_names = ", ".join([student['name'] for student in highest_students])
    print(f"\nHighest average: {highest_avg:.2f} ({highest_names})")

    lowest_names = ", ".join([student['name'] for student in lowest_students])
    print(f"Lowest average:  {lowest_avg:.2f} ({lowest_names})")

    print(f"\nClass average:   {sum(averages) / len(averages):.2f}")

    display_grade_distribution(students)


def search_student(students):
    if not students:
        print("\nNo student records available to search.")
        return
    print()
    delineate("SEARCH STUDENT")
    query_raw = input("Enter student name to search: ")
    query = query_raw.strip().lower()
    if is_esc_input(query_raw) or not query:
        print("Search canceled.")
        return
    found = [student for student in students if query in student["name"].lower()]
    if not found:
        print(f"No student records found for '{query}'.")
        return
    for student in found:
        print("\nFound student:")
        print(f"    Name: {student['name']}")
        print(f"    ID: {student['id']}")
        print(f"    Test 1: {student['test1']:.2f}")
        print(f"    Test 2: {student['test2']:.2f}")
        print(f"    Test 3: {student['test3']:.2f}")
        print(f"    Average: {student['average']:.2f}")
        print(f"    Grade: {student['grade']}")


def display_welcome():
    print("================================================================")
    print("WELCOME TO STUDENT GRADE CALCULATOR")
    print("================================================================")


def show_menu():
    print("\n================================================================")
    print("STUDENT GRADE CALCULATOR")
    print("================================================================")
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. View Class Statistics")
    print("4. Search Student by Name")
    print("5. Save and Exit (or type ESC)")
    print("================================================================")


def main():
    students = load_student_records(GRADE_FILE)
    display_welcome()
    while True:
        show_menu()
        choice = input("Select an option (1-5) or type ESC to exit: ").strip().upper()
        if choice == "ESC":
            save_student_records(GRADE_FILE, students)
            print("Thank you for using Student Grade Calculator!")
            break
        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_all_students(students)
        elif choice == "3":
            calculate_class_statistics(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            save_student_records(GRADE_FILE, students)
            print("Thank you for using Student Grade Calculator!")
        else:
            print("Invalid selection. Please enter 1-5 or ESC.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully.")
        exit(0)
