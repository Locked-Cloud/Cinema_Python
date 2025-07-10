from tkinter import *
from login import LoginPage
from db import setup_database, insert_test_users

setup_database()  # Set up DB tables automatically
insert_test_users()  # Add test users for admin, worker, user

root = Tk()
root.title("Cinema App")
root.geometry("400x300")
LoginPage(root)
root.mainloop()
