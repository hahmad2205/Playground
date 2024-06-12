import argparse
import calendar
import fnmatch
import os
import re

class WeatherReportGenerator:
    
    def filter_filename_by_year(self, user_input):
        return [
            weather_file for weather_file in os.listdir(user_input.path)
            if fnmatch.fnmatch(weather_file, f"*{user_input.e}*.txt")
        ]

    def parse_arguments_for_month(self, month):
        year_pattern = r'^\d{4}'
        month_pattern = r'(0?[1-9]|1[0-2])$'
        matched_year = re.search(year_pattern, month)
        matched_month_number = re.search(month_pattern, month)
        
        if not matched_year or not matched_month_number:
            return []
        
        year = matched_year.group()
        month_abbr = calendar.month_abbr[int(matched_month_number.group())]
        
        return year, month_abbr
    
    def filter_filename_by_month(self, user_input, year, month_abbr):

        for weather_file in os.listdir(user_input.path):
            
            if fnmatch.fnmatch(weather_file, f"*{year}_{month_abbr}*.txt"):
                return weather_file
    
    def read_file(self, file_name, user_input):
        
        with open(user_input.path + file_name, "r") as weather_file:
            headings = weather_file.readline().strip().split(",")
            weather_lines = weather_file.readlines()
            weather_lines_record, date = self.covert_weather_data_in_required_format(headings, weather_lines)
        return weather_lines_record, date
    
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
        date_abbr = "PKT" if "PKT" in headings else "PKST"
        weather_lines_record = [{headings[index] : item for index, item in enumerate(line.strip().split(sep = ","))} for line in weather_lines]
        return weather_lines_record, date_abbr
    
    def generate_weather_record_for_month(self,user_input, key):
        year, month_abbr = self.parse_arguments_for_month(key)
        month_files = self.filter_filename_by_month(user_input, year, month_abbr)
        return self.read_file(month_files, user_input)
               
    def calculate_max_temperature_year(self, weather_record, date_abbr, max_temperature, max_temperature_date):
        for weather_line in weather_record:
            max_temperature_value = weather_line.get("Max TemperatureC")
            
            if max_temperature_value:
                current_temperature = int(max_temperature_value)
                max_temperature = max(max_temperature, current_temperature)
                max_temperature_date = weather_line[date_abbr] if current_temperature == int(max_temperature) else max_temperature_date
        return max_temperature, max_temperature_date
        
    def calculate_min_temperature_year(self, weather_record, date_abbr, min_temperature, min_temperature_date):
        for weather_line in weather_record:
            min_temperature_value = weather_line.get("Min TemperatureC")
            
            if min_temperature_value:
                current_temperature = int(min_temperature_value)
                min_temperature = min(current_temperature, min_temperature)
                min_temperature_date = weather_line[date_abbr] if current_temperature == int(min_temperature) else min_temperature_date
        return min_temperature, min_temperature_date
        
    def calculate_max_humid_year(self, weather_record, date_abbr, max_humid, max_humid_date):
        for weather_line in weather_record:
            max_humidity_value = weather_line.get("Max Humidity")
            
            if max_humidity_value:
                current_humid = int(max_humidity_value)
                max_humid = max(current_humid, max_humid)
                max_humid_date = weather_line[date_abbr] if current_humid == int(max_humid) else max_humid_date
        return max_humid, max_humid_date

    def calculate_avg_max_temperature_month(self, weather_record):
        return self.calculate_average(weather_record, "Max TemperatureC")
    
    def calculate_avg_min_temperature_month(self,weather_record):        
        return self.calculate_average(weather_record, "Min TemperatureC")
        
    def calculate_avg_mean_humid_month(self, weather_record):
        return self.calculate_average(weather_record, " Mean Humidity")
    
    def generate_year_weather_report(self, user_input):
        max_temperature = float("-inf")
        min_temperature = float("inf")
        max_humid = float("-inf")
        max_temperature_date = None
        min_temperature_date = None
        max_humid_date = None
        year_files = self.filter_filename_by_year(user_input)
        
        for file_name in year_files:
            weather_record, date_abbr = self.read_file(file_name, user_input)
            
            max_temperature, max_temperature_date = self.calculate_max_temperature_year(weather_record, date_abbr, max_temperature, max_temperature_date)
            min_temperature, min_temperature_date = self.calculate_min_temperature_year(weather_record, date_abbr, min_temperature, min_temperature_date)
            max_humid, max_humid_date = self.calculate_max_humid_year(weather_record, date_abbr, max_humid, max_humid_date)
            
        self.print_year_weather_report(max_temperature, max_temperature_date, min_temperature, min_temperature_date, max_humid, max_humid_date)
        
    def generate_month_weather_report(self, user_input):
        weather_record, _ = self.generate_weather_record_for_month(user_input, user_input.a)
        avg_high_temperature = self.calculate_avg_max_temperature_month(weather_record)
        avg_low_temperature = self.calculate_avg_min_temperature_month(weather_record)
        avg_mean_humid = self.calculate_avg_mean_humid_month(weather_record)
        self.print_month_weather_report(avg_high_temperature, avg_low_temperature, avg_mean_humid)
        
    def generate_month_temperature_bar_chart(self, user_input):
        weather_record, date_abbr = self.generate_weather_record_for_month(user_input, user_input.c)    
        self.print_month_temperature_bar_chart(weather_record, date_abbr)
    
    def generate_month_temperature_bar_chart_bonus_task(self, user_input):
        weather_record, date_abbr = self.generate_weather_record_for_month(user_input, user_input.b)
        self.print_month_temperature_bar_chart_bonus_task(weather_record, date_abbr)
    
    def print_star(self, plus_count, color):
        
        for i in range(0, plus_count):
            print(f"{color}+\033[0m", end = "")
    
    def print_month_weather_report(self, avg_high_temperature, avg_low_temperature, avg_mean_humid):
        print("Monthly Average Weather Report", end = "\n\n")
        print(f"Highest Average: {avg_high_temperature}C")       
        print(f"Lowest Average: {avg_low_temperature}C")
        print(f"Average Mean Humidity: {avg_mean_humid}C", end = "\n\n")
    
    def print_month_temperature_bar_chart(self, weather_record, date_abbr):
        
        for line in weather_record:
            date = line[date_abbr].split(sep = "-")[2]
            
            if line["Max TemperatureC"]:
                print(date, end = "    ")
                self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                print(f"{line['Max TemperatureC']}C")
            
            if line["Min TemperatureC"]:
                print(date, end = "    ")
                self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                print(f"{line['Min TemperatureC']}C")
    
    def print_month_temperature_bar_chart_bonus_task(self, weather_record, date_abbr):
        
        for line in weather_record:
            
            if line["Min TemperatureC"] or line["Max TemperatureC"]:
                date = line[date_abbr].split(sep = "-")[2]
                print(date, end = "    ")
                
                if line["Min TemperatureC"]:
                    self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                
                if line["Max TemperatureC"]:
                    self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                print(f"{line['Min TemperatureC']}C - {line['Max TemperatureC']}C")
    
    def print_year_weather_report(self, max_temperature, max_temperature_date, min_temperature, min_temperature_date, max_humid, max_humid_date):
        
        if max_temperature != "" and max_temperature_date is not None:
            month_number = int(max_temperature_date.split(sep = "-")[1])
            date = max_temperature_date.split(sep = "-")[2]
            print(f"Highest: {max_temperature}C on {calendar.month_abbr[month_number]} {date}")
        
        if min_temperature != "" and min_temperature_date is not None:
            month_number = int(min_temperature_date.split(sep = "-")[1])
            date = min_temperature_date.split(sep = "-")[2]
            print(f"Lowest: {min_temperature}C on {calendar.month_abbr[month_number]} {date}")
        
        if max_humid != "" and max_humid_date is not None:
            month_number = int(max_humid_date.split(sep = "-")[1])
            date = max_humid_date.split(sep = "-")[2]
            print(f"Humidity: {max_humid}% on {calendar.month_abbr[month_number]} {date}", end = "\n\n")    
    
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
        weather_report_generator.generate_year_weather_report(user_input)
    
    if user_input.a:
        weather_report_generator.generate_month_weather_report(user_input)
        
    if user_input.c:
        weather_report_generator.generate_month_temperature_bar_chart(user_input)
    
    if user_input.b:
        weather_report_generator.generate_month_temperature_bar_chart_bonus_task(user_input)
    
main()
