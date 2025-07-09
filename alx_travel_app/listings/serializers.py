# alx_travel_app/listings/serializers.py

from rest_framework import serializers
from .models import Payment

class PaymentInitiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('booking', 'amount', 'currency')

class PaymentVerifySerializer(serializers.Serializer):
    transaction_id = serializers.CharField()

