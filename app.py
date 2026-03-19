import os
import yfinance as yf
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

# CONFIGURATION DE VOS CIBLES
ACTIONS_CIBLES = {
    "NVDA": {"target": 275, "stop": 162},
    "HBM":  {"target": 18,  "stop": 10.10},
    "CRWD": {"target": 470, "stop": 285}
}
BUDGET_MENSUEL = 1000

def get_stock_data():
    results = []
    for ticker, info in ACTIONS_CIBLES.items():
        data = yf.Ticker(ticker).history(period="20d")
        if data.empty: continue
        
        current_price = data['Close'].iloc[-1]
        
        # Calcul du RSI (14 jours)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # Calcul de la stratégie
        potentiel = ((info['target'] - current_price) / current_price) * 100
        quantite = BUDGET_MENSUEL // current_price
        
        status = "NEUTRE"
        color = "#3498db"
        if rsi > 70: 
            status = "SURACHETÉ (ATTENDRE)"
            color = "#e74c3c"
        elif rsi < 35: 
            status = "SURVENDU (ACHAT !)"
            color = "#2ecc71"

        results.append({
            "ticker": ticker, "price": round(current_price, 2),
            "rsi": round(rsi, 1), "potentiel": round(potentiel, 1),
            "target": info['target'], "stop": info['stop'],
            "qty": int(quantite), "status": status, "color": color
        })
    return results

@app.route('/')
def index():
    stocks = get_stock_data()
    # Template HTML minimaliste optimisé pour mobile
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #121212; color: white; padding: 10px; }
            .card { background: #1e1e1e; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid; }
            .ticker { font-size: 20px; font-weight: bold; }
            .price { font-size: 24px; color: #f1c40f; }
            .badge { padding: 5px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2>🚀 Stock Vision 2026</h2>
        <p>Budget: {{budget}}$ | Date: 19 Mars 2026</p>
        {% for s in stocks %}
        <div class="card" style="border-left-color: {{s.color}}">
            <div style="display:flex; justify-content:space-between;">
                <span class="ticker">{{s.ticker}}</span>
                <span class="badge" style="background:{{s.color}}">{{s.status}}</span>
            </div>
            <div class="price">{{s.price}}$</div>
            <p>RSI: <b>{{s.rsi}}</b> | Potentiel: <b>+{{s.potentiel}}%</b></p>
            <p>Objectif: {{s.target}}$ | Stop-Loss: {{s.stop}}$</p>
            <hr style="border:0.5px solid #333">
            <p style="color:#aaa">Avec 1000$, achetez : <b>{{s.qty}} actions</b></p>
        </div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(html, stocks=stocks, budget=BUDGET_MENSUEL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
