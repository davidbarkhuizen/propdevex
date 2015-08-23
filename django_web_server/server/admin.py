from django.contrib import admin

# -------------------------------------------------------------

from .models import Site

admin.site.register(Site)

# -------------------------------------------------------------
# FRP FisherRoelandProperties

from .models import FRP_Contact
from .models import FRP_Category
from .models import FRP_Property
from .models import FRP_PropertyImage
from .models import FRP_SubProperty
from .models import FRP_SubPropertyImage

admin.site.register(FRP_Contact)
admin.site.register(FRP_Category)

class SubPropertyImageInline(admin.StackedInline):
    model = FRP_SubPropertyImage
    extra = 1

class SubPropertyAdmin(admin.ModelAdmin):
	inlines = [SubPropertyImageInline]

admin.site.register(FRP_SubProperty, SubPropertyAdmin)

class SubPropertyInline(admin.StackedInline):
    model = FRP_SubProperty
    extra = 1

class PropertyImageInline(admin.StackedInline):
    model = FRP_PropertyImage
    extra = 1

class SubPropertyInline(admin.StackedInline):
    model = FRP_SubProperty
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, SubPropertyInline]

admin.site.register(FRP_Property, PropertyAdmin)
