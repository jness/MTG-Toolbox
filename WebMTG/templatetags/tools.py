from django import template
from django.conf import settings

register = template.Library()

@register.filter()
def price(number):
    p = "%.2f" % round(number,2)
    return p
