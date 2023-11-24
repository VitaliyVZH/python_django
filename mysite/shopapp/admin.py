from django.contrib import admin, messages

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from shopapp.models import Product, Order
from .admin_mixins import ExportAsCSVMixin
from .common import save_json_orders
from .forms import JSONImportForm


def short_texts(text: str) -> str:
    if len(text) < 50:
        return text
    return ''.join([text[:50], '...'])


class OrderInline(admin.StackedInline):
    model = Product.orders.through


@admin.action(description='Product archiving')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Product unarchiving')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'count', 'create_at', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description', 'price',
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price', {
            'fields': ('price', 'discount'),
        }),
        ('Archived', {
            'fields': ('archived',),
            'classes': ('collapse',),
        })
    ]

    def description_short(self, obj: Product):
        return short_texts(obj.description)


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Класс определяет внешний вид и функциональность административной панели заказов.
    """
    change_list_template = 'shopapp/orders_changelist.html'
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'delivery_address', 'promo_code', 'created_at', 'user_verbose'
    list_display_links = 'delivery_address',
    search_fields = 'delivery_address', 'promo_code', 'user_verbose', 'created_at'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_json(self, request: HttpRequest) -> HttpResponse:
        """
        Функция принимает json файл с заказами из админ панели, обрабатывает данные.
        """
        if request.method == 'GET':
            form = JSONImportForm()
            context = {
                'form': form
            }
            return render(request, 'admin/json_form.html', context)
        form = JSONImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/json_form.html', context, status=400)

        if save_json_orders(file=form.files['json_file'].file):
            self.message_user(request, "Data from json was imported")
        else:
            messages.error(request, 'JSON data is not imported. Invalid data')

        return redirect("..")

    def get_urls(self):
        """
        Реализуется подключение функции import_json к urls
        """
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-json/',
                self.import_json,
                name='import_orders_json'
            ),
        ]
        return new_urls + urls
