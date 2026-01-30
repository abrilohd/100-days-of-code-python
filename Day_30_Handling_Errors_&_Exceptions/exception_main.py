# FileNotFound

try:
    file = open("file.txt")
    a_dict = {"key":"value"}
    print(a_dict["key"])
except FileNotFoundError:
    file = open("file.txt", "w")
    file.write("something")
except KeyError as error:
    print(f"The key {error} is doesn't Exist")
else:
    content = file.read()
    print(content)
finally:
    file.close()
    print("File was Closed")

#BMI Example

height = float(input("Height: "))
weight = int(input("Weight: "))

if height > 3:
    raise ValueError("Human Height should not be over 3 meters.")

bmi = weight / height ** 2
print(f"BMI  : {bmi}")

