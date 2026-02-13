import streamlit as st
from backend.database import create_tables, register_user, login_user
from backend.gamification import get_gamification_summary

st.set_page_config(
    page_title="FinMentor — Investment Coach for Students",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_tables()

# ── Load Custom CSS ──
st.markdown("""
<style>
/* ── Global Theme ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f3460, #1a1a2e);
    border-right: 1px solid #0f3460;
}

[data-testid="stSidebar"] * {
    color: #e2e2e2;
}

/* ── Card Styles ── */
.card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    border: 1px solid rgba(15, 52, 96, 0.5);
}

.card h2 {
    color: #e2e2e2;
    margin: 0;
}

/* ── Metric Cards ── */
[data-testid="stMetricValue"] {
    color: #00C6FF !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #a8d8ea !important;
    font-weight: 500;
}

[data-testid="stMetricDelta"] {
    color: #69F0AE !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, #007BFF, #00C6FF);
    color: white;
    border-radius: 30px;
    border: none;
    padding: 10px 30px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #00C6FF, #007BFF);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 198, 255, 0.4);
}

/* ── Form Submit Button ── */
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #00C853, #69F0AE);
    color: #0a0a1a;
    border-radius: 30px;
    border: none;
    padding: 12px 30px;
    font-weight: 700;
    font-size: 16px;
}

/* ── Input Fields ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #1a1a2e;
    color: #e2e2e2;
    border: 1px solid #0f3460;
    border-radius: 12px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: #1a1a2e;
    color: #a8d8ea;
    border-radius: 12px 12px 0 0;
    padding: 10px 20px;
    border: 1px solid #0f3460;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #007BFF, #00C6FF) !important;
    color: white !important;
}

/* ── Headings ── */
h1, h2, h3 {
    color: #e2e2e2 !important;
}

/* ── Divider ── */
hr {
    border-color: #0f3460 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Progress Bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #007BFF, #00C6FF);
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1a1a2e;
    color: #a8d8ea;
    border-radius: 12px;
}

/* ── Login Card ── */
.login-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(15, 52, 96, 0.5);
    max-width: 500px;
    margin: 60px auto;
    text-align: center;
}

.login-card h1 {
    color: #00C6FF !important;
    font-size: 32px;
    margin-bottom: 5px;
}

.login-card p {
    color: #a8d8ea;
    font-size: 14px;
}

/* ── Sidebar Profile Badge ── */
.sidebar-profile {
    background: linear-gradient(135deg, #0f3460, #1a1a2e);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 15px;
    border: 1px solid #007BFF;
}

.sidebar-profile h3 {
    color: #00C6FF !important;
    margin: 5px 0;
    font-size: 18px;
}

.sidebar-profile p {
    color: #a8d8ea;
    margin: 3px 0;
    font-size: 13px;
}

/* ── Animations ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="stMetric"] {
    animation: fadeIn 0.5s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── Login / Register Page ──
def login_page():
    col_spacer1, col_form, col_spacer2 = st.columns([1, 2, 1])
    with col_form:
        st.markdown("""
        <div class='login-card'>
            <h1>🎓 FinMentor</h1>
            <p>Your AI-Powered Investment Coach for Students</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            u = st.text_input("Username", key="login_user")
            p = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                if login_user(u, p):
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials")

        with tab2:
            u2 = st.text_input("Choose Username", key="reg_user")
            p2 = st.text_input("Choose Password", type="password", key="reg_pass")
            if st.button("Register", use_container_width=True):
                if u2 and p2:
                    if register_user(u2, p2):
                        st.success("✅ Registered Successfully! Switch to Login tab.")
                    else:
                        st.error("❌ Username already exists")
                else:
                    st.warning("Please fill in both fields")

# ── Main App ──
if not st.session_state.logged_in:
    login_page()
else:
    username = st.session_state.username
    gamification = get_gamification_summary(username)
    level = gamification["level"]
    streak = gamification["streak"]

    # ── Sidebar ──
    st.sidebar.markdown(f"""
    <div class='sidebar-profile'>
        <div style='font-size:40px;'>🎓</div>
        <h3>{username}</h3>
        <p>Level {level['level']} — {level['name']}</p>
        <p>🔥 {streak['current_streak']}-day streak | ⭐ {level['total_xp']} XP</p>
        <p>🏆 {gamification['badge_count']} badges earned</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

    st.sidebar.divider()
    st.sidebar.markdown("### 📌 Quick Tips")
    st.sidebar.info("💡 Log savings daily to build streaks and earn XP!")
    st.sidebar.info("📚 Take quizzes to boost your financial knowledge!")
