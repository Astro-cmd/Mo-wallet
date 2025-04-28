from django.test import TestCase, Client
from django.urls import reverse
from .models import MpesaTransaction

class MpesaTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.payment_notification_url = reverse('mpesa_payment_notification')
        self.initiate_transaction_url = reverse('initiate_mpesa_transaction')

    def test_payment_notification_success(self):
        payload = {
            "transaction_id": "TEST12345",
            "amount": 1000,
            "phone_number": "254712345678"
        }
        response = self.client.post(reverse('mpesa_payment_notification'), payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MpesaTransaction.objects.filter(transaction_id="TEST12345").exists())

    def test_initiate_transaction(self):
        response = self.client.post(self.initiate_transaction_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Transaction initiated successfully.")
