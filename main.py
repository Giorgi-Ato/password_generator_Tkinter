import tkinter as tk
from tkinter import messagebox
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from string import ascii_letters, digits
import random


def generate_password():
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(ascii_letters) for _ in range(random.randint(5, 7))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(1, 2))]
    password_numbers = [random.choice(digits) for _ in range(random.randint(1, 2))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    new_password = ''.join([i for i in password_list])
    password_entry.insert(0, new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    site = web_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        site: {
            'email': email_username,
            'password': password,
        }
    }

    if len(site) == 0 or len(password) == 0:
        messagebox.showinfo(title='Oops', message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title('Password Generator')
window.config(padx=50, pady=50)

# Image Canvas
canvas = tk.Canvas(height=200, width=200)
image = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website_label = tk.Label(text='Website:', font=('Arial', 10, 'bold'), pady=2)
website_label.grid(column=0, row=1)

email_username_label = tk.Label(text='Email/Username:', font=('Arial', 10, 'bold'), pady=2)
email_username_label.grid(column=0, row=2)

password_label = tk.Label(text='Password:', font=('Arial', 10, 'bold'), pady=2)
password_label.grid(column=0, row=3)

# Entry

web_entry = tk.Entry(width=25)
web_entry.grid(column=1, row=1)
web_entry.focus()

email_username_entry = tk.Entry(width=50)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, 'example@email.com')

password_entry = tk.Entry(width=25)
password_entry.grid(column=1, row=3)

# Button
search_button = tk.Button(text='Search', width=20, command=find_password)
search_button.grid(column=2, row=1)

generate_button = tk.Button(text='Generate Password', width=20, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = tk.Button(text='Add', width=42, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
