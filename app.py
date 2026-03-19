import streamlit as st
import yfinance as yf
import pandas as pd

# Configuration Mobile First
st.set_page_config(page_title="Stock Vision Pro", layout="centered")

st.title("🚀 Mon Analyste Privé : Vision 2026")

# 1. Barre d'état Marché (VIX)
vix_data = yf.Ticker("^VIX").history(period="1d")
vix = vix_data['Close'].iloc[-1]
st.metric("Indice de Volatilité (VIX)", f"{vix:.2f}", 
          delta="Calme" if vix < 20 else "Nerveux", delta_color="inverse")

# 2. Base de données des analyses (Dictionnaire centralisé)
analyses = {
    "NVDA": {
        "target": 275, "stop": 162, "entry": "175$ - 180$",
        "geo": "Tensions US/Chine intégrées ; forte demande souveraine au Moyen-Orient.",
        "eco": "Pression sur les taux compensée par la croissance massive du secteur IA.",
        "fin": "BPA attendu +65% ; Cash-flow record permettant des rachats d'actions.",
        "strat": "Domination des puces Blackwell et transition vers les services logiciels."
    },
    "HBM": {
        "target": 18, "stop": 10.10, "entry": "11.20$",
        "geo": "Sécurisation des chaînes d'approvisionnement en métaux critiques (Cuivre).",
        "eco": "Inflation des matières premières tirée par la transition énergétique.",
        "fin": "Dette nette en chute libre ; levier opérationnel maximal sur le prix du cuivre.",
        "strat": "Ouverture de nouvelles mines à forte teneur ; cible d'acquisition (M&A)."
    },
    "CRWD": {
        "target": 470, "stop": 285, "entry": "305$ (Attendre repli)",
        "geo": "Augmentation des cyber-attaques étatiques mondiales.",
        "eco": "Budget IT sanctuarisé pour la cybersécurité malgré le contexte macro.",
        "fin": "Marge brute >75% ; revenus récurrents (ARR) en accélération constante.",
        "strat": "Plateforme Falcon unifiée et intégration native de l'IA générative."
    }
}

st.markdown("---")

# 3. Boucle de génération des cartes d'actions
for t, info in analyses.items():
    stock = yf.Ticker(t)
    hist = stock.history(period="20d")
    
    if not hist.empty:
        price = hist['Close'].iloc[-1]
        
        # Calcul du RSI technique
        delta = hist['Close'].diff()
        up = delta.clip(lower=0).rolling(14).mean()
        down = -1 * delta.clip(upper=0).rolling(14).mean()
        rsi = 100 - (100 / (1 + (up / down).iloc[-1]))
        
        # Header de la carte
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{t} : {round(price, 2)}$")
        with col2:
            if rsi > 70: st.error(f"RSI: {round(rsi,1)}")
            elif rsi < 35: st.success(f"RSI: {round(rsi,1)}")
            else: st.info(f"RSI: {round(rsi,1)}")

        # Infos Clés (Visible immédiatement)
        st.write(f"🎯 **Cible : {info['target']}$** | 🛑 **Stop : {info['stop']}$**")
        st.write(f"📥 **Entrée idéale : {info['entry']}**")
        
        # Menu déroulant pour les détails d'analyse
        with st.expander("🔍 Voir l'analyse complète"):
            st.markdown(f"🌍 **Géopolitique :** {info['geo']}")
            st.markdown(f"📈 **Économie :** {info['eco']}")
            st.markdown(f"💰 **Finances :** {info['fin']}")
            st.markdown(f"💡 **Stratégie :** {info['strat']}")
            
            # Calculateur auto
            qty = 1000 // price
            st.warning(f"Allocation 1000$ : Achetez **{int(qty)}** actions.")

        st.divider()

st.caption("Données mises à jour en temps réel via Yahoo Finance API.")
