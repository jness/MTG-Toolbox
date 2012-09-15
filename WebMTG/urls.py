from WebMTG.views import ShowSetView, AddSetView, MySetView, AddCardView
from WebMTG.views import CardSetView, CardView, LogoutView, GetCardPrices
from WebMTG.views import HomeView, CardIncreaseToday, CardDecreasedToday
from WebMTG.views import TopToday, ApiUsage, IdentifyCard, Search, AddWatchView

from WebMTG.feeds import Top50Feed, CardFeed

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from tastypie.api import Api
from WebMTG.api import MTGCardResource, MTGSetResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MTGCardResource())
v1_api.register(MTGSetResource())

urlpatterns = patterns('',
    url('^$', HomeView.as_view(), name='home_view'),
    url('^sets/$', MySetView.as_view(), name='my_set_view'),
    url('^top/$', TopToday.as_view(), name='top_view'),
    #url('^increased/$', CardIncreaseToday.as_view(), name='increased_view'),
    #url('^decreased/$', CardDecreasedToday.as_view(), name='decreased_view'),
    url('^cards/(?P<set>[\w :\'\.\-/"\(\)]+)/$', CardSetView.as_view(), name='card_set_view'),
    url('^card/(?P<id>[\d]+)/$', CardView.as_view(), name='card_view'),
    url(r'^logout/$', LogoutView.as_view(), name='logout_view'),
    url(r'^identify/(?P<hash>[\d]+)/$', IdentifyCard.as_view(), name='identify_view'),
    url('^search/$', Search.as_view(), name='search_view'),
    url('^addwatch/(?P<id>[\d]+)/$', AddWatchView.as_view(), name='addwatch_view'),
    url('^watch/$', WatchView.as_view(), name='watch_view'),
    
    # secure pages    
    url('^add_sets/$',
            login_required(ShowSetView.as_view()), name='show_set_view'),
    url('^add_set/(?P<set>[\w :\'\.\-/"\(\)]+)/$',
            login_required(AddSetView.as_view()), name='add_set_view'),
    url('^scan_set/(?P<set>[\w :\'\.\-/"\(\)]+)/$',
            login_required(AddCardView.as_view()), name='add_card_view'),
    url('^get_prices/(?P<id>[\d]+)/$',
            login_required(GetCardPrices.as_view()), name='get_card_view'),
    
    # feeds
    url(r'^top/feed/$', Top50Feed(), name='top_feed'),
    url(r'^card/(?P<id>[\d]+)/feed/$', CardFeed(), name='card_feed'),
    
    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
    
    # API
    url(r'^api_usage/$', ApiUsage.as_view(), name='api_usage'),
    url(r'^api/', include(v1_api.urls)),
)