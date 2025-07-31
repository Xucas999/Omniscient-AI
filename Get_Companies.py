import pandas as pd
import yfinance as yf
import time


def get_ftse100_companies():
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    tables = pd.read_html(url)

    # Table 4 contains the FTSE 100 constituents
    df = tables[4]

    # Clean the column names
    df.columns = [col.split('[')[0].strip() for col in df.columns]

    print("Cleaned columns:", df.columns.tolist())  # Optional, for verification

    # Return only what's needed
    return df[["Company", "Ticker"]]

# Step 2: Use yfinance to fetch sector info
def fetch_sector_info(tickers):
    data = []

    for ticker in tickers:
        try:
            yf_ticker = yf.Ticker(ticker + ".L")  # London tickers need ".L"
            info = yf_ticker.info
            sector = info.get("sector", "Unknown")
            data.append((ticker + ".L", sector))
            time.sleep(0.5)  # be polite to the API
        except Exception as e:
            print(f"Failed for {ticker}: {e}")
            data.append((ticker + ".L", "Unknown"))

    return data

# Step 3: Save to CSV
def build_sector_csv():
    companies_df = get_ftse100_companies()
    tickers = companies_df["Ticker"].tolist()
    names = companies_df["Company"].tolist()

    sectors = fetch_sector_info(tickers)

    result_df = pd.DataFrame({
        "Company": names,
        "Ticker": [t for t, s in sectors],
        "Sector": [s for t, s in sectors]
    })

    result_df.to_csv("ftse100_sectors.csv", index=False)
    print("✅ Saved ftse100_sectors.csv")

# Run it
if __name__ == "__main__":
    build_sector_csv()
