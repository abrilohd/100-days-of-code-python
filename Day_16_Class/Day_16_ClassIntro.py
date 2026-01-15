# -------------------------------
# WHAT IS A CLASS?
# -------------------------------
# A class is a blueprint for creating objects.
# An object is created from a class.
# Example: A class is like a design of a phone,
# and an object is the actual phone you use.


# -------------------------------
# STEP 1: CREATE A CLASS
# -------------------------------
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
# STEP 2: CREATE OBJECTS
# -------------------------------
student1 = Student("Abebe", 21, "Python Programming")
student2 = Student("Soliana", 16, "AI Engineer")

# -------------------------------
# STEP 3: USE OBJECT METHODS
# -------------------------------
print("\n--- Student 1 Info ---")
student1.introduce()
print("Status:", student1.is_adult())

print("\n--- Student 2 Info ---")
student2.introduce()
print("Status:", student2.is_adult())