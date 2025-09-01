import sqlite3
import hashlib
import os

# Optional: delete old DB for fresh start
if os.path.exists("attendance_system.db"):
    os.remove("attendance_system.db")

# Connect to the new database
conn = sqlite3.connect('attendance_system.db')
c = conn.cursor()

# Create users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    name TEXT,
    email TEXT,
    phone TEXT,
    department TEXT,
    join_date TEXT, face_encoding BLOB
)
""")

# Create admin user  
username = "admin"
password = "admin123"  # Default admin password
hashed_password = hashlib.sha256(password.encode()).hexdigest()
role = "admin"
name = "Administrator"
email = "admin@example.com"
phone = "1234567890"
department = "Management"
join_date = "2025-01-01"

# Insert admin user
try:
    c.execute("""
    INSERT INTO users (username, password, role, name, email, phone, department, join_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, hashed_password, role, name, email, phone, department, join_date))
    
    # Add a test employee account
    username_emp = "employee"
    password_emp = "employee123"  # Default employee password
    hashed_password_emp = hashlib.sha256(password_emp.encode()).hexdigest()
    
    c.execute("""
    INSERT INTO users (username, password, role, name, email, phone, department, join_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username_emp, hashed_password_emp, "employee", "Test Employee", "employee@example.com", 
          "0987654321", "Operations", "2025-01-15"))
    c.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    c.execute("INSERT INTO sqlite_sequence (NAME, SEQ) VALUES ('users', 1109)")
    
    conn.commit()
    print("Default users created successfully!")
except sqlite3.IntegrityError:
    print("Users already exist in the database.")
# Check if face_encoding column exists, add it if not
c.execute("PRAGMA table_info(users)")
columns = [column[1] for column in c.fetchall()]
if 'face_encoding' not in columns:
    c.execute("ALTER TABLE users ADD COLUMN face_encoding BLOB")
    print("Added face_encoding column to users table")
conn.close()

