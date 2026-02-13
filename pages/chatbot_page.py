import streamlit as st
import pandas as pd
from backend.database import get_transactions, get_streak
from backend.gamification import get_gamification_summary
from ai.chatbot import get_financial_advice

st.title("🤖 AI Financial Coach")

username = st.session_state.username

# Load financial data
data = get_transactions(username)
gamification = get_gamification_summary(username)

income = 0
expense = 0

if data:
    df = pd.DataFrame(data, columns=["Amount", "Type", "Category", "Date"])
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

savings = income - expense
streak = gamification["streak"]
level = gamification["level"]

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

user_query = st.chat_input("Ask anything about your finances...")

if user_query:
    st.chat_message("user").write(user_query)

    # Build smart context prompt with gamification data
    full_prompt = f"""
    You are FinMentor, a friendly and motivating financial mentor for students.
    Communicate in a clear, encouraging, and practical way.
    Use emojis to keep things engaging. Keep answers concise but helpful.

    User Profile:
    - Username: {username}
    - Level: {level['level']} ({level['name']})
    - Current Saving Streak: {streak['current_streak']} days
    - Total XP: {level['total_xp']}
    - Badges Earned: {gamification['badge_count']}

    Financial Summary:
    - Total Income: ₹{income:,.0f}
    - Total Expenses: ₹{expense:,.0f}
    - Net Savings: ₹{savings:,.0f}
    - Saving Rate: {(savings/income*100):.1f}% {'(Excellent! 🌟)' if income > 0 and savings/income > 0.3 else '(Needs improvement 💪)' if income > 0 else '(No data yet)'}

    User Question:
    {user_query}

    Provide clear, practical, and motivating advice tailored to a student.
    If they ask about their data, reference the actual numbers above.
    Suggest specific actionable steps when possible.
    """

    response = get_financial_advice(full_prompt)

    st.chat_message("assistant").write(response)

    st.session_state.messages.append(("user", user_query))
    st.session_state.messages.append(("assistant", response))
