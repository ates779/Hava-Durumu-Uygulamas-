import aiohttp
from utils.config_handler import get_api_key

BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

async def get_weather_data(city_name):
    api_key = get_api_key()
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
        'lang': 'tr'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL_WEATHER, params=params) as response:
            response.raise_for_status()
            return await response.json()

async def get_forecast_data(city_name):
    api_key = get_api_key()
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
        'lang': 'tr'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL_FORECAST, params=params) as response:
            response.raise_for_status()
            return await response.json()