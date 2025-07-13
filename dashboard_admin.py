from tkinter import Tk, Toplevel, Label, Button, Text, END, messagebox, Frame, LEFT, Entry
import db
import movie_manager

def open_admin_dashboard():
    """Open the admin dashboard window for managing movies and viewing tickets."""
    admin = Tk()
    admin.title("Admin Dashboard - Manage Movies")
    admin.geometry("700x550")
    admin.configure(bg="#1e1e1e")

    Label(admin, text="\ud83c\udfac Admin Dashboard", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)

    Button(admin, text="\u2795 Add New Movie", command=lambda: movie_manager.add_movie_window(admin),
           bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="\ud83d\uddd1 Delete Movie", command=lambda: movie_manager.delete_movie_window(admin),
           bg="#f44336", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="\ud83d\udccb View All Movies", command=lambda: movie_manager.view_movies_window(admin),
           bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="\ud83c\udf9f View All Tickets", command=lambda: view_all_tickets(admin),
           bg="#FF9800", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="Search/Filter Movies", command=lambda: search_movies_window(admin),
           bg="#9C27B0", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="Manage Users", command=lambda: manage_users_window(admin),
           bg="#607D8B", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="View Analytics", command=lambda: analytics_window(admin),
           bg="#388E3C", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    Button(admin, text="Logout", command=lambda: logout(admin), bg="#757575", fg="white", font=("Arial", 12), width=20).pack(pady=10)

    admin.mainloop()

def search_movies_window(parent):
    win = Toplevel(parent)
    win.title("Search/Filter Movies")
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

def view_all_tickets(parent):
    """Show all tickets sold in a new window."""
    win = Toplevel(parent)
    win.title("All Tickets Sold")
    win.geometry("700x400")
    try:
        with db.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT t.id, u.username, m.title, t.seat_number, m.datetime FROM tickets t JOIN users u ON t.user_id = u.id JOIN movies m ON t.movie_id = m.id")
            tickets = cursor.fetchall()
        text_area = Text(win, width=90, height=20)
        text_area.pack()
        for ticket in tickets:
            ticket_id, username, title, seat_number, show_time = ticket
            text_area.insert(END, f"Ticket ID: {ticket_id} | User: {username} | Movie: {title} | Seat: {seat_number} | Time: {show_time}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load tickets: {e}")

def manage_users_window(parent):
    win = Toplevel(parent)
    win.title("Manage Users")
    win.geometry("700x500")
    from tkinter import Frame, Label, Entry, Button, Text, END, messagebox
    Label(win, text="All Users", font=("Arial", 16)).pack(pady=10)
    user_area = Text(win, width=80, height=15)
    user_area.pack()
    def load_users():
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, role FROM users")
                users = cursor.fetchall()
            user_area.delete("1.0", END)
            for user in users:
                user_id, username, role = user
                user_area.insert(END, f"ID: {user_id} | Username: {username} | Role: {role}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
    load_users()
    Label(win, text="Enter User ID to Edit/Delete:").pack()
    user_id_entry = Entry(win)
    user_id_entry.pack()
    Label(win, text="New Username (for edit):").pack()
    new_username_entry = Entry(win)
    new_username_entry.pack()
    Label(win, text="New Role (admin/worker/user, for edit):").pack()
    new_role_entry = Entry(win)
    new_role_entry.pack()
    def edit_user():
        user_id = user_id_entry.get().strip()
        new_username = new_username_entry.get().strip()
        new_role = new_role_entry.get().strip()
        if not user_id or not new_username or not new_role:
            messagebox.showerror("Error", "Please fill all fields for edit.")
            return
        if new_role not in ("admin", "worker", "user"):
            messagebox.showerror("Error", "Role must be admin, worker, or user.")
            return
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username=%s, role=%s WHERE id=%s", (new_username, new_role, user_id))
                conn.commit()
            messagebox.showinfo("Success", "User updated.")
            load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")
    def delete_user():
        user_id = user_id_entry.get().strip()
        if not user_id:
            messagebox.showerror("Error", "Please enter a user ID to delete.")
            return
        if messagebox.askyesno("Confirm", f"Delete user ID {user_id}?"):
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
                    conn.commit()
                messagebox.showinfo("Deleted", "User deleted.")
                load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")
    Button(win, text="Edit User", command=edit_user, bg="#FF9800", fg="white").pack(pady=5)
    Button(win, text="Delete User", command=delete_user, bg="#f44336", fg="white").pack(pady=5)

def analytics_window(parent):
    win = Toplevel(parent)
    win.title("Analytics & Statistics")
    win.geometry("400x300")
    from tkinter import Label
    Label(win, text="Cinema Analytics", font=("Arial", 16)).pack(pady=10)
    try:
        with db.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            res = cursor.fetchone()
            total_users = 0
            if res and len(res) > 0:
                (val,) = res
                if isinstance(val, (int, float, str)):
                    try:
                        total_users = int(val)
                    except Exception:
                        total_users = 0
            cursor.execute("SELECT COUNT(*) FROM movies")
            res = cursor.fetchone()
            total_movies = 0
            if res and len(res) > 0:
                (val,) = res
                if isinstance(val, (int, float, str)):
                    try:
                        total_movies = int(val)
                    except Exception:
                        total_movies = 0
            cursor.execute("SELECT COUNT(*) FROM tickets")
            res = cursor.fetchone()
            total_tickets = 0
            if res and len(res) > 0:
                (val,) = res
                if isinstance(val, (int, float, str)):
                    try:
                        total_tickets = int(val)
                    except Exception:
                        total_tickets = 0
            # For revenue, assume each ticket is $10 (customize as needed)
            revenue = total_tickets * 10
        Label(win, text=f"Total Users: {total_users}", font=("Arial", 12)).pack(pady=5)
        Label(win, text=f"Total Movies: {total_movies}", font=("Arial", 12)).pack(pady=5)
        Label(win, text=f"Tickets Sold: {total_tickets}", font=("Arial", 12)).pack(pady=5)
        Label(win, text=f"Total Revenue: ${revenue}", font=("Arial", 12)).pack(pady=5)
    except Exception as e:
        Label(win, text=f"Error loading analytics: {e}", fg="red").pack(pady=10)

def logout(window):
    """Logout and return to the login page."""
    window.destroy()
    from login import LoginPage
    root = Tk()
    LoginPage(root)
    root.mainloop()
