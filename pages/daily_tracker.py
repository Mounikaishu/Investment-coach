import streamlit as st
import pandas as pd
import plotly.express as px
from backend.database import add_transaction, get_transactions
from backend.gamification import check_and_award_badges

st.title("📅 Daily Tracker")
user = st.session_state.username

st.markdown("### ➕ Add Transaction")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Investment", "Salary", "Freelance", "Other"])

with col2:
    t_type = st.selectbox("Type", ["Income", "Expense"])
    st.markdown("")  # spacer
    st.markdown("")  # spacer

if st.button("💾 Add Transaction", use_container_width=True):
    if amount > 0:
        add_transaction(user, amount, t_type, category)
        # Check for new badges after adding transaction
        new_badges = check_and_award_badges(user)
        st.success("✅ Transaction Added!")
        if new_badges:
            for badge in new_badges:
                st.toast(f"🎉 Badge Unlocked: {badge}", icon="🏆")
        st.rerun()
    else:
        st.warning("Please enter a valid amount")

st.divider()

# ── Transaction History ──
data = get_transactions(user)

if data:
    df = pd.DataFrame(data, columns=["Amount", "Type", "Category", "Date"])
    
    # ── Summary Metrics ──
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    savings = income - expense

    st.markdown("### 📋 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Income", f"₹{income:,.0f}")
    col2.metric("🔴 Expense", f"₹{expense:,.0f}")
    col3.metric("💰 Net Savings", f"₹{savings:,.0f}", 
                delta=f"{(savings/income*100):.0f}% saving rate" if income > 0 else None)

    st.divider()

    # ── Charts ──
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### 🍩 Expense by Category")
        expense_df = df[df["Type"] == "Expense"]
        if not expense_df.empty:
            fig = px.pie(
                expense_df, names="Category", values="Amount",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses logged yet")
    
    with chart_col2:
        st.markdown("### 📊 Income by Category")
        income_df = df[df["Type"] == "Income"]
        if not income_df.empty:
            fig = px.pie(
                income_df, names="Category", values="Amount",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No income logged yet")

    st.divider()

    # ── Transaction Table ──
    st.markdown("### 📝 All Transactions")
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.info("🚀 No transactions yet. Add your first entry above to start tracking!")
