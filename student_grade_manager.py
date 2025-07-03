# 1. VARIABLES & DATA TYPES
students = []  # List to store student data
subjects = ["Math", "Science", "English", "History"]  # List of subjects
passing_grade = 60  # Integer variable
school_name = "Namangan Programming Maktabi"  # String variable


# 2. FUNCTIONS - Reusable code blocks
def add_student(name, grades):
    """Add a student with their grades"""
    # 3. DICTIONARIES - Key-value pairs
    student = {
        "name": name,
        "grades": grades,
        "average": sum(grades) / len(grades),  # Calculate average
        "status": "Pass" if sum(grades) / len(grades) >= passing_grade else "Fail"
    }
    students.append(student)
    return student


def display_student(student):
    """Display student information"""
    print(f"\nStudent: {student['name']}")
    # 4. LOOPS - Iterate through data
    for i, subject in enumerate(subjects):
        print(f"  {subject}: {student['grades'][i]}")
    print(f"  Average: {student['average']:.1f}")
    print(f"  Status: {student['status']}")


def get_user_input():
    """Get student data from user input"""
    print("\nAdd a new student:")
    name = input("Enter student name: ")
    grades = []

    # 5. INPUT VALIDATION - Check user input
    for subject in subjects:
        while True:
            try:
                grade = float(input(f"Enter {subject} grade (0-100): "))
                if 0 <= grade <= 100:
                    grades.append(grade)
                    break
                else:
                    print("Grade must be between 0 and 100!")
            except ValueError:
                print("Please enter a valid number!")

    return name, grades


def get_class_statistics():
    """Calculate class statistics"""
    if not students:
        return "No students enrolled"

    # 6. LIST COMPREHENSIONS - Efficient data processing
    averages = [student['average'] for student in students]
    passing_students = [s for s in students if s['status'] == "Pass"]

    return {
        "total_students": len(students),
        "class_average": sum(averages) / len(averages),
        "highest_average": max(averages),
        "lowest_average": min(averages),
        "passing_rate": len(passing_students) / len(students) * 100
    }


# 7. MAIN PROGRAM - Program execution
def main():
    print(f"Welcome to {school_name} Grade Manager!")
    print("=" * 40)

    # Sample data
    sample_students = [
        ("Aziza Karimova", [85, 92, 78, 88]),
        ("Bobur Umarov", [76, 68, 82, 75]),
        ("Dilnoza Rahimova", [95, 89, 91, 94]),
        ("Javohir Tashkentov", [45, 52, 48, 50])
    ]

    # 8. FOR LOOPS - Process multiple items
    for name, grades in sample_students:
        add_student(name, grades)

    # 9. WHILE LOOPS & USER INTERACTION
    while True:
        print("\nOptions:")
        print("1. View all students")
        print("2. Add new student")
        print("3. View statistics")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        # 10. CONDITIONAL STATEMENTS - Make decisions
        if choice == "1":
            print("\nSTUDENT RECORDS:")
            for student in students:
                display_student(student)

        elif choice == "2":
            name, grades = get_user_input()
            add_student(name, grades)
            print(f"Student {name} added successfully!")

        elif choice == "3":
            print("\nCLASS STATISTICS:")
            stats = get_class_statistics()
            if isinstance(stats, dict):
                print(f"Total Students: {stats['total_students']}")
                print(f"Class Average: {stats['class_average']:.1f}")
                print(f"Highest Average: {stats['highest_average']:.1f}")
                print(f"Lowest Average: {stats['lowest_average']:.1f}")
                print(f"Passing Rate: {stats['passing_rate']:.1f}%")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

    # 11. EXCEPTION HANDLING - Handle errors gracefully
    try:
        # Find top performer
        top_student = max(students, key=lambda x: x['average'])
        print(f"\nTop Performer: {top_student['name']} ({top_student['average']:.1f})")
    except ValueError:
        print("No students to analyze")


# 12. PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()