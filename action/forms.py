from django import forms

class SendEmailForm(forms.Form):
    to_email = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField()
