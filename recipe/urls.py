from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^add/$', 'recipe.views.add_recipe', name='add_recipe'),
)
