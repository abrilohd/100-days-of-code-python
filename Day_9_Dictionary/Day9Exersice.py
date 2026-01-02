student_score = {
    "Harry": 81,
    "Ron": 78,
    "hermione": 99,
    "draco": 74,
    "Nevi": 62,

}
student_grades = {}

for grades in student_score:
    score = student_score[grades]
    if score > 90:
        student_grades[grades] = "outstanding"
    elif score > 80:
        student_grades[grades] = "Exceeds Expectitions"
    elif score > 70:
        student_grades[grades] = "Acceptable"
    else:
        student_grades[grades] = "Fail"

print(student_grades)

for grades in student_score:
    print()