import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("WEATHER_API_KEY")
URL = "https://api.weatherapi.com/v1/current.json"

def get_city(user_message):
    user_text = user_message.replace("?", "").strip()

    city_match = re.search(r"\b(di|a|per|su|meteo)\s+([a-z\s]+)$", user_text)

    if city_match:
        return city_match.group(2).strip()
    
    return user_text

def get_weather(user_message):

    city = get_city(user_message)

    parameters = {"key": API_KEY, "q": city, "lang": "it"}
    
    try:
        answer = requests.get(URL, params=parameters)
        answer.raise_for_status()

        weather_data = answer.json()

        return (f"Questo è il tempo a <b>{weather_data['location']['name']}</b>:\n" 
                f"{weather_data['current']['condition']['text']}\n"
                f"<b>{weather_data['current']['temp_c']}°C</b>")
    
    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        
        return f"Non sono riuscito a controllare il meteo! Controlla di aver scritto bene il nome della città."
