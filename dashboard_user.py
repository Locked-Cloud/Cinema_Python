from tkinter import *
from tkinter import messagebox
import db

class UserDashboard:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = Tk()
        self.root.title("User Dashboard - Cinema App")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")
        Label(self.root, text="🎬 User Dashboard", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)
        Button(self.root, text="View Movies", command=self.view_movies, bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        Button(self.root, text="My Tickets", command=self.view_my_tickets, bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        Button(self.root, text="Logout", command=self.logout, bg="#f44336", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        self.root.mainloop()

    def view_movies(self):
        win = Toplevel(self.root)
        win.title("Available Movies")
        win.geometry("600x400")
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, datetime, total_seats FROM movies")
        movies = cursor.fetchall()
        conn.close()
        text_area = Text(win, width=80, height=20)
        text_area.pack()
        for m in movies:
            text_area.insert(END, f"ID: {m[0]} | Title: {m[1]} | Time: {m[2]} | Seats: {m[3]}\n")
        Label(win, text="Enter Movie ID to Book").pack()
        movie_id_entry = Entry(win)
        movie_id_entry.pack()
        Label(win, text="Seat Number").pack()
        seat_entry = Entry(win)
        seat_entry.pack()
        Button(win, text="Book Ticket", command=lambda: self.book_ticket(movie_id_entry.get(), seat_entry.get(), win), bg="#FF9800", fg="white").pack(pady=10)

    def book_ticket(self, movie_id, seat_no, win):
        try:
            movie_id = int(movie_id)
            seat_no = int(seat_no)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for movie ID and seat number.")
            return
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT total_seats FROM movies WHERE id=%s", (movie_id,))
        movie = cursor.fetchone()
        if not movie:
            messagebox.showerror("Error", "Movie not found")
            conn.close()
            return
        total_seats = movie[0]
        if seat_no < 1 or seat_no > total_seats:
            messagebox.showerror("Error", "Invalid seat number")
            conn.close()
            return
        cursor.execute("SELECT * FROM tickets WHERE movie_id=%s AND seat_number=%s", (movie_id, seat_no))
        if cursor.fetchone():
            messagebox.showerror("Error", "Seat already booked")
            conn.close()
            return
        cursor.execute("INSERT INTO tickets (user_id, movie_id, seat_number) VALUES (%s, %s, %s)", (self.user_id, movie_id, seat_no))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Ticket booked for seat {seat_no}")
        win.destroy()

    def view_my_tickets(self):
        win = Toplevel(self.root)
        win.title("My Tickets")
        win.geometry("600x400")
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT t.id, m.title, t.seat_number, m.datetime FROM tickets t JOIN movies m ON t.movie_id = m.id WHERE t.user_id=%s", (self.user_id,))
        tickets = cursor.fetchall()
        conn.close()
        text_area = Text(win, width=80, height=20)
        text_area.pack()
        for t in tickets:
            text_area.insert(END, f"Ticket ID: {t[0]} | Movie: {t[1]} | Seat: {t[2]} | Time: {t[3]}\n")

    def logout(self):
        self.root.destroy()
        from login import LoginPage
        root = Tk()
        LoginPage(root)
        root.mainloop() 