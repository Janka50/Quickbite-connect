"""
QuickBite Connect - Review Serializers
"""
from rest_framework import serializers
from .models import StoreReview, ProductReview, ReviewHelpful, ReviewReport


class StoreReviewSerializer(serializers.ModelSerializer):
    """Serializer for Store Reviews"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = StoreReview
        fields = (
            'id', 'store', 'store_name', 'user', 'user_name', 'order',
            'rating', 'title', 'comment', 'food_quality', 'delivery_speed',
            'value_for_money', 'image1', 'image2', 'image3',
            'is_verified_purchase', 'helpful_count', 'not_helpful_count',
            'store_response', 'responded_at', 'created_at'
        )
        read_only_fields = (
            'id', 'user', 'is_verified_purchase', 'helpful_count',
            'not_helpful_count', 'store_response', 'responded_at', 'created_at'
        )


class StoreReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating store reviews"""
    
    class Meta:
        model = StoreReview
        fields = (
            'store', 'order', 'rating', 'title', 'comment',
            'food_quality', 'delivery_speed', 'value_for_money',
            'image1', 'image2', 'image3'
        )
    
    def validate(self, attrs):
        """Validate review creation"""
        user = self.context['request'].user
        store = attrs['store']
        order = attrs.get('order')
        
        # Check if user has already reviewed this store for this order
        if order and StoreReview.objects.filter(store=store, user=user, order=order).exists():
            raise serializers.ValidationError("You have already reviewed this store for this order")
        
        # Check if order belongs to user and is from this store
        if order and (order.customer != user or order.store != store):
            raise serializers.ValidationError("Invalid order")
        
        return attrs
    
    def create(self, validated_data):
        """Create review"""
        validated_data['user'] = self.context['request'].user
        validated_data['is_verified_purchase'] = bool(validated_data.get('order'))
        return super().create(validated_data)


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for Product Reviews"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = (
            'id', 'product', 'product_name', 'user', 'user_name', 'order',
            'rating', 'title', 'comment', 'pros', 'cons',
            'image1', 'image2', 'image3', 'is_verified_purchase',
            'helpful_count', 'not_helpful_count', 'seller_response',
            'responded_at', 'created_at'
        )
        read_only_fields = (
            'id', 'user', 'is_verified_purchase', 'helpful_count',
            'not_helpful_count', 'seller_response', 'responded_at', 'created_at'
        )


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating product reviews"""
    
    class Meta:
        model = ProductReview
        fields = (
            'product', 'order', 'rating', 'title', 'comment',
            'pros', 'cons', 'image1', 'image2', 'image3'
        )
    
    def validate(self, attrs):
        """Validate review creation"""
        user = self.context['request'].user
        product = attrs['product']
        order = attrs.get('order')
        
        # Check if user has already reviewed this product for this order
        if order and ProductReview.objects.filter(product=product, user=user, order=order).exists():
            raise serializers.ValidationError("You have already reviewed this product for this order")
        
        # Check if order belongs to user and contains this product
        if order:
            if order.customer != user:
                raise serializers.ValidationError("Invalid order")
            if not order.items.filter(product=product).exists():
                raise serializers.ValidationError("This product was not in the order")
        
        return attrs
    
    def create(self, validated_data):
        """Create review"""
        validated_data['user'] = self.context['request'].user
        validated_data['is_verified_purchase'] = bool(validated_data.get('order'))
        return super().create(validated_data)


class ReviewHelpfulSerializer(serializers.ModelSerializer):
    """Serializer for Review Helpful Votes"""
    
    class Meta:
        model = ReviewHelpful
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')


class ReviewReportSerializer(serializers.ModelSerializer):
    """Serializer for Review Reports"""
    
    class Meta:
        model = ReviewReport
        fields = (
            'id', 'store_review', 'product_review', 'reason',
            'description', 'status', 'created_at'
        )
        read_only_fields = ('id', 'reported_by', 'status', 'created_at')