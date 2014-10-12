from django import forms

class SendEmailForm(forms.Form):
    to_email = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField()


class SendHTTPRequestForm(forms.Form):
    http_method = forms.ChoiceField(choices=(
        ("get", "GET"),
        ("post", "POST"),
        ("head", "HEAD"),
        ("put", "PUT"),
    ))
    http_data = forms.CharField()
    http_url = forms.URLField()
