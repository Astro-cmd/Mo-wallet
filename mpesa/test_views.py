# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from unittest.mock import patch
# from django.test import Client

# class MpesaViewsTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.payment_notification_url = reverse('mpesa_payment_notification')
#         self.initiate_transaction_url = reverse('initiate_mpesa_transaction')
#         self.lipa_url = reverse('lipa_na_mpesa_online')

#     def test_mpesa_payment_notification(self):
#         payload = {
#             "transaction_id": "12345",
#             "amount": 1000,
#             "phone_number": "254712345678"
#         }
#         response = self.client.post(self.payment_notification_url, payload, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("ResultCode", response.json())
#         self.assertEqual(response.json()["ResultCode"], 0)

#     def test_initiate_mpesa_transaction(self):
#         payload = {
#             "phone_number": "254712345678",
#             "amount": 500
#         }
#         response = self.client.post(self.initiate_transaction_url, payload, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("message", response.json())

#     @patch('requests.post')
#     @patch('requests.get')
#     def test_lipa_na_mpesa_online(self, mock_get, mock_post):
#         # Mock access token response
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = {"access_token": "test_token"}

#         # Mock STK push response
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = {
#             "MerchantRequestID": "29115-34620561-1",
#             "CheckoutRequestID": "ws_CO_191220231020438232",
#             "ResponseCode": "0",
#             "ResponseDescription": "Success. Request accepted for processing",
#             "CustomerMessage": "Success. Please enter your M-PESA PIN"
#         }

#         payload = {
#             "phone_number": "254712345678",
#             "amount": 1
#         }
#         response = self.client.post(self.lipa_url, payload, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("CustomerMessage", response.json())

# class SendMpesaPaymentViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('mpesa_send')

#     def test_send_mpesa_payment_get(self):
#         """Test GET request to send_mpesa_payment view"""
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mpesa_form.html')

#     def test_send_mpesa_payment_post_valid_data(self):
#         """Test POST request with valid data"""
#         data = {
#             'from_number': '254712345678',
#             'to_number': '254798765432',
#             'amount': '1000',
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Success')

#     def test_send_mpesa_payment_post_invalid_data(self):
#         """Test POST request with invalid data"""
#         data = {
#             'from_number': 'invalid_number',
#             'to_number': '254798765432',
#             'amount': '1000',
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Invalid phone number format.')