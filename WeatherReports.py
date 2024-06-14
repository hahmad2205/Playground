import calendar
import datetime

from Playground.WeatherCalculation import WeatherCalculation

class WeatherReportGenerator:
    weather_calculation = WeatherCalculation()
    
    def generate_year_weather_report(self, weather_record):
        max_temperature, max_temperature_date = (
            self.weather_calculation.calculate_max_weather_reading(
                weather_record, "Max TemperatureC"
                )
        )
        min_temperature, min_temperature_date = (
            self.weather_calculation.calculate_min_temperature_year(
                weather_record
            )
        )
        max_humid, max_humid_date = (
            self.weather_calculation.calculate_max_weather_reading(
                weather_record,"Max Humidity"
            )
        )
        calculation_results = {
                        "max_temperature" : max_temperature, "max_temperature_date"  : max_temperature_date,
                        "min_temperature" : min_temperature, "min_temperature_date" : min_temperature_date,
                        "max_humid" : max_humid, "max_humid_date" : max_humid_date
        }
        self.print_year_weather_report(calculation_results)
            
    def generate_month_weather_report(self, weather_record):
        avg_high_temperature = (
            self.weather_calculation.calculate_average(
                weather_record, "Max TemperatureC"
            )
        )
        avg_low_temperature = (
            self.weather_calculation.calculate_average(
                weather_record, "Min TemperatureC"
            )
        )
        avg_mean_humid = (
            self.weather_calculation.calculate_average(
                weather_record, " Mean Humidity"
            )
        )
        
        calculation_results = {
                        "avg_high_temperature" : avg_high_temperature,
                        "avg_low_temperature" : avg_low_temperature,
                        "avg_mean_humid" : avg_mean_humid
        }
        
        self.print_month_weather_report(calculation_results)
        
    def generate_month_temperature_bar_chart(self, weather_records):
        for record in weather_records:
            day = self.get_date_for_bar_chart(record)
            
            if record["Max TemperatureC"]:
                print(day, end = "    ")
                self.print_star(int(record["Max TemperatureC"]), "\033[91m")
                print(f"{record['Max TemperatureC']}C")
            
            if record["Min TemperatureC"]:
                print(day, end = "    ")
                self.print_star(int(record["Min TemperatureC"]), "\033[94m")
                print(f"{record['Min TemperatureC']}C")
    
    def generate_month_temperature_bar_chart_bonus_task(self, weather_record):
        for reading in weather_record:
            
            if reading["Min TemperatureC"] or reading["Max TemperatureC"]:
                day = self.get_date_for_bar_chart(reading)
                print(day, end = "    ")
                
                if reading["Min TemperatureC"]:
                    self.print_star(int(reading["Min TemperatureC"]), "\033[94m")
                
                if reading["Max TemperatureC"]:
                    self.print_star(int(reading["Max TemperatureC"]), "\033[91m")
                print(f"{reading['Min TemperatureC']}C - {reading['Max TemperatureC']}C")

    def get_date_for_bar_chart(self, reading):
        date_abbr = reading["PKT"] if reading.get("PKT") else reading["PKST"]
        date = datetime.datetime.strptime(date_abbr, "%Y-%m-%d")
        return date.day
        
    def print_star(self, plus_count, color):
        
        for _ in range(0, plus_count):
            print(f"{color}+\033[0m", end = "")
    
    def print_month_weather_report(self, calculation_results):
        print("Monthly Average Weather Report", end = "\n\n")
        print(f"Highest Average: {calculation_results.get('avg_high_temperature')}C")       
        print(f"Lowest Average: {calculation_results.get('avg_low_temperature')}C")
        print(f"Average Mean Humidity: {calculation_results.get('avg_mean_humid')}C", end = "\n\n")
     
    def print_year_weather_report(self, calculation_results):
        print("Yearly Weather Report", end="\n\n")
        
        if calculation_results.get("max_temperature") is not None and calculation_results.get("max_temperature_date"):
            date = datetime.datetime.strptime(calculation_results.get("max_temperature_date"), "%Y-%m-%d")
            print(f"Highest: {calculation_results.get('max_temperature')}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if calculation_results.get("min_temperature") is not None and calculation_results.get("min_temperature_date"):
            date = datetime.datetime.strptime(calculation_results.get("min_temperature_date"), "%Y-%m-%d")
            print(f"Lowest: {calculation_results.get('min_temperature')}C on {calendar.month_abbr[date.month]} {date.day}")
        
        if calculation_results.get("max_humid") is not None and calculation_results.get("max_humid_date"):
            date = datetime.datetime.strptime(calculation_results.get("max_humid_date"), "%Y-%m-%d")
            print(f"Humidity: {calculation_results.get('max_humid')}% on {calendar.month_abbr[date.month]} {date.day}", end="\n\n")
