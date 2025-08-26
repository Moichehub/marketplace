from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "update-cart-item/<int:item_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("history/", views.order_history, name="order_history"),
]
