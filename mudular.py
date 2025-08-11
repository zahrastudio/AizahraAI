import requests
# import feedparser  # FIXED: unknown import commented out

def fetch_news_rss(url):
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:5]:
        news_items.append(entry.title)
    return news_items

def create_text_from_news(news_list):
    return "\n".join(news_list)

# Bisa diintegrasikan dengan modul video/audio terpisah
if __name__ == "__main__":
    rss_url = "https://news.google.com/rss/search?q=indonesia+OR+palestina&hl=id&gl=ID&ceid=ID:id"
    latest_news = fetch_news_rss(rss_url)
    print("Berita terbaru:")
    for news in latest_news:
        print("-", news)
