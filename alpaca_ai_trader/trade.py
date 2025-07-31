import alpaca_trade_api as tradeapi
import numpy as np
from config import API_KEY, API_SECRET, BASE_URL, SYMBOL
from fetch_data import fetch_data
from features import make_features
from model import load_model

def get_trade_signal():
    model, scaler = load_model()
    df = fetch_data()
    X, _, _ = make_features(df)
    latest_features = scaler.transform(X[-1].reshape(1, -1))
    pred = model.predict(latest_features)[0]
    return 'buy' if pred == 1 else 'sell'

def submit_order(signal):
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    position = api.get_position(SYMBOL) if SYMBOL in [p.symbol for p in api.list_positions()] else None
    qty = 1

    if signal == 'buy' and not position:
        api.submit_order(symbol=SYMBOL, qty=qty, side='buy', type='market', time_in_force='gtc')
        print("Buy order submitted.")
    elif signal == 'sell' and position:
        api.submit_order(symbol=SYMBOL, qty=qty, side='sell', type='market', time_in_force='gtc')
        print("Sell order submitted.")
    else:
        print("No action taken.")