import json
import os
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path

import bcrypt

from database import conn, cursor

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "auth_session.json"
ENV_FILE = BASE_DIR / ".env"


def _load_env():
    if not ENV_FILE.exists():
        return {}

    values = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


ENV_VALUES = _load_env()


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def signup(name, email, password):
    email = _normalize_email(email)
    if get_user_by_email(email):
        return False

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO users(name,email,password,auth_provider,profile_picture) VALUES(?,?,?,?,?)",
            (name, email, hashed, "local", None),
        )
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def signup_google(name, email, profile_picture=None):
    email = _normalize_email(email)
    existing = get_user_by_email(email)
    if existing:
        return existing

    hashed = bcrypt.hashpw(f"google-{email}".encode("utf-8"), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO users(name,email,password,auth_provider,profile_picture) VALUES(?,?,?,?,?)",
            (name, email, hashed, "google", profile_picture),
        )
        conn.commit()
        return get_user_by_email(email)
    except Exception as e:
        print(e)
        return None


def get_user_by_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (_normalize_email(email),))
    return cursor.fetchone()


def login(email, password):
    user = get_user_by_email(email)
    if user and user[3] is not None:
        try:
            if bcrypt.checkpw(password.encode("utf-8"), user[3]):
                return user
        except Exception:
            return None
    return None


def update_password(email, new_password):
    email = _normalize_email(email)
    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    try:
        cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed, email))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(e)
        return False


def save_session(user, remember=False):
    payload = {
        "authenticated": True,
        "remember_me": remember,
        "name": user[1],
        "email": user[2],
        "auth_provider": user[4] if len(user) > 4 else "local",
        "profile_picture": user[5] if len(user) > 5 else None,
    }
    SESSION_FILE.write_text(json.dumps(payload), encoding="utf-8")


def load_session():
    if not SESSION_FILE.exists():
        return None
    try:
        data = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        if data.get("authenticated"):
            return data
    except Exception:
        return None
    return None


def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def send_password_reset_otp(email, otp):
    recipient = _normalize_email(email)
    smtp_user = ENV_VALUES.get("SMTP_EMAIL")
    smtp_pass = ENV_VALUES.get("SMTP_PASSWORD")

    if not smtp_user or not smtp_pass:
        return False, "SMTP credentials not configured."

    msg = EmailMessage()
    msg["Subject"] = "CareerPilot AI Password Reset OTP"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.set_content(
        f"Your CareerPilot AI password reset OTP is: {otp}\n\n"
        "Enter this code on the password reset page to continue."
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True, "OTP sent successfully."
    except Exception as exc:
        return False, f"Unable to send OTP: {exc}"