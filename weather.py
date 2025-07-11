import requests
import json
from datetime import datetime

class WeatherApp:
    def __init__(self):
        # You'll need to get a free API key from OpenWeatherMap
        self.api_key = "YOUR_API_KEY_HERE"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """Get current weather for a city."""
        if self.api_key == "YOUR_API_KEY_HERE":
            return self.get_mock_weather(city)
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_mock_weather(self, city):
        """Return mock weather data for demonstration."""
        return {
            'name': city,
            'main': {
                'temp': 22.5,
                'feels_like': 24.1,
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [{'description': 'partly cloudy', 'main': 'Clouds'}],
            'wind': {'speed': 3.2},
            'visibility': 10000
        }
    
    def display_weather(self, weather_data):
        """Display weather information in a formatted way."""
        if not weather_data:
            print("Unable to fetch weather data.")
            return
        
        city = weather_data['name']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        print(f"\n=== Weather in {city} ===")
        print(f"Temperature: {temp}°C (feels like {feels_like}°C)")
        print(f"Conditions: {description.title()}")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def get_weather_emoji(self, weather_main):
        """Get emoji based on weather condition."""
        emoji_map = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Snow': '❄️',
            'Thunderstorm': '⛈️',
            'Drizzle': '🌦️',
            'Mist': '🌫️'
        }
        return emoji_map.get(weather_main, '🌤️')

def main():
    app = WeatherApp()
    
    print("=== Weather App ===")
    print("Note: This demo uses mock data. Get a free API key from OpenWeatherMap for real data.")
    
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not city:
            print("Please enter a valid city name.")
            continue
        
        weather_data = app.get_weather(city)
        app.display_weather(weather_data)
        
        if weather_data:
            emoji = app.get_weather_emoji(weather_data['weather'][0]['main'])
            print(f"Weather mood: {emoji}")

if __name__ == "__main__":
    main()
