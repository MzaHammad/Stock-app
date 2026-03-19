import streamlit as st
import yfinance as yf
import pandas as pd

# Configuration de la page pour Mobile
st.set_page_config(page_title="Stock Vision 2026", layout="centered")

st.title("🚀 Stock Vision 2026")

# 1. Analyse de la Peur (VIX)
vix_data = yf.Ticker("^VIX").history(period="1d")
vix = vix_data['Close'].iloc[-1]
st.metric("Indice de Volatilité (VIX)", f"{vix:.2f}", help="Sous 20 = Calme / Dessus 25 = Peur")

# 2. Vos Cibles (+50% Objectif)
tickers = {
    "NVDA": {"target": 275, "stop": 162},
    "HBM":  {"target": 18,  "stop": 10.10},
    "CRWD": {"target": 470, "stop": 285}
}

st.subheader("Analyses Hebdomadaires")

for t, info in tickers.items():
    stock = yf.Ticker(t)
    hist = stock.history(period="20d")
    
    if not hist.empty:
        price = hist['Close'].iloc[-1]
        
        # Calcul du RSI simple
        delta = hist['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False).mean()
        ema_down = down.ewm(com=13, adjust=False).mean()
        rs = ema_up / ema_down
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        potentiel = ((info['target'] - price) / price) * 100
        
        # Affichage sous forme de "Card"
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### **{t}** : `{round(price, 2)}$`")
            with col2:
                if rsi > 70:
                    st.error(f"RSI: {round(rsi,1)}")
                elif rsi < 35:
                    st.success(f"RSI: {round(rsi,1)}")
                else:
                    st.info(f"RSI: {round(rsi,1)}")
            
            st.write(f"🎯 Objectif: **{info['target']}$** ({round(potentiel,1)}%) | 🛑 Stop: {info['stop']}$")
            
            # Calculateur d'achat (1000$)
            qty = 1000 // price
            st.caption(f"Avec 1000$, vous pouvez acheter **{int(qty)}** actions.")
            st.divider()

st.button("Actualiser les données")
