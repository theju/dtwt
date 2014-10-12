from django import forms

class FeedContainsForm(forms.Form):
    feed_url = forms.URLField()
    phrase = forms.CharField()
