import requests

def send_http_request(recipe, **kwargs):
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

def send_email(recipe, **kwargs):
    pass
