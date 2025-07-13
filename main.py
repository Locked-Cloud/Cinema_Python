from tkinter import *
from login import LoginPage
from db import setup_database, insert_test_users
from tkinter import messagebox

setup_database()  # Set up DB tables automatically
insert_test_users()  # Add test users for admin, worker, user

root = Tk()
root.title("Cinema App")
root.geometry("400x300")

# Add Help menu
menubar = Menu(root)
help_menu = Menu(menubar, tearoff=0)
def show_about():
    messagebox.showinfo("About", "Cinema App\nVersion 1.0\nManage movies, tickets, and users with ease!\nDeveloped by Ibrahim Ahmed.")
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

LoginPage(root)
root.mainloop()
