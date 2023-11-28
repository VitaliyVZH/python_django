from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    products = [
        {
            'name': 'Laptop',
            'description': '',
            'price': 15,
        },
        {
            'name': 'Desctop',
            'description': 'New',
            'price': 1.5,
        },
    ]

    def handle(self, *args, **options):
        for product in self.products:
            Product.objects.get_or_create(
                name=product['name'],
                description=product['description'],
                price=product['price']
            )

