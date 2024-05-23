from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls.exceptions import Resolver404
from django.db import models
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm
import uuid

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


class WomenHome(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "cat_selected": 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related("cat")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Главная страница"
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related("cat")
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

# def handle_upload_file(f):
#     name = f.name
#     ext = ''
#     if '.' in name:
#         ext = name[name.rindex('.'):]
#         name = name[:name.rindex('.')]
#     suffix = str(uuid.uuid4())
#     with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_upload_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu, 'form': form})


# def add_page(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     data = {
#         "menu": menu,
#         "title": "Добавление страницы",
#         "form": form
#     }
#     return render(request, "women/add_page.html", context=data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            "menu": menu,
            "title": "Добавление страницы",
            "form": form
        }
        return render(request, "women/add_page.html", context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
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


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        context['title'] = f"Категория - {cat.name}"
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


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


class WomenTags(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context['title'] = f"Тег - {tag.tag}"
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return tag.womens.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

