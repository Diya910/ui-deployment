from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import base64
from typing import Tuple, Optional
import numpy as np


def resize_image(image: Image.Image, max_size: Tuple[int, int] = (1024, 1024)) -> Image.Image:
    """Resize image while maintaining aspect ratio."""
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def base64_to_image(base64_string: str) -> Image.Image:
    """Convert base64 string to PIL Image."""
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data))


def create_composite(
    background: Image.Image,
    logo: Optional[Image.Image] = None,
    logo_position: str = "top-right",
    logo_size: Tuple[int, int] = (150, 150)
) -> Image.Image:
    """Create a composite image with logo overlay."""
    composite = background.copy()
    
    if logo:
        # Resize logo
        logo = logo.copy()
        logo.thumbnail(logo_size, Image.Resampling.LANCZOS)
        
        # Calculate position
        if logo_position == "top-right":
            x = composite.width - logo.width - 20
            y = 20
        elif logo_position == "top-left":
            x = 20
            y = 20
        elif logo_position == "bottom-right":
            x = composite.width - logo.width - 20
            y = composite.height - logo.height - 20
        elif logo_position == "bottom-left":
            x = 20
            y = composite.height - logo.height - 20
        else:  # center
            x = (composite.width - logo.width) // 2
            y = (composite.height - logo.height) // 2
        
        # Paste logo with transparency
        if logo.mode == 'RGBA':
            composite.paste(logo, (x, y), logo)
        else:
            composite.paste(logo, (x, y))
    
    return composite


def enhance_image(image: Image.Image, brightness: float = 1.0, contrast: float = 1.0) -> Image.Image:
    """Enhance image brightness and contrast."""
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    
    return image


def add_text_overlay(
    image: Image.Image,
    text: str,
    position: str = "bottom",
    font_size: int = 40,
    text_color: Tuple[int, int, int] = (255, 255, 255),
    bg_color: Optional[Tuple[int, int, int, int]] = None
) -> Image.Image:
    """Add text overlay to image."""
    draw = ImageDraw.Draw(image, 'RGBA')
    
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    if position == "bottom":
        x = (image.width - text_width) // 2
        y = image.height - text_height - 40
    elif position == "top":
        x = (image.width - text_width) // 2
        y = 40
    else:  # center
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2
    
    # Draw background if specified
    if bg_color:
        padding = 20
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=bg_color
        )
    
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)
    
    return image


def ensure_rgb(image: Image.Image) -> Image.Image:
    """Ensure image is in RGB mode."""
    if image.mode != 'RGB':
        return image.convert('RGB')
    return image
