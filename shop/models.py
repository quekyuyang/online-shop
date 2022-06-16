from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError


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
                               related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name


def validate_rating(rating):
    if not 1 <= rating <= 5:
        raise ValidationError('Invalid rating')


class Review(models.Model):
    rating_choices = [
        (1, '&#9734;'),
        (2, '&#9734;'),
        (3, '&#9734;'),
        (4, '&#9734;'),
        (5, '&#9734;')
    ]

    content = models.CharField(max_length=2000)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating], choices=rating_choices, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
