import mysql.connector
from mysql.connector import errorcode
from utils import hash_password

def create_database_and_tables():
    """Create the cinema_db database and all required tables if they do not exist."""
    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"  # Set your password
        ) as db:
            cursor = db.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS cinema_db")
            cursor.execute("USE cinema_db")
            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                password VARCHAR(255),
                role ENUM('admin', 'worker', 'user')
            )""")
            # Create movies table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                description TEXT,
                poster LONGBLOB,
                datetime DATETIME,
                total_seats INT
            )""")
            # Create tickets table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                movie_id INT,
                seat_number INT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(movie_id) REFERENCES movies(id)
            )""")
            db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def connect_db():
    """Connect to the cinema_db database and return the connection object."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Set your password
        database="cinema_db"
    )

def setup_database():
    """Ensure all required tables exist in the cinema_db database."""
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        existing = [table[0] for table in cursor.fetchall() if isinstance(table, (list, tuple))]
        if 'users' not in existing:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                password VARCHAR(255),
                role ENUM('admin', 'worker', 'user')
            )""")
        if 'movies' not in existing:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                description TEXT,
                poster LONGBLOB,
                datetime DATETIME,
                total_seats INT
            )""")
        if 'tickets' not in existing:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                movie_id INT,
                seat_number INT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(movie_id) REFERENCES movies(id)
            )""")
        db.commit()

def insert_test_users():
    """Insert test users for admin, worker, and user roles if they do not already exist."""
    users = [
        ("admin", hash_password("admin123"), "admin"),
        ("worker", hash_password("worker123"), "worker"),
        ("user", hash_password("user123"), "user"),
    ]
    with connect_db() as db:
        cursor = db.cursor()
        for username, pwd, role in users:
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, pwd, role))
            except Exception:
                pass  # Ignore if user already exists
        db.commit()
