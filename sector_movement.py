import pandas as pd
import numpy as np
from collections import defaultdict
from get_stock_movement import get_price_change

# === Load FTSE100 Ticker to Sector Mapping ===
SECTOR_CSV = "ftse100_sectors.csv"  # Should have: Ticker, Sector columns

sector_df = pd.read_csv(SECTOR_CSV)
ticker_to_sector = dict(zip(sector_df["Ticker"], sector_df["Sector"]))
sector_list = sorted(sector_df["Sector"].unique())

def get_sector_movements(date_str, window=1):
    sector_returns = defaultdict(list)

    for ticker, sector in ticker_to_sector.items():
        pct = get_price_change(ticker, date_str, window=window, return_pct=True)

        if pct is not None:
            pct = max(-1, min(1, pct))  # clip to [-1, 1]
            sector_returns[sector].append(pct)

    # Average by sector
    sector_avg = {}
    for sector in sector_list:
        values = sector_returns.get(sector, [])
        sector_avg[sector] = round(float(np.mean(values)), 4) if values else 0.0

    return sector_avg


# === Function: Convert Sector Dict to Vector ===
def sector_dict_to_array(sector_avg):
    return [sector_avg[sector] for sector in sector_list]


# === Entry Point ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute average sector movements on a given date.")
    parser.add_argument("--date", required=True, help="Date in format YYYY-MM-DD")
    parser.add_argument("--window", type=int, default=1, help="Lookahead days for price movement")

    args = parser.parse_args()

    print(f"Calculating sector movements for {args.date}...\n")
    sector_avg = get_sector_movements(args.date, window=args.window)
    sector_vector = sector_dict_to_array(sector_avg)

    print("Sector order:")
    for i, sector in enumerate(sector_list):
        print(f"{i:>2}. {sector:<25} : {sector_vector[i]:+0.4f}")