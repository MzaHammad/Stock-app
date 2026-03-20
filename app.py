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
    nasdaq_url = "https://raw.githubusercontent.com/atilsamancioglu/NBA-Players-Stats/master/NASDAQ100.csv"
    nasdaq = pd.read_csv(nasdaq_url)["Ticker"].tolist()
    
    tickers = list(set(sp500 + nasdaq))  # union sans doublons
    return tickers

tickers = get_us_tickers()
st.write(f"🔎 Nombre total de tickers à scanner : {len(tickers)}")

# -----------------------------
# 2️⃣ Calcul RSI maison (14 jours)
# -----------------------------
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def rsi_label(rsi):
    if rsi < 35:
        return "🔥 OPPORTUNITÉ"
    elif rsi > 70:
        return "⚠️ ATTENDRE CORRECTION"
    else:
        return "Neutre"

# -----------------------------
# 3️⃣ Scanner tous les tickers (lent mais complet)
# -----------------------------
results = []
progress_text = "Scanning all tickers..."
my_bar = st.progress(0, text=progress_text)

for i, ticker in enumerate(tickers):
    try:
        data = yf.download(ticker, period="3mo", interval="1d", progress=False)
        if data.empty:
            continue
        price = data["Close"].iloc[-1]
        rsi = compute_rsi(data["Close"], 14).iloc[-1]

        target = price * 1.5  # objectif +50%
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

    except:
        continue

    my_bar.progress((i+1)/len(tickers), text=progress_text)

df = pd.DataFrame(results)
df = df.sort_values(by="Potentiel (%)", ascending=False)

# -----------------------------
# 4️⃣ Affichage tableau
# -----------------------------
st.subheader("📊 Actions filtrées par potentiel + RSI")
st.dataframe(df, use_container_width=True)
st.caption("🔄 Rafraîchis la page pour re-scanner toutes les actions")

# -----------------------------
# 5️⃣ Synthèse rapide
# -----------------------------
st.subheader("📈 Synthèse rapide")
col1, col2, col3 = st.columns(3)
col1.metric("Actions scannées", len(tickers))
col2.metric("Opportunités détectées", len(df))
col3.metric("Top Pick", df.iloc[0]["Ticker"] if not df.empty else "N/A")
