from shopapp.models import Order, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'discount',
            'count',
            'create_at',
            'archived',
            'created_by',
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'delivery_address',
            'promo_code',
            'created_at',
            'user',
            'products',
        ]
