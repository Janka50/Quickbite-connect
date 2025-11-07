"""
QuickBite Connect - Order Views
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, Coupon
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    CartItemCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    CouponSerializer
)
from products.models import Product
from stores.models import Store


class CartView(APIView):
    """API endpoint to manage cart"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's active cart"""
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    """API endpoint to add items to cart"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add product to cart"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        special_instructions = request.data.get('special_instructions', '')
        
        # Get product
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is available
        if not product.is_available or not product.is_in_stock:
            return Response(
                {'error': 'Product is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check stock
        if product.stock_quantity < quantity:
            return Response(
                {'error': f'Only {product.stock_quantity} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart for this store
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            store=product.store
        )
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'special_instructions': special_instructions
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.special_instructions = special_instructions
            cart_item.save()
        
        return Response({
            'message': 'Product added to cart',
            'cart': CartSerializer(cart).data
        }, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    """API endpoint to update cart item"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, item_id):
        """Update cart item quantity"""
        cart_item = get_object_or_404(
            CartItem, 
            id=item_id, 
            cart__user=request.user
        )
        
        quantity = request.data.get('quantity')
        
        if quantity:
            if quantity <= 0:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
            
            # Check stock
            if cart_item.product.stock_quantity < quantity:
                return Response(
                    {'error': f'Only {cart_item.product.stock_quantity} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.quantity = quantity
            cart_item.save()
        
        return Response({
            'message': 'Cart updated',
            'cart_item': CartItemSerializer(cart_item).data
        })
    
    def delete(self, request, item_id):
        """Remove item from cart"""
        cart_item = get_object_or_404(
            CartItem, 
            id=item_id, 
            cart__user=request.user
        )
        cart_item.delete()
        
        return Response({'message': 'Item removed from cart'})


class ClearCartView(APIView):
    """API endpoint to clear cart"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        """Clear all items from cart"""
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'})


class OrderCreateView(generics.CreateAPIView):
    """API endpoint to create order from cart"""
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save
        
        
class CartView(APIView):
    """API endpoint to manage cart"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's active cart"""
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    """API endpoint to add items to cart"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add product to cart"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        special_instructions = request.data.get('special_instructions', '')
        
        product = get_object_or_404(Product, id=product_id)
        
        if not product.is_available or not product.is_in_stock:
            return Response(
                {'error': 'Product is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if product.stock_quantity < quantity:
            return Response(
                {'error': f'Only {product.stock_quantity} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            store=product.store
        )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'special_instructions': special_instructions
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.special_instructions = special_instructions
            cart_item.save()
        
        return Response({
            'message': 'Product added to cart',
            'cart': CartSerializer(cart).data
        }, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    """API endpoint to update cart item"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, item_id):
        """Update cart item quantity"""
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        quantity = request.data.get('quantity')
        
        if quantity:
            if quantity <= 0:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
            
            if cart_item.product.stock_quantity < quantity:
                return Response(
                    {'error': f'Only {cart_item.product.stock_quantity} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.quantity = quantity
            cart_item.save()
        
        return Response({
            'message': 'Cart updated',
            'cart_item': CartItemSerializer(cart_item).data
        })
    
    def delete(self, request, item_id):
        """Remove item from cart"""
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})


class ClearCartView(APIView):
    """API endpoint to clear cart"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        """Clear all items from cart"""
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'})


class OrderCreateView(generics.CreateAPIView):
    """API endpoint to create order from cart"""
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response({
            'order': OrderDetailSerializer(order).data,
            'message': 'Order placed successfully!'
        }, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """API endpoint to list user's orders"""
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """API endpoint for order detail"""
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class StoreOrdersView(generics.ListAPIView):
    """API endpoint for store owners to view their orders"""
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(store__owner=self.request.user)


class ValidateCouponView(APIView):
    """API endpoint to validate coupon"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Validate coupon code"""
        code = request.data.get('code')
        store_id = request.data.get('store_id')
        
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Invalid coupon code'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not coupon.is_valid():
            return Response(
                {'error': 'Coupon is not valid or has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if coupon.store and str(coupon.store.id) != store_id:
            return Response(
                {'error': 'Coupon is not valid for this store'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Coupon is valid',
            'coupon': CouponSerializer(coupon).data
        })