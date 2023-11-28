from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        products = Product.objects.all()

        order = Order.objects.get_or_create(
            delivery_address='Some address',
            user=user,
        )
        order = Order.objects.last()
        for product in products:
            order.products.add(product)
        order.save()
