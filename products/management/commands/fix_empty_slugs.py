from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Product


class Command(BaseCommand):
    help = "Fix products with empty slugs by generating proper slugs"

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing products with empty slugs...")

        empty_slugs = Product.objects.filter(slug="")

        if not empty_slugs:
            self.stdout.write(
                self.style.SUCCESS("✅ No products with empty slugs found")
            )
            return

        self.stdout.write(f"Found {empty_slugs.count()} products with empty slugs")

        fixed_count = 0
        for product in empty_slugs:
            self.stdout.write(f"  Fixing: {product.name} (ID: {product.id})")

            base_slug = slugify(product.name)
            if not base_slug:

                base_slug = f"product-{product.id}"

            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(id=product.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            product.slug = slug
            product.save()

            self.stdout.write(f"    → New slug: {slug}")
            fixed_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Successfully fixed {fixed_count} products")
        )
        self.stdout.write("✅ All products now have proper slugs")
