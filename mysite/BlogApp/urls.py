from django.urls import path
from .views import (
    base_blog,
    BasedView,
    AuthorCreateView,
    ArticleCreateView,
    TagCreateView,
    CategoryCreateView,
)


app_name = 'BlogApp'
urlpatterns = [
    path('', base_blog, name='blog'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('author/create/', AuthorCreateView.as_view(), name='author_create'),
    path('tag/create/', TagCreateView.as_view(), name='tag_create'),
    path('articles/list/', BasedView.as_view(), name='articles_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
]
