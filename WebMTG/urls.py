from WebMTG.views import ShowSetView, AddSetView, MySetView, AddCardView
from WebMTG.views import CardSetView, CardView, LogoutView, GetCardPrices
from WebMTG.views import HomeView, CardIncreaseToday, CardDecreasedToday

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url('^$', HomeView.as_view(), name='home_view'),
    url('^sets/$', MySetView.as_view(), name='my_set_view'),
    url('^increased/$', CardIncreaseToday.as_view(), name='increased_view'),
    url('^decreased/$', CardDecreasedToday.as_view(), name='decreased_view'),
    url('^cards/(?P<set>[\w]+)/$', CardSetView.as_view(), name='card_set_view'),
    url('^card/(?P<id>[\d]+)/$', CardView.as_view(), name='card_view'),
    url(r'^logout/$', LogoutView.as_view(), name='logout_view'),
    
    # secure pages    
    url('^add_sets/$',
            login_required(ShowSetView.as_view()), name='show_set_view'),
    url('^add_set/(?P<set>[\w]+)/$',
            login_required(AddSetView.as_view()), name='add_set_view'),
    url('^scan_set/(?P<set>[\w]+)/$',
            login_required(AddCardView.as_view()), name='add_card_view'),
    url('^get_prices/(?P<id>[\d]+)/$',
            login_required(GetCardPrices.as_view()), name='get_card_view'),
    
    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
)