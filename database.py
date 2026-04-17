import sqlite3

def initialize_database():
    conn = sqlite3.connect("alis.db")
    cursor = conn.cursor()

    print("🔧 Initializing SQLite Database...")

    # 1. Sessions Table: Tracks the metadata for each diagnostic run
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id TEXT,
        topic TEXT,
        target_level TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Responses Table: Tracks individual answer performance and behavioral style
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        style TEXT,
        type TEXT,
        is_correct BOOLEAN,
        time REAL
    )
    """)

    # 3. Users Table: Secure storage for profile data and hashed credentials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        level TEXT,
        goal TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database and tables initialized successfully!")

if __name__ == "__main__":
    initialize_database()