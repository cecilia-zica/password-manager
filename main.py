from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from random import choice, randint, shuffle
import pyperclip
import json
import hashlib

# --- CONSTANTS ---
IMAGE_PATH = "logo.png"
DATA_FILE = "data.json"
CONFIG_FILE = "config.json"
# - - - COLOURS - - -
COLOR_PRIMARY_RED = "#D4483B"
COLOR_LIGHT_RED = "#E4796D"
COLOR_BACKGROUND = "#F5F5F5"
COLOR_TEXT = "#2F4F4F"
COLOR_SECONDARY_ACCENT = "#4A909E"
COLOR_WHITE = "#FFFFFF"
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

    new_credential = {"username": username, "password": password}

    if not all([website, username, password]):
        messagebox.showinfo(title="Oops...", message="Please make sure you haven't left any fields empty.")
        return

    is_ok = custom_askokcancel(title=website, message=f"These are the details entered:\nEmail: {username}"
                                                      f"\nPassword: {password}\nIs it ok to save?")
    if is_ok:
        try:
            with open(DATA_FILE, "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # --- NEW LOGIC FOR HANDLING MULTIPLE ACCOUNTS ---
        if website in data:
            # If the website already exists, append the new credential to its list
            data[website].append(new_credential)
        else:
            # If it's a new website, create a new list with the credential
            data[website] = [new_credential]

        try:
            with open(DATA_FILE, "w") as data_file:
                # Saving the update data in archive
                json.dump(data, data_file, indent=4)
        except IOError:
            messagebox.showerror(title="File Error", message=f"Could not save to file {DATA_FILE}.")
        else:
            messagebox.showinfo(title="Success!", message="Your password has been saved successfully.")
        finally:
            # Clean fields after trying to save it
            input_web.delete(0, END)
            input_user.delete(0, END)
            input_password.delete(0, END)


# --- NEW --- MASTER PASSWORD HELPER FUNCTIONS ---
def get_master_password_hash():
    """Tries to load the master password hash from the config file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("master_password_hash")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def set_master_password_hash(password):
    """Hashes a new password and saves it to the config file."""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with open(CONFIG_FILE, "w") as f:
        json.dump({"master_password_hash": password_hash}, f)
    return password_hash


# --- MAJOR REFACTOR --- VIEW/SEARCH PASSWORD LOGIC ---
def find_password():
    """Main controller function that decides whether to ask for creation or verification."""
    master_hash = get_master_password_hash()
    if not master_hash:
        # No master password exists, ask to create one
        if messagebox.askyesno("Setup Required", "No Master Password has been set. Would you like to create one?"):
            prompt_to_create_master_password()
    else:
        # Master password exists, ask for it
        prompt_for_master_password(master_hash)


def prompt_to_create_master_password():
    """Opens a window for the user to create a new master password."""
    setup_window = Toplevel(window)
    setup_window.title("Create Master Password")
    setup_window.config(padx=20, pady=20, bg=COLOR_BACKGROUND)
    setup_window.grab_set()

    Label(setup_window, text="Enter New Master Password:", bg=COLOR_BACKGROUND, font=FONT).pack(pady=5)
    new_pass_entry = Entry(setup_window, width=30, show="*")
    new_pass_entry.pack()
    new_pass_entry.focus()

    Label(setup_window, text="Confirm New Master Password:", bg=COLOR_BACKGROUND, font=FONT).pack(pady=5)
    confirm_pass_entry = Entry(setup_window, width=30, show="*")
    confirm_pass_entry.pack()

    def save_new_password():
        new_pass = new_pass_entry.get()
        confirm_pass = confirm_pass_entry.get()
        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Fields cannot be empty.", parent=setup_window)
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match.", parent=setup_window)
            return

        set_master_password_hash(new_pass)
        messagebox.showinfo("Success", "Master Password has been set!", parent=setup_window)
        setup_window.destroy()

    Button(setup_window, text="Save", command=save_new_password).pack(pady=10)


def prompt_for_master_password(correct_hash):
    """Opens a window to ask for the existing master password."""
    auth_window = Toplevel(window)
    auth_window.title("Authentication Required")
    auth_window.config(padx=30, pady=30, bg=COLOR_BACKGROUND)
    auth_window.grab_set()

    Label(auth_window, text="Enter Master Password:", bg=COLOR_BACKGROUND, font=FONT).pack(pady=10)
    master_pass_entry = Entry(auth_window, width=25, font=FONT, show="*")
    master_pass_entry.pack()
    master_pass_entry.focus()

    def verify():
        entered_password = master_pass_entry.get()
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        if entered_hash == correct_hash:
            auth_window.destroy()
            show_passwords_window()
        else:
            messagebox.showerror("Error", "Incorrect Master Password.", parent=auth_window)

    Button(auth_window, text="OK", width=10, command=verify).pack(pady=10)


def show_passwords_window():
    """The final window that displays the saved password data in a Treeview."""

    def on_item_select(_event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            password = item['values'][2]
            pyperclip.copy(password)
            messagebox.showinfo("Copied!", "Password has been copied to clipboard.")

    passwords_window = Toplevel(window)
    passwords_window.title("Saved Passwords")
    passwords_window.config(padx=20, pady=20, bg=COLOR_BACKGROUND)
    passwords_window.geometry("850x400")
    passwords_window.grab_set()

    try:
        with open(DATA_FILE, "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    columns = ("Website", "Username", "Password")
    tree = ttk.Treeview(passwords_window, columns=columns, show="headings")
    tree.heading("Website", text="Website")
    tree.heading("Username", text="Email/Username")
    tree.heading("Password", text="Password")
    tree.column("Website", width=200)
    tree.column("Username", width=200)
    tree.column("Password", width=200)

    # ---LOGIC FOR DISPLAYING THE DATA ---
    # We have a nested loop. The outer loop gets the website and the list of credentials.
    # The inner loop goes through each credential in the list.
    for website, credentials_list in data.items():
        for credential in credentials_list:
            tree.insert("", END, values=(website, credential['username'], credential['password']))

    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(passwords_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.bind("<<TreeviewSelect>>", on_item_select)


# --- CUSTOM DIALOG BOX FOR CONSISTENT LANGUAGE ---
def custom_askokcancel(title, message):
    """A custom implementation of messagebox.askokcancel to ensure English buttons."""

    result = [False]  # Use a list to allow modification within nested functions

    dialog = Toplevel(window)
    dialog.title(title)
    dialog.config(padx=30, pady=20, bg=COLOR_BACKGROUND)

    # Make the dialog modal (user must interact with it)
    dialog.grab_set()
    dialog.transient(window)

    # Message Label
    Label(dialog, text=message, font=FONT, bg=COLOR_BACKGROUND, justify="left").pack(pady=10)

    # --- Button Functions ---
    def on_ok():
        result[0] = True
        dialog.destroy()

    def on_cancel():
        result[0] = False
        dialog.destroy()

    # --- Frame for Buttons ---
    button_frame = Frame(dialog, bg=COLOR_BACKGROUND)
    button_frame.pack(pady=10)

    # --- OK and Cancel Buttons ---
    ok_button = Button(button_frame, text="OK", width=10, command=on_ok)
    ok_button.pack(side="left", padx=10)

    cancel_button = Button(button_frame, text="Cancel", width=10, command=on_cancel)
    cancel_button.pack(side="left", padx=10)

    # Wait for the user to close the dialog before continuing
    center_toplevel(dialog)
    dialog.wait_window()

    return result[0]

# --- HELPER FUNCTION TO CENTER TOPLEVEL WINDOWS ---
def center_toplevel(dialog_window):
    """Calculates the position to center a toplevel window on the main window."""
    dialog_window.update_idletasks() # Update "requested size" to the actual size

    # Get the main window's position and size
    main_window_x = window.winfo_x()
    main_window_y = window.winfo_y()
    main_window_width = window.winfo_width()
    main_window_height = window.winfo_height()

    # Get the dialog's size
    dialog_width = dialog_window.winfo_width()
    dialog_height = dialog_window.winfo_height()

    # Calculate the position
    position_x = main_window_x + (main_window_width // 2) - (dialog_width // 2)
    position_y = main_window_y + (main_window_height // 2) - (dialog_height // 2)

    dialog_window.geometry(f"+{position_x}+{position_y}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password manager")
window.config(padx= 50, pady=50, bg= COLOR_BACKGROUND)

# --- CANVAS ---
canvas = Canvas(width=200, height=200, highlightthickness=0, bg = COLOR_BACKGROUND, bd = 0)
logo_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH))
canvas.logo_img = logo_img
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=3, pady= 20)

#--- LABELS & ENTIES ---
Label(text= "Website:", font=FONT, bg= COLOR_BACKGROUND, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
input_web = Entry(highlightthickness=0)
input_web.grid(row= 1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
input_web.focus()

Label(text= "Email/Username:", font=FONT, bg= COLOR_BACKGROUND, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w")
input_user = Entry(highlightthickness=0)
input_user.grid(row= 2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

Label(text= "Password:", font=FONT, bg= COLOR_BACKGROUND, fg=COLOR_TEXT).grid(row=3, column=0, sticky="w")
input_password = Entry(highlightthickness=0, show="*")
input_password.grid(row= 3, column=1, padx=5, pady=5, sticky="ew")

#--- BUTTONS ---
Button(text="Generate password", bg=COLOR_PRIMARY_RED, fg=COLOR_WHITE, activebackground=COLOR_LIGHT_RED,command = generate_password).grid(row= 3, column=2, padx=5, pady=5, sticky="ew")
Button(text="Add", width=36, bg=COLOR_PRIMARY_RED, fg=COLOR_WHITE, activebackground=COLOR_LIGHT_RED,command = save).grid(row= 4 , column=1, columnspan= 2, padx=5, pady=5, sticky="ew")
Button(text="Search", bg=COLOR_SECONDARY_ACCENT, fg=COLOR_WHITE, activebackground=COLOR_LIGHT_RED, command=find_password).grid(row=4, column=0, padx=5, pady=5, sticky="ew")

# Configure the grid to allow the center column to expand
window.grid_columnconfigure(1, weight=1)

window.mainloop()