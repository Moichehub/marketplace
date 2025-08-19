from django.contrib import admin
from .models import Order, OrderItem, PaymentMethod

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    ordering = ['name']

admin.site.register(Order)
admin.site.register(OrderItem)

