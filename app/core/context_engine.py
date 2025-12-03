from typing import Dict, List, Optional
from datetime import datetime
from app.services.weather_service import WeatherService


class ContextEngine:
    """Engine for gathering and enriching context data."""
    
    def __init__(self):
        """Initialize context engine."""
        self.weather_service = WeatherService()
    
    def get_context(
        self,
        city: str,
        product_category: Optional[str] = None,
        custom_context: Optional[Dict] = None
    ) -> Dict:
        """
        Get comprehensive context for creative generation.
        
        Args:
            city: City name
            product_category: Product category (e.g., "beverage", "skincare")
            custom_context: Additional custom context
        
        Returns:
            Context dictionary with all signals
        """
        # Get weather data
        weather_data = self.weather_service.get_weather(city)
        weather_context = self.weather_service.get_weather_context(weather_data)
        
        # Get time context
        season = self.weather_service.get_season()
        time_of_day = self.weather_service.get_time_of_day()
        
        # Get POIs (mock for now)
        pois = self._get_pois(city)
        
        # Get cultural context
        cultural_context = self._get_cultural_context(city, season)
        
        # Get local vibes
        local_vibes = self._get_local_vibes(city)
        
        context = {
            "city": city,
            "weather": weather_data,
            "weather_context": weather_context,
            "season": season,
            "time_of_day": time_of_day,
            "pois": pois,
            "cultural_context": cultural_context,
            "local_vibes": local_vibes,
            "product_category": product_category,
            "timestamp": datetime.now().isoformat()
        }
        
        if custom_context:
            context.update(custom_context)
        
        return context
    
    def _get_pois(self, city: str) -> List[str]:
        """Get points of interest for a city (mock data)."""
        poi_data = {
            "Bangalore": ["cafes", "tech parks", "gardens", "breweries", "malls"],
            "Chennai": ["beaches", "temples", "marina", "shopping districts"],
            "Mumbai": ["marine drive", "malls", "beaches", "street markets"],
            "Delhi": ["monuments", "markets", "malls", "restaurants", "historical sites"],
            "Hyderabad": ["tech hubs", "biryani spots", "lakes", "monuments"],
            "Pune": ["colleges", "cafes", "hills", "restaurants"],
            "Kolkata": ["cultural centers", "markets", "sweets shops", "heritage sites"]
        }
        
        return poi_data.get(city, ["local attractions", "shopping areas", "restaurants"])
    
    def _get_cultural_context(self, city: str, season: str) -> str:
        """Get cultural context for a city and season."""
        # Festival mapping
        festivals = {
            "winter": ["Christmas", "New Year", "Pongal", "Makar Sankranti"],
            "spring": ["Holi", "Ugadi", "Gudi Padwa"],
            "monsoon": ["Raksha Bandhan", "Independence Day", "Onam"],
            "autumn": ["Diwali", "Durga Puja", "Dussehra", "Navratri"]
        }
        
        # City-specific culture
        city_culture = {
            "Bangalore": "tech-savvy, café culture, cosmopolitan vibes",
            "Chennai": "traditional, coastal culture, filter coffee culture",
            "Mumbai": "fast-paced, bollywood, street food culture",
            "Delhi": "historical, diverse cuisine, shopping culture",
            "Hyderabad": "biryani culture, tech hub, historical heritage",
            "Pune": "educational hub, young crowd, café culture",
            "Kolkata": "artistic, literary, sweet culture, cultural festivals"
        }
        
        season_festivals = festivals.get(season, [])
        city_vibe = city_culture.get(city, "vibrant local culture")
        
        context = f"{city} culture: {city_vibe}. "
        if season_festivals:
            context += f"Upcoming festivals: {', '.join(season_festivals[:2])}."
        
        return context
    
    def _get_local_vibes(self, city: str) -> str:
        """Get local vibes and mood for a city."""
        vibes = {
            "Bangalore": "Bangalore monsoon vibes, tech-savvy millennials, café hoppers",
            "Chennai": "Chennai coastal vibes, traditional yet modern, beach lovers",
            "Mumbai": "Mumbai hustle, bollywood dreams, street food enthusiasts",
            "Delhi": "Delhi nightlife, historical charm, food explorers",
            "Hyderabad": "Hyderabad heritage, biryani lovers, tech professionals",
            "Pune": "Pune student life, young energy, weekend adventurers",
            "Kolkata": "Kolkata artistic soul, cultural enthusiasts, sweet lovers"
        }
        
        return vibes.get(city, f"{city} local vibes and culture")
    
    def create_context_variations(self, base_context: Dict, num_variations: int = 10) -> List[Dict]:
        """
        Create multiple context variations for diverse creatives.
        
        Args:
            base_context: Base context dictionary
            num_variations: Number of variations to create
        
        Returns:
            List of context variations
        """
        variations = []
        
        # Variation themes
        themes = [
            "morning energy",
            "afternoon relaxation",
            "evening social",
            "weekend vibes",
            "festive celebration",
            "local culture",
            "weather-specific",
            "POI-focused",
            "lifestyle",
            "aspirational"
        ]
        
        for i in range(num_variations):
            variation = base_context.copy()
            variation["theme"] = themes[i % len(themes)]
            variation["variation_id"] = i + 1
            
            # Add theme-specific context
            if variation["theme"] == "morning energy":
                variation["mood"] = "energetic, fresh start, morning routine"
            elif variation["theme"] == "afternoon relaxation":
                variation["mood"] = "relaxed, leisure time, comfort"
            elif variation["theme"] == "evening social":
                variation["mood"] = "social, gathering, celebration"
            elif variation["theme"] == "weekend vibes":
                variation["mood"] = "fun, adventure, exploration"
            elif variation["theme"] == "festive celebration":
                variation["mood"] = "festive, joyful, celebration"
            elif variation["theme"] == "local culture":
                variation["mood"] = "cultural, traditional, local pride"
            elif variation["theme"] == "weather-specific":
                variation["mood"] = f"weather-aware, {base_context['weather']['description']}"
            elif variation["theme"] == "POI-focused":
                variation["mood"] = "location-specific, local hotspots"
            elif variation["theme"] == "lifestyle":
                variation["mood"] = "lifestyle-focused, aspirational"
            else:  # aspirational
                variation["mood"] = "premium, aspirational, elevated"
            
            variations.append(variation)
        
        return variations
