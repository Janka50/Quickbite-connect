"""
QuickBite Connect - Product Admin
"""
from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, ProductVariant, InventoryLog


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'display_order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'display_order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('name', 'sku', 'price_adjustment', 'stock_quantity', 'is_available')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'store', 'category', 'price', 'stock_quantity', 
        'is_available', 'is_featured', 'average_rating', 'total_sold'
    )
    list_filter = (
        'is_available', 'is_featured', 'is_bestseller', 
        'is_vegetarian', 'is_vegan', 'category', 'store'
    )
    search_fields = ('name', 'description', 'sku', 'store__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('average_rating', 'total_reviews', 'total_sold', 'view_count', 'created_at', 'updated_at')
    inlines = [ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('store', 'category', 'name', 'slug', 'description', 'short_description', 'main_image')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'is_available', 'sku', 'barcode', 'weight', 'unit')
        }),
        ('Dietary Information', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_organic', 'allergens')
        }),
        ('Status & Features', {
            'fields': ('is_featured', 'is_bestseller')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews', 'total_sold', 'view_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_unavailable', 'mark_as_available']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected products as featured"
    
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    mark_as_unavailable.short_description = "Mark as unavailable"
    
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
    mark_as_available.short_description = "Mark as available"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'display_order', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('product__name', 'alt_text')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price_adjustment', 'stock_quantity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('product__name', 'name', 'sku')


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'action', 'quantity_change', 'new_quantity', 'created_at', 'created_by')
    list_filter = ('action', 'created_at')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('created_at',)