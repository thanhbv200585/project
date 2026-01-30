import json, time, hashlib
import feedparser
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

RSS_URLS = {
    "vnexpress": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "bbc": "https://www.bbc.com/news/rss.xml"
}

def article_id(link):
    return hashlib.md5(link.encode()).hexdigest()

while True:
    for source, url in RSS_URLS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            event = {
                "schema_version": "v1",
                "event_type": "news_article",
                "article_id": article_id(entry.link),
                "title": entry.title,
                "summary": entry.get("summary", ""),
                "link": entry.link,
                "published_time": entry.get("published"),
                "source": source,
                "ingest_time": datetime.utcnow().isoformat()
            }

            producer.send(
                "news.raw",
                key=source,
                value=event
            )

    producer.flush()
    time.sleep(60)
