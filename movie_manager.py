from tkinter import *
from tkinter import filedialog, messagebox, ttk
import db
from PIL import Image, ImageTk
import io

class MovieManager:
    def __init__(self, parent):
        """Initialize the Movie Manager window."""
        self.parent = parent
        self.win = Toplevel(parent)
        self.win.title("Movie Manager")
        self.win.geometry("800x600")
        self.win.configure(bg="#23272f")
        Label(self.win, text="🎬 Movie Manager", font=("Arial", 20), fg="white", bg="#23272f").pack(pady=10)
        self.tree = ttk.Treeview(self.win, columns=("ID", "Title", "Showtime", "Seats"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Showtime", text="Showtime")
        self.tree.heading("Seats", text="Seats")
        self.tree.pack(fill=BOTH, expand=True, padx=20, pady=10)
        self.refresh_movies()
        btn_frame = Frame(self.win, bg="#23272f")
        btn_frame.pack(pady=10)
        Button(btn_frame, text="Add Movie", command=self.add_movie_window, bg="#4CAF50", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete Movie", command=self.delete_movie_window, bg="#f44336", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(btn_frame, text="View Poster", command=self.view_poster_window, bg="#2196F3", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Edit Movie", command=self.edit_movie_window, bg="#FF9800", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Close", command=self.win.destroy, bg="#888", fg="white", width=15).pack(side=LEFT, padx=5)

    def refresh_movies(self):
        """Refresh the movie list in the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, datetime, total_seats FROM movies")
                movies = cursor.fetchall()
            for m in movies:
                if isinstance(m, (list, tuple)):
                    self.tree.insert("", END, values=(str(m[0]), str(m[1]), str(m[2]), str(m[3])))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load movies: {e}")

    def add_movie_window(self):
        """Open a window to add a new movie."""
        from datetime import datetime
        win = Toplevel(self.win)
        win.title("Add New Movie")
        win.geometry("400x550")
        win.configure(bg="#23272f")
        Label(win, text="Title", bg="#23272f", fg="white").pack()
        title = Entry(win, width=40)
        title.pack()
        title.insert(0, "Enter movie title...")
        title.bind("<FocusIn>", lambda e: title.delete(0, END) if title.get() == "Enter movie title..." else None)
        title.focus_set()
        Label(win, text="Description", bg="#23272f", fg="white").pack()
        desc = Text(win, height=5, width=40)
        desc.pack()
        desc.insert("1.0", "Enter movie description...")
        def clear_desc_placeholder(event):
            if desc.get("1.0", END).strip() == "Enter movie description...":
                desc.delete("1.0", END)
        desc.bind("<FocusIn>", clear_desc_placeholder)
        Label(win, text="Show Date & Time", bg="#23272f", fg="white").pack()
        dt = Entry(win, width=40)
        dt.pack()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt.insert(0, now_str)
        Label(win, text="(Format: YYYY-MM-DD HH:MM:SS)", bg="#23272f", fg="#bbbbbb", font=("Arial", 8)).pack()
        Label(win, text="Total Seats", bg="#23272f", fg="white").pack()
        seats = Entry(win, width=40)
        seats.pack()
        seats.insert(0, "e.g. 100")
        seats.bind("<FocusIn>", lambda e: seats.delete(0, END) if seats.get() == "e.g. 100" else None)
        poster_data = None
        def upload_poster():
            nonlocal poster_data
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
            if file_path:
                try:
                    with open(file_path, "rb") as f:
                        poster_data = f.read()
                    messagebox.showinfo("Poster", "Poster uploaded successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to upload poster: {e}")
        Button(win, text="Upload Poster (optional)", command=upload_poster, bg="#2196F3", fg="white").pack(pady=10)
        def save_movie():
            if title.get() in ("", "Enter movie title...") or desc.get("1.0", END).strip() in ("", "Enter movie description...") or dt.get() == "" or seats.get() in ("", "e.g. 100"):
                messagebox.showerror("Error", "Please fill all fields.")
                return
            try:
                datetime.strptime(dt.get(), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format. Use YYYY-MM-DD HH:MM:SS")
                return
            try:
                seat_val = int(seats.get())
                if seat_val < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Total seats must be a positive integer.")
                return
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO movies (title, description, poster, datetime, total_seats)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title.get(), desc.get("1.0", END), poster_data, dt.get(), seat_val))
                    conn.commit()
                win.destroy()
                self.refresh_movies()
                messagebox.showinfo("Success", "Movie added.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        Button(win, text="Save Movie", command=save_movie, bg="#4CAF50", fg="white").pack(pady=10)
        Button(win, text="Cancel", command=win.destroy, bg="#888", fg="white").pack(pady=5)

    def delete_movie_window(self):
        """Open a confirmation dialog to delete the selected movie."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a movie to delete.")
            return
        movie_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete movie ID {movie_id}?"):
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM movies WHERE id=%s", (movie_id,))
                    conn.commit()
                self.refresh_movies()
                messagebox.showinfo("Deleted", "Movie deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete movie: {e}")

    def view_poster_window(self):
        """Display the poster for the selected movie, if available."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a movie to view poster.")
            return
        movie_id = self.tree.item(selected[0])["values"][0]
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT poster FROM movies WHERE id=%s", (movie_id,))
                poster = cursor.fetchone()
            if poster and isinstance(poster, (list, tuple)) and poster[0]:
                img_data = poster[0]
                if isinstance(img_data, bytes):
                    try:
                        img = Image.open(io.BytesIO(img_data))
                        img = img.resize((300, 400))
                        img_tk = ImageTk.PhotoImage(img)
                        win = Toplevel(self.win)
                        win.title("Movie Poster")
                        lbl = Label(win, image=img_tk)
                        lbl.pack()
                        # Keep a reference to avoid garbage collection
                        setattr(lbl, '_imgtk', img_tk)
                        Button(win, text="Close", command=win.destroy).pack()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to display image: {e}")
                else:
                    messagebox.showinfo("No Poster", "No poster uploaded for this movie.")
            else:
                messagebox.showinfo("No Poster", "No poster uploaded for this movie.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load poster: {e}")

    def edit_movie_window(self):
        """Open a window to edit the selected movie's details."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a movie to edit.")
            return
        movie_id = self.tree.item(selected[0])["values"][0]
        try:
            with db.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT title, description, datetime, total_seats FROM movies WHERE id=%s", (movie_id,))
                movie = cursor.fetchone()
            if not (movie and isinstance(movie, (list, tuple))):
                messagebox.showerror("Error", "Movie not found.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load movie: {e}")
            return
        win = Toplevel(self.win)
        win.title("Edit Movie")
        win.geometry("400x400")
        win.configure(bg="#23272f")
        Label(win, text="Title", bg="#23272f", fg="white").pack()
        title = Entry(win, width=40)
        title.insert(0, str(movie[0]))
        title.pack()
        Label(win, text="Description", bg="#23272f", fg="white").pack()
        desc = Text(win, height=5, width=40)
        desc.insert(END, str(movie[1]))
        desc.pack()
        Label(win, text="Show DateTime (YYYY-MM-DD HH:MM:SS)", bg="#23272f", fg="white").pack()
        dt = Entry(win, width=40)
        dt.insert(0, str(movie[2]))
        dt.pack()
        Label(win, text="Total Seats", bg="#23272f", fg="white").pack()
        seats = Entry(win, width=40)
        seats.insert(0, str(movie[3]))
        seats.pack()
        def save_edit():
            from datetime import datetime
            if not all([title.get(), desc.get("1.0", END).strip(), dt.get(), seats.get()]):
                messagebox.showerror("Error", "Please fill all fields.")
                return
            try:
                datetime.strptime(dt.get(), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format. Use YYYY-MM-DD HH:MM:SS")
                return
            try:
                seat_val = int(seats.get())
                if seat_val < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Total seats must be a positive integer.")
                return
            try:
                with db.connect_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE movies SET title=%s, description=%s, datetime=%s, total_seats=%s WHERE id=%s", (title.get(), desc.get("1.0", END), dt.get(), seat_val, movie_id))
                    conn.commit()
                win.destroy()
                self.refresh_movies()
                messagebox.showinfo("Success", "Movie updated.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        Button(win, text="Save Changes", command=save_edit, bg="#4CAF50", fg="white").pack(pady=10)
        Button(win, text="Cancel", command=win.destroy, bg="#888", fg="white").pack(pady=5)

# For backward compatibility

def add_movie_window(parent):
    """Open the add movie window from outside the class."""
    MovieManager(parent).add_movie_window()

def delete_movie_window(parent):
    """Open the delete movie window from outside the class."""
    MovieManager(parent).delete_movie_window()

def view_movies_window(parent):
    """Refresh the movies list from outside the class."""
    MovieManager(parent).refresh_movies()
