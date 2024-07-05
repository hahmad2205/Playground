from django.contrib import admin
from .models import Property, PropertyImages

from .models import Property, PropertyImages, PropertyOffers

class PropertyImagesInline(admin.TabularInline):
    model = PropertyImages
    extra = 5

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImagesInline]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyOffers)
