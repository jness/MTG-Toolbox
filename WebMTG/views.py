from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from WebMTG.__base import BaseTemplateView, BaseRedirectView
from WebMTG.models import MTGSet, MTGCard, MTGPrice

from TCGPlayer.Magic import Set, Card
from magiccardsinfo.Set import Set as MagiccardsSet
from magiccardsinfo.Card import Card as MagiccardsCard
from magiccardsinfo.Identifiers import Identifiers
from datetime import datetime
    
class HomeView(BaseTemplateView):
    'View for the home page'
    
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        return self.context
    
class TopToday(BaseTemplateView):
    'View for the top 50 expensive cards'
    template_name = "top.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        # latest entry gives us the last run
        l = MTGPrice.objects.all().latest('created').created
        latest = MTGPrice.objects.filter(created__day=l.day,
                                         created__month=l.month,
                                         created__year=l.year)
        
        self.context['cards'] = latest.order_by('-avg')[0:50]
        return self.context
    
class CardDecreasedToday(BaseTemplateView):
    'View for listing top 100 cards that have decreased from yesterday'
    
    template_name = "decreased.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        # see if we have two sets of data
        try:
            l = MTGPrice.objects.all().latest('created').created
            latest = MTGPrice.objects.filter(created__day=l.day,
                                             created__month=l.month,
                                             created__year=l.year)
            
            pdate = datetime(l.year, l.month, l.day)
            p = MTGPrice.objects.filter(created__lt=pdate).latest('created').created
            prev = MTGPrice.objects.filter(created__day=p.day,
                                           created__month=p.month,
                                           created__year=p.year)
        except:
            return self.context
        
        down_cards = []
        
        for c in latest:
            try:
                latest_avg = c.avg
                prev_avg = prev.get(card=c.card).avg
            except:
                continue
            
            if latest_avg < prev_avg:
                
                print prev_avg, latest_avg
                
                dif = float(prev_avg) - float(latest_avg)
                down_cards.append((c.card, "%.2f" % round(dif,2)))
        
        down_cards.sort()
        down_cards.reverse()
        
        self.context['cards'] = down_cards[0:50]
        return self.context    

class CardIncreaseToday(BaseTemplateView):
    'View for listing top 50 cards that have increased from yesterday'
    
    template_name = "increased.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        # see if we have two sets of data
        try:
            l = MTGPrice.objects.all().latest('created').created
            latest = MTGPrice.objects.filter(created__day=l.day,
                                             created__month=l.month,
                                             created__year=l.year)
            
            pdate = datetime(l.year, l.month, l.day)
            p = MTGPrice.objects.filter(created__lt=pdate).latest('created').created
            prev = MTGPrice.objects.filter(created__day=p.day,
                                           created__month=p.month,
                                           created__year=p.year)
        except:
            return self.context
            
        up_cards = []
        for c in latest:
            try:
                latest_avg = c.avg
                prev_avg = prev.get(card=c.card).avg
            except:
                continue
            
            if latest_avg > prev_avg:
                dif = float(latest_avg) - float(prev_avg)
                up_cards.append((c.card, "%.2f" % round(dif,2)))
        
        up_cards.sort()
        up_cards.reverse()
        
        self.context['cards'] = up_cards[0:50]
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
    
    def identify_set(self, word=None, sets=None):
        matches = []
        for key, value in sets:
            if word in value:
                matches.append((key, value))
        return matches
        
    
    def get_redirect_url(self, **kwargs):
        self.create_context(**kwargs)
        sets = Set().getSets()
        
        # get Magiccards.info set abbreviation
        magiccards_info = None
        s = self.context['set']
        magiccardsets = MagiccardsSet().getSets().items()
        for word in s.split():
            magiccardsets = self.identify_set(word=word, sets=magiccardsets)
            if len(magiccardsets) == 1:
                magiccards_info = magiccardsets[0][0]
                break
                    
        # be sure not to add a duplicate set.
        display_name = sets.get(self.context['set'])
        if display_name:
            stuple = (self.context['set'], display_name, magiccards_info)
            if stuple not in self.context['my_sets']:
                MTGSet.objects.create(label=self.context['set'],
                                      display_name=display_name,
                                      magiccards_info=magiccards_info)
        return reverse('my_set_view')
  
class AddCardView(BaseTemplateView):
    'Add all cards in a given set to our Card collection'
    
    template_name = "log.html"
    def get_context_data(self, **kwargs):
        self.create_context(**kwargs)
        
        # get our set object from our model and card for a given
        # set from tcgplayer.
        db_set = MTGSet.objects.get(label=self.context['set'])
        magiccards_set = MagiccardsCard(set=db_set.magiccards_info)
        
        cards = Card(set=db_set.label).getCards()
        
        messages = []
        # add the cards to our model        
        for card in cards:
            
            # Lookup card name on magiccards info
            name = cards[card]['card_name']
            try:
                message = 'Found card %s on Magiccard Info' % name
                messages.append(message)
                magiccards_card = magiccards_set.getCard(name=name)
            except:
                message = '!! Failed Magiccard Info lookup for %s !!' % name
                messages.append(message)
                continue
            
            # get card details from magiccards info
            i = Identifiers(set=db_set.magiccards_info,
                            id=magiccards_card['card_id'])
            gatherer_id = i.getGathererId()
            tcgplayer_id = i.getTCGPlayerId()
            cards[card]['gatherer_id'] = gatherer_id
            cards[card]['tcgplayer_id'] = tcgplayer_id
            
            # magiccardsinfo has better data
            cards[card]['set'] = db_set
            cards[card]['magiccard_id'] = magiccards_card['card_id']
            cards[card]['type'] = magiccards_card['type']
            cards[card]['rarity'] = magiccards_card['rarity']
            
            # remove prices from dict
            del(cards[card]['low'])
            del(cards[card]['avg'])
            del(cards[card]['high'])
            
            c, created = MTGCard.objects.get_or_create(**cards[card])
            c.save()
            
        self.context['log'] = messages
        return self.context
        
class LogoutView(BaseRedirectView):
    'For all your logging out needs'
    
    permanent = False
    query_string = True
    def get_redirect_url(self, **kwargs):        
        if self.request.user.is_authenticated():
            logout(self.request)
        
        return reverse('my_set_view')