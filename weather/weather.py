from weather.utils import store_weather_api
import json, os

class WeatherAPI:
    def store_weather_info(self, api_key, city_name, file_name):
        """Stores weather data for specified city at the desired file path(JSON format)."""
        return store_weather_api(api_key, city_name, file_name)
    
    def get_weather_data_from_json(self, file_name):
        """Reading stored weather data from the specified filepath."""
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r', encoding='utf-8') as json_file:
                    json_content = json.loads(json_file.read())
                    return json_content, None
            except Exception as exc:
                return None, f'Error reading file:\n{exc}'
        else:
            return None, f'No filepath such as {file_name} exists.'