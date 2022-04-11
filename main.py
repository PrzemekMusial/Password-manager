from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    new_letters = [random.choice(letters) for char in range(nr_letters)]
    new_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    new_numbers = [random.choice(numbers) for char in range(nr_numbers)]
    lista = new_letters + new_symbols + new_numbers

    random.shuffle(lista)

    password = "".join(lista)
    # for char in lista:
    #   password += char
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website.get()
    email = username_entry.get()
    pswd = password_entry.get()
    new_data = {
        web:{
            "email":email,
            "password":pswd
        }
    }

    if len(web) == 0 or len(pswd) == 0:
        messagebox.showinfo(title="Info", message="Some fields are empty")
    else:
        try:
            with open("file.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("file.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("file.json", mode="w") as file:
                data.update(new_data)
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    web = website.get()
    try:
        with open("file.json", mode="r") as file:
            data = json.load(file)
            if web in data or web == "":
                display_email = data[web]["email"]
                display_pswd = data[web]["password"]
                pyperclip.copy(display_pswd)
                messagebox.showinfo(title=web, message=f"Email: {display_email} \nPassword: {display_pswd}")
            else:
                messagebox.showinfo(title="ERROR", message=f"{web} not in data base")
    except KeyError:
        messagebox.showinfo(title="ERROR", message=f"No website entered")
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="Your data base is empty")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=logo_img)
canvas.grid(column=1, row=0)

#create labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#create entries
website = StringVar()
website_entry = Entry(width=35, textvariable=website)
website_entry.grid(column=1, row=1, sticky="ew")
website_entry.focus()     #ustawia kursor w polu

username_entry = Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
username_entry.insert(0, "YouEmail@mail.com")
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="ew")

# #create buttons
generate_button = Button(text="Generate Password", command=pass_gen)
generate_button.grid(column=2, row=3)
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="ew")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")


window.mainloop()
