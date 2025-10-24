"""
QuickBite Connect - Product Views
"""
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProductCategory, Product, ProductImage, ProductVariant
from .serializers import (
    ProductCategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer,
    ProductImageSerializer,
    ProductVariantSerializer
)


class ProductCategoryListView(generics.ListAPIView):
    """API endpoint to list product categories"""
    queryset = ProductCategory.objects.filter(is_active=True, parent=None)
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    """API endpoint to list products"""
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['store', 'category', 'is_available', 'is_featured', 'is_vegetarian', 'is_vegan']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['price', 'average_rating', 'created_at', 'total_sold']
    ordering = ['-is_featured', '-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Filter by store slug
        store_slug = self.request.query_params.get('store_slug', None)
        if store_slug:
            queryset = queryset.filter(store__slug=store_slug)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """API endpoint for product detail"""
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductCreateView(generics.CreateAPIView):
    """API endpoint to create products"""
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Verify user owns the store
        store_id = request.data.get('store')
        if not request.user.owned_stores.filter(id=store_id).exists():
            return Response(
                {'error': 'You can only add products to your own stores'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        return Response({
            'product': ProductDetailSerializer(product).data,
            'message': 'Product created successfully!'
        }, status=status.HTTP_201_CREATED)


class StoreProductsView(generics.ListAPIView):
    """API endpoint to list products for a specific store"""
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        store_slug = self.kwargs.get('store_slug')
        return Product.objects.filter(
            store__slug=store_slug, 
            is_available=True
        )


class MyProductsView(generics.ListAPIView):
    """API endpoint to list user's products"""
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint to update/delete products"""
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)