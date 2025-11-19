"""
QuickBite Connect - Notification Models
"""
import uuid
from django.db import models
from users.models import User


class Notification(models.Model):
    """In-app notifications"""
    
    TYPE_CHOICES = (
        ('order_confirmed', 'Order Confirmed'),
        ('order_preparing', 'Order Preparing'),
        ('order_ready', 'Order Ready'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('payment_received', 'Payment Received'),
        ('payment_failed', 'Payment Failed'),
        ('review_received', 'Review Received'),
        ('store_approved', 'Store Approved'),
        ('store_rejected', 'Store Rejected'),
        ('low_stock', 'Low Stock Alert'),
        ('new_product', 'New Product'),
        ('promotion', 'Promotion'),
        ('system', 'System Notification'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification Details
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related Objects (optional)
    related_object_id = models.UUIDField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)  # 'order', 'store', 'product'
    
    # Action URL
    action_url = models.CharField(max_length=500, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class EmailLog(models.Model):
    """Track email notifications"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_logs', null=True, blank=True)
    
    # Email Details
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=500)
    body = models.TextField()
    html_body = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Metadata
    email_type = models.CharField(max_length=50, blank=True)  # 'order_confirmation', 'welcome', etc.
    related_object_id = models.UUIDField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'email_logs'
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient_email} - {self.subject}"


class SMSLog(models.Model):
    """Track SMS notifications"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_logs', null=True, blank=True)
    
    # SMS Details
    recipient_phone = models.CharField(max_length=17)
    message = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Twilio Response
    twilio_sid = models.CharField(max_length=255, blank=True)
    twilio_status = models.CharField(max_length=50, blank=True)
    
    # Metadata
    sms_type = models.CharField(max_length=50, blank=True)  # 'order_update', 'otp', etc.
    related_object_id = models.UUIDField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'sms_logs'
        verbose_name = 'SMS Log'
        verbose_name_plural = 'SMS Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient_phone} - {self.sms_type}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email Preferences
    email_order_updates = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=True)
    email_reviews = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=False)
    
    # SMS Preferences
    sms_order_updates = models.BooleanField(default=True)
    sms_delivery_updates = models.BooleanField(default=True)
    sms_promotions = models.BooleanField(default=False)
    
    # Push Notification Preferences
    push_order_updates = models.BooleanField(default=True)
    push_promotions = models.BooleanField(default=True)
    push_new_products = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"{self.user.email} - Preferences"


class PushToken(models.Model):
    """Store push notification tokens"""
    
    PLATFORM_CHOICES = (
        ('web', 'Web'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_tokens')
    
    # Token Details
    token = models.TextField(unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    device_id = models.CharField(max_length=255, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'push_tokens'
        verbose_name = 'Push Token'
        verbose_name_plural = 'Push Tokens'
    
    def __str__(self):
        return f"{self.user.email} - {self.platform}"