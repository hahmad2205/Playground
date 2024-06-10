import argparse
import calendar
import fnmatch
import os

class WeatherReportGenerator:
    
    def filter_filename_by_year(self, args):
        year_files = [file for file in os.listdir(args.path)
                      if fnmatch.fnmatch(file, f"*{args.e}*.txt")]
        
        return year_files
    
    def filter_filename_by_month(self, args, month):
        month_year = month.split(sep = "/")
        
        for item in month_year:
            value = int(item)
            if value <= 12:
                month = calendar.month_abbr[value]
            else:
                year = value
        
        if year == None or month == None:
            return []
        
        month_files = [file for file in os.listdir(args.path)
                        if fnmatch.fnmatch(file, f"*{year}_{month}*.txt")]

        return month_files
    
    def read_file(self, file_name, args):
        
        with open(args.path + file_name, "r") as file:
            headings = file.readline().strip().split(",")
            weather_lines = file.readlines()
            weather_lines_record, date = self.covert_weather_data_in_required_format(headings, weather_lines)
        
        return weather_lines_record, date        
    
    def calculate_average(self, weather_record, key):
        sum_of_values = 0
        for line in weather_record:
            value = line.get(key)
            if value:
                sum_of_values = sum_of_values + int(line[key])
                
        return int(sum_of_values / len(weather_record))
    
    def print_star(self, count, color):
        
        for i in range(0, count):
            print(f"{color}+\033[0m", end = "")
    
    def covert_weather_data_in_required_format(self, headings, weather_lines):
        date = "PKT" if "PKT" in headings else "PKST"
        weather_lines_record = [{headings[index] : item for index, item in enumerate(line.strip().split(sep = ","))} for line in weather_lines]
        
        return weather_lines_record, date
    
    def calculate_max_temp_year(self, args, year_files):
        max_temp = float("-inf")
        max_temp_date = None
        
        for file_name in year_files:
            weather_record, date = self.read_file(file_name, args)
            
            for line in weather_record:
                max_temperature_value = line.get("Max TemperatureC")
                if max_temperature_value:
                    current_temp = int(line["Max TemperatureC"])
                    if current_temp > max_temp:
                        max_temp = current_temp
                        max_temp_date = line[date]
        
        return max_temp, max_temp_date
        
    def calculate_min_temp_year(self, args, year_files):
        min_temp = float("inf")
        min_temp_date = None
        
        for file_name in year_files:
            weather_record, date = self.read_file(file_name, args)
            
            for line in weather_record:
                min_temperature_value = line.get("Min TemperatureC")
                if min_temperature_value:
                    current_temp = int(line["Min TemperatureC"])
                    
                    if current_temp < min_temp:
                        min_temp = current_temp
                        min_temp_date = line[date]
        
        return min_temp, min_temp_date
        
    def calculate_max_humid_year(self, args, year_files):
        max_humid = float("-inf")
        max_humid_date = None
        
        for file_name in year_files:
            weather_record, date = self.read_file(file_name, args)
            
            for line in weather_record:
                max_humidity_value = line.get("Max Humidity")
                if max_humidity_value:
                    current_humid = int(max_humidity_value)
                    if current_humid > max_humid:
                        max_humid = current_humid
                        max_humid_date = line[date]
        
        return max_humid, max_humid_date

    def calculate_avg_max_temp_month(self, args, month_files):
        
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            
        avg_high_temp = self.calculate_average(weather_record, "Max TemperatureC")
        
        return avg_high_temp
    
    def calculate_avg_min_temp_month(self, args, month_files):
        
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            
        avg_low_temp = self.calculate_average(weather_record, "Min TemperatureC")
        
        return avg_low_temp

    def calculate_avg_mean_humid_month(self, args, month_files):
        
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            
        avg_mean_humid = self.calculate_average(weather_record, " Mean Humidity")

        return avg_mean_humid
    
    def generate_year_weather_report(self, args):
        year_files = self.filter_filename_by_year(args)
        max_temp, max_temp_date = self.calculate_max_temp_year(args, year_files)
        min_temp, min_temp_date = self.calculate_min_temp_year(args, year_files)
        max_humid, max_humid_date = self.calculate_max_humid_year(args, year_files)
        
        print("Yearly weather report", end = "\n\n")
        
        month_number = int(max_temp_date.split(sep = "-")[1])
        date = max_temp_date.split(sep = "-")[2]
        print(f"Highest: {max_temp}C on {calendar.month_abbr[month_number]} {date}")
        
        month_number = int(min_temp_date.split(sep = "-")[1])
        date = min_temp_date.split(sep = "-")[2]
        print(f"Lowest: {min_temp}C on {calendar.month_abbr[month_number]} {date}")
        
        month_number = int(max_humid_date.split(sep = "-")[1])
        date = max_humid_date.split(sep = "-")[2]
        print(f"Humidity: {max_humid}% on {calendar.month_abbr[month_number]} {date}", end = "\n\n")
        
    def generate_month_weather_report(self, args):
        month_files = self.filter_filename_by_month(args, args.a)
        avg_high_temp = self.calculate_avg_max_temp_month(args, month_files)
        avg_low_temp = self.calculate_avg_min_temp_month(args, month_files)
        avg_mean_humid = self.calculate_avg_mean_humid_month(args, month_files)
        
        print("Monthly Average Weather Report", end = "\n\n")
        
        print(f"Highest Average: {avg_high_temp}C")
        
        print(f"Lowest Average: {avg_low_temp}C")
        
        print(f"Average Mean Humidity: {avg_mean_humid}C", end = "\n\n")
        
    def generate_month_temp_bar_chart(self, args):
        month_files = self.filter_filename_by_month(args, args.c)
        
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            print("Monthly Temperature Chart", end = "\n\n")
            
            for line in weather_record:
                date = line["PKT"].split(sep = "-")[2]
                if line["Max TemperatureC"]:
                    print(date, end = "    ")
                    self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                    print(f"{line['Max TemperatureC']}C")
                if line["Min TemperatureC"]:
                    print(date, end = "    ")
                    self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                    print(f"{line['Min TemperatureC']}C")
                
        print("", end = "\n\n")
    
    def generate_month_temp_bar_chart_bonus_task(self, args):
        month_files = self.filter_filename_by_month(args, args.b)
        
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            print("Bonus Task", end = "\n\n")
            
            for line in weather_record:
                if line["Min TemperatureC"] or line["Max TemperatureC"]:
                    date = line["PKT"].split(sep = "-")[2]
                    print(date, end = "    ")
                    if line["Min TemperatureC"]:
                        self.print_star(int(line["Min TemperatureC"]), "\033[94m")
                    if line["Max TemperatureC"]:
                        self.print_star(int(line["Max TemperatureC"]), "\033[91m")
                    print(f"{line['Min TemperatureC']}C - {line['Max TemperatureC']}C")
        
        print("", end = "\n\n")

def main():
    weather_report_generator = WeatherReportGenerator()
    
    parser=argparse.ArgumentParser(description = "Weather man")
    parser.add_argument("path", help = "It's the path where data is placed")
    parser.add_argument("-a", help = "This is for the average month report")
    parser.add_argument("-b", help = "This is for bonus report")
    parser.add_argument("-c", help = "This is for the chart report")
    parser.add_argument("-e", help = "This is for the year report")
    args = parser.parse_args()
    
    if(args.e):
        weather_report_generator.generate_year_weather_report(args)
    
    if(args.a):
        weather_report_generator.generate_month_weather_report(args)
        
    if(args.c):
        weather_report_generator.generate_month_temp_bar_chart(args)
    
    if(args.b):
        weather_report_generator.generate_month_temp_bar_chart_bonus_task(args)
    
main()
