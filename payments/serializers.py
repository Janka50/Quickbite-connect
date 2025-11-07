"""
QuickBite Connect - Payment Serializers
"""
from rest_framework import serializers
from .models import Payment, PaymentCard, Refund, Payout


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = (
            'id', 'transaction_id', 'stripe_payment_intent_id',
            'stripe_charge_id', 'payment_gateway_response',
            'created_at', 'updated_at', 'completed_at'
        )


class PaymentCardSerializer(serializers.ModelSerializer):
    """Serializer for Payment Card"""
    
    class Meta:
        model = PaymentCard
        fields = (
            'id', 'card_brand', 'last_four', 'exp_month', 'exp_year',
            'cardholder_name', 'is_default', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class RefundSerializer(serializers.ModelSerializer):
    """Serializer for Refund"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = Refund
        fields = '__all__'
        read_only_fields = (
            'id', 'stripe_refund_id', 'approved_by',
            'created_at', 'processed_at'
        )


class PayoutSerializer(serializers.ModelSerializer):
    """Serializer for Payout"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Payout
        fields = '__all__'
        read_only_fields = (
            'id', 'stripe_payout_id', 'created_at', 'processed_at'
        )