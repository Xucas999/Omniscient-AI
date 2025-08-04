import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_bbc_headlines():
    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve BBC News page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # BBC uses h3 elements with class 'gs-c-promo-heading__title' for many headlines
    headlines = soup.find_all("h3", class_="gs-c-promo-heading__title")

    unique_headlines = list(set(h.get_text().strip() for h in headlines if h.get_text().strip()))

    return unique_headlines

def save_to_csv(headlines, filename="bbc_headlines.csv"):
    df = pd.DataFrame(headlines, columns=["headline"])
    df["source"] = "BBC News"
    df["date_scraped"] = datetime.utcnow().isoformat()
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} headlines to {filename}")

if __name__ == "__main__":
    headlines = scrape_bbc_headlines()
    if headlines:
        save_to_csv(headlines)