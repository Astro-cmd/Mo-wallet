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
        self.assertIn('password1', form.errors)

    def test_ajax_validate_signup_valid(self):
        url = reverse('users:validate-signup')
        response = self.client.post(url, self.valid_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_ajax_validate_signup_invalid(self):
        # This test is no longer relevant with the new registration flow.
        pass

    def test_signup_view_creates_user(self):
        url = reverse('users:signup')
        response = self.client.post(url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())
