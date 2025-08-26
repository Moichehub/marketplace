from django.contrib import admin

from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "seller",
        "category",
        "price",
        "stock",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "category", "seller", "created_at"]
    search_fields = ["name", "description", "seller__username"]
    prepopulated_fields = {"slug": ["name"]}
    list_editable = ["price", "stock", "is_active"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "created_at"]
    list_filter = ["rating", "created_at", "product__seller"]
    search_fields = ["product__name", "user__username", "comment"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["rating"]
