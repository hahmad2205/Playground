import json
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.signalmanager import dispatcher
from scrapy.linkextractors import LinkExtractor
from scrapy import signals

class ZameenSpider(CrawlSpider):
    name = "zameen"
    allowed_domains = ["www.zameen.com"]
    start_urls = ["https://www.zameen.com/Houses_Property/Lahore-1-1.html"]
    house_records = []
    whatsapp_regex = re.compile(r'"whatsapp":"(\d{11,13})"')
    rules = (
        Rule(
            LinkExtractor(
                    restrict_xpaths="//a[contains(@aria-label, 'Listing link')]"
            ),
            callback="parse_house_records"
        ),
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@title, 'Next')]")),
    )
        
    def get_house_details(self, response, key):
        house_type = response.xpath(f"//span[contains(@aria-label, '{key}')]/text()").get()
        return house_type.strip() if house_type else ""
        
    def get_whatsapp_number(self, response):
        whatsapp_script = response.css("script::text").getall()
        match = self.whatsapp_regex.search(str(whatsapp_script))
        return match.group(1) if match else ""
    
    def get_amenities_details(self, feature):
        amenity_type = feature.xpath(".//div/div/text()").get()
        amenities = feature.xpath("(.//ul/li/span/text())").getall()
        return amenity_type, amenities
    
    def store_data_to_json(self, house_record):
        with open("data.json", "w") as json_file:
            json.dump(house_record, json_file, indent=4)
        pass
    
    def parse_house_records(self, response):
        amentities = {}
        house_title_text = response.xpath("//main/div/div/div/h1/text()").get()
        house_header_text = response.xpath("//div[contains(@aria-label, 'Property header')]/text()").get()
        house_type_text = self.get_house_details(response, "Type")
        house_price_text = response.xpath(f"string(//span[contains(@aria-label, 'Price')]/div)").get()
        house_location_text = self.get_house_details(response, "Location")
        house_baths_text = self.get_house_details(response, "Baths")
        house_area_text = response.xpath(f"//span[contains(@aria-label, 'Area')]/span/text()").get()
        house_purpose_text = self.get_house_details(response, "Purpose")
        house_bedrooms_text = self.get_house_details(response, "Beds")
        house_added_text = self.get_house_details(response, "Creation date")
        house_description_text = (
                            response.xpath(
                                        f"string(//div[contains(@aria-label, 'Property description')]/div/span)"
                            ).get()
        )
        whatsapp_number = self.get_whatsapp_number(response)
        
        house_images_links = response.xpath("//img[contains(@role, 'presentation')]/@src").getall()
    
        matching_elements = response.xpath(f"//*[contains(text(), 'Amenities')]")
        
        for feature in matching_elements.xpath("following-sibling::div[1]/div/ul/li"):
            category, features = self.get_amenities_details(feature)
            amentities[category] = features
    
        house_record = {
                    "title": house_title_text, "header": house_header_text,
                    "Type": house_type_text, "Price": house_price_text,
                    "Location": house_location_text, "Baths": house_baths_text,
                    "Area": house_area_text, "Purpose": house_purpose_text,
                    "Bedrooms": house_bedrooms_text, "added_date": house_added_text,
                    "house_description_text": house_description_text, "whatsapp": whatsapp_number,
                    "Amenitites": amentities, "images": house_images_links
        }
        
        self.house_records.append(house_record)

    def close(self, reason: str):
        self.store_data_to_json(self.house_records)
        super().close(reason)

