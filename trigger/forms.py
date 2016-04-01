from django import forms


class FeedContainsForm(forms.Form):
    feed_url = forms.URLField()
    phrase = forms.CharField()


class DropboxFileUploadForm(forms.Form):
    _access_token = forms.CharField(widget=forms.HiddenInput())
    folder_name = forms.CharField()
