from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Payment
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.crf import csrf_protect , csrf_exempt
import requests
import uuid 
@method_decorator(csrf_exempt , name ="dispatch")
 class InitializePaymentView(APIView):
    # creating my views for my payment integration 
    permission_classes = [permissions.IsAuthenticated]
    def post (self ,request):
        amount = request.data.get('amount')
        email = request.data.get('email')
        booking_reference = request.data.get('booking_reference')
        print(amount , email ,booking_reference)
        if not booking_reference or not amount:
            return Response({"error": "amount and booking reference are required."}, status=status.HTTP_400_BAD_REQUEST)
        payment_data{
            "tx_ref": str(uuid.uuid4()),
            "amount": amount,
            "currency": "USD",
            "email": request.user.email,
            "phone_number": request.user.profile.phone_number,  # Assuming you have a profile model with phone number
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "callback_url": settings.CHAPA_CALLBACK_URL,
        }
    try:
        response = requests.post{
            headers = {
                "authorization": f"brearer{settings.CHAPA_SECRET_KEY}
                "content-type": 'application/json'
            }
        }
        Payment.objects.create(
            user=request.user,
            amount=amount,
            transaction_id=str(uuid.uuid4()),
            tx_ref=str(uuid.uuid4()),
            booking_reference=booking_reference
            transaction_id = chapa_response.get('transaction_id', ''),
            payment_status='pending',
            chapa_response=chapa_response
        )



# Create your views here.
