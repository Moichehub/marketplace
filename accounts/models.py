from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    ROLES = (
        ("buyer", "Покупець"),
        ("seller", "Продавець"),
    )
    is_seller = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=200, unique=True, help_text="Назва вашого магазину")
    store_slug = models.SlugField(unique=True, blank=True, help_text="URL-адреса магазину")
    description = models.TextField(max_length=2000, blank=True, help_text="Опис магазину")
    logo = models.ImageField(upload_to="store_logos/", blank=True, null=True, help_text="Логотип магазину")
    
    phone = models.CharField(max_length=20, blank=True, help_text="Номер телефону")
    email_contact = models.EmailField(blank=True, help_text="Email для зв'язку")
    website = models.URLField(blank=True, help_text="Веб-сайт магазину")
    
    payment_info = models.TextField(max_length=1000, blank=True, help_text="Інформація про способи оплати")
    shipping_info = models.TextField(max_length=1000, blank=True, help_text="Інформація про доставку")
    
    is_active = models.BooleanField(default=True, help_text="Активний магазин")
    auto_accept_orders = models.BooleanField(default=False, help_text="Автоматично приймати замовлення")
    
    facebook = models.URLField(blank=True, help_text="Facebook сторінка")
    instagram = models.URLField(blank=True, help_text="Instagram сторінка")
    telegram = models.CharField(max_length=100, blank=True, help_text="Telegram username")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профіль продавця"
        verbose_name_plural = "Профілі продавців"

    def save(self, *args, **kwargs):
        if not self.store_slug:
            self.store_slug = slugify(self.store_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Store: {self.store_name}"

    @property
    def average_rating(self):
        """Calculate average rating for the seller based on product reviews"""
        from products.models import Review
        reviews = Review.objects.filter(product__seller=self.user)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @property
    def total_reviews(self):
        """Get total number of reviews for seller's products"""
        from products.models import Review
        return Review.objects.filter(product__seller=self.user).count()

    @property
    def total_products(self):
        """Get total number of active products"""
        return self.user.products.filter(is_active=True).count()

    @property
    def total_sales(self):
        """Get total number of completed orders"""
        from orders.models import Order
        return Order.objects.filter(
            items__product__seller=self.user,
            status='paid'
        ).distinct().count()

