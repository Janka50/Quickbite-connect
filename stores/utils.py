"""
QuickBite Connect - Store Utilities
"""
from django.db.models import Avg, Count


def update_store_rating(store):
    """Update store's average rating"""
    from reviews.models import StoreReview
    
    stats = StoreReview.objects.filter(
        store=store,
        is_approved=True
    ).aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    store.average_rating = stats['avg_rating'] or 0
    store.total_reviews = stats['total_reviews'] or 0
    store.save(update_fields=['average_rating', 'total_reviews'])


def update_product_rating(product):
    """Update product's average rating"""
    from reviews.models import ProductReview
    
    stats = ProductReview.objects.filter(
        product=product,
        is_approved=True
    ).aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    product.average_rating = stats['avg_rating'] or 0
    product.total_reviews = stats['total_reviews'] or 0
    product.save(update_fields=['average_rating', 'total_reviews'])