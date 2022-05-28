from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']
        widgets = {'name': forms.Textarea(attrs={'cols':80, 'rows':1})}

    def clean(self):
        cleaned_data = super().clean()
        if len(self.files.getlist('images')) > 5:
            raise ValidationError('You can only upload up to 5 images')


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
