from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

PADDING_X = 75
PADDING_Y = 50
IMAGE_FILEPATH = "logo.png"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website_name = website_entry.get()
    username = username_entry.get()
    new_password = password_entry.get()

    if website_name == "" or new_password == "":
        messagebox.showwarning(title="Missing Fields", message="Cannot save password. Missing fields detected")
    else:
        is_okay = messagebox.askokcancel(title="Confirmation", message=f"These are the details entered:\n Email:"
                                                                       f"{username}\nPassword:{new_password}\n"
                                                                       f"Is it okay to save?")
        if is_okay:
            with open('data.txt', 'a') as data:
                new_entry = f"{website_name} | {username} | {new_password}\n"
                data.write(new_entry)

            reset_fields()


def reset_fields():
    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    username_entry.insert(0, "example@email.com")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass - Password Manager")
window.config(padx=PADDING_X, pady=PADDING_Y)

canvas = Canvas(width=225, height=270)
logo_img = PhotoImage(file=IMAGE_FILEPATH)
canvas.create_image(115, 150, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0,row=1)

username_label = Label(text="Email/Username: ")
username_label.grid(column=0, row=2)

password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

username_entry = Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "example@email.com")

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

gen_pass_button = Button(text="Generate Password", justify=LEFT, command=generate_password)
gen_pass_button.grid(column=3, row=3)

add_password = Button(text="Add", width=30, command=save_password)
add_password.grid(column=1, row=4, columnspan=1)

window.mainloop()