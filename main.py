import requests

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

results = get_weather("Chicago", "United States")
print(results)

