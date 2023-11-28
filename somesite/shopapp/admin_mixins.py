import csv

from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse


class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta  # получаем поля моделей
        print(meta)
        field_names = [field.name for field in meta.fields]  # записываем поля моделей в список

        response = HttpResponse(content_type="text/csv")  # подготовка respons к записи, указываем тип контента
        # для скачивания файла с готовым именем, добавим заголовок в ответ
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"
        # записываем результат в ответ
        csv_writer = csv.writer(response)  # записываем результат в response
        # записываем заголовки, таким образом первой строчкой будет имя каждой из колонок
        csv_writer.writerow(field_names)

        # пройдём по всем полям модели и запишем их в строчку
        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])  # собираем все поля и записываем в resp
        return response

    export_csv.short_description = "Export as CSV"  # описание действия
