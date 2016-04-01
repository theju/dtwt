from django.conf.urls import url

import trigger.views


urlpatterns = [
    url(r'^(?P<trigger_id>\d+)/render/$', trigger.views.render_trigger_params, name='render_trigger_params'),
]
