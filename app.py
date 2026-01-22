import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Market Mood & Trader Behavior",
    layout="wide"
)

# -----------------------------
# Page Header
# -----------------------------
st.title("How Market Mood Affects Trader Behavior")

st.markdown(
    """
    Markets are driven by emotions.

    When traders feel **fear**, they tend to act cautiously.  
    When traders feel **greed**, they often take bigger risks.

    This interactive tool explores **how market mood changes trader behavior, risk-taking, and losses**
    using real crypto trading data.
    """
)

st.divider()
# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Explore Market Conditions")

selected_sentiment = st.sidebar.selectbox(
    "Select market mood",
    options=["Fear", "Greed"]
)

trade_size_range = st.sidebar.slider(
    "Select trade size range (USD)",
    min_value=0,
    max_value=20000,
    value=(1000, 5000),
    step=500
)

# -----------------------------
# Show selected inputs
# -----------------------------
st.subheader("Your Selection")

st.write(f"**Market mood:** {selected_sentiment}")
st.write(
    f"**Trade size range:** ${trade_size_range[0]:,} to ${trade_size_range[1]:,}"
)

st.divider()
