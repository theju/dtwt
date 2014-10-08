import requests
import feedparser
from dateutil import parser
import time
import datetime

class Trigger(object):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def trigger(self, recipe, **kwargs):
        pass

class HTTPPing(Trigger):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def trigger(self, recipe, **kwargs):
        pass

class DropboxFileUpload(Trigger):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def trigger(self, recipe, **kwargs):
        pass

class FeedContains(Trigger):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def trigger(self, recipe, **kwargs):
        feed_url = kwargs["feed_url"]
        try:
            response = requests.get(feed_url)
        except requests.exceptions.RequestError:
            return False
        parsed_feed = feedparser.parse(response.content.lower())
        if not len(parsed_feed['entries']):
            return False
        for feed in parsed_feed.entries:
            pub_date = parser.parse(feed.published)
            if pub_date > recipe["last_checked"]:
                if kwargs.get("phrase"):
                    if kwargs["phrase"] in feed.description:
                        return True
    
