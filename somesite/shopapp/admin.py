from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


class OrdersInProductsInline(admin.TabularInline):
    """
    Класс открывает доступ к каботе с каждым связанным продуктом в заказе
    """
    model = Product.orders.through


@admin.action(description='Archived Product')  # описание действия в выпадающем списке action в админ панели
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchived Product')  # описание действия в выпадающем списке action в админ панели
def mark_unarchived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [  # перечень групповых действий, которые будут в выпадающем списке
        mark_archived,  # действие добавленное в перечень групповых действий
        mark_unarchived,
        "export_csv",  # действие для скачивания выбранных данных в csv, метод класса ExportAsCSVMixin
    ]
    inlines = [
        OrdersInProductsInline,
    ]
    fieldsets = [
        ('Info product', {  # название группы
            'fields': ('name', 'description'),  # поля, которые будут выведены
        }),
        ('Price options', {  # название группы
            'fields': ('price', ),  # поля, которые будут выведены
            'classes': ('extrapretty',),  # скрывает группу
            'description': 'Some text for description'  # описание группы
        })
    ]
    exclude = ('archived',)  # исключает отображение указанного поля в объекте
    date_hierarchy = 'create_at'  # добавляет перелистывание страниц по месяцам создания заказа
    actions_on_bottom = True  # расположение окна действий action внизу
    actions_on_top = False  # расположение окна действий action вверху
    actions_selection_counter = False  # счётчик выбранных позиций вкл/выкл
    list_display = 'pk', 'name', 'shot_str', 'price', 'create_at', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description'

    def shot_str(self, obj: Product) -> str:
        if len(obj.description) > 40:
            return obj.description[:40] + '...'
        return obj.description
# admin.site.register(Product, ProductAdmin)


class OrderProductsInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductsInline
    ]
    list_display = 'pk', 'delivery_address', 'get_promocode', 'create_at', 'user_verbose'
    list_display_links = 'pk', 'delivery_address'
    ordering = 'pk',

    def get_promocode(self, obj: Order):
        if obj.promocode:
            return obj.promocode
        return '-'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username
