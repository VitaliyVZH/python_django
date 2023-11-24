from django.contrib.sitemaps import Sitemap

from .models import Product


class ShopSitemap(Sitemap):
    """
    Данный класс предназначен для подготовки данных, которые будут отдаваться
    поисковым ботам браузеров.
    """
    changefreq = "monthly"  # атрибут указывает, как часто меняется информация в приложении
    priority = 0.5          # атрибут указывает на важность приложения в сайте, шкала от 0 до 1

    def items(self):
        """
        Обязательный метод определяет, в каком виде (сортировка) и в каком кол-ве (фильтрация по параметрам)
        отдавать данные.
        """
        return Product.objects.filter(archived=False).order_by('-create_at')

    # def lastmod(self, obj: Product):
    #     """
    #     Необязательный метод указывает, когда последний раз модифицировался объект
    #     """
    #     return obj.create_at
