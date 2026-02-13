import streamlit as st
import plotly.graph_objects as go
from backend.finance import compound_growth
from backend.gamification import check_and_award_badges
from backend.database import award_badge

st.title("🎯 Goal Tracker")

st.markdown("Set a savings goal and see if your plan can achieve it!")

col1, col2 = st.columns(2)
with col1:
    goal = st.number_input("Target Goal Amount (₹)", min_value=100.0, value=50000.0, step=5000.0)
    monthly_saving = st.number_input("Monthly Saving (₹)", min_value=100.0, value=2000.0, step=500.0)

with col2:
    months = st.slider("Time Duration (Months)", 1, 60, 12)
    risk_option = st.selectbox("Risk Level", [
        "🟢 Low Risk (6%)",
        "🟡 Medium Risk (10%)",
        "🔴 High Risk (15%)"
    ], index=1)

risk_map = {"🟢 Low Risk (6%)": 0.06, "🟡 Medium Risk (10%)": 0.10, "🔴 High Risk (15%)": 0.15}
risk_rate = risk_map[risk_option]

future_value = compound_growth(monthly_saving, risk_rate, months)
total_invested = monthly_saving * months

st.divider()

# ── Result ──
progress = min(future_value / goal, 1.0)

if future_value >= goal:
    st.success(f"🎉 **Goal Achievable!** Expected Amount: ₹{future_value:,.2f}")
    surplus = future_value - goal
    st.markdown(f"💰 You'll have a surplus of **₹{surplus:,.2f}** beyond your goal!")
    # Award Goal Achiever badge
    username = st.session_state.username
    award_badge(username, "Goal Achiever 🎯")
    check_and_award_badges(username)
else:
    st.warning(f"⚠ **Goal Not Achievable** with current plan. Expected: ₹{future_value:,.2f}")
    shortfall = goal - future_value
    st.markdown(f"📉 You'll be short by **₹{shortfall:,.2f}**. Consider increasing monthly savings or duration.")

# ── Progress Gauge ──
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=future_value,
    title={"text": "Projected vs Goal"},
    delta={"reference": goal, "relative": False},
    gauge={
        "axis": {"range": [0, goal * 1.2]},
        "bar": {"color": "#00C853" if future_value >= goal else "#FF9800"},
        "steps": [
            {"range": [0, goal * 0.5], "color": "#FF5252"},
            {"range": [goal * 0.5, goal * 0.8], "color": "#FFD740"},
            {"range": [goal * 0.8, goal], "color": "#69F0AE"},
            {"range": [goal, goal * 1.2], "color": "#00C853"},
        ],
        "threshold": {
            "line": {"color": "white", "width": 3},
            "thickness": 0.8,
            "value": goal
        }
    }
))
fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20), template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# ── Summary Cards ──
col1, col2, col3 = st.columns(3)
col1.metric("💵 Total Invested", f"₹{total_invested:,.0f}")
col2.metric("📈 Expected Returns", f"₹{future_value - total_invested:,.0f}")
col3.metric("🎯 Goal Progress", f"{progress*100:.1f}%")

st.progress(progress)

st.divider()

# ── Recommendation ──
if future_value < goal:
    needed_monthly = goal  # approximate finding
    for test_monthly in range(int(monthly_saving), int(goal), 100):
        if compound_growth(test_monthly, risk_rate, months) >= goal:
            needed_monthly = test_monthly
            break
    st.info(f"💡 **Suggestion**: To reach your goal of ₹{goal:,.0f}, try saving **₹{needed_monthly:,.0f}/month** instead.")
