from django.db import models

class MTGSet(models.Model):
    label = models.CharField(max_length=75, unique=True)
    display_name = models.CharField(max_length=75)
    magiccards_info = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.display_name
    
class MTGCard(models.Model):
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
    
    def __unicode__(self):
        return self.card_name
    
class MTGPrice(models.Model):
    card = models.ForeignKey(MTGCard)
    low = models.DecimalField()
    avg = models.DecimalField()
    high = models.DecimalField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.card.card_name
    