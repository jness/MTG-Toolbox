from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from WebMTG.models import MTGCard, MTGSet
        
class MTGSetResource(ModelResource):
    class Meta:
        queryset = MTGSet.objects.all()
        resource_name = 'set'
    
class MTGCardResource(ModelResource):
    set = fields.ForeignKey(MTGSetResource, 'set', full=True)
    class Meta:
        queryset = MTGCard.objects.all()
        resource_name = 'card'
        filtering = {
                'card_name': ('exact', 'contains', 'icontains'),
                'set': ALL,
        }
        