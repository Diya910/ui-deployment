from PIL import Image
from typing import Dict, List, Tuple, Optional
from app.utils.palette_utils import (
    extract_dominant_colors,
    get_brand_palette_info,
    create_color_palette_prompt
)


class BrandExtractor:
    """Extractor for brand intelligence from logos and product images."""
    
    def __init__(self):
        """Initialize brand extractor."""
        pass
    
    def extract_brand_info(
        self,
        logo_image: Optional[Image.Image] = None,
        product_image: Optional[Image.Image] = None,
        brand_name: Optional[str] = None,
        product_category: Optional[str] = None
    ) -> Dict:
        """
        Extract comprehensive brand information.
        
        Args:
            logo_image: Brand logo image
            product_image: Product image
            brand_name: Brand name
            product_category: Product category
        
        Returns:
            Brand information dictionary
        """
        brand_info = {
            "brand_name": brand_name or "Brand",
            "product_category": product_category or "Product",
            "has_logo": logo_image is not None,
            "has_product_image": product_image is not None
        }
        
        # Extract colors from logo
        if logo_image:
            logo_colors = extract_dominant_colors(logo_image, num_colors=5)
            logo_palette = get_brand_palette_info(logo_colors)
            brand_info["logo_colors"] = logo_palette
            brand_info["primary_color"] = logo_palette["primary_hex"]
        
        # Extract colors from product
        if product_image:
            product_colors = extract_dominant_colors(product_image, num_colors=5)
            product_palette = get_brand_palette_info(product_colors)
            brand_info["product_colors"] = product_palette
        
        # Determine overall brand palette
        if logo_image and product_image:
            # Combine both palettes
            combined_colors = list(set(
                logo_colors[:3] + product_colors[:3]
            ))[:5]
            brand_palette = get_brand_palette_info(combined_colors)
        elif logo_image:
            brand_palette = logo_palette
        elif product_image:
            brand_palette = product_palette
        else:
            # Default palette
            brand_palette = {
                "hex_colors": ["#667eea", "#764ba2", "#f093fb"],
                "primary_hex": "#667eea",
                "is_dark_palette": False
            }
        
        brand_info["brand_palette"] = brand_palette
        
        return brand_info
    
    def create_brand_prompt_segment(self, brand_info: Dict) -> str:
        """
        Create a prompt segment describing brand identity.
        
        Args:
            brand_info: Brand information dictionary
        
        Returns:
            Brand prompt segment
        """
        prompt = f"Brand: {brand_info['brand_name']}. "
        prompt += f"Product category: {brand_info['product_category']}. "
        
        # Add color information
        palette = brand_info.get("brand_palette", {})
        if palette:
            prompt += create_color_palette_prompt(palette)
        
        # Add style guidance
        if palette.get("is_dark_palette"):
            prompt += "Use premium, sophisticated aesthetics. "
        else:
            prompt += "Use vibrant, energetic aesthetics. "
        
        return prompt
    
    def get_logo_placement_instruction(self) -> str:
        """Get instruction for logo placement in generated images."""
        return (
            "Place the brand logo in the top-right corner, "
            "clearly visible but not overwhelming the composition. "
            "Ensure the logo is crisp and maintains brand identity."
        )
    
    def get_product_category_style(self, category: str) -> str:
        """
        Get style recommendations based on product category.
        
        Args:
            category: Product category
        
        Returns:
            Style description
        """
        category_styles = {
            "beverage": "refreshing, vibrant, lifestyle-focused, showing consumption moments",
            "skincare": "clean, elegant, natural lighting, beauty-focused, aspirational",
            "fashion": "stylish, trendy, lifestyle, model-focused, aspirational",
            "food": "appetizing, colorful, close-up, lifestyle, mouth-watering",
            "technology": "modern, sleek, futuristic, clean, professional",
            "fitness": "energetic, active, motivational, lifestyle, dynamic",
            "home": "cozy, comfortable, lifestyle, aspirational, warm",
            "automotive": "powerful, sleek, dynamic, aspirational, premium"
        }
        
        category_lower = category.lower()
        for key, style in category_styles.items():
            if key in category_lower:
                return style
        
        return "professional, high-quality, lifestyle-focused, aspirational"
    
    def get_brand_safety_guidelines(self) -> List[str]:
        """Get brand safety guidelines for content generation."""
        return [
            "Avoid controversial or sensitive topics",
            "Maintain positive and inclusive messaging",
            "No misleading or false claims",
            "Respect cultural sensitivities",
            "Use appropriate and professional language",
            "Avoid stereotypes and biases",
            "Ensure family-friendly content"
        ]
