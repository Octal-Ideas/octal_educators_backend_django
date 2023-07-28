import requests
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer
from .access_token import generate_token
from .utils import timestamp_conversion
from .password_base64 import generate_password
from django.conf import settings

# Create your views here.
class TestView(APIView):
   
    def get(self, request, format=None):
        access_token = generate_token()
        current_timestamp = timestamp_conversion()
        decoded_password = generate_password(current_timestamp)
        return Response({"access_token" : access_token, "password" : decoded_password })

class Makepayment(APIView):
    def post(self, request, *args, **kwargs):
        requestData = request.data

        amount = requestData["amount"]
        phone = requestData["phone_number"]

        paymentResponseData =self.make_mpesa_payment_request(amount=amount, phone=phone)

        return Response(paymentResponseData)

    def make_mpesa_payment_request(self, amount : str, phone : str) -> dict:
        access_token = generate_token()
        current_timestamp = timestamp_conversion()
        decoded_password = generate_password(current_timestamp)

        headers = {"Authorization" : "Bearer %s" % access_token}

        request = {
            "BusinessShortCode": settings.BUSINESS_SHORT_CODE,    
            "Password": decoded_password,    
            "Timestamp":current_timestamp,    
            "TransactionType": settings.TRANSACTION_TYPE,    
            "Amount": amount,    
            "PartyA":phone,    
            "PartyB":settings.BUSINESS_SHORT_CODE,    
            "PhoneNumber":phone,    
            "CallBackURL":settings.CALL_BACK_URL,    
            "AccountReference":settings.ACCOUNT_REFERENCE,    
            "TransactionDesc":settings.TRANSACTION_DESCRIPTION
        }
      
        response = requests.post(settings.API_RESOURCE_URL, json=request, headers=headers)

        mystr =response.text
        obbstr =json.loads(mystr)

        merchant_request_id=obbstr['MerchantRequestID']
        checkout_request_id=obbstr['CheckoutRequestID']
        response_description=obbstr['ResponseDescription']
        response_code=obbstr['ResponseCode']

        data = {
            "merchant_request_id" : merchant_request_id,
            "checkout_request_id" : checkout_request_id,
            "response_description" : response_description,
            "response_code": response_code
        }

        return data