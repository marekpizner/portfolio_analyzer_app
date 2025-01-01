import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Predefined strategies
def hundred_age_rule(age):
    return {"Stocks": 100 - age, "Bonds": age, "Cash": 0}

def modern_portfolio_theory():
    return {"Stocks": 60, "Bonds": 30, "Cash": 10}

def balanced_portfolio():
    return {"Stocks": 50, "Bonds": 40, "Cash": 10}

def aggressive_growth():
    return {"Stocks": 80, "Bonds": 15, "Cash": 5}

strategies = {
    "100-age rule": hundred_age_rule,
    "Modern Portfolio Theory": modern_portfolio_theory,
    "Balanced Portfolio": balanced_portfolio,
    "Aggressive Growth": aggressive_growth
}

# Future yield calculation
def calculate_future_yield(portfolio, years, historical_returns):
    returns = sum(portfolio[asset] * historical_returns[asset] / 100 for asset in portfolio.keys())
    return (1 + returns) ** years - 1

# App layout
st.title("Enhanced Portfolio Analyzer")

# Step 1: Input user data
st.header("Step 1: Enter your details and portfolio")
age = st.number_input("Your age:", min_value=18, max_value=100, value=30)

# Select assets and their allocation
assets = ["Stocks", "Bonds", "Cash"]
portfolio = {}
remaining_allocation = 100

for asset in assets:
    max_allocation = remaining_allocation + portfolio.get(asset, 0)  # Allow reallocating within limits
    allocation = st.number_input(
        f"Allocate % to {asset}:",
        min_value=0,
        max_value=max_allocation,
        value=portfolio.get(asset, 0),
        step=1
    )
    portfolio[asset] = allocation
    remaining_allocation = max(100 - sum(portfolio.values()), 0)  # Ensure non-negative remaining allocation

# Check if total allocation is 100%
total_allocation = sum(portfolio.values())
if total_allocation != 100:
    st.error(f"Portfolio allocation must total 100%, but you have {total_allocation}%.")
    st.stop()

# Step 2: Choose predefined strategy
st.header("Step 2: Choose a predefined strategy")
strategy_name = st.selectbox("Select a strategy:", list(strategies.keys()))
if strategy_name == "100-age rule":
    strategy = strategies[strategy_name](age)
else:
    strategy = strategies[strategy_name]()

# Step 3: Comparison with strategy
st.header("Step 3: Compare with the chosen strategy")
comparison = pd.DataFrame({
    "Asset": assets,
    "Your Allocation (%)": [portfolio.get(asset, 0) for asset in assets],
    "Strategy Allocation (%)": [strategy.get(asset, 0) for asset in assets]
})

# Radar chart for visualization
fig = go.Figure()

# Your Portfolio
fig.add_trace(go.Scatterpolar(
    r=list(portfolio.values()),
    theta=assets,
    fill='toself',
    name='Your Portfolio',
    fillcolor='rgba(44, 160, 44, 0.4)',  # Green with transparency
    line=dict(color='rgb(44, 160, 44)', width=2)  # Solid green line
))

# Strategy
fig.add_trace(go.Scatterpolar(
    r=list(strategy.values()),
    theta=assets,
    fill='toself',
    name='Strategy',
    fillcolor='rgba(31, 119, 180, 0.4)',  # Blue with transparency
    line=dict(color='rgb(31, 119, 180)', width=2)  # Solid blue line
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100])
    ),
    showlegend=True,
    width=700,  # Adjust the width of the chart
    height=600,  # Adjust the height of the chart
    title="Portfolio vs Strategy Allocation",
    title_font_size=20,
)
st.plotly_chart(fig, use_container_width=False)  # Set to False to respect the custom size  # Set to False to respect the custom size
st.table(comparison)

# Step 4: Suggestions for improvement
st.header("Step 4: Recommendations")
suggestions = {asset: strategy[asset] - portfolio[asset] for asset in assets}
recommendation_text = []
for asset, adjustment in suggestions.items():
    if adjustment > 0:
        recommendation_text.append(f"Buy {adjustment}% more of {asset}.")
    elif adjustment < 0:
        recommendation_text.append(f"Sell {abs(adjustment)}% of {asset}.")
if recommendation_text:
    st.write("To align with the chosen strategy, consider these changes:")
    for text in recommendation_text:
        st.write(f"- {text}")
else:
    st.write("Your portfolio is perfectly aligned with the chosen strategy!")
