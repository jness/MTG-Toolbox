from django.db import models
import caching.base

class MTGSet(caching.base.CachingMixin, models.Model):
    label = models.CharField(max_length=75, unique=True)
    display_name = models.CharField(max_length=75)
    magiccards_info = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = caching.base.CachingManager()
    
    def __unicode__(self):
        return self.display_name
    
class MTGCard(caching.base.CachingMixin, models.Model):
    magiccard_id = models.CharField(max_length=10)
    gatherer_id = models.IntegerField()
    tcgplayer_id = models.IntegerField()
    card_name = models.CharField(max_length=75)
    cost = models.CharField(max_length=20, null=True)
    rarity = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    set = models.ForeignKey(MTGSet)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = caching.base.CachingManager()
    
    def __unicode__(self):
        return self.card_name
    
class MTGPrice(caching.base.CachingMixin, models.Model):
    card = models.ForeignKey(MTGCard)
    low = models.CharField(max_length=20)
    avg = models.CharField(max_length=20)
    high = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = caching.base.CachingManager()
    
    def __unicode__(self):
        return self.card.card_name
    