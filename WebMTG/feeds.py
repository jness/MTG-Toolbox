from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from WebMTG.models import MTGCard, MTGPrice

class Top50Feed(Feed):
    title = "MTGToolbox 50 Most Expensive Cards"
    description = "MTGToolbox 50 Most Expensive Cards"
    link = 'top/'

    def items(self):
        return MTGCard.objects.all().order_by('-avg')[0:50]

    def item_title(self, item):
        return item.card_name
    
    def item_link(self, item):
        return reverse('card_view', kwargs={'id': item.id})

    def item_description(self, item):
        return "$%.2f on %s" % (round(item.avg,2), item.modified.ctime())
        
class CardFeed(Feed):
    title = 'MTGToolbox Card Watch'
    description = "MTGToolbox RSS Feed Card Watch"
    link = ''
    
    def get_object(self, request, id):
        return get_object_or_404(MTGCard, pk=id)

    def items(self, obj):
        cdata = []
        latest = MTGCard.objects.get(id=obj.id)
        past = MTGPrice.objects.filter(card=latest).order_by('-created')
        cdata.append(dict(card_name=latest.card_name, avg=latest.avg,
                          modified=latest.modified, id=latest.id))
        for p in past:
            cdata.append(dict(card_name=p.card.card_name, avg=p.avg,
                              modified=p.modified, id=p.id))
        print cdata
        return cdata

    def item_title(self, item):
        return item['card_name']
    
    def item_link(self, item):
        return reverse('card_view', kwargs={'id': item['id']})

    def item_description(self, item):
        return "$%.2f on %s" % (round(item['avg'],2), item['modified'].ctime())
        