"""
QuickBite Connect - Product Serializers
"""
from rest_framework import serializers
from .models import ProductCategory, Product, ProductImage, ProductVariant, InventoryLog


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for Product Category"""
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductCategory
        fields = '__all__'
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return ProductCategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
        return []


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for Product Images"""
    
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for Product Variants"""
    
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """Minimal serializer for product listings"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'short_description', 'price', 
            'discount_price', 'discount_percentage', 'main_image',
            'store_name', 'category_name', 'average_rating', 
            'is_available', 'is_in_stock', 'is_featured'
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for product detail view"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    store_slug = serializers.CharField(source='store.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating products"""
    
    class Meta:
        model = Product
        exclude = ('average_rating', 'total_reviews', 'total_sold', 'view_count')
    
    def create(self, validated_data):
        # Auto-generate slug from name
        from django.utils.text import slugify
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class InventoryLogSerializer(serializers.ModelSerializer):
    """Serializer for Inventory Logs"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = InventoryLog
        fields = '__all__'
        read_only_fields = ('id', 'created_at')