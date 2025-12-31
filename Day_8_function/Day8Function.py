def greet():
    print("function")

greet()

# Function that allows for inputs

def greet_with_name(name):
    print(f"Hello {name}")
    print(f"How do you do: {name}")

greet_with_name("Angela")

# Arguments is the actual piece of data that send to the parameter when it is called the function     
# Parameter is name of the data of contain arguments in function       

# Function with more than 1 input
def greet_with(name, location):
    print(f"Hello {name}")
    print(f"what is it like in {location}")

greet_with("Jack Bauer", "Nowhere")

# Function with Keyword arguments
def greet_with(name, location):
    print(f"Hello {name}")
    print(f"what is it like in {location}")

greet_with(location = "Nowhere", name = "Angela" )