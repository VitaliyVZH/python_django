from typing import Sequence

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView

from BlogApp.models import Article, Author, Tag, Category


def base_blog(request: HttpRequest):
    return render(request=request, template_name='BlogApp/base.html')


# класс BasedView отображает список статей
class BasedView(ListView):
    queryset = (
        Article.objects
        .select_related('author', 'category')
        .prefetch_related('tags')
    ).defer('content', 'author__bio')
    template_name = 'BlogApp/articles-list.html'


class AuthorCreateView(CreateView):
    model = Author
    template_name = 'BlogApp/author-create.html'
    fields = 'name', 'bio'
    success_url = reverse_lazy('BlogApp:blog')


class TagCreateView(CreateView):
    model = Tag
    template_name = 'BlogApp/tag-create.html'
    fields = 'name',
    success_url = reverse_lazy('BlogApp:blog')


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'BlogApp/category-create.html'
    fields = 'name',
    success_url = reverse_lazy('BlogApp:blog')


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'BlogApp/article-create.html'
    fields = 'title', 'content', 'author', 'category', 'tags'
    success_url = reverse_lazy('BlogApp:blog')
