from django.core.management.base import BaseCommand
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'List all products with their URLs for easy access'

    def handle(self, *args, **options):
        self.stdout.write('📦 Listing all products...')
        
        products = Product.objects.all().order_by('seller__username', 'name')
        
        if not products:
            self.stdout.write(self.style.WARNING('No products found in the system'))
            return
        
        current_seller = None
        for product in products:
            if current_seller != product.seller:
                current_seller = product.seller
                self.stdout.write(f'\n🏪 Seller: {product.seller.username}')
                self.stdout.write('─' * 50)
            
            self.stdout.write(f'  📦 {product.name}')
            self.stdout.write(f'     URL: /products/{product.slug}/')
            self.stdout.write(f'     Edit: /products/{product.slug}/edit/')
            self.stdout.write(f'     Delete: /products/{product.slug}/delete/')
            self.stdout.write(f'     Price: {product.price} ₴')
            self.stdout.write(f'     Stock: {product.stock}')
            self.stdout.write(f'     Status: {"✅ Active" if product.is_active else "⏸️ Inactive"}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Total products: {products.count()}'))
        self.stdout.write('\n💡 Tip: Use these URLs to test product functionality!')
