import argparse
import calendar
import fnmatch
import os

class WeatherMan:
    
    def __init__(self):
        self.max_temp = float("-inf")
        self.min_temp = float("inf")
        self.max_humid = float("-inf")
        self.min_temp_date = None
        self.max_temp_date = None
        self.max_humid_date = None
        self.avg_high_temp = float("inf")
        self.avg_low_temp = float("inf")
        self.avg_mean_humid = float("inf")
    
    def month_number_to_short_name(self, month_number):
        return calendar.month_abbr[month_number]
    
    def open_file_year(self, args):
        year_files = list()
        
        for file in os.listdir(args.path):
            if (fnmatch.fnmatch(file, f"*{args.e}*.txt")):
                year_files.append(file)
        
        return year_files
    
    def open_file_month(self, args, month):
        year = month.split(sep = "/")[0]
        month_number = month.split(sep = "/")[1]
        month = self.month_number_to_short_name(int(month_number))
        month_files = list()
        
        for file in os.listdir(args.path):
            if (fnmatch.fnmatch(file, f"*{year}_{month}*.txt")):
                month_files.append(file)
        
        return month_files
    
    def read_file(self, file_name, args):
        weather_lines_list = list()
        
        with open(args.path + file_name, "r") as file:
            headings = file.readline().strip().split(",")
            weather_lines = file.readlines()
            weather_lines_list = self.covert_weather_data_in_required_format(headings, weather_lines)
        
        return weather_lines_list        
    
    def print_star(self, count, color):
        
        for i in range(0, count):
            print(f"{color}+\033[0m", end = "")
    
    def covert_weather_data_in_required_format(self, headings, weather_lines):
        weather_lines_list = list()
        weather_line_dict = dict()
        
        for line in weather_lines:
            weather_line_dict = dict()
            line_list = line.strip().split(sep = ",")

            for index, item in enumerate(line_list):
                weather_line_dict[headings[index]] = item
                
            weather_lines_list.append(weather_line_dict)

        return weather_lines_list
    
    def calculate_max_temp_year(self, args, year_files):
        weather_record = list()
    
        for file_name in year_files:
            weather_record = self.read_file(file_name, args)
            
            for line in weather_record:
                if line["Max TemperatureC"]:  # Check if the value is not empty
                    current_temp = int(line["Max TemperatureC"])
                    if current_temp > self.max_temp:
                        self.max_temp = current_temp
                        self.max_temp_date = line["PKT"]
        
    def calculate_min_temp_year(self, args, year_files):
        weather_record = list()
        
        for file_name in year_files:
            weather_record = self.read_file(file_name, args)
            
            for line in weather_record:
                if line["Min TemperatureC"]:  # Check if the value is not empty
                    current_temp = int(line["Min TemperatureC"])
                    if current_temp < self.min_temp:
                        self.min_temp = current_temp
                        self.min_temp_date = line["PKT"]
        
    def calculate_max_humid_year(self, args, year_files):
        weather_record = list()
        
        for file_name in year_files:
            weather_record = self.read_file(file_name, args)
            
            for line in weather_record:
                if line["Max Humidity"]:  # Check if the value is not empty
                    current_humid = int(line["Max Humidity"])
                    if current_humid > self.max_humid:
                        self.max_humid = current_humid
                        self.max_humid_date = line["PKT"]
           
    def calculate_avg_max_temp_month(self, args, month_files):
        weather_record = list()
        sum_max_temp = 0
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            for line in weather_record:
                if line["Max TemperatureC"]:  # Check if the value is not empty
                    sum_max_temp = sum_max_temp + int(line["Max TemperatureC"])
            self.avg_high_temp = sum_max_temp / len(weather_record)
        
        self.avg_high_temp = int(self.avg_high_temp)
    
    def calculate_avg_min_temp_month(self, args, month_files):
        weather_record = list()
        sum_min_temp = 0
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            for line in weather_record:
                if line["Min TemperatureC"]:  # Check if the value is not empty
                    sum_min_temp = sum_min_temp + int(line["Min TemperatureC"])
            self.avg_low_temp = sum_min_temp / len(weather_record)
        
        self.avg_low_temp = int(self.avg_low_temp)

    def calculate_avg_mean_humid_month(self, args, month_files):
        weather_record = list()
        sum_mean_humid = 0
        for file_name in month_files:
            weather_record = self.read_file(file_name, args)
            for line in weather_record:
                if line[" Mean Humidity"]:  # Check if the value is not empty
                    sum_mean_humid = sum_mean_humid + int(line[" Mean Humidity"])
            self.avg_mean_humid = sum_mean_humid / len(weather_record)
        
        self.avg_mean_humid = int(self.avg_mean_humid)
    
    def year_weather_report(self, args):
        year_files = self.open_file_year(args)
        self.calculate_max_temp_year(args, year_files)
        self.calculate_min_temp_year(args, year_files)
        self.calculate_max_humid_year(args, year_files)
        
        print("Yearly weather report", end = "\n\n")
        # print for high temp
        month_number = int(self.max_temp_date.split(sep = "-")[1])
        date = self.max_temp_date.split(sep = "-")[2]
        print(f"Highest: {self.max_temp}C on {self.month_number_to_short_name(month_number)} {date}")
        
        # print for min temp
        month_number = int(self.min_temp_date.split(sep = "-")[1])
        date = self.min_temp_date.split(sep = "-")[2]
        print(f"Lowest: {self.min_temp}C on {self.month_number_to_short_name(month_number)} {date}")
        
        # print for max humid
        month_number = int(self.max_humid_date.split(sep = "-")[1])
        date = self.max_humid_date.split(sep = "-")[2]
        print(f"Humidity: {self.max_humid}% on {self.month_number_to_short_name(month_number)} {date}", end = "\n\n")
        
    def month_weather_report(self, args):
        month_files = self.open_file_month(args, args.a)
        self.calculate_avg_max_temp_month(args, month_files)
        self.calculate_avg_min_temp_month(args, month_files)
        self.calculate_avg_mean_humid_month(args, month_files)
        
        print("Monthly Average Weather Report", end = "\n\n")
        # print for avg max temp
        print(f"Highest Average: {self.avg_high_temp}C")
        
        # print for avg min temp
        print(f"Lowest Average: {self.avg_low_temp}C")
        
        # print for avg mean humid
        print(f"Average Mean Humidity: {self.avg_mean_humid}C", end = "\n\n")
        
    def bar_chart(self, args):
        weather_record = list()
        month_files = self.open_file_month(args, args.c)
        
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
    
    def bonus_task(self, args):
        weather_record = list()
        month_files = self.open_file_month(args, args.b)
        
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
    test = WeatherMan()
    
    parser=argparse.ArgumentParser(description = "Weather man")
    parser.add_argument("path", help = "It's the path where data is placed")
    parser.add_argument("-a", help = "This is for the average month report")
    parser.add_argument("-b", help = "This is for bonus report")
    parser.add_argument("-c", help = "This is for the chart report")
    parser.add_argument("-e", help = "This is for the year report")
    args = parser.parse_args()
    
    if(args.e):
        test.year_weather_report(args)
    
    if(args.a):
        test.month_weather_report(args)
        
    if(args.c):
        test.bar_chart(args)
    
    if(args.b):
        test.bonus_task(args)
    
main()