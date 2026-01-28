list_of_string = input().split(",")

# list comprehension to convert strings to integers
numbers = [int(x) for x in list_of_string]

# list comprehension to filter on even numbers
result = [num for num in numbers if num % 2 == 0]




print(result)