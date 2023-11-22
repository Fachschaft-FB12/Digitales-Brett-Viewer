from tkinter import W
import feedparser
from datetime import datetime,timedelta
from time import mktime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
xml = feedparser.parse(os.environ.get("RSS_URL"))
relevantPosts = []

for post in xml.entries:
    datePost = datetime.fromtimestamp(mktime(post.published_parsed))
    twenyFourHoursBack = datetime.today() - timedelta(days=1)
    if(twenyFourHoursBack.date() == datePost.date()):
        description = "[" + post.title + "]" + "(<" + post.link + ">)\n"
        description += post.summary + "\n\n"
        relevantPosts.append(description)

if(len(relevantPosts) > 0):
    if(len(relevantPosts) > 1):
        message = "**Auf dem Digitalen-Brett wurden " + str(len(relevantPosts)) + " neue Artikel veröffentlicht**:\n\n"
    else:
        message = "**Auf dem Digitalen-Brett wurde 1 neuer Artikel veröffentlicht**:\n\n"

    listOfRequests = []
    for post in relevantPosts:
        if(len(message) + len(post) > 2000):
            listOfRequests.append(message)
            message = ""
        message += post

    listOfRequests.append(message)

    for request in listOfRequests:
        requests.post(os.environ.get("DISCORD_URL"), json={ "content" : request })


