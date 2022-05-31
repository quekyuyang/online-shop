from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
import os
from pathlib import Path
import shutil


@override_settings(MEDIA_ROOT='test_media/')
class AddProductViewTests(TestCase):
    def test_add_product(self):
        user = User.objects.create_user('user1', password='misoramen1')
        self.client.force_login(user)

        dirpath = Path(__file__).parent / 'test_images'
        images = []
        for path in list(dirpath.iterdir())[:5]:
            images.append(open(path, 'rb'))

        name = 'Product Name'
        quantity = 100
        price = 45.69
        i_primary_image = 0
        form_data = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'images': images,
            'i_primary_image': i_primary_image
        }
        response = self.client.post(reverse('add_product'), form_data)

        product = Product.objects.all()[0]
        self.assertEqual(product.name, name)
        self.assertEqual(product.quantity, quantity)
        self.assertEqual(product.price, price)
        self.assertEqual(len(product.productimage_set.all()), len(images))

        images[i_primary_image].seek(0)
        self.assertEqual(product.primary_image.image.read(), images[i_primary_image].read())

        product.primary_image.image.close()
        for image in images:
            image.close()
        shutil.rmtree('test_media/')
