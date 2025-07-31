import requests
import os

def get_company_news(company_name, from_date, to_date, api_key=os.getenv("NEWS_API")):
    url = f"https://newsapi.org/v2/everything?q={company_name}&from={from_date}&to={to_date}&language=en&apiKey={api_key}&pageSize=100"
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])