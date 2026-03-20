import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide")
st.title("🚀 Scanner Complet US – Toutes les Actions (S&P500 + Nasdaq100)")

# -----------------------------
# 1️⃣ Récupérer les tickers depuis GitHub CSV (stable pour Streamlit Cloud)
# -----------------------------
@st.cache_data
def get_us_tickers():
    # S&P500
    sp500_url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    sp500 = pd.read_csv(sp500_url)["Symbol"].tolist()
    
    # Nasdaq100 (GitHub public)
    nasdaq_url = "https://raw.githubusercontent.com/
