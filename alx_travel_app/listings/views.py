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
    # creation of view to initate payment
    def initate_payment(self ,request):
        # getting of requests for data for making payment
        amount = request.data.get('amount')
        email = request.data.get('email')
        booking_reference = request.data.get('booking_reference')
        # printing out the output
        print(amount , email ,booking_reference)
        if not booking_reference or not amount:
            # returning the response 
            return Response({"error": "amount and booking reference are required."}, status=status.HTTP_400_BAD_REQUEST)
            # my payment data 
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
        # sending a response to chapa showing my initation for payment 
        response = requests.post(
            headers = {
                "authorization": f"brearer{settings.CHAPA_SECRET_KEY}
                "content-type": 'application/json'
            },
        
            url=settings.CHAPA_INITIALIZE_URL,
            json=payment_data
        )
        if response.status_code == 200 
        response_data = response.json()
        print("response data":response_data)
        check_out_url = response_data.get("check_out_url")
        transaction_reference = reponse_data.get("transaction_reference")
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
        print(check_out_url)
        return jsonresponse(check_out_url)
     return Response({"checkout_url": check_out_url}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to initialize payment.", "details": response.text}, status=response.status_code)
    except requests.exceptions.RequestException as e:
          return Response({"error": "A network error occurred.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def verify_payment(self , request , transaction_reference , *args **kwargs):
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
          }
        url = f"https://api.chapa.co/v1/transaction/verify/{transaction_reference}"
        response = requests.get(url, headers=headers)

      if response.status_code == 200:
         data = response.json()
         if data.get('status') == 'success' and data.get('data', {}).get('status') == 'success':
            payment.payment_status == 'sucessfully'
            payment.save()
                # Payment is successfully verified
              return Response({'message': 'Payment verified successfully', 'data': data}, status=status.HTTP_200_OK)
            else:
               payment = Payment.object.get(txt_ref = transaction_reference) 
               # payment is not suceesfully 
               payment.payment_status == 'failed'
               payment.save()
                return Response({'message': 'Payment verification failed', 'data': data}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Failed to connect to Chapa API', 'details': response.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({"error": "A network error occurred.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# Create your views here.
