from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
    email = forms.EmailField(required=False)
