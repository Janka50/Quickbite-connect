"""
QuickBite Connect - Payment Views
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, PaymentCard, Refund
from .serializers import PaymentSerializer, PaymentCardSerializer, RefundSerializer
from .services import StripePaymentService


class CreatePaymentIntentView(APIView):
    """API endpoint to create payment intent"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create Stripe payment intent"""
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response(
                {'error': 'Order ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = StripePaymentService.create_payment_intent(
            order_id=order_id,
            amount=request.data.get('amount')
        )
        
        if result['success']:
            return Response({
                'client_secret': result['client_secret'],
                'payment_intent_id': result['payment_intent_id'],
                'payment': PaymentSerializer(result['payment']).data
            })
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConfirmPaymentView(APIView):
    """API endpoint to confirm payment"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Confirm payment after Stripe processing"""
        payment_intent_id = request.data.get('payment_intent_id')
        
        if not payment_intent_id:
            return Response(
                {'error': 'Payment Intent ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = StripePaymentService.confirm_payment(payment_intent_id)
        
        if result['success']:
            return Response({
                'message': 'Payment confirmed successfully',
                'payment': PaymentSerializer(result['payment']).data
            })
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentListView(generics.ListAPIView):
    """API endpoint to list user's payments"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    """API endpoint for payment detail"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'transaction_id'
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentCardListView(generics.ListAPIView):
    """API endpoint to list saved cards"""
    serializer_class = PaymentCardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentCard.objects.filter(user=self.request.user, is_active=True)


class RefundRequestView(APIView):
    """API endpoint to request refund"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Request refund for a payment"""
        payment_id = request.data.get('payment_id')
        reason = request.data.get('reason', 'customer_request')
        
        if not payment_id:
            return Response(
                {'error': 'Payment ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = StripePaymentService.create_refund(
            payment_id=payment_id,
            reason=reason
        )
        
        if result['success']:
            return Response({
                'message': 'Refund processed successfully',
                'refund': RefundSerializer(result['refund']).data
            })
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )