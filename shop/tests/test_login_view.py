from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        form = response.context['form']
        self.assertEqual(response.templates[0].name, 'shop/login.html')
        self.assertEqual(len(form.data), 0)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        user = User.objects.create_user('user1', password='misoramen1')
        form_data = {
            'username': 'user1',
            'password': 'misoramen1'
        }

        response = self.client.post(reverse('login'), form_data)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, user)
