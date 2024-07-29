from django.contrib import admin
from .models import Property, PropertyImages

from .models import Property, PropertyImages, PropertyOffers, PropertyAmenity


class PropertyImagesInline(admin.TabularInline):
    model = PropertyImages
    extra = 5


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImagesInline]
    search_fields = ["id"]


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyOffers)
admin.site.register(PropertyAmenity)
admin.site.register(PropertyImages)
