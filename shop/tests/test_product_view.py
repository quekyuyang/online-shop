from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product, Category
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
        self.category = Category.objects.create(name='Category')

    def test_add_product(self):
        images = self.images[:5]
        form_data = dummy_product_form_data(images)
        response = self.client.post(reverse('add_product'), form_data)
        self.assertRedirects(response, reverse('homepage'))

        product = Product.objects.all()[0]
        self.assertEqual(product.name, form_data['name'])
        self.assertEqual(product.quantity, form_data['quantity'])
        self.assertEqual(product.price, form_data['price'])
        self.assertQuerysetEqual(product.categories.all(), [self.category])
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

        form_data['i_primary_image'] = -1
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.templates[0].name, 'shop/add_product.html')
        self.assertEqual(len(Product.objects.all()), 0)

        del form_data['i_primary_image']
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
        'categories': ['1'],
        'images': images,
        'i_primary_image': 0
    }
    return form_data
