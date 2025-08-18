from django.urls import path, register_converter
from . import views
from .converters import UnicodeSlugConverter

register_converter(UnicodeSlugConverter, 'unicode_slug')

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("create-sample-data/", views.create_sample_data, name="create_sample_data"),
    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/create/", views.product_create, name="create"),
    path("seller/<unicode_slug:slug>/edit/", views.product_update, name="update"),
    path("seller/<unicode_slug:slug>/delete/", views.product_delete, name="delete"),
    path("<unicode_slug:slug>/", views.product_detail, name="detail"),
]
