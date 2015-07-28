from django.contrib import admin

# -------------------------------------------------------------

from .models import Site

admin.site.register(Site)

# -------------------------------------------------------------
# FRP FisherRoelandProperties

from .models import FRP_Contact
from .models import FRP_Category
from .models import FRP_Property
from .models import FRP_Stand

admin.site.register(FRP_Contact)
admin.site.register(FRP_Category)

class StandInline(admin.StackedInline):
    model = FRP_Stand
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [StandInline]

admin.site.register(FRP_Property, PropertyAdmin)
