class WeatherCalculation:
    
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
        return round(sum_of_values / len(weather_record))
   
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
