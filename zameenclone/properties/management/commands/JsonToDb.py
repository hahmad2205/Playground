import json

from django.core.management.base import BaseCommand

from core.models import Amenity, AmenityOption
from properties.models import Property, PropertyImages, PropertyAmenity


class Command(BaseCommand):
    help = "Store data from given json file to db"
    
    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="The path of json file")

    def convert_price_to_number(self, price):
        price = price.replace("PKR", "").strip()
        parts = price.split()
        price_number = float(parts[0])
        price_text = parts[1].lower()
        price_in_numbers = 0
        if price_text == "crore":
            price_in_numbers = price_number * 10000000
        elif price_text == "lakh":
            price_in_numbers = price_number * 100000
        
        return price_in_numbers

    def convert_area_in_marla(self, area):
        parts = area.split()
        area_number = float(parts[0])
        area_text = parts[1].lower()
        area_in_numbers = 0
        if area_text == "marla":
            area_in_numbers = area_number * 1
        elif area_text == "kanal":
            area_in_numbers = area_number * 20
        
        return area_in_numbers
    
    def store_property_to_db(self, record):
        area = self.convert_area_in_marla(record["Area"])
        description = record["house_description_text"]
        header = record["header"]
        location = record["Location"]
        purpose = record["Purpose"]
        number_of_bath = record["Baths"].split(sep=" ")[0] if not record["Baths"].split(sep=" ")[0] == "-" else 0
        number_of_bed = record["Bedrooms"].split(sep=" ")[0] if not record["Bedrooms"].split(sep=" ")[0] == "-" else 0
        price = self.convert_price_to_number(record["Price"])
        title = record["title"]
        type = record["Type"]
        whatsapp_number = record["whatsapp"]
        
        property, created = Property.objects.get_or_create(
            area = area,
            description = description,
            header = header,
            location = location,
            purpose = purpose,
            number_of_bath = number_of_bath,
            number_of_bed = number_of_bed,
            price = price,
            title = title,
            type = type,
            whatsapp_number = whatsapp_number
        )
        
        return property
        
    def store_images_to_db(self, images, property):
        for image in images:
            image = PropertyImages.objects.get_or_create(
                image_url = image,
                property = property
            )
    
    def store_amenity_to_db(self):
        amenities = ["main features", "rooms"]
        for amenity_name in amenities:
            amenity, created = Amenity.objects.get_or_create(name = amenity_name)
            if amenity_name == "main features":
                amenity_options = [
                    "built in year", "parking spaces", "double glazed windows", "flooring",
                    "electricity backup", "waste disposal", "floors", "other main features"
                ]
            elif amenity_name == "rooms":
                amenity_options = [
                    "bedrooms", "bathrooms", "servant quarters", "drawing room", "dining room",
                    "kitchens", "study room", "prayer room", "powder room ", "store rooms",
                    "steam room", "lounge or sitting room", "laundry room", "other rooms"
                ]
            self.store_amenity_options_to_db(amenity, amenity_options)

    def store_amenity_options_to_db(self, amenity, amenity_options):
        for amenity_option in amenity_options:
            AmenityOption.objects.get_or_create(
                option = amenity_option,
                amenity = amenity
            )
    
    def is_integer(self, alphabet):
        return alphabet.isdigit()

    def store_amenity_values_to_db(self, amenities, property):
        for amenity_name, amenity_options in amenities.items():
            if amenity_name.lower() in ["main features", "rooms"]:
                for index, amenity_option in enumerate(amenity_options):
                    try:
                        amenity_option_instance = AmenityOption.objects.get(option=amenity_option.lower())                   
                        if amenity_option_instance:
                            value = None
                            if index + 1 < len(amenity_options):
                                next_option = amenity_options[index + 1]
                                if len(next_option.split()) > 1:
                                    value_part = next_option.split()[1]
                                    if self.is_integer(value_part):
                                        value = int(value_part)
                            
                            property_amenity, created = PropertyAmenity.objects.get_or_create(
                                property=property,
                                amenity=amenity_option_instance,
                                value=value
                            )
                            property.amenities.add(property_amenity)
                            
                    except AmenityOption.DoesNotExist:
                        pass


    def handle(self, *args, **kwargs):
        property_records = json.load(open(kwargs["file"], "r"))
        
        for record in property_records:
            property = self.store_property_to_db(record)
            self.store_images_to_db(record["images"], property)
            self.store_amenity_to_db()
            self.store_amenity_values_to_db(record["Amenitites"], property)
            self.stdout.write(self.style.SUCCESS(f"Property {property.title} is created by id {property.id}"))

