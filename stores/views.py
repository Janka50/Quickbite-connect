"""
QuickBite Connect - Store Views
"""
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, StoreStaff, StoreCategory
from .serializers import (
    StoreSerializer,
    StoreCreateSerializer,
    StoreListSerializer,
    StoreStaffSerializer,
    StoreCategorySerializer
)


class StoreListView(generics.ListAPIView):
    """API endpoint to list all approved stores"""
    queryset = Store.objects.filter(status='approved')
    serializer_class = StoreListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'store_type', 'is_open']
    search_fields = ['name', 'description', 'city']
    ordering_fields = ['average_rating', 'created_at', 'name']
    ordering = ['-is_featured', '-average_rating']


class StoreDetailView(generics.RetrieveAPIView):
    """API endpoint for store detail"""
    queryset = Store.objects.filter(status='approved')
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class StoreCreateView(generics.CreateAPIView):
    """API endpoint to create a new store"""
    queryset = Store.objects.all()
    serializer_class = StoreCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is store_owner
        if request.user.user_type != 'store_owner':
            return Response(
                {'error': 'Only store owners can create stores'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = serializer.save()
        
        return Response({
            'store': StoreSerializer(store).data,
            'message': 'Store created successfully! Awaiting admin approval.'
        }, status=status.HTTP_201_CREATED)


class MyStoresView(generics.ListAPIView):
    """API endpoint to list user's stores"""
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreUpdateView(generics.RetrieveUpdateAPIView):
    """API endpoint to update store"""
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreCategoryListView(generics.ListAPIView):
    """API endpoint to list store categories"""
    queryset = StoreCategory.objects.filter(is_active=True)
    serializer_class = StoreCategorySerializer
    permission_classes = [AllowAny]


class StoreStaffListView(generics.ListAPIView):
    """API endpoint to list store staff"""
    serializer_class = StoreStaffSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        return StoreStaff.objects.filter(store_id=store_id, store__owner=self.request.user)