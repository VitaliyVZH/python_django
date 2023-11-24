from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='admin')
        order = Order.objects.create(
            delivery_address='st. Right Side, 2 Kalchik d 136',
            promo_code='SOME PROMO',
            user=user,
        )
        self.stdout.write(f'Created order: {order}')
