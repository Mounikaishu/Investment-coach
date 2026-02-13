import streamlit as st
import plotly.graph_objects as go
from backend.finance import compound_growth

st.title("📈 Investment Simulator")

st.markdown("Simulate micro-investment growth based on different risk levels.")

monthly_saving = st.number_input("Monthly Saving Amount (₹)", min_value=0.0, value=2000.0)
months = st.slider("Investment Duration (Months)", 1, 60, 12)

risk_rates = {
    "Low Risk (6%)": 0.06,
    "Medium Risk (10%)": 0.10,
    "High Risk (15%)": 0.15
}

fig = go.Figure()

for label, rate in risk_rates.items():
    values = [
        compound_growth(monthly_saving, rate, m)
        for m in range(1, months + 1)
    ]

    fig.add_trace(
        go.Scatter(
            x=list(range(1, months + 1)),
            y=values,
            mode='lines',
            name=label
        )
    )

fig.update_layout(
    title="Investment Growth Comparison",
    xaxis_title="Months",
    yaxis_title="Investment Value (₹)"
)

st.plotly_chart(fig, use_container_width=True)
