from django.views.generic.base import TemplateView, RedirectView
from WebMTG.models import MTGSet

class BaseTemplateView(TemplateView):
    'A base template class to use for our application'
    
    def create_context(self, **kwargs):
        'Create our context and add our kwargs to it'
        self.context = {}
        self.context['my_sets'] = [ (i.label, i.display_name, i.magiccards_info) \
                                    for i in MTGSet.objects.all() ]
        for k in kwargs:
            self.context[k] = kwargs[k]
            
class BaseRedirectView(RedirectView):
    'A base template class to use for our application'
    
    def create_context(self, **kwargs):
        'Create our context and add our kwargs to it'
        self.context = {}
        self.context['my_sets'] = [ (i.label, i.display_name, i.magiccards_info) \
                                    for i in MTGSet.objects.all() ]
        for k in kwargs:
            self.context[k] = kwargs[k]