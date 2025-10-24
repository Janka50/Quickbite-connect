"""
QuickBite Connect - Product URLs
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('categories/', views.ProductCategoryListView.as_view(), name='category-list'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('my-products/', views.MyProductsView.as_view(), name='my-products'),
    path('store/<slug:store_slug>/', views.StoreProductsView.as_view(), name='store-products'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<uuid:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
]