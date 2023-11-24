from datetime import datetime, timezone

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='user_test', password='password_test')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='Test address',
            promo_code='Test promocode',
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_detail(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk}),
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promo_code)
        self.assertEqual(self.order.pk, response.context['order'].pk)


class OrdersDataExportViewTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
        'products-fixture.json',
        'users-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.user.is_staff = True
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_data_export(self):
        response = self.client.get(reverse(
            'shopapp:orders_export'),
        )

        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo_code': order.promo_code,
                # 'created_at': datetime.strftime(order.created_at, '%Y-%m-%dT%H:%M:%S.%fZ'),  # order.created_at
                'user': order.user.username,
                'products': [product.id for product in order.products.all()],
            }
            for order in Order.objects.order_by('pk').all()
        ]

        self.assertEqual(response.json()['order'], expected_data)
