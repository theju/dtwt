import requests
import feedparser
from dateutil import parser
import time
import datetime

def http_ping(recipe, **kwargs):
    pass

def dropbox_file_upload(recipe, **kwargs):
    pass

def feed_contains(recipe, **kwargs):
    feed_url = kwargs["feed_url"]
    try:
        response = requests.get(feed_url)
    except requests.exceptions.RequestError:
        return None
    parsed_feed = feedparser.parse(response.content)
    if not len(parsed_feed['entries']):
        return None
    for feed in parsed_feed.entries:
        pub_date = parser.parse(feed.published)
        if pub_date > recipe["last_checked"]:
            if kwargs.get("phrase"):
                if kwargs["phrase"] not in feed.description:
                    return None
            return True
    
