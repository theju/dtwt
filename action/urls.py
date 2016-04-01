from django.conf.urls import url

import action.views


urlpatterns = [
    url(r'^(?P<action_id>\d+)/render/$', action.views.render_action_params, name='render_action_params'),
]
