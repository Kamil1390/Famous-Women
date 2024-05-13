from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls.exceptions import Resolver404
from django.db import models
from .models import Women, Category, TagPost
from .forms import AddPostForm

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"}
]


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related("cat")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu})


def add_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddPostForm()
    data = {
        "menu": menu,
        "title": "Добавление страницы",
        "form": form
    }
    return render(request, "women/add_page.html", context=data)


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Авторизация на сайте")


def show_post(request: HttpRequest, post_slug: models.SlugField) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }
    return render(request, 'women/post.html', context=data)


def show_category(request: HttpRequest, cat_slug: int) -> HttpResponse:
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request: HttpRequest, exception: Resolver404) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


def show_tags(request: HttpRequest, tag_slug: models.SlugField):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.womens.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)

