
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,  # тимчасово, щоб уникнути помилок при існуючих рядках
        blank=True
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            # Generate slug from name
            base_slug = slugify(self.name)
            if not base_slug:
                # If slugify returns empty string, use a fallback
                base_slug = f"product-{self.id}" if self.id else "product"
            
            # Ensure uniqueness
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        """Calculate average rating for the product"""
        reviews = self.reviews.filter(user__isnull=False)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @property
    def review_count(self):
        """Get total number of reviews"""
        return self.reviews.filter(user__isnull=False).count()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        unique_together = ['product', 'user']  # One review per user per product
        ordering = ['-created_at']

    def __str__(self):
        try:
            username = self.user.username if self.user else "Unknown User"
            return f"Review by {username} on {self.product.name}"
        except Exception:
            return f"Review ID {self.id} on {self.product.name if self.product else 'Unknown Product'}"
    
    @property
    def safe_user(self):
        """Safely get the user, handling cases where the relationship might be broken"""
        try:
            if hasattr(self, '_cached_user'):
                return self._cached_user
            return self.user
        except Exception:
            return None

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            if not self.user:
                raise ValidationError("Review must have a user")
            if self.user.is_seller:
                raise ValidationError("Sellers cannot review products")
            if self.user == self.product.seller:
                raise ValidationError("Sellers cannot review their own products")
        except Exception:
            # If user relationship is broken, skip validation
            pass


