"""
Day 2 — BMI Calculator
Covers:
- Input
- Type conversion
- float vs int
- Math operations
- Rounding numbers
"""

# Get user input
height = input("please enter the Height in Metre: ")
waight = input("please enter the Waight in KG: ")

height_as_in_float = float(height)
waight_as_in_int = int(waight)

# Calculate BMI
Bmi = waight_as_in_int / (height_as_in_float * height_as_in_float)
print(round(Bmi, 3))  #rounding the number in  the given number of decimal
