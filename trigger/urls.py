from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<trigger_id>\d+)/render/$', 'trigger.views.render_trigger_params', name='render_trigger_params'),
)
