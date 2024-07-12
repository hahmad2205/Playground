from django import forms
from .models import Property, PropertyImages, PropertyAmenity, PropertyOffers
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
        fields = ['image_url', 'image']
        widgets = {'image_url': forms.HiddenInput()}

        
class PropertyAmenityForm(forms.ModelForm):
    amenity_type = forms.ModelChoiceField(queryset=Amenity.objects.all(), label="Amenity")
    amenity = forms.ModelChoiceField(queryset=AmenityOption.objects.none(), label="Amenity Option")
    value = forms.IntegerField(required=False)

    class Meta:
        model = PropertyAmenity
        fields = ['amenity_type', 'amenity', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity_type'].widget.attrs.update({'class': 'amenity-dropdown'})
        self.fields['amenity'].widget.attrs.update({'class': 'amenity-option-dropdown'})
        if self.is_bound:
            try:
                amenity_type_id = int(self.data.get(self.add_prefix('amenity_type')))
                self.fields['amenity'].queryset = AmenityOption.objects.filter(amenity_id=amenity_type_id)
            except (ValueError, TypeError):
                self.fields['amenity'].queryset = AmenityOption.objects.none()
        elif self.instance.pk:
            self.fields['amenity'].queryset = self.instance.amenity.options.all()
        else:
            self.fields['amenity'].queryset = AmenityOption.objects.none()


class OfferForm(forms.ModelForm):
    price = forms.IntegerField()
    
    class Meta:
        model = PropertyOffers
        fields = ["price"]
