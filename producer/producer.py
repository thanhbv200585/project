import json
import time
import feedparser
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

rss_url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

while True:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:5]:
        msg = {
            "title": entry.title,
            "summary": entry.summary,
            "published": entry.published
        }
        producer.send("news-topic", msg)
        print("Sent:", msg["title"])
        time.sleep(2)

    time.sleep(30)
