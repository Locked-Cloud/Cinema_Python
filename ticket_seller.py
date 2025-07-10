from tkinter import *
from tkinter import messagebox
import db

def sell_ticket_window(parent):
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
            conn = db.connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT total_seats FROM movies WHERE id=%s", (movie_id.get(),))
            movie = cursor.fetchone()
            if not movie:
                messagebox.showerror("Error", "Movie not found")
                return

            total_seats = movie[0]
            seat = int(seat_no.get())

            if seat < 1 or seat > total_seats:
                messagebox.showerror("Error", "Invalid seat number")
                return

            cursor.execute("SELECT * FROM tickets WHERE movie_id=%s AND seat_number=%s", (movie_id.get(), seat))
            if cursor.fetchone():
                messagebox.showerror("Error", "Seat already booked")
                return

            cursor.execute("INSERT INTO tickets (user_id, movie_id, seat_number) VALUES (%s, %s, %s)",
                           (user_id.get() or None, movie_id.get(), seat))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Ticket sold for seat {seat}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Sell Ticket", command=sell, bg="#4CAF50", fg="white").pack(pady=10)
