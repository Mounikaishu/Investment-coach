import streamlit as st
import pandas as pd
import plotly.express as px
from backend.database import add_transaction, get_user_transactions

st.title("📅 Daily Income & Expense Tracker")

username = st.session_state.username

amount = st.number_input("Amount (₹)", min_value=0.0)
category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Investment", "Other"])
t_type = st.selectbox("Type", ["Income", "Expense"])

if st.button("Add Entry"):
    add_transaction(username, amount, t_type, category)
    st.success("Transaction Added")

data = get_user_transactions(username)

if data:
    df = pd.DataFrame(data, columns=["Amount", "Type", "Category", "Date"])
    st.dataframe(df)

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

    st.metric("Total Income", f"₹{total_income}")
    st.metric("Total Expense", f"₹{total_expense}")
    st.metric("Net Savings", f"₹{total_income-total_expense}")

    # Pie Chart
    expense_df = df[df["Type"] == "Expense"]
    if not expense_df.empty:
        fig = px.pie(expense_df, names="Category", values="Amount", title="Expense Breakdown")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No transactions yet")
