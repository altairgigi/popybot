import os
import re
import requests
from dotenv import load_dotenv
import config

load_dotenv()

API_KEY = os.environ.get("WEATHER_API_KEY")
URL = config.WEATHER_SERVICE_URL

def get_city(user_message):
    user_text = user_message.replace("?", "").strip()

    city_match = re.search(config.WEATHER_PATTERN, user_text)

    if city_match:
        return city_match.group(2).strip()
    
    return user_text

def get_weather(user_message):
    city = get_city(user_message)
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
