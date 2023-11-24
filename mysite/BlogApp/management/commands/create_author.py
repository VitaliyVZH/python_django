
from django.core.management import BaseCommand

from BlogApp.models import Author
from myauth.models import Profile


# команда на добавление автора
class Command(BaseCommand):

    def handle(self, *args, **options):
        # список авторов
        authors = ['А. С. Пушкин', 'А. Н. Толстой', 'Н. В. Гоголь', 'И. С. Тургенев', 'М. Ю. Лермонтов']
        # перечисляем авторов и добавляем базу
        for name_autor in authors:
            Author.objects.get_or_create(name=name_autor)


