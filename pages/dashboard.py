import streamlit as st
from backend.finance import calculate_monthly_savings, savings_rate
from backend.scoring import financial_health_score

st.title("📊 Financial Dashboard")

st.markdown("Analyze your savings health and financial discipline.")

income = st.number_input("Monthly Income (₹)", min_value=0.0, value=8000.0)
expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=6000.0)

savings = calculate_monthly_savings(income, expenses)
rate = savings_rate(income, savings)
score, level = financial_health_score(rate)

st.divider()

st.metric("💰 Monthly Savings", f"₹{savings:.2f}")
st.metric("📈 Savings Rate", f"{rate:.2f}%")
st.metric("🏆 Financial Health Score", f"{score}/100")

st.success(f"Level: {level}")
