from django import forms
from .models import Recipe
from channel.models import Channel

class RecipeForm(forms.ModelForm):
    trigger_channel = forms.ModelChoiceField(queryset=Channel.objects.all())
    action_channel = forms.ModelChoiceField(queryset=Channel.objects.all())

    class Meta:
        model = Recipe
        fields = ('trigger', 'action')

