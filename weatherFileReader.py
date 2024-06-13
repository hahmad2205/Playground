import fnmatch
import os

class WeatherFileReader:
    
    def filter_filename_by_year_and_month(self, path, year = None, month_abbr = None):
        if year and month_abbr:
            pattern = f"*{year}_{month_abbr}*.txt"
        else:
            pattern = f"*{year}*.txt"
            
        return [
            weather_file for weather_file in os.listdir(path)
            if fnmatch.fnmatch(weather_file, pattern)
        ]
    
    def read_file(self, weather_file_names, path):
        weather_lines_record = []
        for weather_file_name in weather_file_names:
            with open(path + weather_file_name, "r") as weather_file:
                headings = weather_file.readline().strip().split(",")
                weather_lines = weather_file.readlines()
                weather_lines = self.covert_weather_data_in_required_format(headings, weather_lines)
                weather_lines_record.extend(weather_lines)

        return weather_lines_record
    
    def covert_weather_data_in_required_format(self, headings, weather_lines):
        weather_lines_record = [{headings[index] : item for index, item in enumerate(line.strip().split(sep = ","))} for line in weather_lines]
        return weather_lines_record
