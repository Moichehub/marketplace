from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, Review
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Add sample reviews to products for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of reviews to create per product'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get all products
        products = Product.objects.filter(is_active=True)
        if not products.exists():
            self.stdout.write(
                self.style.ERROR('No active products found. Please create some products first.')
            )
            return
        
        # Get buyer users (non-sellers)
        buyers = User.objects.filter(is_seller=False)
        if not buyers.exists():
            self.stdout.write(
                self.style.ERROR('No buyer users found. Please create some buyer accounts first.')
            )
            return
        
        # Sample review comments
        sample_comments = [
            "Відмінний товар! Дуже задоволений покупкою.",
            "Якість на висоті, рекомендую всім!",
            "Швидка доставка, товар відповідає опису.",
            "Дуже хороша ціна за таку якість.",
            "Купую вже другий раз, все супер!",
            "Товар якісний, але доставка трохи затягнулася.",
            "Рекомендую цей магазин, все на рівні.",
            "Відмінна якість, буду замовляти ще.",
            "Товар прийшов вчасно, все сподобалося.",
            "Дуже задоволений покупкою, дякую!",
            "Якість товару відповідає очікуванням.",
            "Швидко і якісно, рекомендую!",
            "Товар якісний, але міг би бути трохи дешевшим.",
            "Відмінний сервіс, все на найвищому рівні.",
            "Дуже задоволений, обов'язково куплю ще.",
        ]
        
        reviews_created = 0
        
        for product in products:
            # Create reviews for each product
            for i in range(min(count, len(buyers))):
                buyer = buyers[i]
                
                # Check if user already reviewed this product
                if Review.objects.filter(product=product, user=buyer).exists():
                    continue
                
                # Create review
                rating = random.randint(3, 5)  # Mostly positive ratings
                comment = random.choice(sample_comments)
                
                review = Review.objects.create(
                    product=product,
                    user=buyer,
                    rating=rating,
                    comment=comment
                )
                
                reviews_created += 1
                
                self.stdout.write(
                    f'Created review: {buyer.username} rated {product.name} with {rating} stars'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {reviews_created} reviews across {products.count()} products'
            )
        )
        
        # Show some statistics
        for product in products:
            avg_rating = product.average_rating
            review_count = product.review_count
            self.stdout.write(
                f'{product.name}: {avg_rating:.1f} stars ({review_count} reviews)'
            )
