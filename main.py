from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# --- CONSTANTS ---
IMAGE_PATH = "logo.png"
IMAGE = "logo.png"
ORANGE = "#D4483B"
WINDOW_COLOR = "#F0F0F0"
FONT = ("Ariel", 12, "")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 3))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 3))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    input_password.delete(0, END)
    input_password.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    password = input_password.get()
    username = input_user.get()
    website = input_web.get()

    if len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showinfo(title="Oops...", message="Please make sure you haven't left any fields empty.")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {username}"
                                                      f"\nPassword: {password}\nIs it ok to save?")
    if is_ok:
        try:
            with open("data.text", "a") as data_file:
                data_file.write(f"{website} | {username} | {password}\n")
                input_password.delete(0, END)
                input_user.delete(0, END)
                input_web.delete(0, END)
        except IOError:
            messagebox.showerror(title="Erro de Arquivo", message=f"Não foi possível salvar no arquivo {data_file}.")
        finally:
            input_web.delete(0, END)
            input_user.delete(0, END)
            input_password.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

# --- WINDOW CONFIG ---
window = Tk()
window.title("Password manager")
window.config(padx= 50, pady=50, bg= WINDOW_COLOR)

# --- CANVAS CREATION ---
canvas = Canvas(
    width=200,
    height=200,
    highlightthickness=0,
    bg = WINDOW_COLOR,
    bd = 0
    )
canvas.grid(row=0, column=1, padx= 20, pady= 20)
logo_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH))
canvas.create_image(100, 100, image=logo_img)
canvas.logo_img = logo_img

#--- LABELS ---
website = Label(text= "Website:", font=FONT, bg= WINDOW_COLOR)
website.grid(row=1, column=0, sticky="w")

email_username = Label(text= "Email/Username:", font=FONT, bg= WINDOW_COLOR)
email_username.grid(row=2, column=0, sticky="w")

password = Label(text= "Password:", font=FONT, bg= WINDOW_COLOR)
password.grid(row=3, column=0, sticky="w")

#--- ENTRY ---
input_web = Entry(width=35)
input_web.grid(row= 1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

input_user = Entry(width=35)
input_user.grid(row= 2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

input_password = Entry(width=30)
input_password.grid(row= 3, column=1, padx=10, pady=10, sticky="ew")

#--- BUTTON ---

generate_passw = Button(
    text="Generate password", bg=ORANGE, fg="black", activebackground= "green",
    command = lambda: generate_password()
    )
generate_passw.grid(row= 3, column=2, padx=10, pady=10, sticky="ew")

add = Button(
    text="Add", width=36, bg=ORANGE, activebackground= "green",
    command = lambda: save(),
    )
add.grid(row= 4 , column=1, columnspan= 2, padx=10, pady=10, sticky="ew")

window.grid_columnconfigure(1, weight=1)

window.mainloop()