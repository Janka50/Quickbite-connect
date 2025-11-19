from django.contrib import admin
"""
QuickBite Connect - Review Admin
"""
from django.contrib import admin
from .models import StoreReview, ProductReview, ReviewHelpful, ReviewReport


@admin.register(StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    list_display = (
        'store', 'user', 'rating', 'is_verified_purchase',
        'is_approved', 'is_flagged', 'helpful_count', 'created_at'
    )
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'is_flagged', 'created_at')
    search_fields = ('store__name', 'user__email', 'title', 'comment')
    readonly_fields = ('helpful_count', 'not_helpful_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('store', 'user', 'order', 'rating')
        }),
        ('Review Content', {
            'fields': ('title', 'comment', 'food_quality', 'delivery_speed', 'value_for_money')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
        ('Moderation', {
            'fields': ('is_verified_purchase', 'is_approved', 'is_flagged')
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'not_helpful_count')
        }),
        ('Store Response', {
            'fields': ('store_response', 'responded_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_reviews', 'flag_reviews', 'unflag_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True, is_flagged=False)
    approve_reviews.short_description = "Approve selected reviews"
    
    def flag_reviews(self, request, queryset):
        queryset.update(is_flagged=True)
    flag_reviews.short_description = "Flag selected reviews"
    
    def unflag_reviews(self, request, queryset):
        queryset.update(is_flagged=False)
    unflag_reviews.short_description = "Unflag selected reviews"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'user', 'rating', 'is_verified_purchase',
        'is_approved', 'is_flagged', 'helpful_count', 'created_at'
    )
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'is_flagged', 'created_at')
    search_fields = ('product__name', 'user__email', 'title', 'comment')
    readonly_fields = ('helpful_count', 'not_helpful_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'user', 'order', 'rating')
        }),
        ('Review Content', {
            'fields': ('title', 'comment', 'pros', 'cons')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
        ('Moderation', {
            'fields': ('is_verified_purchase', 'is_approved', 'is_flagged')
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'not_helpful_count')
        }),
        ('Seller Response', {
            'fields': ('seller_response', 'responded_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_reviews', 'flag_reviews', 'unflag_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True, is_flagged=False)
    approve_reviews.short_description = "Approve selected reviews"
    
    def flag_reviews(self, request, queryset):
        queryset.update(is_flagged=True)
    flag_reviews.short_description = "Flag selected reviews"
    
    def unflag_reviews(self, request, queryset):
        queryset.update(is_flagged=False)
    unflag_reviews.short_description = "Unflag selected reviews"


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ('user', 'vote', 'created_at')
    list_filter = ('vote', 'created_at')
    search_fields = ('user__email',)


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'reason', 'status', 'created_at')
    list_filter = ('reason', 'status', 'created_at')
    search_fields = ('reported_by__email', 'description')
    readonly_fields = ('created_at', 'resolved_at')
    
    actions = ['mark_as_reviewed', 'mark_as_resolved', 'dismiss_reports']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed', reviewed_by=request.user)
    mark_as_reviewed.short_description = "Mark as reviewed"
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='resolved', reviewed_by=request.user, resolved_at=timezone.now())
    mark_as_resolved.short_description = "Mark as resolved"
    
    def dismiss_reports(self, request, queryset):
        queryset.update(status='dismissed', reviewed_by=request.user)
    dismiss_reports.short_description = "Dismiss reports"
