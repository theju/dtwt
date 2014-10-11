from django.shortcuts import render
from django.http import HttpResponse
from .models import Trigger
from django.contrib.auth.decorators import login_required
from trigger import triggers

@login_required
def render_trigger_params(request, trigger_id=None):
    try:
        trigger = Trigger.objects.get(id=trigger_id)
    except Trigger.DoesNotExist:
        return render(request, "trigger/trigger_not_found.html")
    trigger_klass = getattr(triggers, trigger.klass)
    trigger_obj = trigger_klass()
    template_content = trigger_obj.render(request)
    return template_content
