import datetime
import calendar

from weatherCalculation import WeatherCalculation

class WeatherReportGenerator:
    weather_calculation = WeatherCalculation()
    
    def generate_year_weather_report(self, weather_record):

        if len(weather_record):
            max_temperature, max_temperature_date = self.weather_calculation.calculate_max_value(weather_record, "Max TemperatureC")
            min_temperature, min_temperature_date = self.weather_calculation.calculate_min_temperature_year(weather_record)
            max_humid, max_humid_date = self.weather_calculation.calculate_max_value(weather_record,"Max Humidity")
            self.print_year_weather_report(max_temperature, max_temperature_date, min_temperature, min_temperature_date, max_humid, max_humid_date)
            return
            
    def generate_month_weather_report(self, weather_record):
        if len(weather_record):
            avg_high_temperature = self.weather_calculation.calculate_average(weather_record, "Max TemperatureC")
            avg_low_temperature = self.weather_calculation.calculate_average(weather_record, "Min TemperatureC")
            avg_mean_humid = self.weather_calculation.calculate_average(weather_record, " Mean Humidity")
            self.print_month_weather_report(avg_high_temperature, avg_low_temperature, avg_mean_humid)
        
    def generate_month_temperature_bar_chart(self, weather_record):
        if len(weather_record):
            self.print_month_temperature_bar_chart(weather_record)
    
    def generate_month_temperature_bar_chart_bonus_task(self, weather_record):
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
        print("Yearly Weather Report", end = "\n\n")
        if max_temperature != "" and max_temperature_date:
            date = datetime.datetime.strptime(max_temperature_date, "%Y-%m-%d")
            print(f"Highest: {max_temperature}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if min_temperature != "" and min_temperature_date:
            date = datetime.datetime.strptime(min_temperature_date, "%Y-%m-%d")
            print(f"Lowest: {min_temperature}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if max_humid != "" and max_humid_date:
            date = datetime.datetime.strptime(max_humid_date, "%Y-%m-%d")
            print(f"Humidity: {max_humid}% on {calendar.month_abbr[date.month]} {date.day}", end = "\n\n")    
