from django.core.management.base import BaseCommand
from django.utils.text import slugify
from uuid import uuid4
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Fix all products and categories with empty slugs'

    def handle(self, *args, **options):
        self.stdout.write('Fixing empty slugs...')
        
        # Fix categories with empty slugs
        categories_fixed = 0
        for category in Category.objects.filter(slug=''):
            base_slug = slugify(category.name, allow_unicode=True)
            if not base_slug:
                base_slug = f"category-{uuid4().hex[:8]}"
            unique_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exclude(pk=category.pk).exists():
                counter += 1
                unique_slug = f"{base_slug}-{counter}"
            category.slug = unique_slug
            category.save()
            categories_fixed += 1
            self.stdout.write(f'Fixed category: {category.name} -> {category.slug}')
        
        # Fix products with empty slugs
        products_fixed = 0
        for product in Product.objects.filter(slug=''):
            base_slug = slugify(product.name, allow_unicode=True)
            if not base_slug:
                base_slug = f"product-{uuid4().hex[:8]}"
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exclude(pk=product.pk).exists():
                counter += 1
                unique_slug = f"{base_slug}-{counter}"
            product.slug = unique_slug
            product.save()
            products_fixed += 1
            self.stdout.write(f'Fixed product: {product.name} -> {product.slug}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {categories_fixed} categories and {products_fixed} products!'
            )
        )
