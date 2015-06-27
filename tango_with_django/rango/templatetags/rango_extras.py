__author__ = 'PyBeaner'
from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag("rango/cats.html")
def get_category_list(active_cat=None):
    return {"cats": Category.objects.all(), "active_cat": active_cat}
