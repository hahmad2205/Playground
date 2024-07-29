import django_filters

from properties.models import Property, PropertyOffers
from properties.enums import MobileState


class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "price": ["exact", "gt", "lt"],
            "area": ["exact", "gt", "lt"],
            "number_of_bed": ["exact", "gt", "lt"],
            "number_of_bath": ["exact", "gt", "lt"]
        }

