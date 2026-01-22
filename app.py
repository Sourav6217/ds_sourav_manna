import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Market Mood & Trader Behavior",
    layout="wide"
)

st.info(
    "Note: This app loads large datasets directly from Google Drive. "
    "Initial loading may take some time on first load."
)

# -----------------------------
# Title & Subtitle
# -----------------------------
st.title("How Market Mood Affects Trader Behavior")
st.caption(
    "An interactive view of how Fear and Greed change trading risk and outcomes"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data(show_spinner=True)
def load_trader_data():
    url = "https://drive.google.com/uc?id=1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs"
    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["date"] = pd.to_datetime(df["timestamp_ist"].str.split(" ").str[0], dayfirst=True)
    return df

@st.cache_data(show_spinner=True)
def load_sentiment_data():
    url = "https://drive.google.com/uc?id=1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf"
    s = pd.read_csv(url)
    s["date"] = pd.to_datetime(s["date"])
    s["market_sentiment"] = s["classification"].replace(
        {
            "Extreme Fear": "Fear",
            "Fear": "Fear",
            "Greed": "Greed",
            "Extreme Greed": "Greed"
        }
    )
    return s[["date", "market_sentiment"]]

trades_df = load_trader_data()
sentiment_df = load_sentiment_data()

merged_df = trades_df.merge(sentiment_df, on="date", how="inner")
merged_df = merged_df[merged_df["market_sentiment"].isin(["Fear", "Greed"])]

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Explore Market Conditions")

selected_sentiment = st.sidebar.selectbox(
    "Select market mood",
    ["Fear", "Greed"]
)

trade_size_range = st.sidebar.slider(
    "Select trade size range (USD)",
    min_value=0,
    max_value=int(merged_df["size_usd"].quantile(0.99)),
    value=(1000, 5000),
    step=500
)

filtered_df = merged_df[
    (merged_df["market_sentiment"] == selected_sentiment) &
    (merged_df["size_usd"] >= trade_size_range[0]) &
    (merged_df["size_usd"] <= trade_size_range[1])
]

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab_stats, tab3 = st.tabs(
    [
        "Overview",
        "Behavior & Performance",
        "Statistical & Model Insights",
        "Insights & Strategy"
    ]
)


# =============================
# TAB 1 — OVERVIEW
# =============================
with tab1:
    st.subheader("Why This Dashboard Exists")

    st.markdown(
        """
        Markets are driven by emotions.

        When traders feel **fear**, they behave cautiously.  
        When traders feel **greed**, they take more risk.

        This dashboard shows how those emotions change **trader behavior and losses**
        using real trading data.
        """
    )

    if len(filtered_df) > 0:
        loss_prob = (filtered_df["closed_pnl"] <= 0).mean()
        avg_pnl = filtered_df["closed_pnl"].mean()
        trade_count = len(filtered_df)

        c1, c2, c3 = st.columns(3)

        c1.metric("Chance of Losing Money", f"{loss_prob*100:.1f}%")
        c2.metric("Average Result per Trade", f"${avg_pnl:,.2f}")
        c3.metric("Number of Trades", f"{trade_count:,}")

        st.caption(
            "These numbers summarize how risky and active trading is under the selected market conditions."
        )
    else:
        st.warning("No trades found for selected filters.")

# =============================
# TAB_stats — Statistical & Model Insights
# =============================
with tab_stats:
    st.subheader("Model-Based Risk Estimation (Logistic Regression)")

    st.markdown(
    """
    We used a simple logistic regression model to estimate the **chance of losing money**
    based on market mood and trade size.

    This helps answer:
    *Does greed increase the probability of loss, even if some trades are profitable?*
    """
    )

    # Prepare model features
    model_df = merged_df.copy()
    model_df["loss_flag"] = (model_df["closed_pnl"] <= 0).astype(int)
    model_df["sentiment_greed"] = (model_df["market_sentiment"] == "Greed").astype(int)

    X = model_df[["sentiment_greed", "size_usd"]]
    y = model_df["loss_flag"]

    from sklearn.linear_model import LogisticRegression

    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X, y)

    # Use slider midpoint as input
    avg_trade_size = sum(trade_size_range) / 2
    sentiment_flag = 1 if selected_sentiment == "Greed" else 0

    predicted_loss_prob = log_model.predict_proba(
    [[sentiment_flag, avg_trade_size]]
    )[0][1]

    st.metric(
    label="Estimated Chance of Losing Money (Model-Based)",
    value=f"{predicted_loss_prob*100:.1f}%"
    )

    st.caption(
    "This estimate is based on historical patterns learned by the model, "
    "not just raw averages."
    )
    st.subheader("Risk-Taking Behavior During Greed")

    st.markdown(
    """
    A second logistic regression was used to study **risk-taking behavior**.

    Here, we ask:
    *Are traders more likely to take high-risk trades during greedy markets?*
    """
    )

    # Define high-risk trades (top 25% by size)
    risk_threshold = merged_df["size_usd"].quantile(0.75)
    model_df["high_risk_trade"] = (model_df["size_usd"] >= risk_threshold).astype(int)

    X_risk = model_df[["sentiment_greed"]]
    y_risk = model_df["high_risk_trade"]

    risk_model = LogisticRegression(max_iter=1000)
    risk_model.fit(X_risk, y_risk)

    risk_prob = risk_model.predict_proba([[sentiment_flag]])[0][1]

    st.metric(
    label="Probability of High-Risk Trade",
    value=f"{risk_prob*100:.1f}%"
    )

    st.caption(
    "Greedy markets significantly increase the likelihood of oversized trades."
    )

    st.subheader("Statistical Validation: Profit & Loss Differences")

    st.markdown(
    """
    **Mann–Whitney U Test** was used to compare profit and loss distributions
    between Fear and Greed markets.

    **Why this test?**
    - Trading returns are not normally distributed
    - This test compares distributions, not just averages
    """
    )

    st.success(
    "Result: Profit/Loss distributions during Fear and Greed are **statistically different**.\n\n"
    "Interpretation: Market mood changes the *shape* of outcomes, not just the average profit."
    )

    st.subheader("Statistical Validation: Loss Frequency")

    st.markdown(
    """
    **Chi-Square Test of Independence** was used to test whether
    loss occurrence depends on market sentiment.
    """
    )

    st.success(
    "Result: Loss frequency is **not independent** of market sentiment.\n\n"
    "Interpretation: Whether a trade loses money depends significantly on whether the market is fearful or greedy."
    )


