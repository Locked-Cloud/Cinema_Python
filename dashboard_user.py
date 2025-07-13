from tkinter import *
from tkinter import messagebox
import db

class UserDashboard:
    def __init__(self, user_id):
        """Initialize the user dashboard window."""
        self.user_id = user_id
        self.root = Tk()
        self.root.title("User Dashboard - Cinema App")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")
        Label(self.root, text="\ud83c\udfac User Dashboard", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)
        Button(self.root, text="View Movies", command=self.view_movies, bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        Button(self.root, text="My Tickets", command=self.view_my_tickets, bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        Button(self.root, text="Logout", command=self.logout, bg="#f44336", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        Button(self.root, text="Change Password", command=self.change_password_window, bg="#FF9800", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        self.root.mainloop()

    def view_movies(self):
        """Show all available movies and allow booking tickets. Add search/filter functionality."""
        win = Toplevel(self.root)
        win.title("Available Movies")
        win.geometry("600x500")
        search_frame = Frame(win)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search Title:").pack(side=LEFT)
        title_entry = Entry(search_frame)
        title_entry.pack(side=LEFT, padx=5)
        Label(search_frame, text="Date (YYYY-MM-DD):").pack(side=LEFT)
        date_entry = Entry(search_frame)
        date_entry.pack(side=LEFT, padx=5)
        result_area = Text(win, width=80, height=15)
        result_area.pack()
        def search_movies():
            title = title_entry.get().strip()
            date = date_entry.get().strip()
            query = "SELECT id, title, datetime, total_seats FROM movies WHERE 1=1"
            params = []
            if title:
                query += " AND title LIKE %s"
                params.append(f"%{title}%")
            if date:
                query += " AND DATE(datetime) = %s"
                params.append(date)
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    movies = cursor.fetchall()
                result_area.delete("1.0", END)
                for movie in movies:
                    movie_id, title, showtime, seats = movie
                    result_area.insert(END, f"ID: {movie_id} | Title: {title} | Time: {showtime} | Seats: {seats}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to search movies: {e}")
        Button(search_frame, text="Search", command=search_movies).pack(side=LEFT, padx=5)
        # Initial load
        def load_all_movies():
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, title, datetime, total_seats FROM movies")
                    movies = cursor.fetchall()
                result_area.delete("1.0", END)
                for movie in movies:
                    movie_id, title, showtime, seats = movie
                    result_area.insert(END, f"ID: {movie_id} | Title: {title} | Time: {showtime} | Seats: {seats}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load movies: {e}")
        load_all_movies()
        # Booking section
        Label(win, text="Enter Movie ID to Book").pack()
        movie_id_entry = Entry(win)
        movie_id_entry.pack()
        Label(win, text="Seat Number").pack()
        seat_entry = Entry(win)
        seat_entry.pack()
        Button(win, text="Book Ticket", command=lambda: self.book_ticket(movie_id_entry.get(), seat_entry.get(), win), bg="#FF9800", fg="white").pack(pady=10)

    def book_ticket(self, movie_id, seat_no, win):
        """Book a ticket for a selected movie and seat."""
        try:
            movie_id = int(movie_id)
            seat_no = int(seat_no)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for movie ID and seat number.")
            return
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT total_seats FROM movies WHERE id=%s", (movie_id,))
                movie = cursor.fetchone()
                if not movie:
                    messagebox.showerror("Error", "Movie not found")
                    return
                total_seats = movie[0]
                if seat_no < 1 or seat_no > total_seats:
                    messagebox.showerror("Error", "Invalid seat number")
                    return
                cursor.execute("SELECT * FROM tickets WHERE movie_id=%s AND seat_number=%s", (movie_id, seat_no))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Seat already booked")
                    return
                cursor.execute("INSERT INTO tickets (user_id, movie_id, seat_number) VALUES (%s, %s, %s)", (self.user_id, movie_id, seat_no))
                conn.commit()
            messagebox.showinfo("Success", f"Ticket booked for seat {seat_no}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Booking failed: {e}")

    def view_my_tickets(self):
        """Show all tickets booked by the user and allow cancellation."""
        win = Toplevel(self.root)
        win.title("My Tickets")
        win.geometry("600x400")
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT t.id, m.title, t.seat_number, m.datetime FROM tickets t JOIN movies m ON t.movie_id = m.id WHERE t.user_id=%s", (self.user_id,))
                tickets = cursor.fetchall()
            text_area = Text(win, width=80, height=20)
            text_area.pack()
            ticket_map = {}
            for idx, t in enumerate(tickets, 1):
                ticket_map[str(idx)] = t[0]  # Map display number to ticket ID
                text_area.insert(END, f"[{idx}] Ticket ID: {t[0]} | Movie: {t[1]} | Seat: {t[2]} | Time: {t[3]}\n")
            Label(win, text="Enter number to cancel ticket:").pack()
            cancel_entry = Entry(win)
            cancel_entry.pack()
            def cancel_ticket():
                num = cancel_entry.get()
                if num not in ticket_map:
                    messagebox.showerror("Error", "Invalid ticket number.")
                    return
                ticket_id = ticket_map[num]
                if messagebox.askyesno("Confirm", f"Cancel ticket ID {ticket_id}?"):
                    try:
                        with db.connect_db() as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM tickets WHERE id=%s AND user_id=%s", (ticket_id, self.user_id))
                            conn.commit()
                        messagebox.showinfo("Cancelled", "Ticket cancelled.")
                        win.destroy()
                        self.view_my_tickets()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to cancel ticket: {e}")
            Button(win, text="Cancel Ticket", command=cancel_ticket, bg="#f44336", fg="white").pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tickets: {e}")

    def change_password_window(self):
        win = Toplevel(self.root)
        win.title("Change Password")
        win.geometry("400x300")
        from tkinter import Label, Entry, Button, messagebox
        Label(win, text="Change Password", font=("Helvetica", 16)).pack(pady=20)
        old_pwd = Entry(win, font=("Arial", 12), show="*")
        old_pwd.pack(pady=5)
        old_pwd.insert(0, "Old Password")
        new_pwd = Entry(win, font=("Arial", 12), show="*")
        new_pwd.pack(pady=5)
        new_pwd.insert(0, "New Password")
        confirm_pwd = Entry(win, font=("Arial", 12), show="*")
        confirm_pwd.pack(pady=5)
        confirm_pwd.insert(0, "Confirm Password")
        def change_pwd():
            from utils import hash_password
            import db
            old = old_pwd.get()
            new = new_pwd.get()
            confirm = confirm_pwd.get()
            if not old or not new or not confirm:
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            if new != confirm:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(new) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT password FROM users WHERE id=%s", (self.user_id,))
                    res = cursor.fetchone()
                    if not res:
                        messagebox.showerror("Error", "User not found.")
                        return
                    if hash_password(old) != res[0]:
                        messagebox.showerror("Error", "Old password is incorrect.")
                        return
                    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hash_password(new), self.user_id))
                    conn.commit()
                messagebox.showinfo("Success", "Password changed.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {e}")
        Button(win, text="Change Password", command=change_pwd, bg="#4CAF50", fg="white").pack(pady=10)

    def logout(self):
        """Logout and return to the login page."""
        self.root.destroy()
        from login import LoginPage
        root = Tk()
        LoginPage(root)
        root.mainloop() 