from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **options):
        products_data = [
            {'name': 'iPhone 16', 'price': 65000, 'category_id': 1},
            {'name': 'Samsung Galaxy S22', 'price': 70000, 'category_id': 2},
            {'name': 'Samsung A35', 'price': 60000, 'category_id': 2},
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(**data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {data["name"]}'))
