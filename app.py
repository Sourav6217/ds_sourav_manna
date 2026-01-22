

import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Market Mood & Trader Behavior",
    layout="wide"
)
# -----------------------------
# Info message
# -----------------------------
st.info(
    "Note: This app loads large datasets directly from Google Drive. "
    "Initial loading may take some time."
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

# -----------------------------
# Key Metrics
# -----------------------------
st.subheader("What Happens Under These Conditions?")

if len(filtered_df) == 0:
    st.warning("No trades found for the selected filters.")
else:
    # Loss probability
    loss_probability = (filtered_df["closed_pnl"] <= 0).mean()

    # Average PnL
    avg_pnl = filtered_df["closed_pnl"].mean()

    # Trade count
    trade_count = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Chance of Losing Money",
        value=f"{loss_probability*100:.1f}%"
    )

    col2.metric(
        label="Average Result per Trade",
        value=f"${avg_pnl:,.2f}"
    )

    col3.metric(
        label="Number of Trades",
        value=f"{trade_count:,}"
    )


# -----------------------------
# Profit / Loss Distribution
# -----------------------------
st.subheader("How Trade Results Are Distributed")

if len(filtered_df) > 0:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.hist(
        filtered_df["closed_pnl"],
        bins=50
    )

    ax.set_xlabel("Profit / Loss per Trade")
    ax.set_ylabel("Number of Trades")
    ax.set_title(f"Trade Results During {selected_sentiment} Markets")

    st.pyplot(fig)

    st.caption(
        "This chart shows how profits and losses are spread. "
        "Greedy markets usually show wider swings — bigger wins, but also bigger losses."
    )
else:
    st.warning("Not enough data to show distribution.")

# -----------------------------
# Supporting Visuals: Behavior
# -----------------------------
st.subheader("How Trader Behavior Changes")

import matplotlib.pyplot as plt
import seaborn as sns

# Prepare summary data
behavior_summary = (
    merged_df
    .groupby("market_sentiment")
    .agg(
        trade_count=("closed_pnl", "count"),
        avg_trade_size=("size_usd", "mean")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

# ---- Plot 1: Trade Count ----
with col1:
    fig1, ax1 = plt.subplots()
    sns.barplot(
        data=behavior_summary,
        x="market_sentiment",
        y="trade_count",
        ax=ax1
    )
    ax1.set_title("Trading Activity by Market Mood")
    ax1.set_xlabel("Market Mood")
    ax1.set_ylabel("Number of Trades")
    st.pyplot(fig1)

# ---- Plot 2: Average Trade Size ----
with col2:
    fig2, ax2 = plt.subplots()
    sns.barplot(
        data=behavior_summary,
        x="market_sentiment",
        y="avg_trade_size",
        ax=ax2
    )
    ax2.set_title("Average Trade Size by Market Mood")
    ax2.set_xlabel("Market Mood")
    ax2.set_ylabel("Average Trade Size (USD)")
    st.pyplot(fig2)

st.caption(
    "Greedy markets usually see more trading activity and larger trade sizes, "
    "which increases overall risk exposure."
)

# -----------------------------
# Final Insights & Flow
# -----------------------------
st.subheader("How We Reached These Insights")

st.markdown(
    """
    ### Step-by-step journey

    **1. Started with raw data**  
    We used real trading history and daily market mood (Fear vs Greed).

    **2. Added market context to each trade**  
    Every trade was matched with the market mood of that day.

    **3. Observed behavior changes**  
    We saw how traders changed their activity and trade sizes when the market mood changed.

    **4. Measured outcomes**  
    We checked how often trades lost money and what the average result looked like.

    **5. Turned patterns into insights**  
    Instead of just looking at profits, we focused on risk and consistency.
    """
)

st.markdown(
    """
    ### Key indicators we focused on

    • Chance of losing money  
    • Average profit or loss per trade  
    • Trading activity (number of trades)  
    • Trade size as a proxy for risk  
    """
)

st.markdown(
    """
    ### What this means for smarter trading

    • Greedy markets increase risk faster than skill  
    • Bigger trades do not guarantee better outcomes  
    • Consistent traders during fearful markets are often more reliable  
    • Managing position size is critical during optimistic market phases  
    """
)

st.markdown(
    """
    ### Simple flow

    **Market Mood → Trader Behavior → Risk Exposure → Trade Outcomes → Smarter Decisions**
    """
)

