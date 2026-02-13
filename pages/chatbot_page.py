import streamlit as st
from ai.chatbot import get_financial_advice
from backend.finance import calculate_monthly_savings

st.title("🤖 AI Financial Coach")

st.markdown("Ask your AI mentor for personalized financial advice.")

income = st.number_input("Monthly Income (₹)", min_value=0.0, value=8000.0)
expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=6000.0)
goal = st.number_input("Goal Amount (₹)", min_value=0.0, value=50000.0)
months = st.slider("Goal Duration (Months)", 1, 60, 12)

savings = calculate_monthly_savings(income, expenses)

st.divider()

user_query = st.text_input("Ask your financial question...")

if user_query:
    response = get_financial_advice(
        user_query,
        income,
        expenses,
        savings,
        goal,
        months
    )
    st.markdown("### 💡 AI Advice")
    st.write(response)
