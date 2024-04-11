from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls.exceptions import Resolver404
from django.db import models
from .models import Women, Category

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"}
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
        Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс',
     'is_published': True},
]


def index(request: HttpRequest) -> HttpResponse:
    post = Women.published.all()
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": post,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu})


def add_page(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Добавление страницы")


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
    posts = Women.published.filter(cat_id=category.pk)
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request: HttpRequest, exception: Resolver404) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")
