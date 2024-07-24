import django_filters

from properties.models import Property

class PropertyFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    number_of_bed = django_filters.NumberFilter()
    number_of_bed__gt = django_filters.NumberFilter(field_name="number_of_bed", lookup_expr="gt")
    number_of_bed__lt = django_filters.NumberFilter(field_name="number_of_bed", lookup_expr="lt")
    
    number_of_bath = django_filters.NumberFilter()
    number_of_bath__gt = django_filters.NumberFilter(field_name="number_of_bath", lookup_expr="gt")
    number_of_bath__lt = django_filters.NumberFilter(field_name="number_of_bath", lookup_expr="lt")
    
    area = django_filters.NumberFilter()
    area__gt = django_filters.NumberFilter(field_name="area", lookup_expr="gt")
    area__lt = django_filters.NumberFilter(field_name="area", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["price", "number_of_bed", "number_of_bath", "area"]

