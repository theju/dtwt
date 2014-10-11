from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<action_id>\d+)/render/$', 'action.views.render_action_params', name='render_action_params'),
)
