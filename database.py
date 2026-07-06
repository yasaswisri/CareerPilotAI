import sqlite3

conn = sqlite3.connect("careerpilot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password BLOB,
    auth_provider TEXT DEFAULT 'local',
    profile_picture TEXT
)
""")

conn.commit()

cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]
if "auth_provider" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN auth_provider TEXT DEFAULT 'local'")
if "profile_picture" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN profile_picture TEXT")
conn.commit()