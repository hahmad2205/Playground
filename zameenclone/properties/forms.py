from django import forms
from .models import PropertyOffers

class OfferForm(forms.ModelForm):
    price = forms.IntegerField()
    
    class Meta:
        model = PropertyOffers
        fields = ["price"]
