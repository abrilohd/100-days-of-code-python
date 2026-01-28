from tkinter import *

# Conversion Functions
def convert():
    try:
        value = float(entry.get())
        unit = unit_var.get()

        if unit == "Miles → Km":
            result = round(value * 1.609, 2)
            result_label.config(text=f"{result} Km")

        elif unit == "Km → Miles":
            result = round(value / 1.609, 2)
            result_label.config(text=f"{result} Miles")

        elif unit == "Kg → Pounds":
            result = round(value * 2.205, 2)
            result_label.config(text=f"{result} lbs")

        elif unit == "Pounds → Kg":
            result = round(value / 2.205, 2)
            result_label.config(text=f"{result} Kg")

        elif unit == "Celsius → Fahrenheit":
            result = round((value * 9/5) + 32, 2)
            result_label.config(text=f"{result} °F")

        elif unit == "Fahrenheit → Celsius":
            result = round((value - 32) * 5/9, 2)
            result_label.config(text=f"{result} °C")

    except ValueError:
        result_label.config(text="Invalid Input ❌")


# GUI Setup
window = Tk()
window.title("Multi-Unit Converter")
window.config(padx=20, pady=20)

# Entry
entry = Entry(width=10)
entry.grid(column=1, row=0)

# Dropdown Menu for units
unit_var = StringVar(value="Miles → Km")
unit_menu = OptionMenu(window, unit_var,
                       "Miles → Km", "Km → Miles",
                       "Kg → Pounds", "Pounds → Kg",
                       "Celsius → Fahrenheit", "Fahrenheit → Celsius")
unit_menu.grid(column=2, row=0)

# Result Label
result_label = Label(text="Result")
result_label.grid(column=1, row=1)

# Convert Button
convert_button = Button(text="Convert", command=convert)
convert_button.grid(column=1, row=2)

# Press Enter to Convert
window.bind("<Return>", lambda event: convert())

window.mainloop()
