import argparse

from weatherParser import WeatherDataParser
from weatherFileReader import WeatherFileReader
from weatherReports import WeatherReportGenerator

class WeatherMan:
    weather_file_reader = WeatherFileReader()
    weather_parser = WeatherDataParser()
    weather_report_generator = WeatherReportGenerator()
    
    def handle_user_input_for_year(self, path, year):
        year_files = self.weather_file_reader.filter_filename_by_year_and_month(path, year)
        weather_record = self.weather_file_reader.read_file(year_files, path)
        return weather_record
    
    def handle_user_input_for_month(self, path, valid_date):
        year, month_abbr = valid_date
        month_files = self.weather_file_reader.filter_filename_by_year_and_month(path, year, month_abbr)
        weather_record = self.weather_file_reader.read_file(month_files, path)
        
        return weather_record
    
    def main_execute(self):
        parser = argparse.ArgumentParser(description="Weather man")
    
        parser.add_argument("path", help="It's the path where data is placed")
        parser.add_argument("-a", help="This is for the average month report")
        parser.add_argument("-b", help="This is for bonus report")
        parser.add_argument("-c", help="This is for the chart report")
        parser.add_argument("-e", help="This is for the year report")
        
        user_input = parser.parse_args()
        
        if user_input.e:
            year, _ = self.weather_parser.parse_arguments_for_date(user_input.e)
            # problem validation krty hoay month ko valid kr dyta or agy calculation ma jty hoay ignore kr dyta
            if year:
                weather_record = self.handle_user_input_for_year(user_input.path, year)
                self.weather_report_generator.generate_year_weather_report(weather_record)
            else:
                print("Error: Not a valid year")
        
        if user_input.a:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.a)
            if valid_date:
                weather_record = self.handle_user_input_for_month(user_input.path, valid_date)
                self.weather_report_generator.generate_month_weather_report(weather_record)
            else:
                print("Error: Not a valid month")
            
        if user_input.c:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.c)
            if valid_date:
                weather_record = self.handle_user_input_for_month(user_input.path, valid_date)
                self.weather_report_generator.generate_month_temperature_bar_chart(weather_record)
            else:
                print("Error: Not a valid month")
        
        if user_input.b:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.b)
            
            if valid_date:
                weather_record = self.handle_user_input_for_month(user_input.path, valid_date)
                self.weather_report_generator.generate_month_temperature_bar_chart_bonus_task(weather_record)
            else:
                print("Error: Not a valid month")

def main():
    weatherman = WeatherMan()
    
    weatherman.main_execute()

if __name__ == "__main__":
    main()
     
