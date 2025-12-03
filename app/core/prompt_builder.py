
from typing import Dict, List


class PromptBuilder:
    """Builder for creating adaptive prompts for image generation."""
    
    def __init__(self):
        """Initialize prompt builder."""
        pass
    
    def build_prompt(
        self,
        brand_info: Dict,
        context: Dict,
        creative_type: str = "social_media_ad"
    ) -> str:
        """
        Build a focused, poster-style marketing prompt for image generation.
        
        The goal is a short, clear instruction that DALL·E can follow
        without getting lost in too many details.
        """
        brand_name = brand_info.get("brand_name", "Brand")
        product_category = brand_info.get("product_category", "product")
        city = context.get("city", "")
        theme = context.get("theme", "")
        mood = context.get("mood", "")
        brand_palette = brand_info.get("brand_palette", {})
        primary_color = None
        if brand_palette:
            hex_colors = brand_palette.get("hex_colors", [])
            if hex_colors:
                primary_color = hex_colors[0]

        # Short style phrase based on category / context
        style_phrase = self._get_style_modifiers(brand_info, context)

        # Core prompt: keep it to 1–2 sentences, poster-focused
        parts = []
        parts.append(
            f"Clean marketing poster for {brand_name} {product_category} in {city}"
            if city
            else f"Clean marketing poster for {brand_name} {product_category}"
        )
        parts.append("the product is the main hero in the center, with space for a logo")

        if theme:
            parts.append(f"inspired by {theme}")
        if mood:
            parts.append(f"with a {mood} feel")
        if primary_color:
            parts.append(f"using {primary_color} as the main brand color")
        if style_phrase:
            parts.append(style_phrase)

        # Join everything into a compact sentence
        prompt = ", ".join(parts)

        # Light technical guidance, not a long tail
        prompt += ". High quality, clear composition, easy-to-read poster design"

        return prompt
    
    def _get_creative_type_prompt(self, creative_type: str) -> str:
        """Get base prompt for creative type."""
        creative_types = {
            "social_media_ad": "Professional social media advertisement",
            "billboard": "Large billboard advertisement",
            "instagram_post": "Instagram-worthy lifestyle shot",
            "facebook_ad": "Facebook advertisement creative",
            "banner_ad": "Web banner advertisement",
            "print_ad": "Print magazine advertisement",
            "story_ad": "Instagram/Facebook story advertisement"
        }
        
        return creative_types.get(creative_type, "Professional advertisement")
    
    def _get_style_modifiers(self, brand_info: Dict, context: Dict) -> str:
        """Get a short style phrase based on brand and context."""
        product_category = (brand_info.get("product_category") or "").lower()
        weather = context.get("weather", {})
        time_of_day = context.get("time_of_day", "")

        # Base by category (1 short phrase)
        if "beverage" in product_category:
            base = "refreshing drink visual"
        elif "skincare" in product_category or "beauty" in product_category:
            base = "clean, minimal beauty style"
        elif "food" in product_category:
            base = "appetizing, simple food visual"
        elif "tech" in product_category:
            base = "modern, minimal tech style"
        else:
            base = "simple lifestyle aesthetic"

        # Light touch from weather / time, at most one extra phrase
        extra = None
        if weather:
            main_weather = weather.get("main", "")
            if main_weather == "Rain":
                extra = "cozy feel"
            elif main_weather == "Clear":
                extra = "bright feel"
            elif main_weather == "Clouds":
                extra = "soft light"

        if not extra and time_of_day:
            if time_of_day == "morning":
                extra = "morning light"
            elif time_of_day == "evening":
                extra = "warm evening light"
            elif time_of_day == "night":
                extra = "night-time glow"

        if extra:
            return f"{base}, {extra}"
        return base
    
    def build_multiple_prompts(
        self,
        brand_info: Dict,
        context_variations: List[Dict],
        creative_type: str = "social_media_ad"
    ) -> List[str]:
        """
        Build multiple prompts from context variations.
        
        Args:
            brand_info: Brand information dictionary
            context_variations: List of context variations
            creative_type: Type of creative to generate
        
        Returns:
            List of prompts
        """
        prompts = []
        for context in context_variations:
            prompt = self.build_prompt(brand_info, context, creative_type)
            prompts.append(prompt)
        
        return prompts
    
    def add_negative_prompt(self, base_prompt: str) -> str:
        """
        Add negative prompt elements for better quality.
        
        Args:
            base_prompt: Base prompt
        
        Returns:
            Negative prompt
        """
        negative_elements = [
            "low quality",
            "blurry",
            "pixelated",
            "distorted",
            "ugly",
            "bad composition",
            "watermark",
            "text overlay",
            "logo overlay",
            "amateur",
            "unprofessional"
        ]
        
        return ", ".join(negative_elements)
