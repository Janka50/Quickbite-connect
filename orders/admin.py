"""
QuickBite Connect - Order Admin
"""
from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, Coupon, CouponUsage


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('unit_price', 'total_price')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'total_items', 'subtotal', 'created_at')
    list_filter = ('store', 'created_at')
    search_fields = ('user__email', 'session_key')
    readonly_fields = ('total_items', 'subtotal', 'total', 'created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'cart__user__email')
    readonly_fields = ('unit_price', 'total_price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'subtotal')


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'changed_by', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'customer', 'store', 'status', 
        'payment_status', 'total_amount', 'created_at'
    )
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'customer__email', 'store__name')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'confirmed_at', 'completed_at')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'store', 'status')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'subtotal', 'delivery_fee', 
                      'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Delivery', {
            'fields': ('delivery_address', 'delivery_instructions', 'estimated_delivery_time',
                      'actual_delivery_time', 'assigned_driver')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at')
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_delivered']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark as confirmed"
    
    def mark_as_preparing(self, request, queryset):
        queryset.update(status='preparing')
    mark_as_preparing.short_description = "Mark as preparing"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Mark as delivered"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'product_price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('product_name', 'order__order_number')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'notes')
    readonly_fields = ('created_at',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'discount_type', 'discount_value', 'valid_from', 
        'valid_until', 'times_used', 'is_active'
    )
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'description')
    readonly_fields = ('times_used', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description', 'store')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value', 'min_order_amount', 'max_discount_amount')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'usage_limit', 'usage_per_user', 'times_used', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'order', 'user', 'discount_amount', 'used_at')
    list_filter = ('used_at',)
    search_fields = ('coupon__code', 'order__order_number', 'user__email')
    readonly_fields = ('used_at',)