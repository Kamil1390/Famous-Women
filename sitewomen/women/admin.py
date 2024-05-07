from django.contrib import admin
from .models import Women, Category
# Register your models here.


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'time_create', 'is_published', 'cat']
    list_display_links = ('id', 'title')
    ordering = ('-time_create', 'title')
    list_editable = ('is_published', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ('id', 'name')


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"
