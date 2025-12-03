import openai
import os
from typing import List, Optional
import requests
from PIL import Image
import io


class DalleService:
    """Service for generating images using DALL-E."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize DALL-E service with API key."""
        self.api_key = api_key or os.getenv("IMAGE_API_KEY")
        if self.api_key and self.api_key != "your_openai_api_key_here":
            openai.api_key = self.api_key
        self.model = "dall-e-3"
        self.size = os.getenv("IMAGE_SIZE", "1024x1024")
        self.quality = os.getenv("IMAGE_QUALITY", "standard")
    
    def generate_image(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: str = "vivid"
    ) -> Optional[Image.Image]:
        """
        Generate a single image using DALL-E.
        
        Args:
            prompt: Text prompt for image generation
            size: Image size (1024x1024, 1024x1792, or 1792x1024)
            quality: Image quality (standard or hd)
            style: Image style (vivid or natural)
        
        Returns:
            PIL Image object or None if generation fails
        """
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("⚠️  No valid OpenAI API key found. Using placeholder image.")
            return self._create_placeholder_image(prompt)
        
        try:
            response = openai.images.generate(
                model=self.model,
                prompt=prompt,
                size=size or self.size,
                quality=quality or self.quality,
                style=style,
                n=1
            )
            
            # Download the image
            image_url = response.data[0].url
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_response.content))
            
            return image
            
        except Exception as e:
            print(f"DALL-E generation error: {e}")
            return self._create_placeholder_image(prompt)
    
    def generate_multiple_images(
        self,
        prompts: List[str],
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: str = "vivid"
    ) -> List[Optional[Image.Image]]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts: List of text prompts
            size: Image size
            quality: Image quality
            style: Image style
        
        Returns:
            List of PIL Image objects
        """
        images = []
        for idx, prompt in enumerate(prompts):
            print(f"Generating image {idx + 1}/{len(prompts)}...")
            image = self.generate_image(prompt, size, quality, style)
            images.append(image)
        
        return images
    
    def _create_placeholder_image(self, prompt: str) -> Image.Image:
        """Create a placeholder image when API is not available."""
        from PIL import ImageDraw, ImageFont
        
        # Create a gradient background
        width, height = 1024, 1024
        image = Image.new('RGB', (width, height), color='#667eea')
        draw = ImageDraw.Draw(image)
        
        # Create gradient effect
        for i in range(height):
            r = int(102 + (247 - 102) * i / height)
            g = int(126 + (129 - 126) * i / height)
            b = int(234 + (162 - 234) * i / height)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # Add text
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "AI Creative Studio"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(
            ((width - title_width) // 2, height // 2 - 100),
            title,
            fill='white',
            font=font_large
        )
        
        # Subtitle
        subtitle = "Generated Creative"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(
            ((width - subtitle_width) // 2, height // 2),
            subtitle,
            fill='white',
            font=font_small
        )
        
        # Prompt preview (truncated)
        prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
        prompt_bbox = draw.textbbox((0, 0), prompt_preview, font=font_small)
        prompt_width = prompt_bbox[2] - prompt_bbox[0]
        draw.text(
            ((width - prompt_width) // 2, height // 2 + 80),
            prompt_preview,
            fill=(255, 255, 255),
            font=font_small
        )
        
        return image
