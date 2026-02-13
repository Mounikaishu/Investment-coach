import streamlit as st

st.set_page_config(
    page_title="FinMentor",
    layout="wide"
)

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.title("🔐 FinMentor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")


# --- MAIN APP ---
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.success("Logged in successfully 🚀")
    st.title("💰 FinMentor - AI Investment Coach")
    st.markdown("Navigate using the sidebar to explore features.")
