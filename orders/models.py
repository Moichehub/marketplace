from django.db import models
from accounts.models import User
from products.models import Product

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_seller": False})
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("paid", "Paid"), ("shipped", "Shipped")],
        default="pending"
    )

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
