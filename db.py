import mysql.connector
from mysql.connector import errorcode

def create_database_and_tables():
    # Connect to MySQL server (not to a specific database yet)
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"  # Set your password
    )
    cursor = db.cursor()
    try:
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
    finally:
        db.close()

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Set your password
        database="cinema_db"
    )

def setup_database():
    db = connect_db()
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
    db.close()

# Utility to insert test users
from utils import hash_password

def insert_test_users():
    users = [
        ("admin", hash_password("admin123"), "admin"),
        ("worker", hash_password("worker123"), "worker"),
        ("user", hash_password("user123"), "user"),
    ]
    db = connect_db()
    cursor = db.cursor()
    for username, pwd, role in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, pwd, role))
        except Exception:
            pass  # Ignore if user already exists
    db.commit()
    db.close()
