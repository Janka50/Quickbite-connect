"""
QuickBite Connect - Order URLs
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart endpoints
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/item/<uuid:item_id>/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear-cart'),
    
    # Order endpoints
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<str:order_number>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('store/orders/', views.StoreOrdersView.as_view(), name='store-orders'),
    
    # Coupon endpoints
    path('coupon/validate/', views.ValidateCouponView.as_view(), name='validate-coupon'),
]