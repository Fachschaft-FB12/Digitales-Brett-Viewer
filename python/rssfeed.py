import feedparser
from datetime import datetime,timedelta
from time import mktime
import re
import requests

xml = feedparser.parse("https://brett.fs-matheinfo.de/feed.xml")

embeds = []

for post in xml.entries:
    dt = datetime.fromtimestamp(mktime(post.published_parsed))
    last_hour_date_time = datetime.now() - timedelta(hours = 24)
    if(last_hour_date_time < dt):
        cleantext = re.sub('<[^<]+?>', '', post.description).strip()[:200] + "..."
        embeds.append({
            "title": post.title,
            "description": cleantext,
            "url": post.link,
            "color": 15258703
        })

if(len(embeds) > 0):
    response = requests.post("https://discord.com/api/webhooks/",
            json={
                "content" : "**Auf dem Digitalen-Brett wurden " + len(embeds) + " neue Artikel veröffentlicht**:",
                "embeds": embeds
            })