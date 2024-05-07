from django import template
import women.views as view
from women.models import Women, Category, TagPost
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_category():
    return view.cat_db


@register.inclusion_tag('women/list_categories.html')
def show_category(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_tags():
    return {'tags': TagPost.objects.annotate(total=Count("womens")).filter(total__gt=0)}
