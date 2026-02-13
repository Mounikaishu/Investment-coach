"""
Behavioral Nudges — Smart contextual alerts based on user financial behavior.
"""

from backend.database import get_streak, get_transactions, get_total_savings
from datetime import datetime, timedelta
import pandas as pd


def get_nudges(username):
    """Generate a list of contextual nudge messages based on user behavior."""
    nudges = []
    streak_data = get_streak(username)
    current_streak = streak_data["current_streak"]
    last_date = streak_data["last_saving_date"]

    today = datetime.now().strftime("%Y-%m-%d")

    # ── Streak-based nudges ──

    # No transaction today — streak at risk
    if last_date and last_date != today:
        last = datetime.strptime(last_date, "%Y-%m-%d")
        days_since = (datetime.now() - last).days
        if days_since == 1 and current_streak >= 2:
            nudges.append({
                "type": "warning",
                "message": f"🔥 Don't break your {current_streak}-day streak! Log your savings today."
            })
        elif days_since > 1:
            nudges.append({
                "type": "info",
                "message": "👋 Welcome back! Start a new saving streak today — every day counts!"
            })

    # Streak milestone approaching
    milestones = [3, 7, 14, 30]
    for m in milestones:
        if current_streak == m - 1:
            nudges.append({
                "type": "success",
                "message": f"⚡ You're just 1 day away from a {m}-day streak! Keep going!"
            })
            break

    # Streak celebration
    if current_streak in milestones:
        nudges.append({
            "type": "success",
            "message": f"🎉 Amazing! You've reached a {current_streak}-day saving streak!"
        })

    # ── Spending-based nudges ──
    data = get_transactions(username)
    if data:
        df = pd.DataFrame(data, columns=["Amount", "Type", "Category", "Date"])
        df["Date"] = pd.to_datetime(df["Date"])

        # Check for spending spikes in the last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        two_weeks_ago = datetime.now() - timedelta(days=14)

        recent_expenses = df[(df["Type"] == "Expense") & (df["Date"] >= week_ago)]["Amount"].sum()
        previous_expenses = df[(df["Type"] == "Expense") & (df["Date"] >= two_weeks_ago) & (df["Date"] < week_ago)]["Amount"].sum()

        if previous_expenses > 0 and recent_expenses > previous_expenses * 1.3:
            increase = ((recent_expenses - previous_expenses) / previous_expenses) * 100
            nudges.append({
                "type": "warning",
                "message": f"📉 Your spending this week is up {increase:.0f}% from last week. Consider reviewing your expenses."
            })

        # Check if saving rate is low
        income = df[df["Type"] == "Income"]["Amount"].sum()
        expense = df[df["Type"] == "Expense"]["Amount"].sum()
        if income > 0:
            saving_rate = (income - expense) / income * 100
            if saving_rate < 10:
                nudges.append({
                    "type": "warning",
                    "message": "💡 Your saving rate is below 10%. Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings."
                })
            elif saving_rate >= 30:
                nudges.append({
                    "type": "success",
                    "message": f"🌟 Great job! You're saving {saving_rate:.0f}% of your income. Keep it up!"
                })

    # ── Savings milestones ──
    total_savings = get_total_savings(username)
    savings_milestones = [500, 1000, 2000, 5000, 10000, 25000, 50000]
    for m in savings_milestones:
        if total_savings >= m * 0.9 and total_savings < m:
            nudges.append({
                "type": "success",
                "message": f"🎯 You're almost at ₹{m:,}! Just ₹{m - total_savings:,.0f} more to go!"
            })
            break

    # ── First-time user nudge ──
    if not data:
        nudges.append({
            "type": "info",
            "message": "🚀 Welcome to FinMentor! Start by logging your income in the Daily Tracker to begin your saving journey."
        })

    return nudges
