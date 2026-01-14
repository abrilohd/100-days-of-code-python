class Student:
    """
    This class represents a student.
    """

    # The __init__ method runs automatically
    # when a new object is created.
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

    # Method to introduce the student
    def introduce(self):
        print(f"Hello, my name is {self.name}.")
        print(f"I am {self.age} years old.")
        print(f"I am learning {self.course}.")

    # Method to check if student is adult
    def is_adult(self):
        if self.age >= 18:
            return "Adult"
        else:
            return "Minor"

# -------------------------------
# MINI PROJECT:
# Student Registration System
# -------------------------------
print("\n--- Student Registration System ---")

students = []

def register_student():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    course = input("Enter course name: ")

    new_student = Student(name, age, course)
    students.append(new_student)
    print("Student registered successfully!\n")

def show_students():
    if not students:
        print("No students registered yet.\n")
        return

    for index, student in enumerate(students, start=1):
        print(f"\nStudent {index}")
        student.introduce()
        print("Status:", student.is_adult())

# Simple menu
while True:
    print("\n1. Register Student")
    print("2. Show All Students")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        register_student()
    elif choice == "2":
        show_students()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
