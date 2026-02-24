from django.contrib import admin
from .models import Category, Product, ProductVariant, ChannelListing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ("sku", "name", "price_override", "stock", "attributes")
    readonly_fields = ("created_at",)


class ChannelListingInline(admin.TabularInline):
    model = ChannelListing
    extra = 0
    fields = ("channel", "status", "external_id", "price_override", "last_sync_at")
    readonly_fields = ("last_sync_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "seller", "category", "base_price", "base_stock", "is_active", "created_at")
    list_filter = ("is_active", "category", "seller")
    search_fields = ("sku", "name", "seller__business_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [ProductVariantInline, ChannelListingInline]

    fieldsets = (
        ("Identificación", {"fields": ("seller", "category", "sku", "name", "description")}),
        ("Precios y stock", {"fields": ("base_price", "base_stock", "is_active")}),
        ("Atributos por marketplace", {"fields": ("marketplace_data", "images"), "classes": ("collapse",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(ChannelListing)
class ChannelListingAdmin(admin.ModelAdmin):
    list_display = ("product", "channel", "status", "external_id", "price_override", "last_sync_at")
    list_filter = ("status", "channel")
    search_fields = ("product__sku", "product__name", "external_id")
    readonly_fields = ("last_sync_at", "created_at", "updated_at")
