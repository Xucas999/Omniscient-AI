from datetime import timedelta, datetime
import yfinance as yf
import argparse
from Get_News import get_company_news

def get_price_change(
    ticker: str,
    date_str: str,
    window: int = 3,
    return_pct: bool = False,
    threshold: float = 0.002  # e.g., 0.2% minimum movement
):
    """
    Fetch stock price change after a given date.

    Args:
        ticker (str): Stock ticker (e.g. "HSBA.L").
        date_str (str): Date of the news article (format: "YYYY-MM-DD").
        window (int): How many trading days to look ahead.
        return_pct (bool): If True, return percentage change instead of label.
        threshold (float): Ignore movement smaller than this (e.g., 0.002 = 0.2%).

    Returns:
        float | int | None: % change if return_pct else 1/0, or None if data missing or change < threshold.
    """
    try:
        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=window + 3)  # extra days to account for weekends

        data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

        if data.empty or len(data) <= window:
            return None

        open_price = data["Close"].iloc[0].item()
        future_price = data["Close"].iloc[window].item()

        pct_change = (future_price - open_price) / open_price

        if abs(pct_change) < threshold:
            return None  # Ignore tiny movements (noise)

        if return_pct:
            return round(pct_change, 4)  # e.g., 0.0234 = 2.34%
        else:
            return 1 if pct_change > 0 else 0
    except Exception as e:
        print(f"Error in get_price_change for {ticker} on {date_str}: {e}")
        return None




def generate_training_data(ticker, company_name, start_date, end_date, api_key):
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dataset = []

    while current < end:
        news_date = current.strftime("%Y-%m-%d")
        next_day = (current + timedelta(days=1)).strftime("%Y-%m-%d")
        
        articles = get_company_news(company_name, news_date, next_day, api_key)
        movement = get_price_change(ticker, news_date)  # your own function

        for article in articles:
            if movement is not None:
                dataset.append((article["title"], movement))

        current += timedelta(days=1)
    
    return dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get stock price change after a news event.")
    parser.add_argument("--ticker", required=True, help="Ticker symbol (e.g. 'HSBA.L')")
    parser.add_argument("--date", required=True, help="Date of the news in format YYYY-MM-DD")
    parser.add_argument("--window", type=int, default=1, help="Days after news to compare (default=1)")
    parser.add_argument("--return_pct", action="store_true", help="Return percentage change instead of up/down")
    parser.add_argument("--threshold", type=float, default=0.002, help="Min % movement to be considered valid")

    args = parser.parse_args()

    result = get_price_change(
        ticker=args.ticker,
        date_str=args.date,
        window=args.window,
        return_pct=args.return_pct,
        threshold=args.threshold
    )

    if result is None:
        print("No significant movement or data unavailable.")
    else:
        print(f"Result: {'{:.2%}'.format(result) if args.return_pct else ('UP' if result == 1 else 'DOWN')}")














