import requests

class Action(object):
    def render(self, request):
        pass

    def validate(self, request):
        pass

    def action(self, recipe, **kwargs):
        pass

class SendHTTPRequest(Action):
    def render(self, request):
        pass

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
        pass

    def validate(self, request):
        pass

    def action(self, recipe, **kwargs):
        pass
