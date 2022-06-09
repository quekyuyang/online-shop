from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product


class ProductDetailsViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('user1', password='misoramen1')

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
