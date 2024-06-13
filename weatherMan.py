import argparse
import calendar
import datetime
import fnmatch
import os
import re

class WeatherReportGenerator:
        
    def filter_filename_by_year_and_month(self, user_input, year = None, month_abbr = None):
        if user_input.e:
            pattern = f"*{user_input.e}*.txt"
        else:
            pattern = f"*{year}_{month_abbr}*.txt"
            
        return [
            weather_file for weather_file in os.listdir(user_input.path)
            if fnmatch.fnmatch(weather_file, pattern)
        ]
      
    def parse_arguments_for_date(self, month):
        year_pattern = r'^\d{4}'
        month_pattern = r'(0?[1-9]|1[0-2])$'
        matched_year = re.search(year_pattern, month)
        matched_month_number = re.search(month_pattern, month)
        
        if matched_year and matched_month_number:    
            year = matched_year.group()
            month_abbr = calendar.month_abbr[int(matched_month_number.group())]
            
            return year, month_abbr
        
        if matched_year:
            year = matched_year.group()
            return year
        
        return None
    
    def read_file(self, weather_file_names, user_input):
        weather_lines_record = []
        for weather_file_name in weather_file_names:
            with open(user_input.path + weather_file_name, "r") as weather_file:
                headings = weather_file.readline().strip().split(",")
                weather_lines = weather_file.readlines()
                weather_lines = self.covert_weather_data_in_required_format(headings, weather_lines)
                weather_lines_record.extend(weather_lines)

        return weather_lines_record
    
    def calculate_max_value(self, weather_record, key):
        max_temperatures = []
        for weather_line in weather_record:
            
            if weather_line.get(key):
                current_value = int(weather_line.get(key))
                max_temperatures.append(current_value)
                max_value = max(max_temperatures)
                date_abbr = weather_line["PKT"] if weather_line.get("PKT") else weather_line["PKST"]
                max_value_date = date_abbr if current_value == int(max_value) else max_value_date
        
        return max_value, max_value_date
    
    def calculate_average(self, weather_record, key):
        sum_of_values = 0
        
        if not len(weather_record):
            return 0
        
        for weather_line in weather_record:
            value = weather_line.get(key)
        
            if value:
                sum_of_values = sum_of_values + int(weather_line[key])
        return int(sum_of_values / len(weather_record))
    
    def covert_weather_data_in_required_format(self, headings, weather_lines):
        weather_lines_record = [{headings[index] : item for index, item in enumerate(line.strip().split(sep = ","))} for line in weather_lines]
        return weather_lines_record
  
    def generate_weather_record_for_month(self, valid_date, user_input):
        year, month_abbr = valid_date
        month_files = self.filter_filename_by_year_and_month(user_input, year, month_abbr)
        weather_record = self.read_file(month_files, user_input)
        
        return weather_record
          
    def calculate_min_temperature_year(self, weather_record):
        min_temperatures = []
        for weather_line in weather_record:
            min_temperature_value = weather_line.get("Min TemperatureC")
            
            if min_temperature_value:
                current_temperature = int(min_temperature_value)
                min_temperatures.append(current_temperature)
                min_temperature = min(min_temperatures)
                date_abbr = weather_line["PKT"] if weather_line.get("PKT") else weather_line["PKST"]
                min_temperature_date = date_abbr if current_temperature == int(min_temperature) else min_temperature_date
        
        return min_temperature, min_temperature_date
        
    def generate_year_weather_report(self, user_input):
        year_files = self.filter_filename_by_year_and_month(user_input)
        weather_record = self.read_file(year_files, user_input)

        if len(weather_record):
            max_temperature, max_temperature_date = self.calculate_max_value(weather_record, "Max TemperatureC")
            min_temperature, min_temperature_date = self.calculate_max_value(weather_record,"Max Humidity")
            max_humid, max_humid_date = self.calculate_max_humid_year(weather_record)
            self.print_year_weather_report(max_temperature, max_temperature_date, min_temperature, min_temperature_date, max_humid, max_humid_date)
            return
            
    def generate_month_weather_report(self, user_input, valid_date):
        weather_record = self.generate_weather_record_for_month(valid_date, user_input)
        
        if len(weather_record):
            avg_high_temperature = self.calculate_average(weather_record, "Max TemperatureC")
            avg_low_temperature = self.calculate_average(weather_record, "Min TemperatureC")
            avg_mean_humid = self.calculate_average(weather_record, " Mean Humidity")
            self.print_month_weather_report(avg_high_temperature, avg_low_temperature, avg_mean_humid)
        
    def generate_month_temperature_bar_chart(self, user_input, valid_date):
        weather_record = self.generate_weather_record_for_month(valid_date, user_input)
        if len(weather_record):
            self.print_month_temperature_bar_chart(weather_record)
    
    def generate_month_temperature_bar_chart_bonus_task(self, user_input, valid_date):
        weather_record = self.generate_weather_record_for_month(valid_date, user_input)
        if len(weather_record):
            self.print_month_temperature_bar_chart_bonus_task(weather_record)
    
    def print_star(self, plus_count, color):
        
        for _ in range(0, plus_count):
            print(f"{color}+\033[0m", end = "")
    
    def print_month_weather_report(self, avg_high_temperature, avg_low_temperature, avg_mean_humid):
        print("Monthly Average Weather Report", end = "\n\n")
        print(f"Highest Average: {avg_high_temperature}C")       
        print(f"Lowest Average: {avg_low_temperature}C")
        print(f"Average Mean Humidity: {avg_mean_humid}C", end = "\n\n")
    
    def print_month_temperature_bar_chart(self, weather_record):
        
        for line in weather_record:
            date_abbr = line["PKT"] if line.get("PKT") else line["PKST"]
            date = datetime.datetime.strptime(date_abbr, "%Y-%m-%d")
            date = date.day
            
            if line["Max TemperatureC"]:
                print(date, end = "    ")
                self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                print(f"{line['Max TemperatureC']}C")
            
            if line["Min TemperatureC"]:
                print(date, end = "    ")
                self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                print(f"{line['Min TemperatureC']}C")
    
    def print_month_temperature_bar_chart_bonus_task(self, weather_record):
        
        for line in weather_record:
            
            if line["Min TemperatureC"] or line["Max TemperatureC"]:
                date_abbr = line["PKT"] if line.get("PKT") else line["PKST"]
                date = datetime.datetime.strptime(date_abbr, "%Y-%m-%d")
                date = date.day
                print(date, end = "    ")
                
                if line["Min TemperatureC"]:
                    self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                
                if line["Max TemperatureC"]:
                    self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                print(f"{line['Min TemperatureC']}C - {line['Max TemperatureC']}C")
    
    def print_year_weather_report(self, max_temperature, max_temperature_date, min_temperature, min_temperature_date, max_humid, max_humid_date):
        
        if max_temperature != "" and max_temperature_date:
            date = datetime.datetime.strptime(max_temperature_date, "%Y-%m-%d")
            print(f"Highest: {max_temperature}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if min_temperature != "" and min_temperature_date:
            date = datetime.datetime.strptime(min_temperature_date, "%Y-%m-%d")
            print(f"Lowest: {min_temperature}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if max_humid != "" and max_humid_date:
            date = datetime.datetime.strptime(max_humid_date, "%Y-%m-%d")
            print(f"Humidity: {max_humid}% on {calendar.month_abbr[date.month]} {date.day}", end = "\n\n")    
    
def main():
    
    weather_report_generator = WeatherReportGenerator()
    
    parser = argparse.ArgumentParser(description="Weather man")
    
    parser.add_argument("path", help="It's the path where data is placed")
    parser.add_argument("-a", help="This is for the average month report")
    parser.add_argument("-b", help="This is for bonus report")
    parser.add_argument("-c", help="This is for the chart report")
    parser.add_argument("-e", help="This is for the year report")
    
    user_input = parser.parse_args()
    
    if user_input.e:
        if weather_report_generator.parse_arguments_for_date(user_input.e):
            weather_report_generator.generate_year_weather_report(user_input)
        else:
            print("Error: Not a valid year")
    
    if user_input.a:
        valid_date = weather_report_generator.parse_arguments_for_date(user_input.a)
        
        if valid_date:
            weather_report_generator.generate_month_weather_report(user_input, valid_date)
        else:
            print("Error: Not a valid year")
        
    if user_input.c:
        valid_date = weather_report_generator.parse_arguments_for_date(user_input.c)
        
        if valid_date:
            weather_report_generator.generate_month_temperature_bar_chart(user_input, valid_date)
        else:
            print("Error: Not a valid year")
    
    if user_input.b:
        valid_date = weather_report_generator.parse_arguments_for_date(user_input.b)
        
        if valid_date:
            weather_report_generator.generate_month_temperature_bar_chart_bonus_task(user_input, valid_date)
        else:
            print("Error: Not a valid year")
    
main()
