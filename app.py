st.info(
    "Note: This app loads large datasets directly from Google Drive. "
    "Initial loading may take some time."
)


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

# -----------------------------
# Load Large Data from Google Drive
# -----------------------------
import pandas as pd

@st.cache_data(show_spinner=True)
def load_trader_data():
    url = "https://drive.google.com/uc?id=1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs"
    df = pd.read_csv(url)
    return df

@st.cache_data(show_spinner=True)
def load_sentiment_data():
    url = "https://drive.google.com/uc?id=1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf"
    sentiment = pd.read_csv(url)
    return sentiment

trades_df = load_trader_data()
sentiment_df = load_sentiment_data()

# -----------------------------
# Minimal Cleaning & Merge
# -----------------------------
trades_df.columns = trades_df.columns.str.lower().str.replace(" ", "_")

sentiment_df["date"] = pd.to_datetime(sentiment_df["date"])
trades_df["date"] = pd.to_datetime(trades_df["timestamp_ist"].str.split(" ").str[0], dayfirst=True)

sentiment_df["market_sentiment"] = sentiment_df["classification"].replace(
    {
        "Extreme Fear": "Fear",
        "Fear": "Fear",
        "Neutral": "Neutral",
        "Greed": "Greed",
        "Extreme Greed": "Greed"
    }
)

merged_df = trades_df.merge(
    sentiment_df[["date", "market_sentiment"]],
    on="date",
    how="inner"
)

merged_df = merged_df[merged_df["market_sentiment"].isin(["Fear", "Greed"])]

# -----------------------------
# Apply User Filters
# -----------------------------
filtered_df = merged_df[
    (merged_df["market_sentiment"] == selected_sentiment) &
    (merged_df["size_usd"] >= trade_size_range[0]) &
    (merged_df["size_usd"] <= trade_size_range[1])
]

st.subheader("Filtered Trade Data (Preview)")
st.write(f"Showing **{len(filtered_df):,} trades**")

st.dataframe(
    filtered_df[["market_sentiment", "size_usd", "closed_pnl"]].head(10)
)

