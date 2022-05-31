from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
import os
from pathlib import Path
import shutil


@override_settings(MEDIA_ROOT='test_media/')
class AddProductViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('user1', password='misoramen1')
        self.client.force_login(user)

    def test_add_product(self):
        dirpath = Path(__file__).parent / 'test_images'
        images = []
        for path in list(dirpath.iterdir())[:5]:
            images.append(open(path, 'rb'))

        form_data = dummy_product_form_data(images)
        response = self.client.post(reverse('add_product'), form_data)

        product = Product.objects.all()[0]
        self.assertEqual(product.name, form_data['name'])
        self.assertEqual(product.quantity, form_data['quantity'])
        self.assertEqual(product.price, form_data['price'])
        self.assertEqual(len(product.productimage_set.all()), len(images))

        i_primary_image = form_data['i_primary_image']
        images[i_primary_image].seek(0)
        self.assertEqual(product.primary_image.image.read(), images[i_primary_image].read())

        product.primary_image.image.close()
        for image in images:
            image.close()
        shutil.rmtree('test_media/')

    def test_too_many_images(self):
        dirpath = Path(__file__).parent / 'test_images'
        images = []
        image_paths = list(dirpath.iterdir())
        self.assertGreater(len(image_paths), 5)
        for path in image_paths:
            images.append(open(path, 'rb'))

        form_data = dummy_product_form_data(images)
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.templates[0].name, 'shop/add_product.html')
        self.assertEqual(len(Product.objects.all()), 0)

        for image in images:
            image.close()


def dummy_product_form_data(images):
    form_data = {
        'name': 'Product Name',
        'quantity': 100,
        'price': 45.69,
        'images': images,
        'i_primary_image': 0
    }
    return form_data
