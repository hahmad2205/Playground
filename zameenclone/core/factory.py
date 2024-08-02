import factory
from factory.django import DjangoModelFactory
from core.models import Amenity, AmenityOption


class AmenityFactory(DjangoModelFactory):

    class Meta:
        model = Amenity

    name = factory.Sequence(lambda n: f"Amenity {n}")


class AmenityOptionFactory(DjangoModelFactory):

    class Meta:
        model = AmenityOption

    option = factory.Sequence(lambda n: f"Option {n}")
    amenity = factory.SubFactory(AmenityFactory)

