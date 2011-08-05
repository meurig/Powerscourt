from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
    email = forms.EmailField(required=False)

class ClientSearchForm(forms.Form):
    client_code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    post_code = forms.CharField(required=False)
    email = forms.CharField(required=False)