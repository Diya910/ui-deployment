import zipfile
import os
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def create_creative_package(
    output_path: str,
    images: List[str],
    captions: List[str],
    metadata: List[Dict],
    package_name: str = None
) -> str:
    """
    Create a ZIP package containing all generated creatives.
    
    Args:
        output_path: Directory to save the ZIP file
        images: List of image file paths
        captions: List of captions corresponding to images
        metadata: List of metadata dicts for each creative
        package_name: Optional custom package name
    
    Returns:
        Path to the created ZIP file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Generate package name
    if package_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"creatives_{timestamp}"
    
    zip_path = os.path.join(output_path, f"{package_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add images
        for idx, image_path in enumerate(images):
            if os.path.exists(image_path):
                # Add to images folder in ZIP
                arcname = f"images/creative_{idx+1:02d}.png"
                zipf.write(image_path, arcname)
        
        # Create and add captions.txt
        captions_content = ""
        for idx, caption in enumerate(captions):
            captions_content += f"=== Creative {idx+1:02d} ===\n"
            captions_content += f"{caption}\n\n"
        
        zipf.writestr("captions.txt", captions_content)
        
        # Create and add metadata.json
        metadata_content = {
            "generated_at": datetime.now().isoformat(),
            "total_creatives": len(images),
            "creatives": [
                {
                    "id": idx + 1,
                    "filename": f"creative_{idx+1:02d}.png",
                    "caption": caption,
                    "metadata": meta
                }
                for idx, (caption, meta) in enumerate(zip(captions, metadata))
            ]
        }
        
        zipf.writestr("metadata.json", json.dumps(metadata_content, indent=2))
        
        # Add README
        readme_content = f"""# AI Creative Studio - Generated Creatives

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Creatives: {len(images)}

## Contents

- `/images/` - All generated creative images
- `captions.txt` - Captions for each creative
- `metadata.json` - Detailed metadata including context signals

## Usage

Each creative is numbered and corresponds to its caption and metadata entry.

Enjoy your hyper-personalized, context-aware creatives! 🎨
"""
        zipf.writestr("README.md", readme_content)
    
    return zip_path


def get_zip_size(zip_path: str) -> int:
    """Get the size of a ZIP file in bytes."""
    return os.path.getsize(zip_path)


def get_zip_size_mb(zip_path: str) -> float:
    """Get the size of a ZIP file in megabytes."""
    return get_zip_size(zip_path) / (1024 * 1024)
