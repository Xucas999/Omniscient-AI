from newsapi import NewsApiClient
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize
api_key = os.getenv("NEWS_API")
print(api_key)
newsapi = NewsApiClient(api_key=api_key)

# Define parameters
query = (
    "FTSE OR FTSE100 OR FTSE-100 OR "
    "Shell OR HSBC OR AstraZeneca OR "
    "BP OR GlaxoSmithKline OR Barclays OR "
    "British_American_Tobacco OR Diageo OR "
    "Rio_Tinto OR Vodafone OR "
    "energy OR financial OR healthcare OR "
    "consumer OR industrial OR materials OR "
    "real estate OR technology OR telecom"
)  # your keywords
page_size = 20  # max per request
max_pages = 5  # adjust for more data
all_articles = []


for page in range(1, max_pages + 1):
    print(f"Fetching page {page}...")
    articles = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='publishedAt',
        page=page,
        page_size=page_size,
        from_param='2025-04-26',  # start date
        to='2025-05-26'           # end date
    )
    
    for article in articles['articles']:
        headline = article['title']
        date = article['publishedAt'][:10]  # YYYY-MM-DD
        all_articles.append({'headline': headline, 'date': date})
    
    time.sleep(1)  # to respect API rate limits

# Save to CSV
df = pd.DataFrame(all_articles)
df.to_csv('headlines.csv', index=False)
print(f"Saved {len(df)} headlines to headlines.csv")