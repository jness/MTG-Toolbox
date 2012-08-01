from django.core.management import setup_environ
import settings
setup_environ(settings)

from WebMTG.models import MTGCard, MTGHash

from datetime import datetime
from urllib2 import urlopen
import os, sys
import pHash

print 'Started: %s' % datetime.now().ctime()

if not os.path.exists('gatherer_images'):
    os.mkdir('gatherer_images')

cards = MTGCard.objects.all()

for card in cards:
    
    # check if we already have a hash
    try:
        MTGHash.objects.get(card=card)
    except:
        url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card' \
                                                             % card.gatherer_id
        print 'Downloading Card Image for %s from %s' % (card, url)
        i = urlopen(url).read()
        
        filename = 'tmp/%s.jpg' % card.gatherer_id
        f = open(filename, 'wb')
        f.write(i)
        f.close()
        
        h = pHash.imagehash(filename)
        print 'Got %s for %s' % (h, card)
        
        MTGHash.objects.create(card=card, hash=h) # create object in DB
    else:
        continue
    
    sys.exit()
