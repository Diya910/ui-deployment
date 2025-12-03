from colorthief import ColorThief
from PIL import Image
import io
from typing import List, Tuple, Dict
import numpy as np
from sklearn.cluster import KMeans


def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
    """Extract dominant colors from an image using ColorThief."""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Extract colors
    color_thief = ColorThief(img_byte_arr)
    
    if num_colors == 1:
        dominant_color = color_thief.get_color(quality=1)
        return [dominant_color]
    else:
        palette = color_thief.get_palette(color_count=num_colors, quality=1)
        return palette


def extract_colors_kmeans(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
    """Extract dominant colors using K-means clustering."""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize for faster processing
    image.thumbnail((150, 150))
    
    # Convert to numpy array
    img_array = np.array(image)
    pixels = img_array.reshape(-1, 3)
    
    # Apply K-means
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get cluster centers (dominant colors)
    colors = kmeans.cluster_centers_.astype(int)
    
    return [tuple(color) for color in colors]


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_color_brightness(rgb: Tuple[int, int, int]) -> float:
    """Calculate perceived brightness of a color (0-255)."""
    # Using perceived brightness formula
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])


def is_dark_color(rgb: Tuple[int, int, int], threshold: int = 128) -> bool:
    """Check if a color is dark."""
    return get_color_brightness(rgb) < threshold


def get_contrasting_color(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Get a contrasting color (black or white) for text."""
    if is_dark_color(rgb):
        return (255, 255, 255)  # White
    else:
        return (0, 0, 0)  # Black


def get_brand_palette_info(colors: List[Tuple[int, int, int]]) -> Dict:
    """Get detailed information about a brand color palette."""
    hex_colors = [rgb_to_hex(color) for color in colors]
    
    # Find primary (most vibrant/saturated) color
    primary_idx = 0
    max_saturation = 0
    
    for idx, color in enumerate(colors):
        r, g, b = color
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        saturation = (max_val - min_val) / max_val if max_val > 0 else 0
        
        if saturation > max_saturation:
            max_saturation = saturation
            primary_idx = idx
    
    return {
        "colors": colors,
        "hex_colors": hex_colors,
        "primary_color": colors[primary_idx],
        "primary_hex": hex_colors[primary_idx],
        "is_dark_palette": sum(is_dark_color(c) for c in colors) > len(colors) / 2,
        "color_descriptions": [
            {
                "rgb": color,
                "hex": hex_color,
                "brightness": get_color_brightness(color),
                "is_dark": is_dark_color(color)
            }
            for color, hex_color in zip(colors, hex_colors)
        ]
    }


def create_color_palette_prompt(palette_info: Dict) -> str:
    """Create a prompt segment describing the color palette."""
    hex_colors = palette_info["hex_colors"]
    primary_hex = palette_info["primary_hex"]
    
    prompt = f"Brand colors: {', '.join(hex_colors)}. "
    prompt += f"Primary brand color: {primary_hex}. "
    
    if palette_info["is_dark_palette"]:
        prompt += "Use a dark, sophisticated color scheme. "
    else:
        prompt += "Use a bright, vibrant color scheme. "
    
    return prompt
