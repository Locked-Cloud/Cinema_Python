# Cinema App

A desktop cinema management application using Python, Tkinter, and MySQL. Supports admin/worker roles, movie upload (with poster), and ticket selling.

## Features

- User authentication (admin, worker, user)
- Admin: Add/delete/view movies (with poster upload)
- Worker: Sell tickets, seat validation
- Passwords stored securely (SHA-256)

## Setup

1. Install MySQL and create a database named `cinema_db`.
2. Update `db.py` with your MySQL credentials if needed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python main.py
   ```

## Usage

- Admins can add/delete/view movies and upload posters.
- Workers can sell tickets and validate seat numbers.

## File Structure

- `main.py` - App entry point
- `login.py`, `signup.py` - Auth system
- `dashboard_admin.py`, `dashboard_worker.py` - Role dashboards
- `movie_manager.py` - Movie CRUD
- `ticket_seller.py` - Ticket selling
- `db.py` - Database connection and setup
- `utils.py` - Password hashing

---

_Built with Python, Tkinter, and MySQL._
# Cinema_Python
