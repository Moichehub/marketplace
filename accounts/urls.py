from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("seller/register/", views.seller_register, name="seller_register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    # Seller profile URLs
    path("seller/profile/setup/", views.seller_profile_setup, name="seller_profile_setup"),
    path("seller/profile/edit/", views.seller_profile_edit, name="seller_profile_edit"),
    path("seller/profile/", views.seller_profile_view, name="seller_profile_view"),
    path("store/<slug:store_slug>/", views.seller_store_view, name="seller_store_view"),
]


