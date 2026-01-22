programming_dictionary = {
    "Bug": "An error in the program that prevents the program from running as expexted.",
    "Function": "A piece of code that you can easily call over and over again."
    ,"Loop": "The action of doing something over and over again"
    ,123: "This is a number not String"
    }

print(programming_dictionary["Bug"])
print(programming_dictionary[123])

# Adding new items to dictionary.
programming_dictionary["added"] = "This is adding in Python dictionary"

for thing in programming_dictionary:
    print(thing)
    print(programming_dictionary[thing])

empty_dictionary = {}

# Wipe the existing dictionary

programming_dictionary = {}
print(programming_dictionary)