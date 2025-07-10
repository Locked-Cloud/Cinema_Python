from tkinter import *
from tkinter import messagebox
import db
import movie_manager

def open_admin_dashboard():
    admin = Tk()
    admin.title("Admin Dashboard - Manage Movies")
    admin.geometry("700x500")
    admin.configure(bg="#1e1e1e")

    Label(admin, text="🎬 Admin Dashboard", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)

    Button(admin, text="➕ Add New Movie", command=lambda: movie_manager.add_movie_window(admin),
           bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="🗑 Delete Movie", command=lambda: movie_manager.delete_movie_window(admin),
           bg="#f44336", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="📋 View All Movies", command=lambda: movie_manager.view_movies_window(admin),
           bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="🎟 View All Tickets", command=lambda: view_all_tickets(admin),
           bg="#FF9800", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    admin.mainloop()

def view_all_tickets(parent):
    win = Toplevel(parent)
    win.title("All Tickets Sold")
    win.geometry("700x400")
    conn = db.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, u.username, m.title, t.seat_number, m.datetime FROM tickets t JOIN users u ON t.user_id = u.id JOIN movies m ON t.movie_id = m.id")
    tickets = cursor.fetchall()
    conn.close()
    text_area = Text(win, width=90, height=20)
    text_area.pack()
    for t in tickets:
        text_area.insert(END, f"Ticket ID: {t[0]} | User: {t[1]} | Movie: {t[2]} | Seat: {t[3]} | Time: {t[4]}\n")
