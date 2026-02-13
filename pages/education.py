import streamlit as st
import random
from backend.database import save_quiz_score, get_quiz_scores, add_xp
from backend.gamification import check_and_award_badges

st.title("📚 Financial Education")
username = st.session_state.username

# ── Financial Tips ────────────────────────────────────

TIPS = [
    {"title": "The 50-30-20 Rule", "content": "Allocate 50% of income to needs, 30% to wants, and 20% to savings. This simple budgeting framework helps students manage money without overthinking.", "icon": "📐"},
    {"title": "Start an Emergency Fund", "content": "Aim to save at least ₹5,000 as a starter emergency fund. Even ₹500/month adds up quickly and protects you from unexpected expenses.", "icon": "🛡️"},
    {"title": "The Power of Compound Interest", "content": "₹2,000/month at 10% annual return becomes ₹4.1 lakh in 10 years! Start early — time is your greatest asset.", "icon": "📈"},
    {"title": "Avoid Lifestyle Inflation", "content": "When your income grows, resist the urge to increase spending proportionally. Channel the extra into savings and investments.", "icon": "🎯"},
    {"title": "Track Every Rupee", "content": "Small expenses add up. ₹50/day on snacks = ₹18,250/year! Awareness is the first step to smarter spending.", "icon": "🔍"},
    {"title": "SIP: Your Best Friend", "content": "Systematic Investment Plans let you invest as little as ₹500/month in mutual funds. It's the easiest way for students to start investing.", "icon": "💰"},
    {"title": "Good Debt vs Bad Debt", "content": "Education loans can be good debt (investment in future earning). Credit card debt at 36%+ interest is bad debt. Know the difference.", "icon": "⚖️"},
    {"title": "The Latte Factor", "content": "Small daily luxuries compound over time. ₹150/day coffee × 365 = ₹54,750/year. Redirect even half to savings.", "icon": "☕"},
    {"title": "Pay Yourself First", "content": "Transfer savings the moment you receive money — before paying bills or shopping. Treat savings as a non-negotiable expense.", "icon": "🥇"},
    {"title": "Diversify Your Savings", "content": "Don't put all your money in one place. Split between savings account, fixed deposit, and mutual funds for safety and growth.", "icon": "🌈"},
]

# ── Tip of the Day ──
st.markdown("### 💡 Tip of the Day")
tip_index = hash(str(st.session_state.get("username", "")) + str(random.Random(42).randint(0, 100))) % len(TIPS)
tip = TIPS[tip_index]
st.markdown(f"""
<div style='background:linear-gradient(135deg,#0f3460,#16213e); padding:25px; border-radius:15px;
            border-left:5px solid #00C6FF; margin-bottom:20px;'>
    <h3 style='margin:0; color:#e2e2e2;'>{tip['icon']} {tip['title']}</h3>
    <p style='color:#a8d8ea; margin-top:10px; font-size:15px;'>{tip['content']}</p>
</div>
""", unsafe_allow_html=True)

# ── Browse All Tips ──
with st.expander("📖 Browse All Financial Tips"):
    for t in TIPS:
        st.markdown(f"**{t['icon']} {t['title']}**")
        st.markdown(f"{t['content']}")
        st.markdown("---")

st.divider()

# ── Financial Quizzes ────────────────────────────────

