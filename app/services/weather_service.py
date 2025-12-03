import requests
from typing import Dict, Optional
import os
from datetime import datetime


class WeatherService:
    """Service for fetching weather information based on target location."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize weather service with optional API key."""
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str, country_code: str = "IN") -> Dict:
        """
        Get current weather for the target city.
        Uses real API if key available, otherwise uses intelligent mock data.
        
        Args:
            city: Target city for the ad campaign
            country_code: Country code (default: IN for India)
        
        Returns:
            Weather data dictionary for the target location
        """
        # Try real API first if key is available
        if self.api_key and self.api_key != "your_weather_api_key_here":
            try:
                params = {
                    "q": f"{city},{country_code}",
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                return {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "main": data["weather"][0]["main"],
                    "icon": data["weather"][0]["icon"],
                    "wind_speed": data["wind"]["speed"],
                    "clouds": data["clouds"]["all"],
                    "source": "real_api"
                }
            except Exception as e:
                print(f"Weather API error: {e}. Using location-based mock data.")
        
        # Use intelligent mock data based on location and season
        return self._get_location_based_weather(city, country_code)
    
    def _get_location_based_weather(self, city: str, country_code: str = "IN") -> Dict:
        """
        Generate realistic weather data based on location and current season.
        This provides contextually accurate weather for the target location.
        """
        current_month = datetime.now().month
        season = self.get_season()
        
        # Location-based weather patterns
        location_weather = {
            # India - South
            "Bangalore": self._get_seasonal_weather(season, {
                "winter": {"temp": 22, "desc": "pleasant weather", "main": "Clear"},
                "spring": {"temp": 28, "desc": "warm and sunny", "main": "Clear"},
                "monsoon": {"temp": 24, "desc": "rainy", "main": "Rain"},
                "autumn": {"temp": 25, "desc": "pleasant", "main": "Clouds"}
            }),
            "Chennai": self._get_seasonal_weather(season, {
                "winter": {"temp": 28, "desc": "warm", "main": "Clear"},
                "spring": {"temp": 35, "desc": "hot and sunny", "main": "Clear"},
                "monsoon": {"temp": 30, "desc": "humid with rain", "main": "Rain"},
                "autumn": {"temp": 32, "desc": "hot", "main": "Clear"}
            }),
            "Hyderabad": self._get_seasonal_weather(season, {
                "winter": {"temp": 24, "desc": "pleasant", "main": "Clear"},
                "spring": {"temp": 32, "desc": "hot", "main": "Clear"},
                "monsoon": {"temp": 26, "desc": "rainy", "main": "Rain"},
                "autumn": {"temp": 28, "desc": "warm", "main": "Clouds"}
            }),
            
            # India - North
            "Delhi": self._get_seasonal_weather(season, {
                "winter": {"temp": 15, "desc": "cold", "main": "Clouds"},
                "spring": {"temp": 30, "desc": "hot", "main": "Clear"},
                "monsoon": {"temp": 32, "desc": "humid with rain", "main": "Rain"},
                "autumn": {"temp": 28, "desc": "pleasant", "main": "Clear"}
            }),
            "Gurgaon": self._get_seasonal_weather(season, {
                "winter": {"temp": 14, "desc": "cold", "main": "Clouds"},
                "spring": {"temp": 31, "desc": "hot", "main": "Clear"},
                "monsoon": {"temp": 33, "desc": "humid", "main": "Rain"},
                "autumn": {"temp": 27, "desc": "pleasant", "main": "Clear"}
            }),
            
            # India - West
            "Mumbai": self._get_seasonal_weather(season, {
                "winter": {"temp": 26, "desc": "pleasant", "main": "Clear"},
                "spring": {"temp": 32, "desc": "hot and humid", "main": "Clear"},
                "monsoon": {"temp": 28, "desc": "heavy rain", "main": "Rain"},
                "autumn": {"temp": 30, "desc": "humid", "main": "Clouds"}
            }),
            "Pune": self._get_seasonal_weather(season, {
                "winter": {"temp": 20, "desc": "cool", "main": "Clear"},
                "spring": {"temp": 30, "desc": "warm", "main": "Clear"},
                "monsoon": {"temp": 24, "desc": "rainy", "main": "Rain"},
                "autumn": {"temp": 26, "desc": "pleasant", "main": "Clouds"}
            }),
            
            # India - East
            "Kolkata": self._get_seasonal_weather(season, {
                "winter": {"temp": 22, "desc": "pleasant", "main": "Clear"},
                "spring": {"temp": 34, "desc": "hot and humid", "main": "Clear"},
                "monsoon": {"temp": 30, "desc": "heavy rain", "main": "Rain"},
                "autumn": {"temp": 28, "desc": "humid", "main": "Clouds"}
            }),
            
            # US - West Coast
            "Los Angeles": self._get_seasonal_weather(season, {
                "winter": {"temp": 18, "desc": "mild", "main": "Clear"},
                "spring": {"temp": 22, "desc": "pleasant", "main": "Clear"},
                "monsoon": {"temp": 28, "desc": "warm and sunny", "main": "Clear"},
                "autumn": {"temp": 24, "desc": "pleasant", "main": "Clear"}
            }),
            "San Francisco": self._get_seasonal_weather(season, {
                "winter": {"temp": 14, "desc": "cool and foggy", "main": "Clouds"},
                "spring": {"temp": 18, "desc": "mild", "main": "Clouds"},
                "monsoon": {"temp": 20, "desc": "cool", "main": "Clouds"},
                "autumn": {"temp": 19, "desc": "mild", "main": "Clouds"}
            }),
            
            # US - East Coast
            "New York": self._get_seasonal_weather(season, {
                "winter": {"temp": 2, "desc": "cold", "main": "Snow"},
                "spring": {"temp": 18, "desc": "mild", "main": "Clear"},
                "monsoon": {"temp": 28, "desc": "hot and humid", "main": "Clear"},
                "autumn": {"temp": 16, "desc": "cool", "main": "Clouds"}
            }),
            
            # UK
            "London": self._get_seasonal_weather(season, {
                "winter": {"temp": 8, "desc": "cold and rainy", "main": "Rain"},
                "spring": {"temp": 14, "desc": "mild", "main": "Clouds"},
                "monsoon": {"temp": 20, "desc": "pleasant", "main": "Clouds"},
                "autumn": {"temp": 12, "desc": "cool and rainy", "main": "Rain"}
            }),
        }
        
        # Get weather for city or use default
        weather = location_weather.get(city, {
            "temp": 25,
            "desc": "pleasant",
            "main": "Clear"
        })
        
        return {
            "city": city,
            "temperature": weather["temp"],
            "feels_like": weather["temp"],
            "humidity": 65,
            "description": weather["desc"],
            "main": weather["main"],
            "icon": "01d",
            "wind_speed": 3.5,
            "clouds": 20,
            "source": "location_based_mock"
        }
    
    def _get_seasonal_weather(self, season: str, seasonal_data: dict) -> dict:
        """Get weather data for current season."""
        return seasonal_data.get(season, seasonal_data.get("spring", {}))
    
    def get_weather_context(self, weather_data: Dict) -> str:
        """
        Generate contextual description from weather data for the target location.
        
        Args:
            weather_data: Weather data dictionary
        
        Returns:
            Contextual weather description for ad targeting
        """
        temp = weather_data["temperature"]
        desc = weather_data["description"]
        main = weather_data["main"]
        city = weather_data["city"]
        
        context = f"{city} is experiencing {desc} with {temp}°C temperature"
        
        # Add temperature context
        if temp > 35:
            context += ", extremely hot weather - perfect for cooling products"
        elif temp > 30:
            context += ", hot and sunny conditions - ideal for refreshing products"
        elif temp > 25:
            context += ", warm and pleasant conditions - great for outdoor activities"
        elif temp > 20:
            context += ", comfortable weather - perfect for all activities"
        elif temp > 15:
            context += ", cool weather - good for warm products"
        else:
            context += ", cold weather - ideal for warming products"
        
        # Add weather type context
        if "rain" in desc.lower() or main == "Rain":
            context += ". Rainy conditions - focus on indoor comfort and convenience"
        elif "cloud" in desc.lower() or main == "Clouds":
            context += ". Cloudy skies - versatile conditions"
        elif "clear" in desc.lower() or main == "Clear":
            context += ". Clear skies - perfect for outdoor messaging"
        
        return context
    
    def get_season(self) -> str:
        """Get current season based on month (Northern Hemisphere)."""
        month = datetime.now().month
        
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "monsoon"  # Summer/Monsoon for India
        else:  # 9, 10, 11
            return "autumn"
    
    def get_time_of_day(self) -> str:
        """Get current time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
