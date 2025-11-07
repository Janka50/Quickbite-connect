"""
QuickBite Connect - Payment Services
Stripe payment processing logic
"""
import stripe
from django.conf import settings
from .models import Payment, PaymentCard, Refund
from orders.models import Order

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:
    """Service class for Stripe payment operations"""
    
    @staticmethod
    def create_payment_intent(order_id, amount, currency='usd'):
        """Create a Stripe Payment Intent"""
        try:
            order = Order.objects.get(id=order_id)
            
            # Create Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata={
                    'order_id': str(order.id),
                    'order_number': order.order_number,
                    'customer_email': order.customer.email,
                }
            )
            
            # Create Payment record
            payment = Payment.objects.create(
                order=order,
                user=order.customer,
                payment_method='card',
                amount=amount,
                currency=currency.upper(),
                status='pending',
                stripe_payment_intent_id=intent.id
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'payment': payment
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """Confirm payment after successful charge"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            
            if intent.status == 'succeeded':
                payment.status = 'completed'
                payment.stripe_charge_id = intent.charges.data[0].id if intent.charges.data else None
                payment.payment_gateway_response = intent
                
                from django.utils import timezone
                payment.completed_at = timezone.now()
                payment.save()
                
                # Update order
                payment.order.payment_status = 'completed'
                payment.order.status = 'confirmed'
                payment.order.save()
                
                return {'success': True, 'payment': payment}
            else:
                payment.status = 'failed'
                payment.failure_reason = f"Payment intent status: {intent.status}"
                payment.save()
                return {'success': False, 'error': 'Payment not successful'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_refund(payment_id, amount=None, reason='customer_request'):
        """Create a refund for a payment"""
        try:
            payment = Payment.objects.get(id=payment_id)
            
            if not payment.stripe_charge_id:
                return {'success': False, 'error': 'No charge ID found'}
            
            # Create Stripe refund
            refund_amount = int((amount or payment.amount) * 100)
            stripe_refund = stripe.Refund.create(
                charge=payment.stripe_charge_id,
                amount=refund_amount
            )
            
            # Create Refund record
            refund = Refund.objects.create(
                payment=payment,
                order=payment.order,
                amount=amount or payment.amount,
                reason=reason,
                status='completed' if stripe_refund.status == 'succeeded' else 'processing',
                stripe_refund_id=stripe_refund.id,
                requested_by=payment.user
            )
            
            # Update payment status
            payment.status = 'refunded'
            payment.save()
            
            return {'success': True, 'refund': refund}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def add_payment_card(user, token):
        """Add a payment card for user"""
        try:
            # Create or retrieve Stripe customer
            if not hasattr(user, 'stripe_customer_id') or not user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name
                )
                # You might want to add stripe_customer_id to User model
            else:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
            
            # Add card to customer
            card = stripe.Customer.create_source(
                customer.id,
                source=token
            )
            
            # Save card details
            payment_card = PaymentCard.objects.create(
                user=user,
                stripe_card_id=card.id,
                card_brand=card.brand,
                last_four=card.last4,
                exp_month=card.exp_month,
                exp_year=card.exp_year,
                cardholder_name=card.name or user.full_name
            )
            
            return {'success': True, 'card': payment_card}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}