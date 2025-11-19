from django.db import models
"""
QuickBite Connect - Review Models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from stores.models import Store
from products.models import Product
from orders.models import Order


class StoreReview(models.Model):
    """Reviews for stores"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_reviews')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='store_reviews')
    
    # Rating (1-5 stars)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Review Content
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Specific Ratings
    food_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    delivery_speed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    value_for_money = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    
    # Review Images
    image1 = models.ImageField(upload_to='reviews/stores/', null=True, blank=True)
    image2 = models.ImageField(upload_to='reviews/stores/', null=True, blank=True)
    image3 = models.ImageField(upload_to='reviews/stores/', null=True, blank=True)
    
    # Moderation
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    # Engagement
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    
    # Store Response
    store_response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'store_reviews'
        verbose_name = 'Store Review'
        verbose_name_plural = 'Store Reviews'
        ordering = ['-created_at']
        unique_together = ('store', 'user', 'order')
        indexes = [
            models.Index(fields=['store', 'is_approved']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.store.name} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        """Update store average rating on save"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new or 'rating' in kwargs.get('update_fields', []):
            self.store.update_rating()


class ProductReview(models.Model):
    """Reviews for products"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_reviews')
    
    # Rating (1-5 stars)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Review Content
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Product Specific
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    
    # Review Images
    image1 = models.ImageField(upload_to='reviews/products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='reviews/products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='reviews/products/', null=True, blank=True)
    
    # Moderation
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    # Engagement
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    
    # Seller Response
    seller_response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_reviews'
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-created_at']
        unique_together = ('product', 'user', 'order')
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        """Update product average rating on save"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new or 'rating' in kwargs.get('update_fields', []):
            self.product.update_rating()


class ReviewHelpful(models.Model):
    """Track helpful votes on reviews"""
    
    VOTE_CHOICES = (
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Polymorphic - can vote on either store or product review
    store_review = models.ForeignKey(StoreReview, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    product_review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    
    vote = models.CharField(max_length=20, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_helpful_votes'
        verbose_name = 'Review Vote'
        verbose_name_plural = 'Review Votes'
        constraints = [
            models.CheckConstraint(
                check=models.Q(store_review__isnull=False) | models.Q(product_review__isnull=False),
                name='review_helpful_check'
            )
        ]
    
    def __str__(self):
        if self.store_review:
            return f"{self.user.email} - Store Review - {self.vote}"
        return f"{self.user.email} - Product Review - {self.vote}"


class ReviewReport(models.Model):
    """Report inappropriate reviews"""
    
    REASON_CHOICES = (
        ('spam', 'Spam'),
        ('offensive', 'Offensive Language'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Review'),
        ('irrelevant', 'Irrelevant'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_reports')
    
    # Polymorphic - can report either store or product review
    store_review = models.ForeignKey(StoreReview, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    product_review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin Actions
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'review_reports'
        verbose_name = 'Review Report'
        verbose_name_plural = 'Review Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reported_by.email} - {self.reason}"
