from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entries.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entries.get()
    email = email_entries.get()
    password = password_entries.get()
    if len(website) == 0 or len(password) == 0:
         messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty .")
    else:
        is_ok = messagebox.askokcancel(title="Website", message=f"These are the details entered: \nEmail: {email}"
                                                                f"\nPassword: {password}\nIs it ok to save?")

        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password} \n")
                website_entries.delete(0, END)
                password_entries.delete(0, END)





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Label
website_label = Label(text="Website:")
website_label.grid(row=1)
email_label = Label(text="Email/Username:")
email_label.grid(row=2)
password_label = Label(text="Password:")
password_label.grid(row=3)

#Entries
website_entries = Entry(width=35)
website_entries.grid(row=1, column=1, columnspan=2)
website_entries.focus()
email_entries = Entry(width=35)
email_entries.grid(row=2, column=1, columnspan=2)
email_entries.insert(0, "abrsh@gmail.com")
password_entries = Entry(width=21)
password_entries.grid(row=3, column=1)

#buttons
gen_button = Button(text="Generate Password", command=generate_password)
gen_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)



window.mainloop()