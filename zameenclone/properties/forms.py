from django import forms
from .models import Property, PropertyImages, PropertyAmenity
from core.models import Amenity, AmenityOption

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'area', 'description', 'header', 'location', 'purpose',
            'number_of_bath', 'number_of_bed', 'price', 'title', 
            'type', 'whatsapp_number'
        ]

class PropertyImagesForm(forms.ModelForm):
    class Meta:
        model = PropertyImages
        fields = ['image']

class PropertyAmenityForm(forms.ModelForm):
    amenity = forms.ModelChoiceField(queryset=Amenity.objects.all(), label="Amenity")
    amenity_option = forms.ModelChoiceField(queryset=AmenityOption.objects.none(), label="Amenity Option")
    value = forms.IntegerField(required=False)

    class Meta:
        model = PropertyAmenity
        fields = ['amenity', 'amenity_option', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity'].widget.attrs.update({'class': 'amenity-dropdown'})
        self.fields['amenity_option'].widget.attrs.update({'class': 'amenity-option-dropdown'})