QUIZZES = {
    "Budgeting Basics": [
        {
            "question": "What does the 50-30-20 rule recommend for savings?",
            "options": ["10%", "20%", "30%", "50%"],
            "answer": "20%"
        },
        {
            "question": "Which of these is a 'need' expense?",
            "options": ["Netflix subscription", "Groceries", "New phone", "Concert tickets"],
            "answer": "Groceries"
        },
        {
            "question": "What should you do FIRST when you receive money?",
            "options": ["Go shopping", "Pay bills", "Save/invest a portion", "Buy gifts"],
            "answer": "Save/invest a portion"
        },
        {
            "question": "An emergency fund should ideally cover how many months of expenses?",
            "options": ["1 month", "3-6 months", "12 months", "24 months"],
            "answer": "3-6 months"
        },
        {
            "question": "Which is the best tool for tracking daily expenses?",
            "options": ["Memory", "A budgeting app or spreadsheet", "Asking friends", "Bank SMS only"],
            "answer": "A budgeting app or spreadsheet"
        },
    ],
    "Understanding Interest": [
        {
            "question": "What does 'compound interest' mean?",
            "options": [
                "Interest on the original amount only",
                "Interest on both principal and accumulated interest",
                "A flat fee charged monthly",
                "Interest that decreases over time"
            ],
            "answer": "Interest on both principal and accumulated interest"
        },
        {
            "question": "If you invest ₹1000 at 10% simple interest for 2 years, how much interest do you earn?",
            "options": ["₹100", "₹200", "₹210", "₹300"],
            "answer": "₹200"
        },
        {
            "question": "Which interest type grows your money faster over long periods?",
            "options": ["Simple interest", "Compound interest", "Both are the same", "Neither"],
            "answer": "Compound interest"
        },
        {
            "question": "What is the 'Rule of 72' used for?",
            "options": [
                "Calculating tax",
                "Estimating how long it takes to double your money",
                "Finding loan EMI",
                "Budgeting monthly expenses"
            ],
            "answer": "Estimating how long it takes to double your money"
        },
        {
            "question": "At 12% annual return, approximately how many years to double your money?",
            "options": ["4 years", "6 years", "8 years", "12 years"],
            "answer": "6 years"
        },
    ],
    "Smart Investing": [
        {
            "question": "What is a SIP?",
            "options": [
                "Single Investment Plan",
                "Systematic Investment Plan",
                "Simple Interest Protocol",
                "Savings Insurance Policy"
            ],
            "answer": "Systematic Investment Plan"
        },
        {
            "question": "Which investment is generally considered the safest?",
            "options": ["Stocks", "Crypto", "Fixed Deposits", "Options trading"],
            "answer": "Fixed Deposits"
        },
        {
            "question": "What does 'diversification' mean in investing?",
            "options": [
                "Putting all money in one stock",
                "Spreading investments across different assets",
                "Only investing in gold",
                "Borrowing to invest"
            ],
            "answer": "Spreading investments across different assets"
        },
        {
            "question": "What is the minimum SIP amount in most mutual funds in India?",
            "options": ["₹100", "₹500", "₹5,000", "₹10,000"],
            "answer": "₹500"
        },
        {
            "question": "Higher potential returns usually come with what?",
            "options": ["Lower risk", "Higher risk", "No risk", "Government guarantee"],
            "answer": "Higher risk"
        },
    ],
    "Spending Habits": [
        {
            "question": "What is 'lifestyle inflation'?",
            "options": [
                "Rising prices of groceries",
                "Increasing spending as income grows",
                "Investing in luxury stocks",
                "Getting a raise at work"
            ],
            "answer": "Increasing spending as income grows"
        },
        {
            "question": "Which is an example of a 'want' vs a 'need'?",
            "options": [
                "Rent payment",
                "Food groceries",
                "Designer clothes",
                "Health insurance"
            ],
            "answer": "Designer clothes"
        },
        {
            "question": "How much can ₹100/day of unnecessary spending cost per year?",
            "options": ["₹12,000", "₹24,000", "₹36,500", "₹50,000"],
            "answer": "₹36,500"
        },
        {
            "question": "What is the '24-hour rule' for purchases?",
            "options": [
                "Return items within 24 hours",
                "Wait 24 hours before making non-essential purchases",
                "Shop only between 24-hour sales",
                "Only buy things that last 24 hours"
            ],
            "answer": "Wait 24 hours before making non-essential purchases"
        },
        {
            "question": "Which technique helps reduce impulsive online shopping?",
            "options": [
                "Saving items to cart and waiting",
                "Using credit cards",
                "Enabling one-click purchase",
                "Shopping at midnight"
            ],
            "answer": "Saving items to cart and waiting"
        },
    ],
}

st.markdown("### 🧠 Financial Quizzes")
st.markdown("Test your knowledge and earn XP! Each correct answer = 5 XP bonus.")

selected_quiz = st.selectbox("Choose a topic:", list(QUIZZES.keys()))
questions = QUIZZES[selected_quiz]

# Quiz form
with st.form(f"quiz_{selected_quiz}"):
    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        ans = st.radio(
            f"Select answer for Q{i+1}:",
            q["options"],
            key=f"q_{selected_quiz}_{i}",
            label_visibility="collapsed"
        )
        user_answers.append(ans)

    submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True)

if submitted:
    score = 0
    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            score += 1

    total = len(questions)
    percentage = (score / total) * 100

    # Save score and award XP
    save_quiz_score(username, selected_quiz, score, total)
    check_and_award_badges(username)

    st.divider()

    if percentage >= 80:
        st.success(f"🎉 Excellent! You scored {score}/{total} ({percentage:.0f}%)")
        st.balloons()
    elif percentage >= 50:
        st.warning(f"👍 Good effort! You scored {score}/{total} ({percentage:.0f}%)")
    else:
        st.error(f"📖 Keep learning! You scored {score}/{total} ({percentage:.0f}%)")

    # Show correct answers
    with st.expander("📋 Review Answers"):
        for i, q in enumerate(questions):
            is_correct = user_answers[i] == q["answer"]
            icon = "✅" if is_correct else "❌"
            st.markdown(f"{icon} **Q{i+1}.** {q['question']}")
            if not is_correct:
                st.markdown(f"   Your answer: *{user_answers[i]}* → Correct: **{q['answer']}**")
            else:
                st.markdown(f"   Your answer: **{user_answers[i]}** ✓")

st.divider()

# ── Past Quiz Scores ──
st.markdown("### 📊 Your Quiz History")
past_scores = get_quiz_scores(username)
if past_scores:
    for s in past_scores[:10]:
        pct = (s["score"] / s["total"]) * 100
        icon = "🟢" if pct >= 80 else ("🟡" if pct >= 50 else "🔴")
        st.markdown(f"{icon} **{s['topic']}** — {s['score']}/{s['total']} ({pct:.0f}%) — `{s['date']}`")
else:
    st.info("Complete a quiz above to see your scores here!")
