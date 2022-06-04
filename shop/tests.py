from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, ProductImage
import os
from pathlib import Path
import shutil


@override_settings(MEDIA_ROOT='test_media/')
class AddProductViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        dirpath = Path(__file__).parent / 'test_images'
        cls.images = []
        for path in list(dirpath.iterdir()):
            cls.images.append(open(path, 'rb'))
        assert(len(cls.images) > 5)  # Need more than 5 images to run tests

    def setUp(self):
        user = User.objects.create_user('user1', password='misoramen1')
        self.client.force_login(user)

    def test_add_product(self):
        images = self.images[:5]
        form_data = dummy_product_form_data(images)
        response = self.client.post(reverse('add_product'), form_data)
        self.assertRedirects(response, reverse('homepage'))

        product = Product.objects.all()[0]
        self.assertEqual(product.name, form_data['name'])
        self.assertEqual(product.quantity, form_data['quantity'])
        self.assertEqual(product.price, form_data['price'])
        self.assertEqual(len(product.productimage_set.all()), len(images))

        i_primary_image = form_data['i_primary_image']
        self.images[i_primary_image].seek(0)
        self.assertEqual(product.primary_image.image.read(), images[i_primary_image].read())

        product.primary_image.image.close()
        shutil.rmtree('test_media/')

    def test_too_many_images(self):
        form_data = dummy_product_form_data(self.images)
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.templates[0].name, 'shop/add_product.html')
        self.assertEqual(len(Product.objects.all()), 0)

    def test_invalid_i_primary_images(self):
        form_data = dummy_product_form_data(self.images[:5])
        form_data['i_primary_image'] = 5
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.templates[0].name, 'shop/add_product.html')
        self.assertEqual(len(Product.objects.all()), 0)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        for image in cls.images:
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


class HomePageViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', password='misoramen1')

    def test_homepage(self):
        products = dummy_products(10)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.templates[0].name, 'shop/homepage.html')

        products_homepage = response.context['products'].order_by('id')
        self.assertQuerysetEqual(products_homepage, products)


class ProductDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', password='misoramen1')

    def test_product_details(self):
        product = dummy_products(1)[0]

        response = self.client.get(reverse('product_details', args=[product.id]))
        self.assertEqual(response.templates[0].name, 'shop/product_details.html')

        product_from_view = response.context['product']
        self.assertEqual(product, product_from_view)


def dummy_products(quantity):
    products = []
    for i in range(quantity):
        product = Product.objects.create(
            name=f'Product Name {i}',
            quantity=100,
            price=45.69,
            seller=User.objects.get(id=1),
        )
        products.append(product)
    return products


class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', password='misoramen1')

    def test_add_to_cart(self):
        product = dummy_products(1)[0]
        form_data = {
            'quantity': 10,
        }

        response = self.client.post(reverse('add_to_cart', args=[product.id]), form_data)
        self.assertRedirects(response, reverse('homepage'))

        session = self.client.session
        cart = session[settings.CART_SESSION_ID]
        entry = cart[str(product.id)]
        self.assertEqual(entry['name'], product.name)
        self.assertEqual(entry['quantity'], form_data['quantity'])
        self.assertEqual(entry['price'], product.price*form_data['quantity'])

    def test_remove_from_cart(self):
        product = dummy_products(1)[0]

        session = self.client.session
        cart = session[settings.CART_SESSION_ID] = {}
        cart[str(product.id)] = {
            'name': product.name,
            'quantity': 10,
            'price': 45.69,
        }
        session.save()
        
        response = self.client.post(reverse('remove_from_cart', args=[product.id]))
        session = self.client.session
        cart = session[settings.CART_SESSION_ID]
        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(cart, {})
