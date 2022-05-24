from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']
        widgets = {'name': forms.Textarea(attrs={'cols':80, 'rows':1})}


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
