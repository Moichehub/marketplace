from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()

class Command(BaseCommand):
    help = 'Diagnose and fix seller button issues'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Diagnosing seller button issues...')
        
        # Check users
        total_users = User.objects.count()
        sellers = User.objects.filter(is_seller=True)
        buyers = User.objects.filter(is_seller=False)
        
        self.stdout.write(f'📊 User Statistics:')
        self.stdout.write(f'   Total users: {total_users}')
        self.stdout.write(f'   Sellers: {sellers.count()}')
        self.stdout.write(f'   Buyers: {buyers.count()}')
        
        # Test seller URLs
        if sellers.exists():
            seller = sellers.first()
            self.stdout.write(f'\n🧪 Testing URLs for seller: {seller.username}')
            
            client = Client()
            client.force_login(seller)
            
            # Test create URL
            create_response = client.get(reverse('products:create'))
            self.stdout.write(f'   Create URL: {create_response.status_code}')
            
            # Test dashboard URL
            dashboard_response = client.get(reverse('products:seller_dashboard'))
            self.stdout.write(f'   Dashboard URL: {dashboard_response.status_code}')
            
            # Test profile URL
            profile_response = client.get(reverse('accounts:seller_profile_view'))
            self.stdout.write(f'   Profile URL: {profile_response.status_code}')
            
            if create_response.status_code == 200 and dashboard_response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ All seller URLs are working correctly!'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ Some URLs are not working as expected'))
        else:
            self.stdout.write(self.style.ERROR('❌ No sellers found in the system'))
        
        # Provide instructions
        self.stdout.write(f'\n📋 Instructions to fix seller buttons:')
        self.stdout.write(f'1. Make sure you are logged in as a seller')
        self.stdout.write(f'2. Available seller accounts:')
        for seller in sellers[:5]:
            self.stdout.write(f'   - {seller.username}')
        self.stdout.write(f'3. Login at: http://127.0.0.1:8000/accounts/login/')
        self.stdout.write(f'4. Use any seller username with password: pass123')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Diagnosis complete!'))
