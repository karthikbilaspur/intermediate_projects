import requests

def get_weather_data():
    api_key = "YOUR_API_KEY"
    city = "YOUR_CITY"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    weather_data = response.json()
    return weather_data