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
PASSWORD_STATE_FILE = BASE_DIR / "password_state.json"


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
        if cursor.rowcount > 0:
            PASSWORD_STATE_FILE.write_text(json.dumps({"updated": True}), encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(e)
        return False


def get_password_state():
    if not PASSWORD_STATE_FILE.exists():
        return False
    try:
        data = json.loads(PASSWORD_STATE_FILE.read_text(encoding="utf-8"))
        return bool(data.get("updated", False))
    except Exception:
        return False


def reset_password_state():
    try:
        PASSWORD_STATE_FILE.write_text(json.dumps({"updated": False}), encoding="utf-8")
        return True
    except Exception:
        return False


def save_session(user, remember=False):
    profile_data = get_user_profile(user[2]) or {}
    theme_mode = profile_data.get("theme_mode") or ("dark" if profile_data.get("dark_mode", 0) else "light")
    payload = {
        "authenticated": True,
        "remember_me": remember,
        "name": user[1],
        "email": user[2],
        "auth_provider": user[4] if len(user) > 4 else "local",
        "profile_picture": user[5] if len(user) > 5 else None,
        "theme_mode": theme_mode,
    }
    SESSION_FILE.write_text(json.dumps(payload), encoding="utf-8")


def get_user_profile(email):
    email = _normalize_email(email)
    cursor.execute(
        """
        SELECT name, email, phone, bio, skills, education, experience, certifications,
               linkedin, github, portfolio, dark_mode, theme_mode, language, response_style,
               email_notifications, push_notifications, share_anonymous_usage_data, resume_score
        FROM users
        WHERE email=?
        """,
        (email,),
    )
    row = cursor.fetchone()
    if not row:
        return None

    columns = [
        "name",
        "email",
        "phone",
        "bio",
        "skills",
        "education",
        "experience",
        "certifications",
        "linkedin",
        "github",
        "portfolio",
        "dark_mode",
        "theme_mode",
        "language",
        "response_style",
        "email_notifications",
        "push_notifications",
        "share_anonymous_usage_data",
        "resume_score",
    ]
    return dict(zip(columns, row))


def update_user_profile(email, profile_data):
    email = _normalize_email(email)
    allowed_fields = {
        "name": "name",
        "phone": "phone",
        "bio": "bio",
        "skills": "skills",
        "education": "education",
        "experience": "experience",
        "certifications": "certifications",
        "linkedin": "linkedin",
        "github": "github",
        "portfolio": "portfolio",
        "resume_score": "resume_score",
    }

    updates = []
    values = []
    for field, db_field in allowed_fields.items():
        if field in profile_data:
            updates.append(f"{db_field}=?")
            values.append(profile_data[field])

    if not updates:
        return False

    values.append(email)
    try:
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE email=?", values)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as exc:
        print(exc)
        return False


def update_user_settings(email, settings_data):
    email = _normalize_email(email)
    allowed_fields = {
        "dark_mode": "dark_mode",
        "language": "language",
        "response_style": "response_style",
        "theme_mode": "theme_mode",
        "email_notifications": "email_notifications",
        "push_notifications": "push_notifications",
        "share_anonymous_usage_data": "share_anonymous_usage_data",
    }

    updates = []
    values = []
    for field, db_field in allowed_fields.items():
        if field in settings_data:
            updates.append(f"{db_field}=?")
            values.append(settings_data[field])

    if not updates:
        return False

    values.append(email)
    try:
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE email=?", values)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as exc:
        print(exc)
        return False


def delete_user_account(email):
    email = _normalize_email(email)
    try:
        cursor.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as exc:
        print(exc)
        return False


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