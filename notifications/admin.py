from django.contrib import admin
"""
QuickBite Connect - Notification Admin
"""
from django.contrib import admin
from .models import Notification, EmailLog, SMSLog, NotificationPreference, PushToken


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_read=True, read_at=timezone.now())
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, read_at=None)
    mark_as_unread.short_description = "Mark as unread"


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'subject', 'email_type', 'status', 'created_at', 'sent_at')
    list_filter = ('status', 'email_type', 'created_at')
    search_fields = ('recipient_email', 'subject', 'body')
    readonly_fields = ('created_at', 'sent_at')
    
    fieldsets = (
        ('Recipient', {
            'fields': ('user', 'recipient_email')
        }),
        ('Email Content', {
            'fields': ('subject', 'body', 'html_body')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('email_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at')
        }),
    )


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('recipient_phone', 'sms_type', 'status', 'created_at', 'sent_at')
    list_filter = ('status', 'sms_type', 'created_at')
    search_fields = ('recipient_phone', 'message', 'twilio_sid')
    readonly_fields = ('twilio_sid', 'twilio_status', 'created_at', 'sent_at', 'delivered_at')
    
    fieldsets = (
        ('Recipient', {
            'fields': ('user', 'recipient_phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Twilio', {
            'fields': ('twilio_sid', 'twilio_status')
        }),
        ('Metadata', {
            'fields': ('sms_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at', 'delivered_at')
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'email_order_updates', 'sms_order_updates',
        'push_order_updates', 'created_at'
    )
    list_filter = (
        'email_order_updates', 'email_promotions',
        'sms_order_updates', 'push_order_updates'
    )
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'is_active', 'created_at', 'last_used')
    list_filter = ('platform', 'is_active', 'created_at')
    search_fields = ('user__email', 'device_id')
    readonly_fields = ('created_at', 'last_used')