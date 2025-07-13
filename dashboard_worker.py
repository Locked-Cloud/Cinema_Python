from tkinter import *
import ticket_seller
import db

def open_worker_dashboard():
    """Open the worker dashboard window for selling tickets and viewing movies."""
    worker = Tk()
    worker.title("Worker Dashboard - Sell Tickets")
    worker.geometry("500x400")
    worker.configure(bg="#1e1e1e")

    Label(worker, text="\ud83c\udf9f Worker Dashboard", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)

    Button(worker, text="Sell Ticket", command=lambda: ticket_seller.sell_ticket_window(worker),
           bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=20)

    Button(worker, text="View Movies & Seats", command=lambda: view_movies_and_seats(worker),
           bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(worker, text="View Tickets Sold", command=lambda: view_tickets_sold(worker),
           bg="#FF9800", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(worker, text="Logout", command=lambda: logout(worker), bg="#757575", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    worker.mainloop()

def view_movies_and_seats(parent):
    """Show all movies and available seats in a new window."""
    win = Toplevel(parent)
    win.title("Movies & Available Seats")
    win.geometry("600x400")
    try:
        with db.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, datetime, total_seats FROM movies")
            movies = cursor.fetchall()
        text_area = Text(win, width=80, height=20)
        text_area.pack()
        for m in movies:
            if isinstance(m, (list, tuple)):
                text_area.insert(END, f"ID: {m[0]} | Title: {m[1]} | Time: {m[2]} | Total Seats: {m[3]}\n")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Failed to load movies: {e}")

def view_tickets_sold(parent):
    """Show all tickets sold in a new window."""
    win = Toplevel(parent)
    win.title("Tickets Sold")
    win.geometry("700x400")
    try:
        with db.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT t.id, u.username, m.title, t.seat_number, m.datetime FROM tickets t JOIN users u ON t.user_id = u.id JOIN movies m ON t.movie_id = m.id")
            tickets = cursor.fetchall()
        text_area = Text(win, width=90, height=20)
        text_area.pack()
        for t in tickets:
            if isinstance(t, (list, tuple)):
                text_area.insert(END, f"Ticket ID: {t[0]} | User: {t[1]} | Movie: {t[2]} | Seat: {t[3]} | Time: {t[4]}\n")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Failed to load tickets: {e}")

def logout(window):
    """Logout and return to the login page."""
    window.destroy()
    from login import LoginPage
    root = Tk()
    LoginPage(root)
    root.mainloop()
