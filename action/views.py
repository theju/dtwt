from django.shortcuts import render
from django.http import HttpResponse
from .models import Action
from django.contrib.auth.decorators import login_required
from action import actions

@login_required
def render_action_params(request, action_id=None):
    try:
        action = Action.objects.get(id=action_id)
    except Action.DoesNotExist:
        return render(request, "action/action_not_found.html")
    action_klass = getattr(actions, action.klass)
    action_obj = action_klass()
    template_content = action_obj.render(request)
    return template_content
