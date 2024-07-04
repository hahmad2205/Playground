from django.contrib import admin
from .models import Property, PropertyImages

class ImageInline(admin.StackedInline):
    model = PropertyImages
    extra = 5

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
admin.site.register(Property)