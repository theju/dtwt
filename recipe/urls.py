from django.conf.urls import url

import recipe.views


urlpatterns = [
    url(r'^add/$', recipe.views.recipe, name='add_recipe'),
    url(r'^user/$', recipe.views.view_user_recipes, name='view_user_recipes'),
    url(r'^edit/(?P<recipe_id>\d+)/$', recipe.views.recipe, name='edit_recipe'),
]
