from rest_framework import serializers
from payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'oreder', 'amount', 'status', 'transaction_id']
        read_only_fields = ['status', 'transaction_id']
