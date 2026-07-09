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
    profile_picture TEXT,
    phone TEXT,
    bio TEXT,
    skills TEXT,
    education TEXT,
    experience TEXT,
    certifications TEXT,
    linkedin TEXT,
    github TEXT,
    portfolio TEXT,
    dark_mode INTEGER DEFAULT 0,
    theme_mode TEXT DEFAULT 'light',
    language TEXT DEFAULT 'English',
    response_style TEXT DEFAULT 'Balanced',
    email_notifications INTEGER DEFAULT 1,
    push_notifications INTEGER DEFAULT 1,
    share_anonymous_usage_data INTEGER DEFAULT 0,
    resume_score INTEGER DEFAULT 0
)
""")

conn.commit()
# Create History Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    module TEXT,
    title TEXT,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]
for column_name, definition in {
    "auth_provider": "TEXT DEFAULT 'local'",
    "profile_picture": "TEXT",
    "phone": "TEXT",
    "bio": "TEXT",
    "skills": "TEXT",
    "education": "TEXT",
    "experience": "TEXT",
    "certifications": "TEXT",
    "linkedin": "TEXT",
    "github": "TEXT",
    "portfolio": "TEXT",
    "dark_mode": "INTEGER DEFAULT 0",
    "theme_mode": "TEXT DEFAULT 'light'",
    "language": "TEXT DEFAULT 'English'",
    "response_style": "TEXT DEFAULT 'Balanced'",
    "email_notifications": "INTEGER DEFAULT 1",
    "push_notifications": "INTEGER DEFAULT 1",
    "share_anonymous_usage_data": "INTEGER DEFAULT 0",
    "resume_score": "INTEGER DEFAULT 0",
}.items():
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {definition}")
conn.commit()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())