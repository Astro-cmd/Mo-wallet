from django.test import TestCase, Client
from django.urls import reverse
from .forms import SignupForm
from .models import User

class SignupTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '0712345678',
            'password1': 'Test@1234',
            'password2': 'Test@1234',
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalid',
            'phone_number': '123',
            'password1': 'short',
            'password2': 'short',
        }
        self.client = Client()

    def test_signup_form_valid(self):
        form = SignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form = SignupForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('phone_number', form.errors)
        self.assertIn('password2', form.errors)
        self.assertIn('username', form.errors)

    def test_signup_view_creates_user(self):
        url = reverse('users:signup')
        response = self.client.post(url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        # Create user first
        User.objects.create_user(username='testlogin', email='testlogin@example.com', phone_number='0712345678', password='Test@1234')
        url = reverse('users:login')
        response = self.client.post(url, {'username': 'testlogin', 'password': 'Test@1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_view(self):
        # Create and login user
        user = User.objects.create_user(username='testlogout', email='testlogout@example.com', phone_number='0712345678', password='Test@1234')
        self.client.login(username='testlogout', password='Test@1234')
        url = reverse('users:logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
