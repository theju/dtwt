from django import forms
from .models import Recipe
from channel.models import Channel


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['trigger_channel'].initial = self.instance.trigger.channel
            self.fields['action_channel'].initial = self.instance.action.channel

    trigger_channel = forms.ModelChoiceField(queryset=Channel.objects.all())
    action_channel = forms.ModelChoiceField(queryset=Channel.objects.all())

    class Meta:
        model = Recipe
        fields = ('trigger', 'action')