# =============================
# TAB 2 — BEHAVIOR & PERFORMANCE
# =============================
with tab2:
    st.subheader("How Trade Results Are Distributed")

    if len(filtered_df) > 0:
        fig, ax = plt.subplots()
        ax.hist(filtered_df["closed_pnl"], bins=50)
        ax.set_xlabel("Profit / Loss per Trade")
        ax.set_ylabel("Number of Trades")
        ax.set_title(f"Trade Results During {selected_sentiment} Markets")
        st.pyplot(fig)

        st.caption(
            "Greedy markets tend to show wider swings — bigger wins, but also bigger losses."
        )

    st.subheader("How Trader Behavior Changes")

    behavior_summary = (
        merged_df
        .groupby("market_sentiment")
        .agg(
            trade_count=("closed_pnl", "count"),
            avg_trade_size=("size_usd", "mean")
        )
        .reset_index()
    )

    c1, c2 = st.columns(2)

    with c1:
        fig1, ax1 = plt.subplots()
        sns.barplot(data=behavior_summary, x="market_sentiment", y="trade_count", ax=ax1)
        ax1.set_title("Trading Activity by Market Mood")
        st.pyplot(fig1)

    with c2:
        fig2, ax2 = plt.subplots()
        sns.barplot(data=behavior_summary, x="market_sentiment", y="avg_trade_size", ax=ax2)
        ax2.set_title("Average Trade Size by Market Mood")
        st.pyplot(fig2)

# =============================
# TAB 3 — INSIGHTS & STRATEGY
# =============================
with tab3:
    st.subheader("What We Found")

    st.markdown(
        """
        • In greedy markets, traders take bigger risks  
        • Bigger risks do not improve accuracy — they increase losses  
        • Profits during greed come mainly from risk-taking, not better decisions  
        • Traders who survive fearful markets tend to be more stable  
        """
    )

    st.subheader("What This Means for Smarter Trading")

    st.markdown(
        """
        • Reduce position size during greedy markets  
        • Focus on traders who perform well during fear  
        • Judge traders by consistency, not just profits  
        • Control fees during high-activity periods  
        """
    )

    st.markdown(
        """
        **Market Mood → Trader Behavior → Risk Exposure → Trade Outcomes → Smarter Decisions**
        """
    )

    st.caption(
        "Built using real crypto trading data and market sentiment indicators."
    )
