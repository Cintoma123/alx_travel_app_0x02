from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Payment
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
import requests
import uuid

@method_decorator(csrf_exempt, name="dispatch")
class InitializePaymentView(APIView):
    permission_classes = [AllowAny]

    def initiate_payment(self, request):
        # Get request data for making payment
        amount = request.data.get('amount')
        booking_reference = request.data.get('booking_reference')
        # Print out the output
        print(amount, request.user.email, booking_reference)
        if not booking_reference or not amount:
            return Response({"error": "amount and booking reference are required."}, status=status.HTTP_400_BAD_REQUEST)
        # Payment data
        payment_data = {
            "tx_ref": str(uuid.uuid4()),
            "amount": amount,
            "currency": "USD",
            "email": request.user.email,
            "phone_number": getattr(request.user.profile, 'phone_number', ''),  # Assuming you have a profile model with phone number
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "callback_url": settings.CHAPA_CALLBACK_URL,
        }
        try:
            # Send a request to Chapa to initiate payment
            response = requests.post(
                url=settings.CHAPA_INITIALIZE_URL,
                headers = {
                    "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
                    "Content-Type": 'application/json'
                },
            json=payment_data
            )
            if response.status_code == 200:
                response_data = response.json()
                print("response data:", response_data)
                check_out_url = response_data.get("data", {}).get("checkout_url")
                transaction_reference = response_data.get("data", {}).get("tx_ref")
                Payment.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_id=response_data.get("data", {}).get("transaction_id", str(uuid.uuid4())),
                    tx_ref=transaction_reference,
                    booking_reference=booking_reference,
                    payment_status='pending',
                    chapa_response=response_data
                )
                print(check_out_url)
                return Response({"checkout_url": check_out_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to initialize payment.", "details": response.text}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "A network error occurred.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def verify_payment(self, request, transaction_reference):
        # Verify payment
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }
        url = f"https://api.chapa.co/v1/transaction/verify/{transaction_reference}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success' and data.get('data', {}).get('status') == 'success':
                    payment = Payment.objects.filter(tx_ref=transaction_reference).first()
                    if payment:
                        payment.payment_status = 'successful'
                        payment.save()
                    return Response({'message': 'Payment verified successfully', 'data': data}, status=status.HTTP_200_OK)
                else:
                    payment = Payment.objects.filter(tx_ref=transaction_reference).first()
                    if payment:
                        payment.payment_status = 'failed'
                        payment.save()
                    return Response({'message': 'Payment verification failed', 'data': data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Failed to connect to Chapa API', 'details': response.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({"error": "A network error occurred.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# Create your views here.
