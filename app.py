import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator

st.set_page_config(layout="wide")
st.title("🚀 Scanner Complet US – Toutes les Actions (lent mais complet)")

# -----------------------------
# 1️⃣ Récupérer tous les tickers US (S&P500 + Nasdaq)
# -----------------------------
@st.cache_data
def get_us_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500 = pd.read_html(url)[0]["Symbol"].tolist()

    # Nasdaq top 100 (pour exemple, tu peux l’élargir)
    nasdaq_url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    nasdaq = pd.read_html(nasdaq_url)[3]["Ticker"].tolist()

    tickers = list(set(sp500 + nasdaq))  # Union sans doublon
    return tickers

tickers = get_us_tickers()
st.write(f"🔎 Nombre total de tickers à scanner : {len(tickers)}")

# -----------------------------
# 2️⃣ Fonctions pour récupérer prix et RSI
# -----------------------------
def get_stock_data(ticker):
    try:
        data = yf.download(ticker, period="3mo", interval="1d", progress=False)
        if data.empty:
            return None
        price = data["Close"].iloc[-1]
        rsi = RSIIndicator(close=data["Close"], window=14).rsi().iloc[-1]
        return price, rsi
    except:
        return None

def rsi_label(rsi):
    if rsi < 35:
        return "🔥 OPPORTUNITÉ"
    elif rsi > 70:
        return "⚠️ ATTENDRE CORRECTION"
    else:
        return "Neutre"

# -----------------------------
# 3️⃣ Scanner tous les tickers (lent)
# -----------------------------
results = []
progress_text = "Scanning all tickers..."
my_bar = st.progress(0, text=progress_text)

for i, ticker in enumerate(tickers):
    result = get_stock_data(ticker)
    if result:
        price, rsi = result
        target = price * 1.5  # +50% objectif
        upside = ((target - price)/price)*100
        shares = int(1000/price)

        results.append({
            "Ticker": ticker,
            "Prix ($)": round(price,2),
            "RSI": round(rsi,1),
            "Signal": rsi_label(rsi),
            "Target ($)": round(target,2),
            "Potentiel (%)": round(upside,1),
            "Nb actions (1000$)": shares
        })

    my_bar.progress((i+1)/len(tickers), text=progress_text)

df = pd.DataFrame(results)
df = df.sort_values(by="Potentiel (%)", ascending=False)

# -----------------------------
# 4️⃣ Affichage
# -----------------------------
st.subheader("📊 Actions filtrées par potentiel + RSI")
st.dataframe(df, use_container_width=True)
st.caption("🔄 Rafraîchis la page pour re-scanner toutes les actions")

# -----------------------------
# 5️⃣ Metrics synthèse
# -----------------------------
st.subheader("📈 Synthèse rapide")
col1, col2, col3 = st.columns(3)
col1.metric("Actions scannées", len(tickers))
col2.metric("Opportunités détectées", len(df))
col3.metric("Top Pick", df.iloc[0]["Ticker"] if not df.empty else "N/A")
