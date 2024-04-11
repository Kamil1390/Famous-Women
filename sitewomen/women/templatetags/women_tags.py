from django import template
import women.views as view
from women.models import Women, Category

register = template.Library()


@register.simple_tag()
def get_category():
    return view.cat_db


@register.inclusion_tag('women/list_categories.html')
def show_category(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
