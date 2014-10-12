import requests
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, RequestContext, Context
from .forms import SendEmailForm, SendHTTPRequestForm

class Action(object):
    form_class = None
    template_name = None

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

    def action(self, recipe, **kwargs):
        raise NotImplementedError


class SendHTTPRequest(Action):
    template_name = "actions/send_http_request.html"
    form_class = SendHTTPRequestForm

    def action(self, recipe, **kwargs):
        http_fn = getattr(requests, kwargs["action"]["http_method"])
        nkwargs = {}
        if kwargs["action"]["http_method"] == "get":
            nkwargs["params"] = kwargs["action"].get("http_data", {})
        else:
            nkwargs["data"] = kwargs["action"].get("http_data", {})
        try:
            response = http_fn(kwargs["action"]["http_url"], **nkwargs)
        except requests.exceptions.RequestException:
            return False
        if not response.ok:
            return False
        return True


class SendEmail(Action):
    template_name = "actions/send_email.html"
    form_class = SendEmailForm

    def action(self, recipe, **kwargs):
        subject_template = kwargs["action"]["subject"]
        message_template = kwargs["action"]["message"]
        subject = Template(subject_template).render(Context(kwargs))
        message = Template(message_template).render(Context(kwargs))
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  kwargs["action"]["to_email"].split(","))
        return True
