from django.db import models


class Author(models.Model):
    class Meta:
        # сортировка по имени автора
        ordering = ['name', ]

    # имя автора
    name = models.CharField(max_length=100, blank=False)
    # биография автора
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Category(models.Model):
    # название категории
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f'{self.name}'


class Tag(models.Model):
    class Meta:
        # сортировка по имени
        ordering = ['name', ]

    # название тега
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.name}'


# сущность статья
class Article(models.Model):
    # заголовок статьи
    title = models.CharField(max_length=200)
    # содержимое статьи
    content = models.TextField()
    # дата публикации
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    tags = models.ManyToManyField(Tag)
