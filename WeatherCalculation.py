class WeatherCalculation:
    
    def calculate_max_weather_reading(self, weather_records, key):
        max_weather_readings = []
        for record in weather_records:
            
            if not record.get(key):
                continue
            
            current_weather_reading = int(record.get(key))
            max_weather_readings.append(current_weather_reading)
            max_weather_reading = max(max_weather_readings)
            date_abbr = record["PKT"] if record.get("PKT") else record["PKST"]
            max_weather_date = (
                date_abbr 
                if current_weather_reading == int(max_weather_reading)
                else max_weather_date
            )
        
        return max_weather_reading, max_weather_date
    
    def calculate_average(self, weather_records, key):
        sum_of_temperatures = 0
        
        for record in weather_records:
            temperature = record.get(key)
            sum_of_temperatures = sum_of_temperatures + int(record[key]) if temperature else 0
        
        return round(sum_of_temperatures / len(weather_records))
   
    def calculate_min_temperature_year(self, weather_records):
        min_temperatures = []
        for record in weather_records:
            min_temperature_value = record.get("Min TemperatureC")
            
            if not min_temperature_value:
                continue

            current_temperature = int(min_temperature_value)
            min_temperatures.append(current_temperature)
            min_temperature = min(min_temperatures)
            date_abbr = record["PKT"] if record.get("PKT") else record["PKST"]
            min_temperature_date = (
                date_abbr
                if current_temperature == int(min_temperature)
                else min_temperature_date
            )
        
        return min_temperature, min_temperature_date
