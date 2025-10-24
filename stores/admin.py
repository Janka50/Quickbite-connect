"""
QuickBite Connect - Store Admin
"""
from django.contrib import admin
from .models import Store, StoreStaff, StoreCategory, StoreCategoryMapping


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'status', 'is_open', 'is_verified', 'average_rating', 'created_at')
    list_filter = ('status', 'store_type', 'is_open', 'is_verified', 'is_featured', 'city')
    search_fields = ('name', 'owner__email', 'city', 'postal_code')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'average_rating', 'total_reviews', 'total_orders', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'slug', 'description', 'store_type', 'logo', 'cover_image')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'website')
        }),
        ('Location', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude')
        }),
        ('Business Settings', {
            'fields': ('delivery_radius', 'min_order_amount', 'delivery_fee', 'estimated_delivery_time', 'business_hours')
        }),
        ('Status & Verification', {
            'fields': ('status', 'is_open', 'is_featured', 'is_verified', 'business_license', 'tax_id')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews', 'total_orders')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_stores', 'reject_stores', 'feature_stores']
    
    def approve_stores(self, request, queryset):
        queryset.update(status='approved', is_verified=True)
    approve_stores.short_description = "Approve selected stores"
    
    def reject_stores(self, request, queryset):
        queryset.update(status='rejected')
    reject_stores.short_description = "Reject selected stores"
    
    def feature_stores(self, request, queryset):
        queryset.update(is_featured=True)
    feature_stores.short_description = "Feature selected stores"


@admin.register(StoreStaff)
class StoreStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'role', 'is_active', 'hired_date')
    list_filter = ('role', 'is_active', 'hired_date')
    search_fields = ('user__email', 'store__name')


@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StoreCategoryMapping)
class StoreCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('store', 'category')
    list_filter = ('category',)
    search_fields = ('store__name', 'category__name')