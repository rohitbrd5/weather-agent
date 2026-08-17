from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@tool
def get_current_weather(location: str) -> dict:
    """Fetches the current weather for a given location."""
    if not OPENWEATHER_API_KEY:
        return {"error": "OpenWeatherMap API key not set.", "location": location}

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        if response.status_code == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            return {"location": location, "temperature": f"{temperature}°C", "conditions": description}
        else:
            return {"location": location, "temperature": "N/A", "conditions": "Error fetching weather data"}
    except requests.exceptions.RequestException as e:
        return {"location": location, "temperature": "N/A", "conditions": f"Request error: {e}"}
    except Exception as e:
        return {"location": location, "temperature": "N/A", "conditions": f"An unexpected error occurred: {e}"}

tools = [get_current_weather]
