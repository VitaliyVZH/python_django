import json

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect

from shopapp.models import Order, Product


def save_json_orders(file):
    """
    Функция преобразовывает данные из байтов к словарю JSON (десериализация).
    Проверяет на валидность к базе данных.
    Создаёт и сохраняет новый заказ.
    Выводит сообщение в админ панель об успешности сохранения данных.
    """
    json_orders = json.load(file)['orders']
    try:
        for key in json_orders:
            user = User.objects.get(username=key['user'])
            products = [Product.objects.get(name=product_name) for product_name in key['products']]

            Order.objects.create(
                delivery_address=key['delivery_address'],
                promo_code=key['promo_code'],
                user=user,
            )
            order = Order.objects.last()
            for product in products:
                order.products.add(product)
            order.save()
        return redirect("..")
    except Exception:
        return False
