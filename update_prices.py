from django.core.management import setup_environ
import settings
setup_environ(settings)

from WebMTG.models import MTGPrice, MTGCard, MTGSet
from TCGPlayer.Magic import Card

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
    
        # Update with the price
        MTGPrice.objects.create(card=card, low=prices['low'],
                                avg=prices['avg'], high=prices['high'])
    
        print 'Successfully updated Price database'
