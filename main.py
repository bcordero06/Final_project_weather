import requests
import json

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

    current_weather = weather_data.get("current_weather," ())

    weather_object = {
        "city":city_name,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": current_weather.get("temperature"),
        "windspeed":current_weather.get("windspeed"),
        "elevation": weather_data.get("elevation"),
        "obersavtion_time": current_weather.get("time")
    }

    return weather_object

if __name__ == "__main__":
    weather = get_weather("chicago","US")
    print(weather)