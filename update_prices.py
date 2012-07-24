from django.core.management import setup_environ
import settings
setup_environ(settings)

from WebMTG.models import MTGPrice, MTGCard, MTGSet
from magiccardsinfo.Price import Price
import sys

# see if we need to scan all or just one set
try:
    set_input = sys.argv[1]
    set = MTGSet.objects.get(label=set_input)
    cards = MTGCard.objects.filter(set=set)
except IndexError:
    cards = MTGCard.objects.all()

for card in cards:

    print 'Looking up price for %s with tcgplayer_id %s' % (card.card_name, 
                                                            card.tcgplayer_id)

    p = Price(id=card.tcgplayer_id)
    prices = p.getPrices()

    print 'Found the following prices %s' % prices

    # Update with the price
    MTGPrice.objects.create(card=card, low=prices['low'],
                            avg=prices['avg'], high=prices['high'])

    print 'Successfully updated Price database'
