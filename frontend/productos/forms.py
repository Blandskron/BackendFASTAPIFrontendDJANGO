from django import forms

class ProductForm(forms.Form):
    id = forms.IntegerField(label='ID')
    name = forms.CharField(label='Name', max_length=100)
    price = forms.FloatField(label='Price')
