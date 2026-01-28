# *args: Positional Variable-Length Arguments
def add(*args):
    sum = 0
    for n in args:
        sum += n
    return sum


# Unlimited Positional Arguments

print(add(3,4,23,25,34,2))

def calculate(n, **kwargs):
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)
    n += kwargs["add"]
    n *= kwargs["multy"]
    # print(n)


calculate(2, add=3, multy=5)


# How To use a **kwargs dictionary safely
# **kwargs is unlimited Keyword Arguments

class Car:
    def __init__(self, **kw):
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.colour = kw.get("colour")
        self.seats = kw.get("seats")

my_car = Car(make="Nissan", model="Skyline")
print(my_car)