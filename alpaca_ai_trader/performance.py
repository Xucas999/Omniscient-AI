import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL

def show_positions():
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    positions = api.list_positions()
    for pos in positions:
        print(f"{pos.symbol} | Qty: {pos.qty} | Avg Entry: {pos.avg_entry_price} | Unrealized PnL: {pos.unrealized_pl} | Current Price: {pos.current_price}")

if __name__ == '__main__':
    show_positions()