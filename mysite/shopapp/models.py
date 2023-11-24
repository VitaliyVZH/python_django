from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Класс Product создаёт таблицу в db
    """
    class Meta:
        ordering = ['pk', 'name', ]
        verbose_name = _('Product')
        verbose_name_plural = _('Product')

    def __str__(self):
        return f'Product № {self.pk}, product name: {self.name!r}'

    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=False)
    discount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    count = models.PositiveSmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        """
        Функция возвращает ссылку на продукт при её запросе
        """
        return reverse('shopapp:product_details', kwargs={'pk': self.pk, 'name': self.name})


class Order(models.Model):
    class Meta:
        ordering = ['pk', ]  # Sort by name,  ['-name'], or ['name', 'price']
        # db_table = ''
        verbose_name = _('Orders')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(blank=True)
    promo_code = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f'Order №{self.pk}, delivery address={self.delivery_address!r}'
