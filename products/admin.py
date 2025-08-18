from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "category", "price", "stock", "is_active")
    list_filter = ("is_active", "category", "seller")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}

