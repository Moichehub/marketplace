# Generated manually for SellerProfile model

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_role_user_is_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(help_text='Назва вашого магазину', max_length=200, unique=True)),
                ('store_slug', models.SlugField(blank=True, help_text='URL-адреса магазину', unique=True)),
                ('description', models.TextField(blank=True, help_text='Опис магазину', max_length=2000)),
                ('logo', models.ImageField(blank=True, help_text='Логотип магазину', null=True, upload_to='store_logos/')),
                ('phone', models.CharField(blank=True, help_text='Номер телефону', max_length=20)),
                ('email_contact', models.EmailField(blank=True, help_text='Email для зв\'язку', max_length=254)),
                ('website', models.URLField(blank=True, help_text='Веб-сайт магазину')),
                ('payment_info', models.TextField(blank=True, help_text='Інформація про способи оплати', max_length=1000)),
                ('shipping_info', models.TextField(blank=True, help_text='Інформація про доставку', max_length=1000)),
                ('is_active', models.BooleanField(default=True, help_text='Активний магазин')),
                ('auto_accept_orders', models.BooleanField(default=False, help_text='Автоматично приймати замовлення')),
                ('facebook', models.URLField(blank=True, help_text='Facebook сторінка')),
                ('instagram', models.URLField(blank=True, help_text='Instagram сторінка')),
                ('telegram', models.CharField(blank=True, help_text='Telegram username', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_profile', to='accounts.user')),
            ],
            options={
                'verbose_name': 'Профіль продавця',
                'verbose_name_plural': 'Профілі продавців',
            },
        ),
    ]
