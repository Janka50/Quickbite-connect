"""
QuickBite Connect - Order Serializers
"""
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, Coupon
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for Cart Items"""
    product = ProductListSerializer(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('id', 'cart', 'created_at', 'updated_at')


class CartItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating cart items"""
    
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'special_instructions')


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('id', 'user', 'session_key', 'created_at', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for Order Items"""
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for Order Status History"""
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class OrderListSerializer(serializers.ModelSerializer):
    """Minimal serializer for order listings"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'store_name', 'customer_name',
            'status', 'payment_status', 'total_amount', 'created_at'
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    
    class Meta:
        model = Order
        fields = (
            'store', 'delivery_address', 'payment_method',
            'delivery_instructions'
        )
    
    def validate(self, attrs):
        """Validate order creation"""
        user = self.context['request'].user
        
        # Check if user has items in cart for this store
        cart = Cart.objects.filter(user=user, store=attrs['store']).first()
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Cart is empty for this store")
        
        # Check if delivery address belongs to user
        if attrs['delivery_address'].user != user:
            raise serializers.ValidationError("Invalid delivery address")
        
        return attrs
    
    def create(self, validated_data):
        """Create order from cart"""
        user = self.context['request'].user
        store = validated_data['store']
        
        # Get user's cart
        cart = Cart.objects.get(user=user, store=store)
        
        # Calculate totals
        subtotal = cart.subtotal
        delivery_fee = store.delivery_fee
        tax_amount = subtotal * 0.05  # 5% tax
        total_amount = subtotal + delivery_fee + tax_amount
        
        # Create order
        order = Order.objects.create(
            customer=user,
            store=store,
            delivery_address=validated_data['delivery_address'],
            payment_method=validated_data['payment_method'],
            delivery_instructions=validated_data.get('delivery_instructions', ''),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='pending',
            payment_status='pending'
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.unit_price,
                quantity=cart_item.quantity,
                subtotal=cart_item.total_price,
                special_instructions=cart_item.special_instructions
            )
            
            # Update product stock
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.total_sold += cart_item.quantity
            cart_item.product.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order created',
            changed_by=user
        )
        
        # Clear cart
        cart.items.all().delete()
        
        return order


class CouponSerializer(serializers.ModelSerializer):
    """Serializer for Coupons"""
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Coupon
        fields = '__all__'
    
    def get_is_valid(self, obj):
        return obj.is_valid()