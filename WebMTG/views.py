from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from WebMTG.__base import BaseTemplateView, BaseRedirectView
from WebMTG.models import MTGSet, MTGCard, MTGPrice

from TCGPlayer.Magic import Set, Card
    
class HomeView(BaseTemplateView):
    'View for the home page'
    
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        return self.context
    
class CardDecreasedToday(BaseTemplateView):
    'View for listing top 100 cards that have decreased from yesterday'
    
    template_name = "decreased.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        down_cards = []
        cards = MTGCard.objects.all()
        for card in cards:
            prices = MTGPrice.objects.filter(card=card).order_by('-created')[:2]
            if len(prices) == 2:
                if float(prices[0].avg) < float(prices[1].avg):
                    increase = float(prices[1].avg) - float(prices[0].avg)
                    down_cards.append((card, "%.2f" % round(increase,2)))
        
        self.context['cards'] = down_cards
        return self.context    

class CardIncreaseToday(BaseTemplateView):
    'View for listing top 100 cards that have increased from yesterday'
    
    template_name = "increased.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        up_cards = []
        cards = MTGCard.objects.all()
        for card in cards:
            prices = MTGPrice.objects.filter(card=card).order_by('-created')[:2]
            if len(prices) == 2:
                if float(prices[0].avg) > float(prices[1].avg):
                    increase = float(prices[0].avg) - float(prices[1].avg)
                    up_cards.append((card, "%.2f" % round(increase,2)))
        
        self.context['cards'] = up_cards
        return self.context

class MySetView(BaseTemplateView):
    'View for listing all sets you have imported from tcgplayer'
    
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
        
        if prices:
            self.context['latest_prices'] = prices.latest('created')
        else:
            self.context['latest_prices'] = None
            
        price_list = prices.order_by('-created')[:7]
        price_list = price_list.reverse()
        self.context['prices'] = price_list
        return self.context
    
class GetCardPrices(BaseRedirectView):
    'Get current prices for a card'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):
        self.create_context(**kwargs)
        card = MTGCard.objects.get(id=self.context['id'])
        c = Card(set=card.set.label)
        prices = c.getCard(card=card.card_name)
        
        MTGPrice.objects.create(card=card, low=prices['low'], avg=prices['avg'],
                                high=prices['high'])
        return reverse('card_view', kwargs={'id': card.id})
    
class ShowSetView(BaseTemplateView):
    'View for listing all sets from tcgplayer'
    
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
        # set from tcgplayer.
        db_set = MTGSet.objects.get(label=self.context['set'])
        cards = Card(set=db_set.display_name).getCards()
        
        # add the cards to our model        
        for card in cards:
            cards[card]['set'] = db_set
            
            # remove prices from dict
            del(cards[card]['low'])
            del(cards[card]['avg'])
            del(cards[card]['high'])
            
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