from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recipe/', include('recipe.urls')),
    url(r'^trigger/', include('trigger.urls')),
    url(r'^action/', include('action.urls')),

    url(r'dropbox/oauth2/redirect/', 'accounts.views.dropbox_oauth2_redirect', name="dropbox_oauth2_redirect")
)
