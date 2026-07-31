import feedparser
from datetime import datetime
import config

def get_news(number, location = None):
    feed = feedparser.parse(config.NEWS_OUTLET_URL)

    if len(feed) == 0:
        return config.RESPONSES['news_error']

    news_feed = ""

    if location is not None:
        filtered_feed = []

        for entry in feed:
            if location.lower() in entry.title.lower() or location.lower() in entry.description.lower():
                filtered_feed.append(entry)

        feed = filtered_feed

    x = range(number)
    for n in x:
        date_raw = datetime.strptime(feed.entries[n].published, "%a, %d %b %Y %H:%M:%S %z")
        date_final = datetime.strftime(date_raw, "%d %B %Y - %H:%M")

        news_entry = config.TEMPLATES['news_feed'].format(
            title= feed.entries[n].title,
            description= feed.entries[n].description,
            date= date_final,
            link= feed.entries[n].link
        )

        news_feed += news_entry

    news_report = config.TEMPLATES['news_report'].format(
        news = news_feed
    )

    return news_report