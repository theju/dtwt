import requests
import feedparser
from dateutil import parser
import time
import datetime
from django.shortcuts import render
from .forms import FeedContainsForm
from django.template import RequestContext

class Trigger(object):
    template_name = None
    form_class = None

    def __init__(self, *args, **kwargs):
        self.form = self.form_class()

    def render(self, request):
        return render(request, self.template_name,
                      context_instance=RequestContext(request, {"form": self.form}))

    def validate(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return (True, form.cleaned_data)
        return (False, form.errors)

    def trigger(self, recipe, **kwargs):
        raise NotImplementedError


class DropboxFileUpload(Trigger):
    def validate(self, request):
        pass

    def trigger(self, recipe, **kwargs):
        pass


class FeedContains(Trigger):
    template_name = "triggers/feed_contains.html"
    form_class = FeedContainsForm

    def trigger(self, recipe, **kwargs):
        feed_url = kwargs["trigger"]["feed_url"]
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
                if kwargs["trigger"].get("phrase"):
                    if kwargs["trigger"]["phrase"] in feed.description:
                        return True
    
