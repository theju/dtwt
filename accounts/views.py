from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from dropbox.client import DropboxOAuth2Flow, DropboxClient
from django.conf import settings
from django.contrib.sites.requests import RequestSite
from django.core.urlresolvers import reverse


def dropbox_oauth2_redirect(request):
    redirect_uri = "{0}://{1}{2}".format("https" if request.is_secure() else "http",
                                         RequestSite(request).domain,
                                         reverse("dropbox_oauth2_redirect"))
    csrf_key = "dropbox-auth-csrf-token"
    try:
        access_token, user_id, url_state = DropboxOAuth2Flow(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, redirect_uri,
                                                             request.session, csrf_key).finish(request.GET)
    except DropboxOAuth2Flow.BadRequestException:
        return HttpResponseBadRequest("Bad Request")
    except DropboxOAuth2Flow.BadStateException:
        return HttpResponseBadRequest("Bad Response")
    except DropboxOAuth2Flow.CsrfException:
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException:
        return HttpResponseBadRequest("Not approved")
    except DropboxOAuth2Flow.ProviderException:
        return HttpResponseForbidden()
    request.session["dropbox_access_token"] = access_token
    return HttpResponseRedirect(reverse("add_recipe"))
