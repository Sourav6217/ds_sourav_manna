# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Explore Market Conditions")

# Market sentiment selector
selected_sentiment = st.sidebar.selectbox(
    "Select market mood",
    options=["Fear", "Greed"]
)

# Trade size slider (USD)
trade_size_range = st.sidebar.slider(
    "Select trade size range (USD)",
    min_value=0,
    max_value=20000,
    value=(1000, 5000),
    step=500
)

# -----------------------------
# Show selected

