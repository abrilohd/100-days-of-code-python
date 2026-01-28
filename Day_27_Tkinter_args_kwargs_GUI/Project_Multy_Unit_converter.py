import tkinter as tk
from tkinter import ttk, messagebox

# Conversion formulas stored in dictionary
conversions = {
    "Miles → Km": lambda x: round(x * 1.609, 3),
    "Km → Miles": lambda x: round(x / 1.609, 3),
    "Kg → Pounds": lambda x: round(x * 2.205, 3),
    "Pounds → Kg": lambda x: round(x / 2.205, 3),
    "Celsius → Fahrenheit": lambda x: round((x * 9/5) + 32, 2),
    "Fahrenheit → Celsius": lambda x: round((x - 32) * 5/9, 2),
    "Liters → Gallons": lambda x: round(x * 0.264, 3),
    "Gallons → Liters": lambda x: round(x / 0.264, 3),
}


class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🌍 Universal Converter")
        self.geometry("500x400")
        self.config(padx=20, pady=20, bg="#f7f9fc")

        # Title Label
        title = tk.Label(
            self,
            text="Universal Converter",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#f7f9fc"
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Input
        tk.Label(self, text="Enter Value:", font=("Arial", 12), bg="#f7f9fc").grid(row=1, column=0, sticky="w")
        self.entry = tk.Entry(self, width=12, font=("Arial", 12))
        self.entry.grid(row=1, column=1, pady=5, sticky="w")

        # Combobox for conversions
        tk.Label(self, text="Conversion Type:", font=("Arial", 12), bg="#f7f9fc").grid(row=2, column=0, sticky="w")
        self.combo = ttk.Combobox(self, values=list(conversions.keys()), font=("Arial", 12), width=20, state="readonly")
        self.combo.grid(row=2, column=1, pady=5, sticky="w")
        self.combo.current(0)  # Default selection

        # Result Label
        self.result_label = tk.Label(
            self, text="Result: --", font=("Arial", 14, "bold"), fg="#16a085", bg="#f7f9fc"
        )
        self.result_label.grid(row=3, column=0, columnspan=2, pady=15)

        # Buttons
        convert_btn = ttk.Button(self, text="Convert", command=self.convert)
        convert_btn.grid(row=4, column=0, pady=10)

        clear_btn = ttk.Button(self, text="Clear", command=self.clear)
        clear_btn.grid(row=4, column=1, pady=10)

        exit_btn = ttk.Button(self, text="Exit", command=self.quit)
        exit_btn.grid(row=4, column=2, pady=10)

        # History Panel
        tk.Label(self, text="Conversion History", font=("Arial", 12, "underline"), bg="#f7f9fc").grid(row=5, column=0, columnspan=3, pady=(20, 5))
        self.history_listbox = tk.Listbox(self, height=8, width=50)
        self.history_listbox.grid(row=6, column=0, columnspan=3, pady=5)

        # Keyboard shortcuts
        self.bind("<Return>", lambda event: self.convert())
        self.bind("<Control-c>", lambda event: self.clear())

    def convert(self):
        try:
            value = float(self.entry.get())
            conversion_type = self.combo.get()

            result = conversions[conversion_type](value)
            self.result_label.config(text=f"Result: {result}")

            # Save to history
            self.history_listbox.insert(tk.END, f"{value} {conversion_type} = {result}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")

    def clear(self):
        self.entry.delete(0, tk.END)
        self.result_label.config(text="Result: --")


if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()
