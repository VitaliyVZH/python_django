from django.urls import path

from .views import (
    ShopView,
    ProductsListView,
    ProductDetailViews,
    ProductDeleteView,
    OrdersList,
    OrderDetailsView,
    ProductCreateView,
    ProductUpdateView,
    OrderCreateView,
    OrderUpdateView,
)

app_name = 'shopapp'
urlpatterns = [
    path('', ShopView.as_view(), name='base'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/details/<int:pk>/', ProductDetailViews.as_view(), name='product_details'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersList.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/details/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
]
