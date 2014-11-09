from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import RecipeForm
from .models import Recipe
from django.contrib.auth.decorators import login_required
import json
from trigger.models import Trigger
from trigger import triggers
from action.models import Action
from action import actions
import collections

@login_required
def recipe(request, recipe_id=None):
    instance = None
    if recipe_id:
        try:
            instance = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            trigger = getattr(triggers, instance.trigger.klass)()
            trigger_validated, trigger_params = trigger.validate(request)
            if trigger_validated:
                instance.trigger_params = json.dumps(trigger_params)
            else:
                form.errors.update(trigger_params)
            action = getattr(actions, instance.action.klass)()
            action_validated, action_params = action.validate(request)
            if action_validated:
                instance.action_params = json.dumps(action_params)
            else:
                form.errors.update(action_params)
            if trigger_validated and action_validated:
                instance.user = request.user
                instance.save()
            else:
                return HttpResponse(json.dumps(form.errors),
                                    content_type="application/json",
                                    status=400)
    else:
        form = RecipeForm(instance=instance)
    channel_trigger_map = collections.defaultdict(list)
    channel_action_map = collections.defaultdict(list)
    for trigger in Trigger.objects.all():
        channel_trigger_map[trigger.channel.id].append({"id": trigger.id, "name": trigger.name})
    for action in Action.objects.all():
        channel_action_map[action.channel.id].append({"id": action.id, "name": action.name})
    ctxt = {
        "form": form,
        "channel_trigger_map": json.dumps(channel_trigger_map),
        "channel_action_map": json.dumps(channel_action_map),
        "recipe": instance
    }
    return render(request, "recipes/recipe.html", ctxt)


@login_required
def view_user_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    ctxt = {"recipes": recipes}
    return render(request, "recipes/recipes.html", ctxt)
