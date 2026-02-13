import streamlit as st
from backend.database import create_users_table, register_user, login_user

st.set_page_config(page_title="FinMentor", layout="wide")

create_users_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.title("🔐 FinMentor Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN TAB
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid Credentials ❌")

    # REGISTER TAB
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("User Registered Successfully 🎉")
            else:
                st.error("Username already exists ❌")


if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("💰 FinMentor - AI Investment Coach")
    st.markdown("Use sidebar to navigate between features.")
