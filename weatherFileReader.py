import fnmatch
import os

class WeatherFileReader:
    
    def filter_filename_by_year_and_month(self, path, year=None, month_abbr=None):
        pattern = f"*{year}_{month_abbr}*.txt" if year and month_abbr else f"*{year}*.txt"
            
        return [
            weather_file for weather_file in os.listdir(path)
            if fnmatch.fnmatch(weather_file, pattern)
        ]
    
    def read_file(self, weather_file_names, path):
        weather_records = []
        for weather_file_name in weather_file_names:
            with open(path + weather_file_name, "r") as weather_file:
                weather_headings = weather_file.readline().strip().split(",")
                weather_records_per_file = weather_file.readlines()
                weather_records_per_file = self.covert_weather_data_in_required_format(weather_headings, weather_records_per_file)
                weather_records.extend(weather_records_per_file)

        return weather_records
    
    def covert_weather_data_in_required_format(self, weather_headings, weather_records_per_file):
        return [
            {weather_headings[index] : item for index, item in enumerate(record.strip().split(sep = ","))}
            for record in weather_records_per_file
        ]
        