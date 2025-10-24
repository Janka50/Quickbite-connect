"""
QuickBite Connect - Store Serializers
"""
from rest_framework import serializers
from .models import Store, StoreStaff, StoreCategory, StoreCategoryMapping
from users.serializers import UserSerializer


class StoreCategorySerializer(serializers.ModelSerializer):
    """Serializer for Store Category"""
    
    class Meta:
        model = StoreCategory
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model"""
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    categories = StoreCategorySerializer(source='category_mappings.category', many=True, read_only=True)
    
    class Meta:
        model = Store
        fields = (
            'id', 'owner', 'owner_email', 'name', 'slug', 'description',
            'store_type', 'logo', 'cover_image', 'phone_number', 'email',
            'website', 'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'latitude', 'longitude',
            'delivery_radius', 'min_order_amount', 'delivery_fee',
            'estimated_delivery_time', 'business_hours', 'status',
            'is_open', 'is_featured', 'average_rating', 'total_reviews',
            'total_orders', 'is_verified', 'categories', 'created_at', 'full_address'
        )
        read_only_fields = (
            'id', 'owner', 'status', 'is_verified', 'average_rating',
            'total_reviews', 'total_orders', 'created_at', 'full_address'
        )


class StoreCreateSerializer(serializers.ModelSerializer):
    """Serializer for Store creation"""
    
    class Meta:
        model = Store
        fields = (
            'name', 'description', 'store_type', 'logo', 'cover_image',
            'phone_number', 'email', 'website', 'address_line1',
            'address_line2', 'city', 'state', 'postal_code', 'country',
            'latitude', 'longitude', 'delivery_radius', 'min_order_amount',
            'delivery_fee', 'estimated_delivery_time', 'business_hours',
            'business_license', 'tax_id'
        )
    
    def create(self, validated_data):
        # Set owner from request user
        validated_data['owner'] = self.context['request'].user
        # Auto-generate slug from name
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class StoreStaffSerializer(serializers.ModelSerializer):
    """Serializer for Store Staff"""
    user = UserSerializer(read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = StoreStaff
        fields = '__all__'
        read_only_fields = ('id', 'hired_date')


class StoreListSerializer(serializers.ModelSerializer):
    """Minimal serializer for store listings"""
    
    class Meta:
        model = Store
        fields = (
            'id', 'name', 'slug', 'logo', 'store_type', 'city',
            'is_open', 'average_rating', 'total_reviews',
            'delivery_fee', 'estimated_delivery_time', 'min_order_amount'
        )