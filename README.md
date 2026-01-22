# ds_sourav_manna
One click demo(streamlit): https://dappuravmanna-pcklturxqps3ltmz5puhdp.streamlit.app/

Google colab link: https://colab.research.google.com/drive/1b7kzEPnKm9Xd3ePVpxUmevzj7GT3ino7?usp=sharing

# Market Mood & Trader Behavior Analysis

## Overview
This project explores how **market sentiment (Fear vs Greed)** influences
**trader behavior, risk-taking, and trading outcomes** using real crypto trading data.

The goal is to uncover behavioral patterns and translate them into
**practical insights for smarter trading strategies**, as outlined in the assignment.

---

## Problem Statement
Markets are driven by emotions.

When traders feel **fear**, they tend to trade cautiously.
When traders feel **greed**, they often take larger risks.

This project studies:
- How trader behavior changes under Fear and Greed
- How those behavior changes impact losses and performance
- Whether increased profits during Greed come from better decisions or higher risk

---

## Data Sources
Two datasets were used:

1. **Historical Trader Data (Hyperliquid)**
   - Trade-level data including trade size, profit/loss, fees, and timestamps

2. **Bitcoin Fear & Greed Index**
   - Daily market sentiment classified as Fear, Neutral, or Greed

The datasets were merged by date to assign a market mood to each trade.

---

## Approach
The analysis was conducted in two layers:

### 1. Exploratory & Statistical Analysis (Colab)
- Cleaned and merged large raw datasets
- Compared trading behavior and outcomes under Fear vs Greed
- Used statistical tests:
  - Mann–Whitney U Test (PnL distribution differences)
  - Chi-square Test (loss frequency dependence on sentiment)

### 2. Modeling & Interpretation
- Logistic Regression used for:
  - Estimating probability of loss based on market mood and trade size
  - Measuring likelihood of high-risk behavior during Greed
- Focus was kept on **interpretability**, not complex models

### 3. Interactive Dashboard (Streamlit)
- Built an interactive dashboard to explore insights visually
- Allows users to:
  - Select market mood (Fear / Greed)
  - Adjust trade size range
  - Observe changes in risk, losses, and behavior

---

## Key Insights
- Greedy markets increase **risk-taking behavior** more than trading accuracy
- Larger trades do not guarantee better outcomes
- Loss probability is significantly higher during Greed regimes
- Traders who perform well during Fear tend to be more stable
- Risk management is more important than raw profitability

---

## Project Structure
ds_sourav_manna/
│
├── app.py # Streamlit dashboard
├── requirements.txt # Dependencies
├── notebooks/
│ └── notebook_1.ipynb # Full analysis in Google Colab
├── csv_files/ # (Optional) Cleaned datasets
└── README.md # Project overview


> Note: The app loads large datasets directly from Google Drive.
> Initial loading may take some time.

---

## Final Note
This project focuses on **clarity, behavioral understanding, and real-world relevance**.
Instead of complex models, the emphasis is on
**explainable insights that can drive better trading decisions**.
