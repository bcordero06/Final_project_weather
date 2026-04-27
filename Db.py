import requests
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from Db_manager import create_table, insert_weather, get_all_observations, get_observations_by_id

load_dotenv()

@dataclass
class weather_info:
        def __init__(self,city,country,latitude,longitude,temperature,windspeed,elevation,observation_time):
            self.city = city
            self.country = country
            self.latitude = latitude
            self.longitude = longitude
            self.temperature = temperature
            self.windspeed = windspeed
            self.elevation = elevation
            self.observation_time = observation_time
        
        def __str__(self):
             return(
                  f"City: {self.city}\n"
                  f"Country: {self.country}\n"
                  f"Latitude: {self.latitude}\n"
                  f"Longitude: {self.longitude}\n"
                  f"Temperature: {self.temperature}\n"
                  f"Windspeed: {self.windspeed}\n"
                  f"Elevation: {self.elevation}\n"
                  f"observation Time: {self.observation_time}\n"
             )
        
def get_weather(city, country, count=1):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": city,
        "country": country,
        "count": count
    }

    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if 'results' not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError("City not found")
    
    location = geo_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country_name = location["country"]

    weather_url = "https://api.open-meteo.com/v1/forecast?current_weather=true"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
    }
    weather_reponse = requests.get(weather_url, params=weather_params)
    weather_data = weather_reponse.json()

    current_weather = weather_data.get("current_weather" )

    weather_object = weather_info(
         city_name,
         country_name,
         latitude,
         longitude,
         current_weather.get("temperature"),
         current_weather.get("windspeed"),
         weather_data.get("elevation"),
         current_weather.get("time")
    )
    
    return weather_object
 
cities = [
    {"city": "Barcelona", "country": "Spain"},
    {"city": "Cuenca", "country": "Ecuador"},
    {"city": "Guayaquil", "country": "Ecuador"},
    {"city": "Quito", "country": "Ecuador"},
    {"city": "Ambato", "country": "Ecuador"},
    {"city": "Loja", "country": "Ecuador"},
    {"city": "Stockholm", "country": "Sweden"},
    {"city": "Chicago", "country": "United States"},
    {"city": "Puebla", "country": "Mexico"},
    {"city": "Bogota", "country": "Colombia"},
]

if __name__ == "__main__":
     
    create_table()

    for city in cities:
        result = get_weather(city["city"], city["country"])
        insert_weather(
            result.city,
            result.country,
            result.temperature,
            0,
            result.observation_time
          )
    
    get_all_observations()