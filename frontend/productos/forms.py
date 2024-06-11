from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
