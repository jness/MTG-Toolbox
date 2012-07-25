from django.db import models

class MTGSet(models.Model):
    label = models.CharField(max_length=10, unique=True)
    display_name = models.CharField(max_length=75)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.display_name
    
class MTGCard(models.Model):
    card_name = models.CharField(max_length=75)
    cost = models.CharField(max_length=10, null=True)
    rarity = models.CharField(max_length=50)
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
    