# default parametre when you call function with out argument
def greet(name="User"):
    print(f"Hello, {name}!")

greet()         # Hello, User!
greet("Abebe") # Hello, Abebe!
