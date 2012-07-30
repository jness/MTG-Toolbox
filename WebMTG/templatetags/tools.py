from django import template
from django.conf import settings
from WebMTG.models import MTGPrice

register = template.Library()

@register.filter()
def price(number):
    p = "%.2f" % round(abs(number),2)
    return p

@register.filter()
def upordown(card):
    try:
        latest = MTGPrice.objects.filter(card=card).latest('created')
        if latest.avg > card.avg:
            return '<font size=1 color=red>Down</font> <i class=icon-arrow-down></i>'
        elif latest.avg < card.avg:
            return '<font size=1 color=#33CC33>Up</font> <i class=icon-arrow-up></i>'
        else:
            return '<font size=1 color=grey>No Change</font>'
    except:
        return '<font size=1 color=grey>No Data</font>'
        
