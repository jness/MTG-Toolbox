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
    low = models.DecimalField(decimal_places=2, max_digits=10)
    avg = models.DecimalField(decimal_places=2, max_digits=10)
    high = models.DecimalField(decimal_places=2, max_digits=10) 
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.card_name
    
class MTGPrice(models.Model):
    card = models.ForeignKey(MTGCard)
    low = models.DecimalField(decimal_places=2, max_digits=10)
    avg = models.DecimalField(decimal_places=2, max_digits=10)
    high = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    
    def __unicode__(self):
        return self.card.card_name
    
class MTGPriceArchive(models.Model):
    card = models.ForeignKey(MTGCard)
    datelabel = models.CharField(max_length=12)
    avg = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.card.card_name
    
class MTGHash(models.Model):
    card = models.ForeignKey(MTGCard)
    hash = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.card.card_name
    