import pandas
import tkinter as tk
from tkinter import messagebox

# Load data
data = pandas.read_csv("nato_phonetic_alphabet.csv")
phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}

# Function to convert word to phonetic
def generate_phonetic():
    word = entry.get().upper()
    try:
        output_list = [phonetic_dict[letter] for letter in word]
    except KeyError:
        messagebox.showerror("Invalid Input", "Please enter letters only (A-Z).")
    else:
        result_label.config(text=" ".join(output_list))

# Create window
window = tk.Tk()
window.title("NATO Phonetic Converter")
window.config(padx=30, pady=30)

# UI Elements
title_label = tk.Label(window, text="NATO Phonetic Converter", font=("Arial", 16, "bold"))
title_label.grid(column=0, row=0, columnspan=2, pady=10)

entry_label = tk.Label(window, text="Enter a word:")
entry_label.grid(column=0, row=1)

entry = tk.Entry(window, width=20, font=("Arial", 14))
entry.grid(column=1, row=1, pady=5)

convert_button = tk.Button(window, text="Convert", command=generate_phonetic, font=("Arial", 12))
convert_button.grid(column=0, row=2, columnspan=2, pady=10)

result_label = tk.Label(window, text="", font=("Arial", 14), fg="blue", wraplength=400)
result_label.grid(column=0, row=3, columnspan=2, pady=10)

window.mainloop()
