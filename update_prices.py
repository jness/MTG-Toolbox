from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.core.cache import cache
from WebMTG.models import MTGPrice, MTGCard, MTGSet, MTGPriceArchive
from TCGPlayer.Magic import Card

from datetime import datetime, timedelta
from urllib2 import urlopen

# archive historic prices
now = datetime.now()
if now.day == 1:
    print 'Running Archive for last month'
    yesterday = now - timedelta(hours=24)
    cards = MTGCard.objects.all()
    for card in cards:
        prices = MTGPrice.objects.filter(card=card)
        if prices:
            pricelist = [ p.avg for p in prices ]
            avg = sum(pricelist) / len(pricelist)
            
            # Add to archive
            datelabel = yesterday.strftime('%m/%Y')
            MTGPriceArchive.objects.create(card=card,
                                           datelabel=datelabel,
                                           avg=avg)
            
# delete last months prices
if now.day == 8:
    print 'Running Cleanup for last month'
    lastmonth = now - timedelta(hours=24*8)
    cards = MTGCard.objects.all()
    for card in cards:
        prices = MTGPrice.objects.filter(card=card,
                                         created__lt=lastmonth)
        if prices:
            [ p.delete() for p in prices ]
            
print 'Started: %s' % datetime.now().ctime()

sets = MTGSet.objects.all()

for set in sets:
    print 'Working on Set %s' % set.label
    c = Card(set=set.label)
    cards = MTGCard.objects.filter(set=set)

    for card in cards:
        print 'Looking up price for %s in set %s' % (card.card_name, 
                                                     card.set.label)
        
        # get prices from TCGPlayer
        prices = c.getCard(card=card.card_name)
    
        print 'Found the following prices %s' % prices
    
        # Move the card objects current prices to history
        MTGPrice.objects.create(card=card, low=card.low, avg=card.avg,
                                high=card.high, created=card.modified,
                                modified=card.modified)
        
        # update card object with latest
        card.low = prices['low']
        card.avg = prices['avg']
        card.high = prices['high']
        card.save()
    
        print 'Successfully updated Price database'    
    
        
print 'Updating Caches'

cache.delete('iPrices')
cache.delete('dPrices')

urlopen('http://mtgtoolbox.flip-edesign.com/increased/').read()
urlopen('http://mtgtoolbox.flip-edesign.com/decreased/').read()

print 'Ended: %s' % datetime.now().ctime()
