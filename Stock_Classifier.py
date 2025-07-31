import yfinance as yf

def get_company_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info  # Or use ticker.get_info() if using newer versions
    return {
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "summary": info.get("longBusinessSummary")
    }

