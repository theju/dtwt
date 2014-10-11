from django.shortcuts import render
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
import json
from trigger.models import Trigger
from action.models import Action
import collections

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
    else:
        form = RecipeForm()
    channel_trigger_map = collections.defaultdict(list)
    channel_action_map = collections.defaultdict(list)
    for trigger in Trigger.objects.all():
        channel_trigger_map[trigger.channel.id].append({"id": trigger.id, "name": trigger.name})
    for action in Action.objects.all():
        channel_action_map[action.channel.id].append({"id": action.id, "name": action.name})
    ctxt = {
        "form": form,
        "channel_trigger_map": json.dumps(channel_trigger_map),
        "channel_action_map": json.dumps(channel_action_map)
    }
    return render(request, "recipes/add.html", ctxt)
