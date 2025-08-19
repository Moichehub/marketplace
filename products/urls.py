from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("create/", views.product_create, name="create"),
    path("dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("<slug:slug>/edit/", views.product_update, name="update"),
    path("<slug:slug>/delete/", views.product_delete, name="delete"),
    path("<slug:slug>/review/", views.add_review, name="add_review"),
    path("<slug:slug>/", views.product_detail, name="detail"),
]
