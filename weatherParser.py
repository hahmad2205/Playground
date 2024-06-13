import calendar
import re

class WeatherDataParser:
    
    def parse_arguments_for_date(self, date):
        year_pattern = r'^\d{4}'
        month_pattern = r'(0?[1-9]|1[0-2])$'
        matched_year = re.search(year_pattern, date)
        matched_month_number = re.search(month_pattern, date)
        
        if matched_year and matched_month_number:    
            year = matched_year.group()
            month_abbr = calendar.month_abbr[int(matched_month_number.group())]
            
            return year, month_abbr
        
        if matched_year:
            year = matched_year.group()
            return year
        
        return None
