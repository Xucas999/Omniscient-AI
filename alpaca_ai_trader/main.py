import logging
from fetch_data import fetch_data
from features import make_features
from model import train_model
from trade import get_trade_signal, submit_order

logging.basicConfig(filename='trading_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def run():
    df = fetch_data()
    X, y, _ = make_features(df)
    train_model(X, y)
    signal = get_trade_signal()
    logging.info(f"Predicted signal: {signal}")
    submit_order(signal)

if __name__ == '__main__':
    run()