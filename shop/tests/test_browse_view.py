from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product, Category


class HomePageViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('user1', password='misoramen1')

    def test_homepage(self):
        products = dummy_products(10)

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.templates[0].name, 'shop/browse.html')

        products_homepage = response.context['products'].order_by('id')
        self.assertQuerysetEqual(products_homepage, products)


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


class BrowseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', password='misoramen1')

    def test_browse_category(self):
        category_parent = Category.objects.create(name='Computer Component')
        category_gpu = Category.objects.create(name='GPU', parent=category_parent)
        category_ssd = Category.objects.create(name='SSD', parent=category_parent)
        category_psu = Category.objects.create(name='Power Supply', parent=category_parent)

        product_gpu1 = Product.objects.create(name='GPU1', quantity=10, price=999, seller=self.user)
        product_gpu1.categories.set([category_gpu])

        product_gpu2 = Product.objects.create(name='GPU2', quantity=10, price=999, seller=self.user)
        product_gpu2.categories.set([category_gpu])

        product_ssd1 = Product.objects.create(name='SSD1', quantity=10, price=200, seller=self.user)
        product_ssd1.categories.set([category_ssd])

        product_psu1 = Product.objects.create(name='Power Supply 1', quantity=10, price=100, seller=self.user)
        product_psu1.categories.set([category_psu])

        response = self.client.get(reverse('browse', args=['GPU']))
        self.assertEqual(response.context['current_category'], category_gpu)
        self.assertCountEqual(response.context['sibling_categories'],
                              [category_ssd, category_psu])
        self.assertCountEqual(response.context['child_categories'],[])
        self.assertEqual(response.context['parent_category'], category_parent)
        self.assertCountEqual(response.context['products'],
                              [product_gpu1, product_gpu2])

        response = self.client.get(reverse('browse', args=['SSD']))
        self.assertCountEqual(response.context['products'], [product_ssd1])

        response = self.client.get(reverse('browse', args=['Computer Component']))
        self.assertEqual(response.context['current_category'], category_parent)
        self.assertCountEqual(response.context['sibling_categories'],
                              [])
        self.assertCountEqual(response.context['child_categories'],
                              [category_gpu, category_ssd, category_psu])
        self.assertEqual(response.context['parent_category'], None)
        self.assertCountEqual(response.context['products'],
                              [product_gpu1, product_gpu2, product_ssd1, product_psu1])

    def test_multi_category(self):
        category1 = Category.objects.create(name='Fantasy')
        category2 = Category.objects.create(name='Romance')
        product = Product.objects.create(name='book', quantity=10, price=10, seller=self.user)
        product.categories.set([category1, category2])

        response = self.client.get(reverse('browse', args=['Fantasy']))
        self.assertQuerysetEqual(response.context['products'], [product])

        response = self.client.get(reverse('browse', args=['Romance']))
        self.assertQuerysetEqual(response.context['products'], [product])
