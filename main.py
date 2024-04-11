from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
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

    new_data = {
        website_name: {
            "email": username,
            "password": new_password,
        }
    }

    if len(website_name) == 0 or len(new_password) == 0:
        messagebox.showwarning(title="Missing Fields", message="Cannot save password. Missing fields detected")
    else:
        is_okay = messagebox.askokcancel(title="Confirmation", message=f"These are the details entered:\n Email:"
                                                                       f"{username}\nPassword:{new_password}\n"
                                                                       f"Is it okay to save?")
        if is_okay:
            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open('data.json', 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                reset_fields()


def reset_fields():
    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    username_entry.insert(0, "example@email.com")


# ---------------------------- UI SETUP ------------------------------- #
def search_password():
    # Try to open up file
    website_search = website_entry.get()

    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Uh Oh!", message="There are currently no passwords stored! Add a password first!")

    else:
        if website_search in data:

            messagebox.showinfo(title=f"Login Information for: {website_search}",
                                message=f"Email/Username: {data[website_search]['email']}\n"
                                        f"Password: {data[website_search]['password']}")
        else:
            messagebox.showwarning(title="Uh Oh!", message=f"Password for {website_search} not found!")


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

search_button = Button(text="Search", width=15, command=search_password)
search_button.grid(column=3, row=1)

window.mainloop()
