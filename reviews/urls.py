"""
QuickBite Connect - Review URLs
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Store Reviews
    path('stores/<uuid:store_id>/', views.StoreReviewListView.as_view(), name='store-review-list'),
    path('stores/create/', views.StoreReviewCreateView.as_view(), name='store-review-create'),
    
    # Product Reviews
    path('products/<uuid:product_id>/', views.ProductReviewListView.as_view(), name='product-review-list'),
    path('products/create/', views.ProductReviewCreateView.as_view(), name='product-review-create'),
    
    # My Reviews
    path('my-reviews/', views.MyReviewsView.as_view(), name='my-reviews'),
    
    # Review Actions
    path('helpful/', views.ReviewHelpfulView.as_view(), name='review-helpful'),
    path('report/', views.ReviewReportView.as_view(), name='review-report'),
]