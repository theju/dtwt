import requests
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context

class Action(object):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def action(self, recipe, **kwargs):
        pass

class SendHTTPRequest(Action):
    def render(self, request):
        return render(request, "actions/send_http_request.html")

    def validate(self, request):
        pass

    def action(self, recipe, **kwargs):
        http_fn = getattr(requests, kwargs["http_method"])
        nkwargs = {}
        if kwargs["http_method"] == "get":
            nkwargs["params"] = kwargs.get("http_data", {})
        else:
            nkwargs["data"] = kwargs.get("http_data", {})
        try:
            response = http_fn(kwargs["http_url"], **nkwargs)
        except requests.exceptions.RequestException:
            return False
        if not response.ok:
            return False
        return True

class SendEmail(Action):
    def render(self, request):
        return render(request, "actions/send_email.html")

    def validate(self, request):
        pass

    def action(self, recipe, **kwargs):
        subject_template = kwargs["action"]["subject"]
        message_template = kwargs["action"]["message"]
        subject = Template(subject_template).render(Context(kwargs))
        message = Template(message_template).render(Context(kwargs))
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  kwargs["action"]["to_email"].split(","))
        return True
