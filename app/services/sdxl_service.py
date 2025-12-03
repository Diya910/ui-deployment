from PIL import Image, ImageDraw, ImageFont
from typing import Optional, List


class SDXLService:
    """Service for generating images using Stable Diffusion XL."""
    
    def __init__(self):
        """Initialize SDXL service."""
        print("⚠️  SDXL service is in placeholder mode. For production, integrate with Stability AI API.")
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg_scale: float = 7.0
    ) -> Optional[Image.Image]:
        """
        Generate a single image using SDXL.
        
        Args:
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt to avoid certain elements
            width: Image width
            height: Image height
            steps: Number of inference steps
            cfg_scale: Classifier-free guidance scale
        
        Returns:
            PIL Image object
        """
        # Placeholder implementation
        return self._create_placeholder_image(prompt, width, height)
    
    def generate_multiple_images(
        self,
        prompts: List[str],
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg_scale: float = 7.0
    ) -> List[Optional[Image.Image]]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts: List of text prompts
            negative_prompt: Negative prompt
            width: Image width
            height: Image height
            steps: Number of inference steps
            cfg_scale: Classifier-free guidance scale
        
        Returns:
            List of PIL Image objects
        """
        images = []
        for idx, prompt in enumerate(prompts):
            print(f"Generating SDXL image {idx + 1}/{len(prompts)}...")
            image = self.generate_image(prompt, negative_prompt, width, height, steps, cfg_scale)
            images.append(image)
        
        return images
    
    def _create_placeholder_image(self, prompt: str, width: int = 1024, height: int = 1024) -> Image.Image:
        """Create a placeholder image."""
        # Create a gradient background
        image = Image.new('RGB', (width, height), color='#764ba2')
        draw = ImageDraw.Draw(image)
        
        # Create gradient effect
        for i in range(height):
            r = int(118 + (245 - 118) * i / height)
            g = int(75 + (106 - 75) * i / height)
            b = int(162 + (255 - 162) * i / height)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # Add text
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 25)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "SDXL Creative"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(
            ((width - title_width) // 2, height // 2 - 50),
            title,
            fill='white',
            font=font_large
        )
        
        # Prompt preview
        prompt_preview = prompt[:60] + "..." if len(prompt) > 60 else prompt
        prompt_bbox = draw.textbbox((0, 0), prompt_preview, font=font_small)
        prompt_width = prompt_bbox[2] - prompt_bbox[0]
        draw.text(
            ((width - prompt_width) // 2, height // 2 + 20),
            prompt_preview,
            fill='rgba(255, 255, 255, 0.9)',
            font=font_small
        )
        
        return image
