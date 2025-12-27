year = int(input("Please enter the year:"))


if year % 4 ==0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("leap year")
        else:
            print("not leap year")
    else:
        print("leap year")

else:
    print("not leap year")