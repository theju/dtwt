import requests
import feedparser
from dateutil import parser
import time
import datetime
import requests
import json
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from .forms import FeedContainsForm, DropboxFileUploadForm
from recipe.models import Recipe

from dropbox.client import DropboxOAuth2Flow, DropboxClient

class Trigger(object):
    template_name = None
    form_class = None

    def __init__(self, *args, **kwargs):
        self.form = self.form_class() if self.form_class else None

    def render(self, request, **kwargs):
        context = {"form": self.form}
        if kwargs.get("recipe"):
            recipe = kwargs["recipe"]
            recipe.trigger_params = json.loads(recipe.trigger_params)
            context["recipe"] = recipe
        return render(request, self.template_name, context)

    def validate(self, request):
        if not self.form_class:
            return (True, {})
        form = self.form_class(request.POST)
        if form.is_valid():
            return (True, form.cleaned_data)
        return (False, form.errors)

    def trigger(self, recipe, **kwargs):
        raise NotImplementedError


class DropboxFileUpload(Trigger):
    template_name = "triggers/dropbox_file_upload.html"
    form_class = DropboxFileUploadForm

    def render(self, request, **kwargs):
        recipe = kwargs.get("recipe")
        if not recipe:
            redirect_uri = "{0}://{1}{2}".format("https" if request.is_secure() else "http",
                                                 RequestSite(request).domain,
                                                 reverse("dropbox_oauth2_redirect"))
            csrf_key = "dropbox-auth-csrf-token"
            session_dict = {}
            authorize_url = DropboxOAuth2Flow(settings.DROPBOX_APP_KEY,
                                              settings.DROPBOX_APP_SECRET,
                                              redirect_uri,
                                              session_dict, csrf_key).start()
            request.session[csrf_key] = str(session_dict[csrf_key])
            dropbox_access_token = request.session.get("dropbox_access_token")
            folder_name = ""
        else:
            trigger_params = json.loads(recipe.trigger_params)
            dropbox_access_token = trigger_params["_access_token"]
            authorize_url = None
            folder_name = trigger_params["folder_name"]
        context = {"form": self.form,
                   "redirect_url": authorize_url,
                   "dropbox_access_token": dropbox_access_token,
                   "folder_name": folder_name}
        return render(request, self.template_name, context)
        
    def trigger(self, recipe, **kwargs):
        url = ("https://api.dropbox.com/1/metadata/auto/"
               "{0}?access_token={1}").format(kwargs["trigger"]["folder_name"],
                                              kwargs["trigger"]["_access_token"])
        if kwargs["trigger"].get("hash"):
            url += "&hash={0}".format(kwargs["trigger"]["hash"])
        response = requests.get(url)
        if not response.ok:
            return (False, ())
        if response.status_code == 304:
            return (False, ())
        kwargs["trigger"]["response"] = response.json()
        instance = Recipe.objects.get(id=recipe["id"])
        trigger_params = json.loads(instance.trigger_params)
        trigger_params["hash"] = response.json()["hash"]
        instance.trigger_params = json.dumps(trigger_params)
        instance.save()
        return (True, kwargs["trigger"])


class FeedContains(Trigger):
    template_name = "triggers/feed_contains.html"
    form_class = FeedContainsForm

    def trigger(self, recipe, **kwargs):
        feed_url = kwargs["trigger"]["feed_url"]
        try:
            response = requests.get(feed_url)
        except requests.exceptions.RequestError:
            return (False, ())
        parsed_feed = feedparser.parse(response.content.lower())
        if not len(parsed_feed['entries']):
            return (False, ())
        matched_feeds = []
        for feed in parsed_feed.entries:
            pub_date = parser.parse(feed.published)
            if pub_date > recipe["last_checked"]:
                if kwargs["trigger"].get("phrase"):
                    if kwargs["trigger"]["phrase"] in feed.description:
                        matched_feeds.append(feed)
        if matched_feeds:
            kwargs["trigger"]["matched_entries"] = matched_feeds
            return (True, kwargs["trigger"])
        return (False, ())
