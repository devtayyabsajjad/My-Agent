# api_calling_agent.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API keys from .env

class APICallingAgent:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.trading_economics_api_key = os.getenv("TRADING_ECONOMICS_API_KEY")

    def fetch_weather_data(self, location):
        """
        Calls the OpenWeatherMap API to fetch real-time weather data for the given location.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            rainfall = data.get("rain", {}).get("1h", 0)
            return {"temperature": temperature, "humidity": humidity, "rainfall": rainfall}
        else:
            # Handle errors (you might raise an exception in production)
            return {"temperature": None, "humidity": None, "rainfall": None}

    def fetch_economic_data(self, location):
        """
        Calls the Trading Economics API to fetch real-time economic data for the given location.
        Example endpoint: https://api.tradingeconomics.com/country/{location}?c={API_KEY}
        """
        url = f"https://api.tradingeconomics.com/country/{location}?c={self.trading_economics_api_key}&f=json"
        response = requests.get(url)
        if response.status_code == 200:
            # Assume the API returns a list; we take the first element for simplicity.
            data = response.json()
            if data and isinstance(data, list):
                item = data[0]
                # Extract economic values; adjust keys as per the actual API response.
                average_income = item.get("LatestValue", 4000)  # For example, using LatestValue as avg income
                # For crop prices, you might have to call a different endpoint.
                # Here we call a placeholder endpoint; replace with your actual call.
                crop_prices = {
                    "Wheat": 3.0,
                    "Corn": 2.5,
                    "Soybean": 4.0,
                    "Rice": 3.2,
                    "Barley": 2.8
                }
                return {"average_income": average_income, "crop_prices": crop_prices}
            else:
                return {"average_income": None, "crop_prices": None}
        else:
            return {"average_income": None, "crop_prices": None}

    def get_all_api_data(self, location):
        """
        Combines real-time weather and economic data.
        """
        weather_data = self.fetch_weather_data(location)
        economic_data = self.fetch_economic_data(location)
        return {"economic": economic_data, "environmental": weather_data}
