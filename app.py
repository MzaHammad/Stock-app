import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Scanner Dynamique 2026", layout="centered")

# --- INTERFACE DE CONTRÔLE ---
st.title("🤖 Scanner Boursier Dynamique")

with st.sidebar:
    st.header("Configuration")
    market = st.selectbox("Marché", ["US", "Europe", "Asie"])
    goal = st.select_slider("Objectif de gain %", options=[10, 20, 30, 50, 100], value=50)
    
    # Liste dynamique selon le marché
    if market == "US": tickers = ["NVDA", "AAPL", "MSFT", "TSLA", "HBM", "CRWD"]
    elif market == "Europe": tickers = ["ASML.AS", "MC.PA", "OR.PA", "SAP.DE", "AIR.PA"]
    else: tickers = ["2330.TW", "7203.T", "9984.T", "005930.KS"]
    
    selected_ticker = st.selectbox("Choisir une action à analyser", tickers)

st.button("🔄 Actualiser les données en direct")

# --- MOTEUR D'ANALYSE DYNAMIQUE ---
@st.cache_data(ttl=3600) # Garde en mémoire 1h pour éviter de ralentir
def fetch_dynamic_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1mo")
    return stock, info, hist

stock, info, hist = fetch_dynamic_data(selected_ticker)

if not hist.empty:
    current_price = hist['Close'].iloc[-1]
    currency = info.get('currency', '$')
    
    # 1. Calcul RSI Dynamique
    delta = hist['Close'].diff()
    up = delta.clip(lower=0).rolling(14).mean()
    down = -1 * delta.clip(upper=0).rolling(14).mean()
    rsi = 100 - (100 / (1 + (up / down).iloc[-1]))

    # 2. Affichage des Métriques Live
    col1, col2, col3 = st.columns(3)
    col1.metric("Prix Actuel", f"{round(current_price, 2)} {currency}")
    col2.metric("RSI (14j)", f"{round(rsi, 1)}")
    col3.metric("Cible", f"{round(current_price * (1+goal/100), 2)} {currency}")

    # 3. ANALYSE FINANCIÈRE AUTOMATIQUE
    st.subheader(f"📊 Analyse de {info.get('longName', selected_ticker)}")
    st.write(info.get('longBusinessSummary', 'Description non disponible.'))

    with st.expander("💰 Santé Financière (Données réelles)"):
        f1, f2 = st.columns(2)
        f1.write(f"**Marge Opérationnelle :** {round(info.get('operatingMargins', 0)*100, 2)}%")
        f1.write(f"**Croissance CA (YoY) :** {round(info.get('revenueGrowth', 0)*100, 2)}%")
        f2.write(f"**Dette/Equity :** {info.get('debtToEquity', 'N/A')}")
        f2.write(f"**Bénéfice par Action (EPS) :** {info.get('trailingEps', 'N/A')} {currency}")

    with st.expander("🌍 Contexte Économique & News"):
        news = stock.news[:3] # Récupère les 3 dernières news
        if news:
            for n in news:
                st.write(f"🔹 **{n['title']}**")
                st.caption(f"Source: {n['publisher']}")
        else:
            st.write("Aucune news récente trouvée.")

    with st.expander("🛡️ Stratégie de Sortie (Stop-Loss)"):
        # Calcul dynamique du stop loss (basé sur la volatilité - ATR simplifié)
        low_month = hist['Low'].min()
        st.write(f"Point d'entrée suggéré : **{round(current_price * 0.97, 2)} {currency}**")
        st.error(f"Stop-Loss conseillé (Support 30j) : **{round(low_month, 2)} {currency}**")

    # 4. Calculateur d'allocation
    st.divider()
    montant = st.number_input("Montant à investir", value=1000)
    st.info(f"Pour {montant}{currency}, vous devriez acheter **{int(montant // current_price)}** actions.")
