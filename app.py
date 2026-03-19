import streamlit as st
import yfinance as yf
import pandas as pd

# Configuration Mobile First & Style
st.set_page_config(page_title="Stock Vision Pro", layout="centered")
st.markdown("""
    <style>
    .reportview-container .main .block-container{ padding-top: 1rem; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Mon Analyste Privé : Vision 2026")

# --- 1. BASE DE DONNÉES GLOBALE (Centralisée) ---
# Format : { "Ticker": { "region": "US/EU/ASIA", "desc": "...", "stop": 00, ... analyses } }
db = {
    "NVDA": {
        "region": "États-Unis",
        "desc": "Concepteur leader mondial de processeurs graphiques (GPU) et de puces pour l'IA.",
        "stop": 162, "entry": "175$ - 180$",
        "geo": "Tensions US/Chine intégrées ; demande souveraine au Moyen-Orient.",
        "eco": "Pression sur les taux compensée par la croissance massive du secteur IA.",
        "fin": "BPA attendu +65% ; Cash-flow record permettant des rachats d'actions.",
        "strat": "Domination Blackwell et transition vers les services logiciels."
    },
    "HBM": {
        "region": "États-Unis",
        "desc": "Compagnie minière diversifiée produisant du cuivre, du zinc et des métaux précieux.",
        "stop": 10.10, "entry": "11.20$",
        "geo": "Sécurisation des chaînes d'approvisionnement en métaux critiques.",
        "eco": "Inflation des matières premières tirée par la transition énergétique.",
        "fin": "Dette nette en chute libre ; levier opérationnel maximal sur le prix du cuivre.",
        "strat": "Ouverture de nouvelles mines ; cible d'acquisition (M&A)."
    },
    "ASML": {
        "region": "Europe",
        "desc": "Fournisseur néerlandais unique au monde de machines de lithographie EUV pour semi-conducteurs.",
        "stop": 850, "entry": "900€ - 920€",
        "geo": "Souveraineté technologique européenne ; contrôles d'exportation vers la Chine.",
        "eco": "Bénéficie des plans d'investissement massifs (Chips Act).",
        "fin": "Marge brute >50% ; carnet de commandes plein jusqu'en 2027.",
        "strat": "Monopole technologique sur la lithographie la plus avancée."
    },
    "LVMH": {
        "region": "Europe",
        "desc": "Leader mondial du luxe, possédant des marques comme Louis Vuitton, Dior, Moët & Chandon.",
        "stop": 710, "entry": "740€ - 760€",
        "geo": "Dépendance à la consommation chinoise et américaine.",
        "eco": "Pouvoir de prix (pricing power) exceptionnel face à l'inflation.",
        "fin": "Marge opérationnelle >25% ; flux de trésorerie disponible massif.",
        "strat": "Stratégie de désirabilité et d'élévation de gamme."
    },
    "TSM": {
        "region": "Asie",
        "desc": "Première fonderie de semi-conducteurs au monde, basés à Taïwan (produit pour Apple, NVDA).",
        "stop": 140, "entry": "150$ - 155$",
        "geo": "Risque géopolitique majeur (Taïwan/Chine) ; diversification géographique (USA, Japon).",
        "eco": "Indispensable à l'économie numérique mondiale.",
        "fin": "Marge brute proche de 60% ; investissements massifs (CAPEX).",
        "strat": "Maîtrise inégalée des gravures les plus fines (3nm, 2nm)."
    },
    "7203.T": { # Toyota
        "region": "Asie",
        "desc": "Constructeur automobile japonais, leader mondial en volume et pionnier de l'hybride.",
        "stop": 3100, "entry": "3300 JPY",
        "geo": "Concurrence accrue des VE chinois ; impact des taux de change (Yen).",
        "eco": "Ralentissement potentiel de la demande automobile mondiale.",
        "fin": "Bilan solide ; profits records portés par les véhicules hybrides.",
        "strat": "Pari sur une approche multi-énergies (hybride, hydrogène, électrique)."
    }
}

# --- 2. BARRE LATÉRALE (Filtres Interactifs) ---
with st.sidebar:
    st.header("Paramètres de Screening")
    
    # Sélecteur de Région
    region_filter = st.multiselect(
        "Sélectionner les marchés :",
        options=["États-Unis", "Europe", "Asie"],
        default=["États-Unis", "Europe", "Asie"]
    )
    
    st.markdown("---")
    
    # Sélecteur d'Objectif Dynamique
    goal_percentages = [10, 20, 30, 50, 100]
    selected_goal = st.select_slider(
        "Définir l'objectif de gain (%) :",
        options=goal_percentages,
        value=50, # Valeur par défaut
        help="L'application recalculera la cible et le potentiel par rapport au prix actuel."
    )
    goal_multiplier = 1 + (selected_goal / 100)

    st.markdown("---")
    # Analyse de la Peur (VIX)
    vix_data = yf.Ticker("^VIX").history(period="1d")
    vix = vix_data['Close'].iloc[-1]
    st.metric("Indice de Peur (VIX)", f"{vix:.2f}", 
              delta="Calme" if vix < 20 else "Nerveux", delta_color="inverse")

# --- 3. AFFICHAGE DES RÉSULTATS ---
st.markdown("---")
# Filtrage de la base de données
filtered_tickers = {t: info for t, info in db.items() if info['region'] in region_filter}

if not filtered_tickers:
    st.warning("Aucune action ne correspond aux filtres sélectionnés.")
else:
    for t, info in filtered_tickers.items():
        stock = yf.Ticker(t)
        # Gestion du symbole pour le Yen (Toyota)
        currency = "$" if t != "720
