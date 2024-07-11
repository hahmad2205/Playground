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
        highest_form_count = 0
        for key in self.data.keys():
            if key.startswith('form-') and '-amenity' in key:
                try:
                    index = int(key.split('-')[1])
                    if index > highest_form_count:
                        highest_form_count = index
                except ValueError:
                    pass
        
        for formCount in range(0,highest_form_count+1):
            if f'form-{formCount}-amenity_type' in self.data:
                try:
                    self.fields['amenity'].queryset = AmenityOption.objects.filter(amenity=self.data.get(f'form-{formCount}-amenity_type'))
                except (ValueError, TypeError):
                    self.fields['amenity'].queryset = AmenityOption.objects.none()
            elif self.instance.pk:
                self.fields['amenity'].queryset = self.instance.amenity.options.all()
            else:
                self.fields['amenity'].queryset = AmenityOption.objects.none()
