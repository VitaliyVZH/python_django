from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order, Product
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('created_by').all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    # filterset_fields = [
    #     'name',
    #     'description',
    #     'price',
    #     'discount',
    #     'count',
    #     'create_at',
    #     'archived',
    #     'created_by',
    # ]
    search_fields = [
        'name',
        'description',
        'price',
        'discount',
        'count',
        'create_at',
        'archived',
        'created_by',
    ]
    ordering_fields = [
        'name',
        'description',
        'price',
        'discount',
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('products').select_related('user').all()
    serializer_class = OrderSerializer
    filter_backends = [
        # SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    # filterset_fields = [
    #     'delivery_address',
    #     'promo_code',
    #     'created_at',
    #     'user',
    #     'products',
    # ]
    # search_fields = [
    #     'delivery_address',
    #     'promo_code',
    #     'created_at',
    #     'user',
    #     'products',
    # ]
    ordering_fields = [
        'delivery_address',
        'promo_code',
        'created_at',
        'user',
        'products',
    ]
