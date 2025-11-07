"""
QuickBite Connect - Payment Admin
"""
from django.contrib import admin
from .models import Payment, PaymentCard, Refund, Payout


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'order', 'user', 'payment_method',
        'amount', 'status', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'transaction_id', 'order__order_number', 'user__email',
        'stripe_payment_intent_id', 'stripe_charge_id'
    )
    readonly_fields = (
        'transaction_id', 'stripe_payment_intent_id', 'stripe_charge_id',
        'payment_gateway_response', 'created_at', 'updated_at', 'completed_at'
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order', 'user')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'amount', 'currency', 'status', 'transaction_id')
        }),
        ('Stripe Integration', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id', 'stripe_customer_id')
        }),
        ('Gateway Response', {
            'fields': ('payment_gateway_response',)
        }),
        ('Failure Information', {
            'fields': ('failure_reason', 'failure_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'card_brand', 'last_four', 'exp_month',
        'exp_year', 'is_default', 'is_active'
    )
    list_filter = ('card_brand', 'is_default', 'is_active')
    search_fields = ('user__email', 'last_four', 'cardholder_name')
    readonly_fields = ('stripe_card_id', 'created_at', 'updated_at')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        'payment', 'order', 'amount', 'reason',
        'status', 'created_at'
    )
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('order__order_number', 'stripe_refund_id', 'description')
    readonly_fields = ('stripe_refund_id', 'created_at', 'processed_at')
    
    actions = ['approve_refunds']
    
    def approve_refunds(self, request, queryset):
        queryset.update(status='processing', approved_by=request.user)
    approve_refunds.short_description = "Approve selected refunds"


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = (
        'store', 'amount', 'period_start', 'period_end',
        'status', 'created_at'
    )
    list_filter = ('status', 'created_at', 'period_start')
    search_fields = ('store__name', 'stripe_payout_id')
    readonly_fields = ('stripe_payout_id', 'created_at', 'processed_at')
    filter_horizontal = ('orders',)
