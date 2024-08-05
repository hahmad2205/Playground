import factory
from factory.django import DjangoModelFactory

from core.factory import AmenityOptionFactory
from properties.enums import MobileState
from properties.models import Property, PropertyImages, PropertyAmenity, PropertyOffers
from users.factory import UserFactory


class PropertyFactory(DjangoModelFactory):
    class Meta:
        model = Property

    owner = factory.SubFactory(UserFactory)
    is_active = True
    area = 10
    description = "A beautiful property"
    header = "Luxury Property"
    location = "1234 Main St, Anytown, USA"
    purpose = "Residential"
    title = "Beautiful Home"
    number_of_bath = 2
    number_of_bed = 3
    price = 250000
    type = "House"
    whatsapp_number = "+123456789"
    is_sold = False


class PropertyImagesFactory(DjangoModelFactory):
    class Meta:
        model = PropertyImages

    property = factory.SubFactory(PropertyFactory)
    image = factory.django.ImageField()


class PropertyAmenityFactory(DjangoModelFactory):
    class Meta:
        model = PropertyAmenity

    property = factory.SubFactory(PropertyFactory)
    amenity = factory.SubFactory(AmenityOptionFactory)


class PropertyOfferFactory(DjangoModelFactory):
    class Meta:
        model = PropertyOffers

    property = factory.SubFactory(PropertyFactory)
    price = 12000
    state = MobileState.PENDING
    offered_by = factory.SubFactory(UserFactory)
