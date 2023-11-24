import logging

from timeit import default_timer

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Product, Order

log = logging.getLogger(__name__)


def shop_index(request: HttpRequest) -> HttpResponse:
    products = [
        ('laptop', 2569),
        ('desktop', 75000),
        ('smart', 7000),
        ('pop', 3719),
        ('jawa', 71)

    ]
    context = {
        'time_running': default_timer(),
        'products': products,
        'all_products': Product.objects.all(),
    }
    return render(request=request, template_name='shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest) -> HttpResponse:
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request=request, template_name='shopapp/group-list.html', context=context)


class ProductListView(ListView):
    model = Product


class ProductDetailsView(DetailView):
    model = Product


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'add_product',
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'count', 'archived'
    success_url = reverse_lazy('shopapp:products_list')

    def get_success_url(self):
        return reverse(
            'shopapp:products_list', kwargs={'name': self.request.user}
        )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_superuser or \
                Product.objects.all().filter(created_by_id=self.request.user).filter(name=self.get_object().name):
            return True
        return False

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'count', 'archived'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details', kwargs={'pk': self.object.pk, 'name': self.request.user}
        )


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_product',
    model = Product

    # success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse(
            'shopapp:products_list', kwargs={'name': self.request.user}
        )


class OrderListView(LoginRequiredMixin, ListView):
    model = Order


class OrderCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'add_product',
    model = Order
    fields = 'delivery_address', 'promo_code', 'user', 'products'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderDetailsView(DetailView):
    model = Order


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'change_product',
    model = Order
    fields = 'user', 'products'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('shopapp:order_details', kwargs={'pk': self.object.pk})


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_product',
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersDataExportView(UserPassesTestMixin, View):
    """
    Класс реализует экспорт данных в файл в json формате
    """
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').select_related('user').prefetch_related('products').all()
        order_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo_code': order.promo_code,
                # 'created_at': order.created_at,
                'user': order.user.username,
                'products': [product.id for product in order.products.all()],
            }
            for order in orders]
        return JsonResponse({'order': order_data})


class LatestProductsFeed(Feed):
    """
    Класс отдаёт данные RSS каналам.
    """
    title = 'Магазин продуктов'  # текст будет отображаться над статьёй
    description = 'Новые продукты'
    link = reverse_lazy('shopapp:products_list', kwargs={'name': 'Lol'})

    def items(self):
        """
        Возвращает список продуктов, можно фильтровать, сортировать
        """
        return Product.objects.filter(archived=False).order_by('-create_at')[:3]

    def item_title(self, item: Product):  # возвращает заголовок статьи в ленту
        return item.name

    def item_description(self, item: Product):  # возвращает описание товара с ограничением по символам
        if item.description:
            return item.description[:100]
        return 'No description'


class UserOrdersListView(UserPassesTestMixin, ListView):
    """
    Клас принимает на вход id пользователя и возвращает список заказов пользователя
    """

    def test_func(self):
        """
        Функция относится к классу UserPassesTestMixin и реализует проверку, если возвращается True,
        тогда класс UserOrdersListView будет работать
        """
        return self.request.user.is_staff or (self.request.user.is_authenticated and
                                              self.kwargs['user_id'] == self.request.user.id)

    template_name = 'shopapp/user_orders.html'  # путь к шаблону
    context_object_name = 'user_orders'  # имя, по которому будет доступ к данным внутри шаблона

    def get_queryset(self, **kwargs):
        """
        Функция определяет данные, которые будет принимать класс UserOrdersListView
        и которыми можно оперировать в шаблоне
        """
        owner = get_object_or_404(User, pk=self.kwargs['user_id'])  # получаем объект пользователя
        orders = Order.objects.filter(user=owner).all()  # получаем заказы отфильтрованные по пользователю
        context = {
            'user': owner,
            'orders': orders,
        }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def user_orders_export_data(request: HttpRequest, user_id: int):
    """
    Функция принимает id пользователя, получает пользователя и его заказы, далее формирует словарь
    с заказами пользователя и отправляет его в json формате, если ранее данные подгружались,
    в этом случае они берутся из кэша
    """

    cache_key = f'user_orders_{user_id}'  # индивидуальный ключ кэша для каждого пользователя
    context = cache.get(cache_key)  # проверка наличия ключа в кэше
    if context is None:  # если ключа в кэше не найден
        user = get_object_or_404(User, pk=user_id)  # получаем из базы пользователя по id
        orders = Order.objects.filter(user=user).all().order_by('-pk')  # получаем из базы список заказа пользователя
        context = [
            {
                'user': user.username,
                'orders': [
                    {
                     'pk': order.pk,
                     'delivery_address': order.delivery_address,
                     'products': [product.id for product in order.products.all()],
                    }
                    for order in orders]
            }
        ]
        cache.set(cache_key, context, 60 * 2)  # создаём кэш с указанием ключа и временем существования
    return JsonResponse({'orders': context})
