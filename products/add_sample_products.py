from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Add sample products to sellers'

    def handle(self, *args, **options):
        self.stdout.write("=== Adding Sample Products to Sellers ===\n")
        
        # Create categories
        categories_data = [
            'Electronics',
            'Clothing', 
            'Books',
            'Home & Garden',
            'Sports',
            'Toys & Games',
            'Automotive',
            'Health & Beauty'
        ]
        
        categories = {}
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = category
            if created:
                self.stdout.write(f"✓ Created category: {cat_name}")
            else:
                self.stdout.write(f"✓ Category exists: {cat_name}")
        
        # Create or get sellers
        sellers_data = [
            {
                'username': 'techstore',
                'email': 'techstore@example.com',
                'name': 'TechStore'
            },
            {
                'username': 'fashionboutique', 
                'email': 'fashion@example.com',
                'name': 'Fashion Boutique'
            },
            {
                'username': 'bookworld',
                'email': 'books@example.com', 
                'name': 'BookWorld'
            },
            {
                'username': 'homeimprovement',
                'email': 'home@example.com',
                'name': 'Home Improvement'
            }
        ]
        
        sellers = {}
        for seller_data in sellers_data:
            seller, created = User.objects.get_or_create(
                username=seller_data['username'],
                defaults={
                    'email': seller_data['email'],
                    'is_seller': True
                }
            )
            if created:
                seller.set_password('sellerpass123')
                seller.save()
                self.stdout.write(f"✓ Created seller: {seller_data['name']}")
            else:
                self.stdout.write(f"✓ Seller exists: {seller_data['name']}")
            sellers[seller_data['username']] = seller
        
        # Define products for each seller
        products_data = {
            'techstore': [
                {
                    'name': 'iPhone 15 Pro',
                    'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
                    'price': 999.99,
                    'stock': 25,
                    'category': 'Electronics'
                },
                {
                    'name': 'MacBook Air M2',
                    'description': 'Lightweight laptop with M2 chip, perfect for work and creativity',
                    'price': 1199.99,
                    'stock': 15,
                    'category': 'Electronics'
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'description': 'Premium noise-cancelling headphones with exceptional sound quality',
                    'price': 349.99,
                    'stock': 30,
                    'category': 'Electronics'
                },
                {
                    'name': 'Samsung Galaxy S24',
                    'description': 'Android flagship with AI features and stunning display',
                    'price': 899.99,
                    'stock': 20,
                    'category': 'Electronics'
                }
            ],
            'fashionboutique': [
                {
                    'name': 'Classic Denim Jacket',
                    'description': 'Timeless denim jacket perfect for any casual occasion',
                    'price': 89.99,
                    'stock': 50,
                    'category': 'Clothing'
                },
                {
                    'name': 'Premium Cotton T-Shirt',
                    'description': 'Soft, breathable cotton t-shirt in various colors',
                    'price': 24.99,
                    'stock': 100,
                    'category': 'Clothing'
                },
                {
                    'name': 'Leather Crossbody Bag',
                    'description': 'Stylish leather bag with adjustable strap',
                    'price': 129.99,
                    'stock': 25,
                    'category': 'Clothing'
                },
                {
                    'name': 'Running Shoes',
                    'description': 'Comfortable running shoes with excellent support',
                    'price': 79.99,
                    'stock': 40,
                    'category': 'Clothing'
                }
            ],
            'bookworld': [
                {
                    'name': 'The Great Gatsby',
                    'description': 'F. Scott Fitzgerald\'s classic American novel',
                    'price': 12.99,
                    'stock': 75,
                    'category': 'Books'
                },
                {
                    'name': 'Python Programming Guide',
                    'description': 'Comprehensive guide to Python programming for beginners',
                    'price': 29.99,
                    'stock': 30,
                    'category': 'Books'
                },
                {
                    'name': 'The Art of War',
                    'description': 'Sun Tzu\'s ancient Chinese military treatise',
                    'price': 9.99,
                    'stock': 60,
                    'category': 'Books'
                },
                {
                    'name': 'Harry Potter and the Sorcerer\'s Stone',
                    'description': 'J.K. Rowling\'s magical first book in the series',
                    'price': 15.99,
                    'stock': 45,
                    'category': 'Books'
                }
            ],
            'homeimprovement': [
                {
                    'name': 'LED Desk Lamp',
                    'description': 'Adjustable LED lamp with multiple brightness levels',
                    'price': 49.99,
                    'stock': 35,
                    'category': 'Home & Garden'
                },
                {
                    'name': 'Garden Tool Set',
                    'description': 'Complete set of essential gardening tools',
                    'price': 89.99,
                    'stock': 20,
                    'category': 'Home & Garden'
                },
                {
                    'name': 'Kitchen Mixer',
                    'description': 'Professional stand mixer for baking enthusiasts',
                    'price': 199.99,
                    'stock': 15,
                    'category': 'Home & Garden'
                },
                {
                    'name': 'Smart Thermostat',
                    'description': 'WiFi-enabled thermostat with energy saving features',
                    'price': 149.99,
                    'stock': 25,
                    'category': 'Home & Garden'
                }
            }
        }
        
        # Create products
        total_created = 0
        for seller_username, products in products_data.items():
            seller = sellers[seller_username]
            self.stdout.write(f"\n📦 Adding products for {seller.username}:")
            
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    seller=seller,
                    defaults={
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'stock': product_data['stock'],
                        'category': categories[product_data['category']],
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f"  ✓ Created: {product.name} - ${product.price}")
                    total_created += 1
                else:
                    self.stdout.write(f"  ✓ Already exists: {product.name}")
        
        # Summary
        self.stdout.write(f"\n🎉 Successfully added {total_created} new products!")
        self.stdout.write(f"📊 Total sellers: {len(sellers)}")
        self.stdout.write(f"📊 Total categories: {len(categories)}")
        
        self.stdout.write("\n=== Marketplace Summary ===")
        self.stdout.write(f"👥 Total users: {User.objects.count()}")
        self.stdout.write(f"👨‍💼 Sellers: {User.objects.filter(is_seller=True).count()}")
        self.stdout.write(f"🛍️ Total products: {Product.objects.count()}")
        self.stdout.write(f"📚 Categories: {Category.objects.count()}")
        
        self.stdout.write("\n✅ Products have been successfully added to sellers!")
        self.stdout.write("🌐 You can now browse the marketplace at http://127.0.0.1:8000/products/")
