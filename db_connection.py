"""
DATABASE CONNECTION - Handles SQLite setup
"""

import sqlite3

from datetime import datetime

def get_connection():
    """Create and return database connection"""
    return sqlite3.connect('health_ai.db')

def init_database():
    """Create all tables if they don't exist"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE,
                     password TEXT,
                     created_at TIMESTAMP
                 )''')
    
    # Table 2: Health logs
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_logs
                 (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     date TIMESTAMP,
                     heart_rate REAL,
                     sleep_hours REAL,
                     activity REAL,
                     risk_score REAL,
                     alert_level TEXT,
                     explanation TEXT
                 )''')
    
    # Table 3: User baselines
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_baselines
                 (
                     user_id INTEGER PRIMARY KEY,
                     baseline_hr REAL,
                     baseline_sleep REAL,
                     baseline_activity REAL,
                     last_updated TIMESTAMP
                 )''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")