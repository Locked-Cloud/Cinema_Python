# Cinema App

A modern, user-friendly cinema management system built with Python and Tkinter.

## Features

- **Role-based Dashboards:** Separate dashboards for Admin, Worker, and User roles.
- **User Authentication:** Secure login, signup, and password hashing.
- **Password Reset/Change:** Users can reset forgotten passwords and change their password after login.
- **Movie Management:** Admins can add, edit, delete, and search/filter movies. Poster upload supported.
- **Ticket Management:** Users and workers can book tickets. Users can view and cancel their own tickets.
- **User Management:** Admins can view, edit, and delete users.
- **Analytics:** Admins can view statistics (total users, movies, tickets sold, revenue).
- **Movie Search/Filter:** Users and admins can search/filter movies by title or date.
- **Help Menu:** Built-in help/about dialog for user guidance.
- **Input Validation & Tooltips:** Improved error messages and user guidance throughout.

## Setup

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Database:**
   - MySQL server must be running on `localhost` with user `root` and password `root` (edit `db.py` if needed).
   - The app will auto-create the `cinema_db` database and tables on first run.
3. **Run the App:**
   ```bash
   python main.py
   ```

## User Roles

- **Admin:** Full access to all features, including user and movie management, analytics.
- **Worker:** Can sell tickets and view movies/seats.
- **User:** Can book/cancel tickets, view movies, and change their password.

## Default Test Users

- **Admin:** `admin` / `admin123`
- **Worker:** `worker` / `worker123`
- **User:** `user` / `user123`

## Screenshots

_Add your screenshots here_

## License

MIT
