import requests

def fetch_news_api():
    API_KEY = "YOUR_NEWSAPI_KEY"
    url = f"https://newsapi.org/v2/top-headlines?q=palestina,indonesia&language=id&apiKey={API_KEY}"
    resp = requests.get(url).json()
    news = []
    if resp.get("status") == "ok":
        for article in resp.get("articles", [])[:5]:
            news.append(article["title"])
    return news

if __name__ == "__main__":
    news_list = fetch_news_api()
    for news in news_list:
        print(news)

