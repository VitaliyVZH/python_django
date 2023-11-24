
from rest_framework.routers import DefaultRouter
from django.urls import path, include


from shopapp.api import ProductViewSet, OrderViewSet
from .views import (
    shop_index,
    groups_list,
    ProductListView,
    ProductDetailsView,
    ProductUpdateView,
    ProductCreateView,
    ProductDeleteView,
    OrderListView,
    OrderCreateView,
    OrderDetailsView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersDataExportView,
    LatestProductsFeed,
    UserOrdersListView,
    user_orders_export_data,
)

routers_product = DefaultRouter()
routers_product.register('products', ProductViewSet)

routers_order = DefaultRouter()
routers_order.register('orders', OrderViewSet)

app_name = 'shopapp'
urlpatterns = [ 
    path('', shop_index, name='index'),
    path('api/products/', include(routers_product.urls)),
    path('api/orders/', include(routers_order.urls)),
    path('groups/', groups_list, name='groups_list'),
    path('products/<str:name>/', ProductListView.as_view(), name='products_list'),
    path('products/create/<str:name>', ProductCreateView.as_view(), name='product_create'),
    path('products/<str:name>/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<str:name>/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<str:name>/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_archive'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create', OrderCreateView.as_view(), name='order_create'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders_export'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders'),
    path('users/<int:user_id>/orders/export/', user_orders_export_data, name='user_orders_export'),
]
