from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]

    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    # def is_upperclass(self):
    #     return self.year_in_school in {self.JUNIOR, self.SENIOR}

    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False, blank=False)
    test = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')

    def __str__(self):
        return f'pk={self.pk}, name: {self.name!r}'


class Order(models.Model):
    delivery_address = models.TextField(max_length=100, blank=False)
    promocode = models.CharField(max_length=25, null=False, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f'№{self.pk}, delivery address: {self.delivery_address!r}'
