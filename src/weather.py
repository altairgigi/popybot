import os
import re
import requests
from dotenv import load_dotenv
import config

load_dotenv()

API_KEY = os.environ.get("WEATHER_API_KEY")
URL = config.WEATHER_SERVICE_URL

def get_weather(city):
    parameters = {"key": API_KEY, "q": city, "lang": config.LANG}
    
    try:
        answer = requests.get(URL, params=parameters)
        answer.raise_for_status()

        weather_data = answer.json()

        return config.TEMPLATES['weather_report'].format(
            city=weather_data['location']['name'],
            condition=weather_data['current']['condition']['text'],
            temperature=weather_data['current']['temp_c']
        )
    
    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        
        return config.RESPONSES['missing_city']
