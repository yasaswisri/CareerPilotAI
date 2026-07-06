import random
import re
import time

import streamlit as st

from auth import get_user_by_email, send_password_reset_otp, update_password

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='page-title'>Forgot Password</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#6b7280;margin-bottom:2rem;'>Reset your password securely using a one-time code.</p>", unsafe_allow_html=True)

if "fp_email" not in st.session_state:
    st.session_state["fp_email"] = ""
if "fp_otp" not in st.session_state:
    st.session_state["fp_otp"] = ""
if "fp_verified" not in st.session_state:
    st.session_state["fp_verified"] = False
if "fp_message" not in st.session_state:
    st.session_state["fp_message"] = ""

with st.form("forgot_password_form"):
    email = st.text_input("Registered Email", value=st.session_state["fp_email"], placeholder="Enter your registered email")
    send_otp = st.form_submit_button("Send OTP")

if send_otp:
    st.session_state["fp_email"] = email.strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", st.session_state["fp_email"]):
        st.session_state["fp_message"] = "Please enter a valid email address."
    else:
        user = get_user_by_email(st.session_state["fp_email"])
        if not user:
            st.session_state["fp_message"] = "No account found with that email."
        else:
            otp = f"{random.randint(100000, 999999):06d}"
            st.session_state["fp_otp"] = otp
            st.session_state["fp_verified"] = False
            ok, message = send_password_reset_otp(st.session_state["fp_email"], otp)
            st.session_state["fp_message"] = message
            if ok:
                st.session_state["fp_message"] += " Please enter the OTP below."

st.markdown(f"<p style='color:#2563eb;margin-top:1rem;'>{st.session_state['fp_message']}</p>", unsafe_allow_html=True)

if st.session_state["fp_otp"]:
    with st.form("otp_form"):
        otp_code = st.text_input("Enter OTP", placeholder="6-digit code")
        verify = st.form_submit_button("Verify OTP")

    if verify:
        if otp_code.strip() == st.session_state["fp_otp"]:
            st.session_state["fp_verified"] = True
            st.success("OTP verified successfully.")
        else:
            st.error("Invalid OTP. Please try again.")

if st.session_state["fp_verified"]:
    with st.form("reset_form"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        reset = st.form_submit_button("Reset Password")

    if reset:
        if len(new_password) < 8:
            st.error("Password must be at least 8 characters long.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            ok = update_password(st.session_state["fp_email"], new_password)
            if ok:
                st.success("Password reset successful.")
                time.sleep(1)
                st.switch_page("pages/login.py")
            else:
                st.error("Unable to reset password. Please try again.")

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
st.page_link("pages/login.py", label="Back to Login")
