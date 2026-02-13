import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.database import get_transactions, get_streak, get_badges, get_recent_transactions, get_total_savings
from backend.gamification import get_gamification_summary, check_and_award_badges, BADGE_DEFINITIONS
from backend.scoring import health_score
from backend.nudges import get_nudges
import pandas as pd
from datetime import datetime

st.title("📊 Financial Dashboard")
user = st.session_state.username

# ── Check & award any new badges ──
new_badges = check_and_award_badges(user)
if new_badges:
    for badge in new_badges:
        st.toast(f"🎉 Badge Unlocked: {badge}", icon="🏆")

# ── Load data ──
data = get_transactions(user)
gamification = get_gamification_summary(user)
streak = gamification["streak"]
level = gamification["level"]
badges = gamification["badges"]

# ── Behavioral Nudges ──
nudges = get_nudges(user)
if nudges:
    for nudge in nudges:
        if nudge["type"] == "warning":
            st.warning(nudge["message"])
        elif nudge["type"] == "success":
            st.success(nudge["message"])
        elif nudge["type"] == "info":
            st.info(nudge["message"])

# ── Summary Cards Row ──
st.markdown("### 📋 Overview")
col1, col2, col3, col4 = st.columns(4)

total_savings = get_total_savings(user)
col1.metric("💰 Total Savings", f"₹{total_savings:,.0f}")
col2.metric("🔥 Current Streak", f"{streak['current_streak']} days",
            delta=f"Best: {streak['longest_streak']} days")
col3.metric("⭐ Level", f"{level['level']} — {level['name']}")
col4.metric("🏆 Badges", f"{gamification['badge_count']} / {gamification['total_badges']}")

# ── XP Progress Bar ──
st.markdown(f"**XP Progress** — {level['total_xp']} XP total")
if level["xp_needed"] > 0:
    st.progress(level["progress"], text=f"{level['xp_in_level']} / {level['xp_needed']} XP to next level")
else:
    st.progress(1.0, text="🏆 Max Level Reached!")

st.divider()

if data:
    df = pd.DataFrame(data, columns=["Amount", "Type", "Category", "Date"])

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    rate = (income - expense) / income * 100 if income > 0 else 0
    score = health_score(rate)

    # ── Financial Health + Savings Trend (side by side) ──
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### 💚 Financial Health Score")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00C853"},
                "steps": [
                    {"range": [0, 30], "color": "#FF5252"},
                    {"range": [30, 60], "color": "#FFD740"},
                    {"range": [60, 100], "color": "#69F0AE"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.8,
                    "value": score
                }
            }
        ))
        fig_gauge.update_layout(height=300,  margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with chart_col2:
        st.markdown("### 📈 Savings Trend")
        df["Date"] = pd.to_datetime(df["Date"])
        df_sorted = df.sort_values("Date")

        # Calculate cumulative savings over time
        df_sorted["NetAmount"] = df_sorted.apply(
            lambda r: r["Amount"] if r["Type"] == "Income" else -r["Amount"], axis=1
        )
        df_sorted["CumulativeSavings"] = df_sorted["NetAmount"].cumsum()

        fig_trend = px.area(
            df_sorted, x="Date", y="CumulativeSavings",
            labels={"CumulativeSavings": "Cumulative Savings (₹)", "Date": ""},
            color_discrete_sequence=["#00C6FF"]
        )
        fig_trend.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # ── Expense Breakdown + Income vs Expense ──
    pie_col, bar_col = st.columns(2)

    with pie_col:
        st.markdown("### 🍩 Expense Breakdown")
        expense_df = df[df["Type"] == "Expense"]
        if not expense_df.empty:
            fig_pie = px.pie(
                expense_df, names="Category", values="Amount",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_pie.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenses logged yet.")

    with bar_col:
        st.markdown("### 📊 Income vs Expense")
        fig_bar = go.Figure(data=[
            go.Bar(name="Income", x=["Summary"], y=[income], marker_color="#69F0AE"),
            go.Bar(name="Expense", x=["Summary"], y=[expense], marker_color="#FF5252"),
        ])
        fig_bar.update_layout(
            barmode="group", height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

# ── Badge Showcase ──
st.markdown("### 🏆 Badge Showcase")
if badges:
    badge_cols = st.columns(min(len(badges), 6))
    for i, badge in enumerate(badges[:6]):
        with badge_cols[i]:
            st.markdown(f"""
            <div style='text-align:center; padding:15px; background:linear-gradient(135deg,#1a1a2e,#16213e);
                        border-radius:15px; border:1px solid #0f3460; margin:5px;'>
                <div style='font-size:28px;'>{badge['name'].split()[-1] if badge['name'] else '🏅'}</div>
                <div style='font-size:11px; color:#a8d8ea; margin-top:5px;'>{badge['name']}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("🎮 Start saving to earn your first badge!")

# Show all available badges
with st.expander("📋 All Available Badges"):
    for badge_name, badge_info in BADGE_DEFINITIONS.items():
        earned = any(b["name"] == badge_name for b in badges)
        icon = "✅" if earned else "🔒"
        st.markdown(f"{icon} **{badge_name}** — {badge_info['description']}")

st.divider()

# ── Recent Activity ──
st.markdown("### 📝 Recent Activity")
recent = get_recent_transactions(user, 5)
if recent:
    for txn in recent:
        amount, t_type, category, date = txn
        emoji = "🟢" if t_type == "Income" else "🔴"
        st.markdown(f"{emoji} **{t_type}** — ₹{amount:,.0f} in *{category}* — `{date}`")
else:
    st.info("No transactions yet. Start tracking in the Daily Tracker! 📅")
