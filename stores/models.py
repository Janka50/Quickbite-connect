"""
QuickBite Connect - Store Models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Store(models.Model):
    """Store model for local and chain stores"""
    
    STORE_TYPE_CHOICES = (
        ('local', 'Local Store'),
        ('chain', 'Chain Store'),
        ('restaurant', 'Restaurant'),
        ('grocery', 'Grocery Store'),
        ('supermarket', 'Supermarket'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES, default='local')
    logo = models.ImageField(upload_to='stores/logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='stores/covers/', null=True, blank=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=17)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Location Information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Business Settings
    delivery_radius = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=5.0,
        help_text="Delivery radius in miles"
    )
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=2.99)
    estimated_delivery_time = models.IntegerField(
        default=30, 
        help_text="Estimated delivery time in minutes"
    )
    
    # Business Hours (stored as JSON)
    business_hours = models.JSONField(default=dict, blank=True, help_text="Store business hours")
    
    # Status and Rating
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_open = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    
    # Certifications and Documents
    business_license = models.FileField(upload_to='stores/documents/', null=True, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stores'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ['-is_featured', '-average_rating', 'name']
        indexes = [
            models.Index(fields=['city', 'status']),
            models.Index(fields=['status', 'is_open']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        """Return full address as string"""
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.extend([self.city, self.state, self.postal_code])
        return ', '.join(parts)


class StoreStaff(models.Model):
    """Store staff management"""
    
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('delivery', 'Delivery Personnel'),
        ('kitchen', 'Kitchen Staff'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_positions')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    hired_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'store_staff'
        verbose_name = 'Store Staff'
        verbose_name_plural = 'Store Staff'
        unique_together = ('store', 'user')
    
    def __str__(self):
        return f"{self.user.email} - {self.store.name} ({self.role})"


class StoreCategory(models.Model):
    """Categories for stores"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'store_categories'
        verbose_name = 'Store Category'
        verbose_name_plural = 'Store Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class StoreCategoryMapping(models.Model):
    """Many-to-many relationship between stores and categories"""
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, related_name='store_mappings')
    
    class Meta:
        db_table = 'store_category_mappings'
        unique_together = ('store', 'category')
    
    def __str__(self):
        return f"{self.store.name} - {self.category.name}"