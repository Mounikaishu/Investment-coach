import streamlit as st
from backend.database import (
    create_users_table,
    create_transactions_table,
    register_user,
    login_user
)

st.set_page_config(page_title="FinMentor", layout="wide")

create_users_table()
create_transactions_table()

# LIGHT UI
st.markdown("""
<style>
body { background: linear-gradient(to right, #f8fbff, #eaf4ff); }
.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #2ecc71);
    color: white;
    border-radius: 12px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.markdown("<div class='card'><h2>🔐 FinMentor Login</h2></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid Credentials")

    with tab2:
        u2 = st.text_input("New Username")
        p2 = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(u2, p2):
                st.success("Registered Successfully")
            else:
                st.error("User already exists")


if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("FinMentor")
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("<div class='card'><h1>💰 Welcome to FinMentor</h1></div>", unsafe_allow_html=True)
