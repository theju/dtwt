from django import forms

class FeedContainsForm(forms.Form):
    feed_url = forms.URLField()
    phrase = forms.CharField()


class DropboxFileUploadForm(forms.Form):
    _access_token = forms.CharField()
    folder_name = forms.CharField()
