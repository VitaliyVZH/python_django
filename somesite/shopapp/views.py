from django.contrib.auth.models import Group, Permission
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from shopapp.forms import ProductForm, GroupCreateForm
from shopapp.models import Product, Order


class ShopView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'groups': Group.objects.prefetch_related('permissions').all(),
            "form": GroupCreateForm()
        }
        return render(request, 'shopapp/base.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(reverse("shopapp:base"))


class ProductDetailViews(DetailView):
    """
    Класс реализует детали продуктов
    """
    template_name = 'shopapp/product_details.html'
    model = Product
    context_object_name = 'product'

    # def get(self, request: HttpRequest, pk: int):
    #     product = get_object_or_404(Product, pk=pk)
    #     context = {
    #         "product": product,
    #     }
    #
    #     return render(request, "shopapp/product_details.html", context=context)


class ProductsListView(ListView):
    """
    Класс реализует список имеющихся продуктов
    """
    template_name = "shopapp/products.html"
    model = Product
    context_object_name = 'products'
    # queryset = Order.objects.prefetch_related('user')

    # def get_context_data(self, **kwargs):
    #     """
    #     Функция переопределяет/определяет значение 'products' и присваивает ему Queryset Product.
    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #     return context


class ProductCreateView(CreateView):
    """
    Класс реализует создание нового продукта
    """
    template_name = "shopapp/product_create.html"
    fields = 'name', 'description', 'archived'
    model = Product
    success_url = reverse_lazy("shopapp:products")


class ProductUpdateView(UpdateView):
    """
    Класс реализует обновление выбранного продукта
    """
    template_name = "shopapp/product_update.html"
    model = Product
    fields = "name", "description", "price", "archived",
    context_object_name = "product"

    def get_success_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    """
    Класс реализует удаление выбранного продукта
    """
    template_name = "shopapp/product_delete.html"
    model = Product
    success_url = reverse_lazy("shopapp:products")
    context_object_name = "product"


class OrdersList(ListView):
    """
    Класс реализует страницу со списком заказом
    """
    template_name = "shopapp/orders_list.html"
    model = Order
    context_object_name = "orders"


class OrderDetailsView(DetailView):
    """
    Класс реализует список заказов
    """
    template_name = 'shopapp/order_details.html'
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    context_object_name = 'order'


class OrderCreateView(CreateView):
    """
    Класс реализует создание нового заказа
    """
    template_name = "shopapp/order_create.html"
    fields = "delivery_address", "user", "products",
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    """
    Класс реализует обновление объявления
    """
    template_name = "shopapp/order_update.html"
    model = Order
    fields = "delivery_address", "user", "products",

    def get_success_url(self):
        return reverse("shopapp:order_details", kwargs={'pk': self.object.pk})

