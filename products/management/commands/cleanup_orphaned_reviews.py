from django.core.management.base import BaseCommand
from products.models import Review


class Command(BaseCommand):
    help = 'Clean up orphaned reviews that don\'t have associated users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find orphaned reviews (reviews without users)
        orphaned_reviews = Review.objects.filter(user__isnull=True)
        count = orphaned_reviews.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No orphaned reviews found. Database is clean!')
            )
            return
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} orphaned reviews:'
                )
            )
            for review in orphaned_reviews[:10]:  # Show first 10
                self.stdout.write(f'  - Review ID {review.id} for product "{review.product.name}"')
            if count > 10:
                self.stdout.write(f'  ... and {count - 10} more')
        else:
            # Actually delete the orphaned reviews
            orphaned_reviews.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} orphaned reviews'
                )
            )
        
        # Also check for reviews with invalid users (users that don't exist)
        invalid_user_reviews = Review.objects.filter(user__isnull=False).exclude(
            user__in=Review.objects.values_list('user', flat=True).distinct()
        )
        invalid_count = invalid_user_reviews.count()
        
        if invalid_count > 0:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f'DRY RUN: Would delete {invalid_count} reviews with invalid users'
                    )
                )
            else:
                invalid_user_reviews.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted {invalid_count} reviews with invalid users'
                    )
                )
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS('Database cleanup completed successfully!')
            )
