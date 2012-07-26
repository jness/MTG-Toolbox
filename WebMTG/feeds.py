from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from WebMTG.models import MTGCard, MTGPrice

class Top50Feed(Feed):
    title = "MTGToolbox 50 Most Expensive Cards"
    description = "MTGToolbox 50 Most Expensive Cards"
    link = '/top/'

    def items(self):
        return MTGCard.objects.all().order_by('-avg')[0:50]

    def item_title(self, item):
        return item.card_name
    
    def item_link(self, item):
        return reverse('card_view', kwargs={'id': item.id})

    def item_description(self, item):
        return "$%.2f on %s" % (round(item.avg,2), item.modified.ctime())
        
class CardFeed(Feed):
    title = 'Card Watch'
    description = "Card Watch"
    link = '/card/'
    
    def get_object(self, request, id):
        return get_object_or_404(MTGCard, pk=id)

    def items(self, obj):
        prices = MTGCard.objects.filter(id=obj.id)
        return prices

    def item_title(self, item):
        return item.card_name
    
    def item_link(self, item):
        return reverse('card_view', kwargs={'id': item.id})

    def item_description(self, item):
        return "$%.2f on %s" % (round(item.avg,2), item.modified.ctime())
        