from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    primary_image = models.ForeignKey('ProductImage', on_delete=models.SET_NULL,
                                      related_name='+', null=True, blank=True)
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'product_id':self.id})


def get_product_dir(image, filename):
    return f'{image.product.id}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_product_dir, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return self.name
