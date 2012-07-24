from django.db import models

class MTGSet(models.Model):
    label = models.CharField(max_length=10, unique=True)
    display_name = models.CharField(max_length=75)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.display_name
    
class MTGCard(models.Model):
    card_id = models.CharField(max_length=5)
    multiverse_id = models.IntegerField()
    tcgplayer_id = models.IntegerField()
    card_name = models.CharField(max_length=75)
    type = models.CharField(max_length=100)
    cost = models.CharField(max_length=10, null=True)
    artist = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    power = models.CharField(max_length=10, null=True)
    toughness = models.CharField(max_length=10, null=True)
    set = models.ForeignKey(MTGSet)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.card_name
    
class MTGPrice(models.Model):
    card = models.ForeignKey(MTGCard)
    low = models.CharField(max_length=10)
    avg = models.CharField(max_length=10)
    high = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.card.card_name
    