from django.core.management.base import BaseCommand
from orders.models import PaymentMethod


class Command(BaseCommand):
    help = 'Add default payment methods to the system'

    def handle(self, *args, **options):
        self.stdout.write('💳 Adding default payment methods...')
        
        payment_methods = [
            {
                'name': 'Банківська карта',
                'description': 'Оплата картою Visa, MasterCard або іншими картами',
                'icon': '💳',
                'is_active': True
            },
            {
                'name': 'Готівка при отриманні',
                'description': 'Оплата готівкою при отриманні товару',
                'icon': '💵',
                'is_active': True
            },
            {
                'name': 'Банківський переказ',
                'description': 'Переказ на банківський рахунок',
                'icon': '🏦',
                'is_active': True
            },
            {
                'name': 'PayPal',
                'description': 'Оплата через PayPal',
                'icon': '📱',
                'is_active': True
            },
            {
                'name': 'Криптовалюта',
                'description': 'Оплата криптовалютою (Bitcoin, Ethereum)',
                'icon': '₿',
                'is_active': False  # Disabled by default
            }
        ]
        
        created_count = 0
        for method_data in payment_methods:
            payment_method, created = PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            
            if created:
                self.stdout.write(f'  ✅ Created: {payment_method.icon} {payment_method.name}')
                created_count += 1
            else:
                self.stdout.write(f'  ℹ️  Already exists: {payment_method.icon} {payment_method.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully added {created_count} payment methods'))
        self.stdout.write('✅ Payment methods are now available for selection')
