from tkinter import Toplevel, Label, Entry, Button, messagebox
import db

def sell_ticket_window(parent):
    """Open a window to sell a ticket for a movie."""
    win = Toplevel(parent)
    win.title("Sell Ticket")
    win.geometry("400x400")

    Label(win, text="Movie ID").pack()
    movie_id = Entry(win)
    movie_id.pack()

    Label(win, text="User ID (optional)").pack()
    user_id = Entry(win)
    user_id.pack()

    Label(win, text="Seat Number").pack()
    seat_no = Entry(win)
    seat_no.pack()

    def sell():
        try:
            m_id = movie_id.get()
            s_no = seat_no.get()
            if not m_id or not s_no:
                messagebox.showerror("Error", "Movie ID and Seat Number are required.")
                return
            seat = int(s_no)
        except ValueError:
            messagebox.showerror("Error", "Seat number must be an integer.")
            return
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT total_seats FROM movies WHERE id=%s", (m_id,))
                movie = cursor.fetchone()
                if not movie:
                    messagebox.showerror("Error", "Movie not found")
                    return
                (total_seats,) = movie
                if not isinstance(total_seats, int):
                    if isinstance(total_seats, (str, float, bytes)):
                        try:
                            total_seats = int(total_seats)
                        except Exception:
                            messagebox.showerror("Error", "Invalid total seats value in database.")
                            return
                    else:
                        messagebox.showerror("Error", "Invalid total seats value in database.")
                        return
                if seat < 1 or seat > total_seats:
                    messagebox.showerror("Error", "Invalid seat number")
                    return
                cursor.execute("SELECT * FROM tickets WHERE movie_id=%s AND seat_number=%s", (m_id, seat))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Seat already booked")
                    return
                cursor.execute("INSERT INTO tickets (user_id, movie_id, seat_number) VALUES (%s, %s, %s)",
                               (user_id.get() or None, m_id, seat))
                conn.commit()
            messagebox.showinfo("Success", f"Ticket sold for seat {seat}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Sell Ticket", command=sell, bg="#4CAF50", fg="white").pack(pady=10)
