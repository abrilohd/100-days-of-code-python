"""
Day 4 - Index Error & Nested Lists
"""

fruits = ["apple", "banana", "orange"]

# Length of list
print("Number of fruits:", len(fruits))
print("Last index:", len(fruits) - 1)

vegetables = ["carrot", "potato", "watermelon"]

# Nested list
foods = [fruits, vegetables]
print("Nested list:", foods)

# print(fruits[3])  # IndexError: list index out of range
# because index start form 0