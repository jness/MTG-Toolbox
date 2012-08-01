from WebMTG.models import MTGCard, MTGSet, MTGPrice, MTGHash
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

# Remove unused
admin.site.unregister(Site)
admin.site.unregister(Group)

# Add our Models
admin.site.register(MTGSet)
admin.site.register(MTGCard)
admin.site.register(MTGPrice)
admin.site.register(MTGHash)