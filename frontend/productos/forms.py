from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    price = forms.FloatField(label='Price')
    description = forms.CharField(label='Description')
