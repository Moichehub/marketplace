from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SellerProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "is_seller", "is_active", "date_joined"]
    list_filter = ["is_seller", "is_active", "date_joined"]
    search_fields = ["username", "email"]
    ordering = ["-date_joined"]


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ["store_name", "user", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["store_name", "user__username", "description"]
    prepopulated_fields = {"store_slug": ["store_name"]}
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]

    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("user", "store_name", "store_slug", "description", "logo")},
        ),
        ("Контактна інформація", {"fields": ("phone", "email_contact", "website")}),
        (
            "Інформація про оплату та доставку",
            {"fields": ("payment_info", "shipping_info")},
        ),
        ("Налаштування магазину", {"fields": ("is_active", "auto_accept_orders")}),
        ("Соціальні мережі", {"fields": ("facebook", "instagram", "telegram")}),
        (
            "Метадані",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
