target = int(input())

total_even = 0 
for number in range(0, target + 1, 2 ):
    total_even += number

print(total_even)

# alternative way

numbers = int (input("please enter the next number:  "))

total_even_sum = 0
for num in range(1, numbers + 1):
    if num % 2 == 0:
        total_even_sum += num

print(total_even_sum)