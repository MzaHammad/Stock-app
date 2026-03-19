import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Scanner Full Dynamique", layout="centered")

# --- INTERFACE DE CONTRÔLE ---
st.title("🤖 Scanner Boursier Dynamique")

with st.sidebar:
    st.header("Configuration")
    
    # Barre de recherche libre
    search_ticker = st.text_input("Recherche libre (ex: AAPL, LVMH.PA, 7203.T)", "").upper()
    
    market = st.selectbox("Marchés suggérés", ["US", "Europe", "Asie"])
    goal = st.select_slider("Objectif de gain %", options=[10, 20, 30, 50, 100], value=50)
    
    # Listes par défaut si la recherche est vide
    if not search_ticker:
        if market == "US": tickers = ["NVDA", "AAPL", "MSFT", "TSLA", "CRWD"]
        elif market == "Europe": tickers = ["ASML.AS", "MC.PA", "OR.PA", "SAP.DE"]
        else: tickers = ["2330.TW", "7203.T", "9984.T"]
        selected_ticker = st.selectbox("Actions suggérées", tickers)
    else:
        selected_ticker = search_ticker

st.button("🔄 Actualiser les données en direct")

# --- MOTEUR DE DONNÉES (CORRIGÉ) ---
# On ne cache que les données brutes (dictionnaires/dataframes), pas l'objet Ticker
@st.cache_data(ttl=3600)
def get_clean_data(ticker_symbol):
    s = yf.Ticker(ticker_symbol)
    i = s.info
    h = s.history(period="1mo")
    n = s.news[:3]
    return i, h, n

try:
    info, hist, news = get_clean_data(selected_ticker)

    if not hist.empty:
        current_price = hist['Close'].iloc[-1]
        currency = info.get('currency', '$')
        
        # 1. RSI Dynamique
        delta = hist['Close'].diff()
        up = delta.clip(lower=0).rolling(14).mean()
        down = -1 * delta.clip(upper=0).rolling(14).mean()
        rs = up / down.replace(0, 0.001)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))

        # 2. Métriques Flash
        col1, col2, col3 = st.columns(3)
        col1.metric("Prix Actuel", f"{round(current_price, 2)} {currency}")
        col2.metric("RSI (14j)", f"{round(rsi, 1)}")
        col3.metric("Cible", f"{round(current_price * (1+goal/100), 2)} {currency}")

        # 3. Identité
        st.subheader(f"📊 {info.get('longName', selected_ticker)}")
        st.caption(f"Secteur : {info.get('sector', 'N/A')} | Industrie : {info.get('industry', 'N/A')}")
        st.write(info.get('longBusinessSummary', 'Description non disponible.'))

        # 4. Analyse Financière Live
        with st.expander("💰 Santé Financière (Chiffres réels)"):
            f1, f2 = st.columns(2)
            margin = info.get('operatingMargins', 0)
            growth = info.get('revenueGrowth', 0)
            f1.write(f"**Marge Opérationnelle :** {round(margin*100, 2) if margin else 'N/A'}%")
            f1.write(f"**Croissance CA :** {round(growth*100, 2) if growth else 'N/A'}%")
            f2.write(f"**PER (Ratio cours/bénéfice) :** {info.get('trailingPE', 'N/A')}")
            f2.write(f"**EPS (Bénéfice/Action) :** {info.get('trailingEps', 'N/A')} {currency}")

        # 5. News & Économie
        with st.expander("🌍 Actualités Récentes"):
            if news:
                for n in news:
                    st.markdown(f"🔹 **[{n['title']}]({n['link']})**")
                    st.caption(f"Source: {n['publisher']}")
            else:
                st.write("Aucune news récente trouvée.")

        # 6. Stratégie de Protection
        with st.expander("🛡️ Point d'Entrée & Sécurité"):
            low_30j = hist['Low'].min()
            st.write(f"Prix d'entrée suggéré (-3% du cours) : **{round(current_price * 0.97, 2)} {currency}**")
            st.error(f"Stop-Loss conseillé (Support 30j) : **{round(low_30j, 2)} {currency}**")

        # 7. Calculateur Mobile
        st.divider()
        budget = st.number_input("Budget d'investissement ($/€/¥)", value=1000)
        st.success(f"Nombre d'actions à acheter : **{int(budget // current_price)}**")

    else:
        st.error("Données historiques introuvables. Vérifiez le Ticker (ex: 'MC.PA' pour LVMH).")

except Exception as e:
    st.warning(f"Le ticker '{selected_ticker}' est invalide ou Yahoo Finance ne répond pas.")
