from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Women, Category
# Register your models here.


class MarriedFilter(admin.SimpleListFilter):
    title = "Семейное положение"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_photo', 'time_create', 'is_published', 'cat']
    list_display_links = ('title', )
    ordering = ('-time_create', 'title')
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    list_per_page = 5
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published', 'tags']
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']
    readonly_fields = ['post_photo']
    # prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    save_on_top = True


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Предварительная загрузка связанных объектов 'women'
        queryset = queryset.select_related('cat', 'husband')
        queryset = queryset.prefetch_related('tags')
        return queryset

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без строк"

    @admin.action(description="Опубликовать выбранные статьи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей")

    @admin.action(description="Снять выбранные статьи с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записей", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ('id', 'name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Предварительная загрузка связанных объектов 'women'
        queryset = queryset.prefetch_related('posts')
        return queryset


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"
