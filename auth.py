"""
AUTHENTICATION - Login and Signup
"""

import hashlib
import sqlite3
from datetime import datetime
from db_connection import get_connection

def hash_password(password):
    """Convert password to SHA-256 hash"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    """Verify user credentials"""
    if not username or not password:
        return None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed))
    user = cursor.fetchone()
    
    conn.close()
    return user[0] if user else None

def register_user(username, password):
    """Create new user account - returns True/False"""
    if not username or not password:
        return False
    
    if len(password) < 6:
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
            (username, hashed, datetime.now())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()

def init_users_table():
    """Create users table if it doesn't exist"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    conn.close()
