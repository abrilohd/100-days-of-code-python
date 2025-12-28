#list of student
student_score = []
# Take input from user as space-separated scores
student_score = input("Enter scores separated by space: ").split()

# Convert each string score to integer
for n in range(len(student_score)):
    student_score[n] = int(student_score[n])

print(student_score)


highest_score = 0
for highest in student_score:
    if highest > highest_score:
        highest_score = highest

print(f"The highest score in the class is:  {highest_score}")


# for loop 
# for item in list_of_items:
#     #do somethig to each other
print('''The next work is find
       the sum of number between 1 upto 100
      
      
      
    ''')

total_sum = 0
for number in range(1, 101):
    total_sum += number

print(f"The total sum =  {total_sum}")