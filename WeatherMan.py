import argparse

from WeatherParser import WeatherDataParser
from WeatherFileReader import WeatherFileReader
from WeatherReports import WeatherReportGenerator

class WeatherMan:
    weather_file_reader = WeatherFileReader()
    weather_parser = WeatherDataParser()
    weather_report_generator = WeatherReportGenerator()
    
    def handle_user_input_for_month_and_year(self, files_path, valid_date):
        year, month_abbr = valid_date
        weather_files = self.weather_file_reader.filter_filename_by_year_and_month(files_path, year, month_abbr)
        
        return self.weather_file_reader.read_file(weather_files, files_path)
        
    def main_execute(self):
        parser = argparse.ArgumentParser(description="Weather man")
    
        parser.add_argument("files_path", help="It's the files_path where data is placed")
        parser.add_argument("-a", help="This is for the average month report")
        parser.add_argument("-b", help="This is for bonus report")
        parser.add_argument("-c", help="This is for the chart report")
        parser.add_argument("-e", help="This is for the year report")
        
        user_input = parser.parse_args()
        
        if user_input.e:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.e)
            year, month_abbr = valid_date
            
            if year and not month_abbr:
                weather_records = self.handle_user_input_for_month_and_year(user_input.files_path, valid_date)
                
                if len(weather_records):
                    self.weather_report_generator.generate_year_weather_report(weather_records)
            else:
                print("Error: Not a valid year")
        
        if user_input.a:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.a)
            year, month_abbr = valid_date
            
            if year and month_abbr:
                weather_records = self.handle_user_input_for_month_and_year(user_input.files_path, valid_date)
                
                if len(weather_records):
                    self.weather_report_generator.generate_month_weather_report(weather_records)
            else:
                print("Error: Not a valid month")
            
        if user_input.c:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.c)
            year, month_abbr = valid_date
            
            if year and month_abbr:
                weather_records = self.handle_user_input_for_month_and_year(user_input.files_path, valid_date)
                
                if len(weather_records):    
                    self.weather_report_generator.generate_month_temperature_bar_chart(weather_records)
            else:
                print("Error: Not a valid month")
        
        if user_input.b:
            valid_date = self.weather_parser.parse_arguments_for_date(user_input.b)
            year, month_abbr = valid_date
        
            if year and month_abbr:
                weather_records = self.handle_user_input_for_month_and_year(user_input.files_path, valid_date)
            
                if len(weather_records):
                    self.weather_report_generator.generate_month_temperature_bar_chart_bonus_task(weather_records)
            else:
                print("Error: Not a valid month")

def main():
    weatherman = WeatherMan()
    
    weatherman.main_execute()

if __name__ == "__main__":
    main()
