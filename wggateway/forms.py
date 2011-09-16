from django import forms
from models import Product

class ContactForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField()
    email = forms.EmailField(required=False)

class ClientSearchForm(forms.Form):
    client_code = forms.CharField(required=False)
    #commented because it doesn't make much sense since a client can be a sipp with no name field
    #name = forms.CharField(required=False)
    post_code = forms.CharField(required=False)
    email = forms.CharField(required=False)

#class ProductForm(forms.ModelForm):
    #class Meta:
        #model = Product
