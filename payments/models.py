"""
QuickBite Connect - Payment Models
"""
import uuid
from django.db import models
from users.models import User
from orders.models import Order


class Payment(models.Model):
    """Payment transaction model"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery'),
        ('wallet', 'Digital Wallet'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    
    # Payment Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe Integration
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Transaction Details
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True)
    payment_gateway_response = models.JSONField(default=dict, blank=True)
    
    # Failure Information
    failure_reason = models.TextField(blank=True)
    failure_code = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Generate transaction ID if not exists"""
        if not self.transaction_id:
            import random
            self.transaction_id = f"TXN-{random.randint(100000000, 999999999)}"
        super().save(*args, **kwargs)


class PaymentCard(models.Model):
    """Saved payment cards for users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_cards')
    
    # Card Details (PCI compliant - only store safe data)
    stripe_card_id = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=50)  # visa, mastercard, amex
    last_four = models.CharField(max_length=4)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    
    # Card holder
    cardholder_name = models.CharField(max_length=255)
    
    # Settings
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_cards'
        verbose_name = 'Payment Card'
        verbose_name_plural = 'Payment Cards'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.card_brand} ending in {self.last_four}"
    
    def save(self, *args, **kwargs):
        """Ensure only one default card per user"""
        if self.is_default:
            PaymentCard.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Refund(models.Model):
    """Refund model for payment returns"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    REASON_CHOICES = (
        ('customer_request', 'Customer Request'),
        ('order_cancelled', 'Order Cancelled'),
        ('product_unavailable', 'Product Unavailable'),
        ('quality_issue', 'Quality Issue'),
        ('delivery_failed', 'Delivery Failed'),
        ('duplicate_charge', 'Duplicate Charge'),
        ('other', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    
    # Refund Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe Integration
    stripe_refund_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Processing
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_refunds')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_refunds')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'refunds'
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund ${self.amount} - {self.order.order_number}"


class Payout(models.Model):
    """Store owner payouts"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='payouts')
    
    # Payout Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Orders included in this payout
    orders = models.ManyToManyField(Order, related_name='payouts')
    
    # Stripe Integration
    stripe_payout_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Bank Details
    bank_account_last_four = models.CharField(max_length=4, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payouts'
        verbose_name = 'Payout'
        verbose_name_plural = 'Payouts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payout ${self.amount} - {self.store.name}"
