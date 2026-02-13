import streamlit as st
from backend.finance import compound_growth

st.title("🎯 Goal Tracker")

st.markdown("Check whether your savings plan can achieve your financial goal.")

goal = st.number_input("Target Goal Amount (₹)", min_value=0.0, value=50000.0)
monthly_saving = st.number_input("Monthly Saving (₹)", min_value=0.0, value=2000.0)
months = st.slider("Time Duration (Months)", 1, 60, 12)

risk_rate = 0.10  # Medium risk default

future_value = compound_growth(monthly_saving, risk_rate, months)

st.divider()

if future_value >= goal:
    st.success(f"🎉 Goal Achievable! Expected Amount: ₹{future_value:.2f}")
else:
    st.warning(f"⚠ Goal Not Achievable. Expected Amount: ₹{future_value:.2f}")

progress = min(future_value / goal, 1.0)
st.progress(progress)
