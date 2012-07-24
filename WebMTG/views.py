from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from WebMTG.__base import BaseTemplateView, BaseRedirectView
from WebMTG.models import MTGSet, MTGCard, MTGPrice
from magiccardsinfo.Set import Set
from magiccardsinfo.Card import Card
from magiccardsinfo.Identifiers import Identifiers
from magiccardsinfo.Price import Price
    
class HomeView(BaseTemplateView):
    'View for the home page'
    
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        return self.context
        
class MySetView(BaseTemplateView):
    'View for listing all sets you have imported from magiccards.info'
    
    template_name = "mysets.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        return self.context
    
class CardSetView(BaseTemplateView):
    'View for listing all cards in a given set'
    
    template_name = "cards.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        db_set = MTGSet.objects.get(label=self.context['set'])
        cards = MTGCard.objects.filter(set=db_set)
        for card in cards:
            prices = MTGPrice.objects.filter(card=card)
            if prices:
                card.prices = prices.latest('created')
            else:
                card.prices = None
        self.context['cards'] = cards
        return self.context
    
class CardView(BaseTemplateView):
    'View for listing a card'
    
    template_name = "card.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        self.context['card'] = MTGCard.objects.get(id=self.context['id'])
        prices = MTGPrice.objects.filter(card=self.context['card'])
        self.context['prices'] = prices.order_by('-created')[:7]
        if prices:
            self.context['latest_prices'] = prices.latest('created')
        else:
            self.context['latest_prices'] = None
        return self.context
    
class GetCardPrices(BaseRedirectView):
    'Get current prices for a card'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):
        self.create_context(**kwargs)
        card = MTGCard.objects.get(id=self.context['id'])
        prices = Price(id=card.tcgplayer_id).getPrices()
        MTGPrice.objects.create(card=card, low=prices['low'], avg=prices['avg'],
                                high=prices['high'])
        return reverse('card_view', kwargs={'id': card.id})
    
class ShowSetView(BaseTemplateView):
    'View for listing all sets from magiccards.info'
    
    template_name = "sets.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        sets = Set().getSets().items()
        self.context['sets'] = sorted(sets)
        return self.context

class AddSetView(BaseRedirectView):
    'View for adding a set from ShowSetView to our collection'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):
        self.create_context(**kwargs)
        sets = Set().getSets()
        
        # be sure not to add a duplicate set.
        display_name = sets.get(self.context['set'])
        if display_name:
            stuple = (self.context['set'], display_name)
            if stuple not in self.context['my_sets']:
                MTGSet.objects.create(label=self.context['set'],
                                      display_name=display_name)
        return reverse('my_set_view')
  
class AddCardView(BaseRedirectView):
    'Add all cards in a given set to our Card collection'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):
        self.create_context(**kwargs)
        
        # get our set object from our model and card for a given
        # set from magiccards.info.
        db_set = MTGSet.objects.get(label=self.context['set'])
        cards = Card(set=self.context['set']).getCards()
    
        # add the cards to our model        
        for card in cards:
            # skip basic lands
            if 'Basic Land' not in cards[card]['type']:
                cards[card]['set_id'] = db_set.id
                
                # get the external id's for a card
                i = Identifiers(set=self.context['set'],
                               id=cards[card]['card_id'])
                cards[card]['multiverse_id'] = i.getGathererId()
                cards[card]['tcgplayer_id'] = i.getTCGPlayerId()
                
                c, created = MTGCard.objects.get_or_create(**cards[card])
                c.save()
        return reverse('card_set_view', kwargs={'set': self.context['set']})
        
class LogoutView(BaseRedirectView):
    'For all your logging out needs'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):        
        if self.request.user.is_authenticated():
            logout(self.request)
        
        return reverse('my_set_view')