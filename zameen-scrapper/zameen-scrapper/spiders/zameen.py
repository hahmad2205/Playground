import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ZameenSpider(CrawlSpider):
    name = 'zameen'
    allowed_domains = ['www.zameen.com']
    start_urls = ['https://www.zameen.com/Houses_Property/Lahore-1-1.html']
    house_records = []
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@aria-label, "Listing link")]'), callback='parse_house_links'),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@title, "Next")]')),
    )
    
    def details_span_scraper(self, response, key):
        house_type = response.xpath(f'//span[contains(@aria-label, "{key}")]/text()').get()
        return house_type.strip() if house_type else ""
    
    def details_amenities_scraper(self, response, key):
        amenity_type = response.xpath(f'//ul/li[{key}]/div/div/text()').get()
        amenities = response.xpath('//li/ul[1]/li/span/text()').getall()
        return amenity_type, amenities
    
    def whatsapp_number_scrapper(self, response):
        whatsapp_script = response.css(f'script::text').getall()
        regex = '"whatsapp":"(\d{11,13})"'
        match = re.search(regex, str(whatsapp_script))
        return match.group(1) if match else ""
    
    def parse_house_links(self, response):
        amentities = {}
        house_type_text = self.details_span_scraper(response, "Type")
        house_price_text = response.xpath(f'string(//span[contains(@aria-label, "Price")]/div)').get()
        house_location_text = self.details_span_scraper(response, "Location")
        house_baths_text = self.details_span_scraper(response, "Baths")
        house_area_text = response.xpath(f'//span[contains(@aria-label, "Area")]/span/text()').get()
        house_purpose_text = self.details_span_scraper(response, "Purpose")
        house_bedrooms_text = self.details_span_scraper(response, "Beds")
        house_added_text = self.details_span_scraper(response, "Creation date")
        house_description_text = response.xpath(f'string(//div[contains(@aria-label, "Property description")]/div/span)').get()
        whatsapp_number = self.whatsapp_number_scrapper(response)
        
        house_images_links = response.xpath('//img[contains(@role, "presentation")]/@src').getall()
    
        matching_elements = response.xpath(f"//*[contains(text(), 'Amenities')]")
        features = matching_elements.xpath("following-sibling::div[1]/div/ul/li").getall()
        for index in range(1, len(features)):
            catergory, features = self.details_amenities_scraper(response, index)
            amentities[catergory] = features
    
        house_record = {
                    "Type": house_type_text, "Price": house_price_text,
                    "Location": house_location_text, "Baths": house_baths_text,
                    "Area": house_area_text, "Purpose": house_purpose_text,
                    "Bedrooms": house_bedrooms_text, "added_date": house_added_text,
                    "house_description_text": house_description_text, "whatsapp": whatsapp_number,
                    "Amenitites": amentities, "images": house_images_links
        }
        
        self.house_records.append(house_record)

# {
#  'downloader/request_bytes': 656605,
#  'downloader/request_count': 1289,
#  'downloader/request_method_count/GET': 1289,
#  'downloader/response_bytes': 226857378,
#  'downloader/response_count': 1289,
#  'downloader/response_status_count/200': 1289,
#  'dupefilter/filtered': 12,
#  'elapsed_time_seconds': 493.064812,
#  'finish_reason': 'finished',
#  'finish_time': datetime.datetime(2024, 6, 22, 14, 40, 29, 861849, tzinfo=datetime.timezone.utc),
#  'httpcompression/response_bytes': 1238931685,
#  'httpcompression/response_count': 1289,
#  'log_count/DEBUG': 1293,
#  'log_count/INFO': 18,
#  'memusage/max': 237535232,
#  'memusage/startup': 66908160,
#  'request_depth_max': 50,
#  'response_received_count': 1289,
#  'robotstxt/request_count': 1,
#  'robotstxt/response_count': 1,
#  'robotstxt/response_status_count/200': 1,
#  'scheduler/dequeued': 1288,
#  'scheduler/dequeued/memory': 1288,
#  'scheduler/enqueued': 1288,
#  'scheduler/enqueued/memory': 1288,
#  'start_time': datetime.datetime(2024, 6, 22, 14, 32, 16, 797037, tzinfo=datetime.timezone.utc)
# }
