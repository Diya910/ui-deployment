import google.generativeai as genai
import os
from typing import List, Dict, Optional


class CaptionGenerator:
    """Generator for creating brand-aligned, context-aware captions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize caption generator with Gemini API."""
        self.api_key = api_key or os.getenv("TEXT_API_KEY")
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
    
    def generate_caption(
        self,
        brand_info: Dict,
        context: Dict,
        tone: str = "engaging",
        max_length: int = 150
    ) -> str:
        """
        Generate a single caption.
        
        Args:
            brand_info: Brand information dictionary
            context: Context dictionary
            tone: Caption tone (engaging, professional, playful, etc.)
            max_length: Maximum caption length
        
        Returns:
            Generated caption
        """
        if not self.model:
            return self._generate_fallback_caption(brand_info, context)
        
        try:
            prompt = self._create_caption_prompt(brand_info, context, tone, max_length)
            response = self.model.generate_content(prompt)
            caption = response.text.strip()
            
            # Clean up caption
            caption = self._clean_caption(caption)
            
            # Ensure length constraint
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
            
            return caption
            
        except Exception as e:
            print(f"Gemini caption generation error: {e}")
            return self._generate_fallback_caption(brand_info, context)
    
    def generate_multiple_captions(
        self,
        brand_info: Dict,
        context_variations: List[Dict],
        tone: str = "engaging",
        max_length: int = 150
    ) -> List[str]:
        """
        Generate multiple captions for different contexts.
        
        Args:
            brand_info: Brand information dictionary
            context_variations: List of context variations
            tone: Caption tone
            max_length: Maximum caption length
        
        Returns:
            List of generated captions
        """
        captions = []
        for idx, context in enumerate(context_variations):
            print(f"Generating caption {idx + 1}/{len(context_variations)}...")
            caption = self.generate_caption(brand_info, context, tone, max_length)
            captions.append(caption)
        
        return captions
    
    def _create_caption_prompt(
        self,
        brand_info: Dict,
        context: Dict,
        tone: str,
        max_length: int
    ) -> str:
        """Create a prompt for caption generation."""
        brand_name = brand_info.get("brand_name", "Brand")
        product_category = brand_info.get("product_category", "product")
        city = context.get("city", "")
        weather_context = context.get("weather_context", "")
        mood = context.get("mood", "")
        theme = context.get("theme", "")
        
        prompt = f"""Create a compelling advertisement caption for {brand_name} {product_category}.

Context:
- Location: {city}
- Weather: {weather_context}
- Theme: {theme}
- Mood: {mood}
- Tone: {tone}

Requirements:
1. Maximum {max_length} characters
2. Include a strong call-to-action (CTA)
3. Be contextually relevant to the location and weather
4. Use {tone} tone
5. Make it engaging and shareable
6. Include relevant emojis (2-3 maximum)
7. No hashtags
8. Brand-safe and positive messaging
9. Avoid making false claims
10. Make it feel personal and relatable

Generate only the caption text, nothing else."""
        
        return prompt
    
    def _generate_fallback_caption(self, brand_info: Dict, context: Dict) -> str:
        """Generate a fallback caption when API is unavailable."""
        brand_name = brand_info.get("brand_name", "Brand")
        product_category = brand_info.get("product_category", "product")
        city = context.get("city", "your city")
        theme = context.get("theme", "lifestyle")
        
        # Template-based captions
        templates = [
            f"✨ Experience {brand_name} like never before! Perfect for {city}'s {theme}. Get yours today! 🎯",
            f"🌟 {brand_name} brings you the perfect {product_category} for every moment in {city}. Try it now! 💫",
            f"💎 Elevate your {theme} with {brand_name}. Made for {city}, made for you. Shop now! 🛍️",
            f"🎨 {brand_name}: Where quality meets {theme}. Available now in {city}! ✨",
            f"⚡ Transform your day with {brand_name}. The perfect {product_category} for {city}. Order today! 🚀",
            f"🌈 Discover the {brand_name} difference. Crafted for {city}'s {theme}. Get it now! 💝",
            f"🔥 {brand_name} - Your perfect companion for {city}'s {theme}. Don't miss out! 🎁",
            f"💫 Make every moment special with {brand_name}. Now in {city}! Shop today! ✨",
            f"🎯 {brand_name}: Premium {product_category} for {city}'s vibrant {theme}. Try it now! 🌟",
            f"✨ Embrace the {brand_name} experience. Perfect for {city}, perfect for you! 🎊"
        ]
        
        # Use variation_id to select template if available
        variation_id = context.get("variation_id", 1)
        template_idx = (variation_id - 1) % len(templates)
        
        return templates[template_idx]
    
    def _clean_caption(self, caption: str) -> str:
        """Clean and format caption."""
        # Remove quotes if present
        caption = caption.strip('"').strip("'")
        
        # Remove any markdown formatting
        caption = caption.replace("**", "").replace("*", "")
        
        # Ensure it doesn't start with "Caption:"
        if caption.lower().startswith("caption:"):
            caption = caption[8:].strip()
        
        return caption
    
    def validate_caption(self, caption: str) -> bool:
        """
        Validate caption for brand safety and quality.
        
        Args:
            caption: Caption to validate
        
        Returns:
            True if caption passes validation
        """
        # Check length
        if len(caption) < 10 or len(caption) > 300:
            return False
        
        # Check for inappropriate content (basic check)
        inappropriate_words = ["hate", "violence", "offensive"]
        caption_lower = caption.lower()
        
        for word in inappropriate_words:
            if word in caption_lower:
                return False
        
        return True
