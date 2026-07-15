import os
import dateparser
from datetime import datetime
import requests
from dotenv import load_dotenv
import config

load_dotenv()

API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_URL = config.WEATHER_SERVICE_URL
FORECAST_URL = config.FORECAST_SERVICE_URL

def get_weather(location, when):
    if when == config.DAYS['today'] or when is None:
        weather = get_current_weather(location)
    else:
        parsed_date = dateparser.parse(
            when,
            languages=[config.LANG],
            settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()}
        )

        if parsed_date:
            date = parsed_date.date()
            
            delta_days = (date - datetime.now().date()).days

            days = delta_days + 1
        else: 
            days = 1
            
        weather = get_weather_forecast(location, days)

    return weather

def get_current_weather(location):
    parameters = {"key": API_KEY, "q": location, "lang": config.LANG}
    
    try:
        answer = requests.get(WEATHER_URL, params=parameters)
        answer.raise_for_status()

        weather_data = answer.json()

        return config.TEMPLATES['weather_report'].format(
            location=weather_data['location']['name'],
            condition=weather_data['current']['condition']['text'],
            temperature=weather_data['current']['temp_c']
        )
    
    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        
        return config.RESPONSES['missing_city']

def get_weather_forecast(location, when):
    if(when > 14):
        days = 14
    else:
        days = when
    print(f"DEBUG: days: {days} and when: {when}")
    parameters = {"key": API_KEY, "q": location, "days": days, "lang": config.LANG}
    
    try:
        answer = requests.get(FORECAST_URL, params=parameters)
        answer.raise_for_status()

        forecast_data = answer.json()

        city = forecast_data['location']['name']
        forecast_per_day = forecast_data['forecast']['forecastday']
        forecast_report = [config.TEMPLATES['forecast_header'].format(location=city)]

        for forecast in forecast_per_day:
            date = forecast['date']
            temp_max = forecast['day']['maxtemp_c']
            temp_min = forecast['day']['mintemp_c']
            condition = forecast['day']['condition']['text']

            day_forecast = config.TEMPLATES['forecast_report'].format(
                date=date,
                temp_max=temp_max,
                temp_min=temp_min,
                condition=condition
            )

            forecast_report.append(day_forecast)

        return "\n".join(forecast_report)
    
    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        
        return config.RESPONSES['missing_city']