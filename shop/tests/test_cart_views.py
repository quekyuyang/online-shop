from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product


class CartTest(TestCase):
    def setUp(self):
        User.objects.create_user('user1', password='misoramen1')

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
