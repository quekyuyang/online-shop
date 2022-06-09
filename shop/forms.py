from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    i_primary_image = forms.IntegerField()

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price', 'categories']
        widgets = {'name': forms.Textarea(attrs={'cols':80, 'rows':1})}

    def clean_i_primary_image(self):
        i_primary_image = self.cleaned_data.get('i_primary_image')
        if i_primary_image < 0:
            raise ValidationError('Invalid primary image index')
        return i_primary_image

    def clean(self):
        cleaned_data = super().clean()
        if len(self.files.getlist('images')) > 5:
            raise ValidationError('You can only upload up to 5 images')

        i_primary_image = cleaned_data.get('i_primary_image')
        if i_primary_image and i_primary_image > len(self.files.getlist('images')) - 1:
            raise ValidationError('Primary image index exceeding number of images')


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
