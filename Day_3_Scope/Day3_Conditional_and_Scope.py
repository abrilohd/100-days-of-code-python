"""
Day 3 - Conditional Statements, Logical Operators, Code Blocks & Scope
Author: Abrham
"""

# -----------------------------
# CONDITIONAL STATEMENTS
# -----------------------------

age = int(input("Enter your age: "))

if age < 18:
    print("You are under 18. Access denied.")
elif age >= 18 and age < 60:
    print("You are an adult. Access granted.")
else:
    print("You are a senior citizen. Welcome!")

# -----------------------------
# LOGICAL OPERATORS
# -----------------------------

has_id = True
has_ticket = False

if has_id and has_ticket:
    print("You can enter the event.")
elif has_id and not has_ticket:
    print("You have ID but no ticket.")
else:
    print("Access denied. No ID.")

# -----------------------------
# CODE BLOCKS (INDENTATION)
# -----------------------------

score = int(input("Enter your exam score: "))

if score >= 90:
    print("Grade: A")
    print("Excellent work!")   # same block
elif score >= 70:
    print("Grade: B")
    print("Good job!")
else:
    print("Grade: C")
    print("Needs improvement.")

# -----------------------------
# SCOPE (LOCAL vs GLOBAL)
# -----------------------------

# Global variable
school_name = "global academy"

def student_info():
    # Local variable
    student_name = "Abebe"
    print("Student Name:", student_name)
    print("School:", school_name)  # accessing global variable

student_info()

# Uncommenting the line below will cause an error
# because student_name is local to the function
# print(student_name)

print("School from outside function:", school_name)
