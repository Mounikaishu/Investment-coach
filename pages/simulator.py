import streamlit as st
import plotly.graph_objects as go
from backend.finance import compound_growth

st.title("📈 Investment Simulator")

st.markdown("Simulate how your micro-investments can grow over time at different risk levels.")

col1, col2 = st.columns(2)
with col1:
    monthly_saving = st.number_input("Monthly Saving Amount (₹)", min_value=100.0, value=2000.0, step=500.0)
with col2:
    months = st.slider("Investment Duration (Months)", 1, 60, 12)

risk_rates = {
    "🟢 Low Risk (6% — FD/RD)": 0.06,
    "🟡 Medium Risk (10% — Index Fund)": 0.10,
    "🔴 High Risk (15% — Equity SIP)": 0.15
}

fig = go.Figure()

final_values = {}
for label, rate in risk_rates.items():
    values = [
        compound_growth(monthly_saving, rate, m)
        for m in range(1, months + 1)
    ]
    final_values[label] = values[-1]

    fig.add_trace(
        go.Scatter(
            x=list(range(1, months + 1)),
            y=values,
            mode='lines',
            name=label,
            line=dict(width=3),
            fill='tonexty' if rate > 0.06 else 'tozeroy',
        )
    )

# Total invested line
invested_values = [monthly_saving * m for m in range(1, months + 1)]
fig.add_trace(
    go.Scatter(
        x=list(range(1, months + 1)),
        y=invested_values,
        mode='lines',
        name='💵 Total Invested',
        line=dict(width=2, dash='dash', color='white'),
    )
)

fig.update_layout(
    title="Investment Growth Comparison",
    xaxis_title="Months",
    yaxis_title="Value (₹)",
    height=450,
    template="plotly_dark",
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# ── Results Summary ──
st.markdown("### 💡 Results Summary")
total_invested = monthly_saving * months
cols = st.columns(len(risk_rates) + 1)

cols[0].metric("💵 Total Invested", f"₹{total_invested:,.0f}")

for i, (label, value) in enumerate(final_values.items()):
    returns = value - total_invested
    cols[i+1].metric(
        label.split("(")[0].strip(),
        f"₹{value:,.0f}",
        delta=f"+₹{returns:,.0f} returns"
    )

st.divider()
st.info("💡 **Tip**: Even ₹500/month in a SIP can grow significantly over 5+ years thanks to compound interest!")
