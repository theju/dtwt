from django.shortcuts import render
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

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
    return render(request, "recipes/add.html", {"form": form})
