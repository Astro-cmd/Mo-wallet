import base64
import logging
from django.shortcuts import render
import requests
from django.conf import settings
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import MpesaTransaction

# Logging setup
logger = logging.getLogger(__name__)

# Get access token
def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=(consumer_key, consumer_secret))
        response.raise_for_status()
        access_token = response.json().get("access_token")
        logger.debug(f"Access token acquired: {access_token}")
        return access_token
    except Exception as e:
        logger.error(f"Failed to get access token: {str(e)}")
        return None

@csrf_exempt
@api_view(["POST"])
def lipa_na_mpesa_online(request):
    try:
        access_token = get_access_token()
        if not access_token:
            return JsonResponse({"error": "Could not get access token"}, status=500)

        data = request.data
        phone_number = data.get("phone_number")
        amount = int(data.get("amount"))

        timestamp = now().strftime("%Y%m%d%H%M%S")
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/api/mpesa/callback/",
            "AccountReference": "Mo-Wallet",
            "TransactionDesc": "Mo-Wallet Payment",
        }

        mpesa_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(mpesa_url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            logger.info(f"STK Push Request Sent Successfully: {response_data}")
            return JsonResponse(response_data)
        else:
            logger.warning(f"STK Push Failed: {response_data}")
            return JsonResponse({"error": response_data}, status=400)

    except Exception as e:
        logger.error(f"Error in Lipa Na M-Pesa: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@api_view(["POST"])
def mpesa_payment_notification(request):
    try:
        data = request.data
        logger.info(f"Payment notification received: {data}")
        transaction_id = data.get("transaction_id") or f"TXN{now().strftime('%Y%m%d%H%M%S')}"
        amount = data.get("amount") or 0
        phone_number = data.get("phone_number") or "Unknown"
        MpesaTransaction.objects.create(transaction_id=transaction_id, amount=amount, phone_number=phone_number)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"}, status=200)
    except Exception as e:
        logger.error(f"Error processing payment notification: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@api_view(["POST"])
def initiate_mpesa_transaction(request):
    try:
        data = request.data
        phone_number = data.get("phone_number")
        amount = data.get("amount")
        logger.info(f"Initiating transaction for {phone_number} with amount {amount}")
        # Add logic to initiate the transaction here
        return JsonResponse({"message": "Transaction initiated successfully."}, status=200)
    except Exception as e:
        logger.error(f"Error initiating transaction: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient

class MpesaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lipa_url = reverse('lipa_na_mpesa_online')
        self.callback_url = reverse('mpesa_callback')

    @patch('requests.post')
    @patch('requests.get')
    def test_stk_push_initiation(self, mock_get, mock_post):
        # Mock access token response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"access_token": "test_token"}

        # Mock STK push response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "MerchantRequestID": "29115-34620561-1",
            "CheckoutRequestID": "ws_CO_191220231020438232",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Please enter your M-PESA PIN"
        }

        payload = {
            "phone_number": "254712345678",
            "amount": 1
        }
        response = self.client.post(self.lipa_url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("CustomerMessage", response.json())
 

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import base64
from django.utils.timezone import now

def normalize_phone_number(number):
    number = number.strip().replace(" ", "")
    if number.startswith("07") or number.startswith("01"):
        return "254" + number[1:]
    elif number.startswith("+254"):
        return number[1:]
    elif number.startswith("254") and len(number) == 12:
        return number
    else:
        return None  # Invalid number

@csrf_exempt
def send_mpesa_payment(request):
    context = {}
    if request.method == "POST":
        from_number = normalize_phone_number(request.POST.get("from_number", ""))
        to_number = normalize_phone_number(request.POST.get("to_number", ""))
        amount = request.POST.get("amount")

        if not from_number or not to_number:
            context['message'] = "Invalid phone number format."
            context['status'] = "error"
            return render(request, "mpesa_form.html", context)

        # Get access token
        token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        token_response = requests.get(token_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
        access_token = token_response.json().get("access_token")

        # Generate password
        timestamp = now().strftime("%Y%m%d%H%M%S")
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        # STK push request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": from_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": from_number,
            "CallBackURL": "https://yourdomain.com/api/mpesa/callback/",
            "AccountReference": "Mo-Wallet",
            "TransactionDesc": f"Transfer to {to_number}",
        }

        response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", headers=headers, json=payload)
        result = response.json()

        if response.status_code == 200:
            context['message'] = result.get("CustomerMessage", "Success. Enter M-Pesa PIN")
            context['status'] = "success"
        else:
            context['message'] = result.get("errorMessage", "Transaction failed.")
            context['status'] = "error"

    return render(request, "mpesa_form.html", context)

