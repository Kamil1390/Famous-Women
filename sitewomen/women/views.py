from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.urls.exceptions import Resolver404
from django.db import models
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm
from django.core.paginator import Paginator
from .utils import DataMixin
import uuid


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related("cat")


def about(request: HttpRequest) -> HttpResponse:
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, "women/about.html",
                  {"title": "О сайте", 'page_obj': page_object})


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    title_page = "Добавление статьи"


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
    template_name = 'women/add_page.html'


class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = 'women/delete_page.html'
    success_url = reverse_lazy('home')


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Авторизация на сайте")


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_data(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return self.get_mixin_data(context, title=f"Категория - {cat.name}", cat_selected=cat.pk)

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def page_not_found(request: HttpRequest, exception: Resolver404) -> HttpResponseNotFound:
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


class WomenTags(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_data(context, title=f"Тег - {tag.tag}")

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related("cat")
