def prime_cheker(number):
    prime_number = True
    for i in range(2, number):
        if number % i == 0:
            prime_number = False
    if prime_number == True:
        print("it is prime")
    else:
        print("it is not prime")
n = int(input("please enter the number: "))
prime_cheker(number = n)