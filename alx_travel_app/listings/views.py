# alx_travel_app/listings/views.py

import os
import requests
from django.conf import settings
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentInitiateSerializer, PaymentVerifySerializer

CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')

class PaymentInitiateAPIView(generics.CreateAPIView):
    serializer_class = PaymentInitiateSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payload = {
            "amount": str(payment.amount),
            "currency": payment.currency,
            "tx_ref": str(payment.id),
            "callback_url": settings.PAYMENT_CALLBACK_URL,
            "return_url": settings.PAYMENT_RETURN_URL,
        }
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload,
            headers=headers,
        )
        resp_data = resp.json()
        transaction_id = resp_data.get('data', {}).get('id')
        payment.transaction_id = transaction_id
        payment.status = Payment.STATUS_PENDING
        payment.save()
        return payment

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        payment = resp.data
        return Response({
            "transaction_id": payment['id'],
            "checkout_url": resp.data.get('checkout_url')
        }, status=status.HTTP_201_CREATED)

class PaymentVerifyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx_id = serializer.validated_data['transaction_id']
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
        }
        resp = requests.get(
            f"https://api.chapa.co/v1/transaction/verify/{tx_id}",
            headers=headers
        )
        data = resp.json().get('data', {})
        try:
            payment = Payment.objects.get(transaction_id=tx_id)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        if data.get('status') == 'success':
            payment.status = Payment.STATUS_COMPLETED
        else:
            payment.status = Payment.STATUS_FAILED
        payment.save()
        return Response({
            "transaction_id": tx_id,
            "status": payment.status,
            "amount": payment.amount
        }, status=status.HTTP_200_OK)

