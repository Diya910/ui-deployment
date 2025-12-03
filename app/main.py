from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
from typing import Optional, List
from datetime import datetime
from dotenv import load_dotenv

from app.core.context_engine import ContextEngine
from app.core.brand_extractor import BrandExtractor
from app.core.prompt_builder import PromptBuilder
from app.core.caption_generator import CaptionGenerator
from app.services.dalle_service import DalleService
from app.utils.image_utils import create_composite, ensure_rgb
from app.utils.zip_utils import create_creative_package

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Creative Studio API",
    description="Generate hyper-personalized, context-aware ad creatives",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
context_engine = ContextEngine()
brand_extractor = BrandExtractor()
prompt_builder = PromptBuilder()
caption_generator = CaptionGenerator()
dalle_service = DalleService()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Creative Studio API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate": "/generate (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/generate")
async def generate_creatives(
    brand_name: str = Form(...),
    product_category: str = Form(...),
    city: str = Form(...),
    num_creatives: int = Form(10),
    caption_tone: str = Form("engaging"),
    logo: Optional[UploadFile] = File(None),
    product_image: Optional[UploadFile] = File(None)
):
    """
    Generate hyper-personalized ad creatives.
    
    Args:
        brand_name: Brand name
        product_category: Product category
        city: Target city
        num_creatives: Number of creatives to generate
        caption_tone: Tone for captions
        logo: Brand logo file
        product_image: Product image file
    
    Returns:
        ZIP file containing all creatives
    """
    try:
        # Process uploaded images
        logo_img = None
        product_img = None
        
        if logo:
            logo_content = await logo.read()
            logo_img = Image.open(io.BytesIO(logo_content))
        
        if product_image:
            product_content = await product_image.read()
            product_img = Image.open(io.BytesIO(product_content))
        
        # Extract brand information
        brand_info = brand_extractor.extract_brand_info(
            logo_image=logo_img,
            product_image=product_img,
            brand_name=brand_name,
            product_category=product_category
        )
        
        # Get context
        base_context = context_engine.get_context(
            city=city,
            product_category=product_category
        )
        
        # Create variations
        context_variations = context_engine.create_context_variations(
            base_context,
            num_variations=num_creatives
        )
        
        # Build prompts
        prompts = prompt_builder.build_multiple_prompts(
            brand_info=brand_info,
            context_variations=context_variations
        )
        
        # Generate images
        generated_images = []
        for prompt in prompts:
            image = dalle_service.generate_image(prompt)
            if image:
                # Add logo if provided
                if logo_img:
                    image = create_composite(image, logo_img)
                generated_images.append(image)
        
        # Generate captions
        captions = caption_generator.generate_multiple_captions(
            brand_info=brand_info,
            context_variations=context_variations,
            tone=caption_tone.lower()
        )
        
        # Save images
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        image_paths = []
        for idx, img in enumerate(generated_images):
            img_path = os.path.join(output_dir, f"creative_{idx+1:02d}.png")
            img = ensure_rgb(img)
            img.save(img_path)
            image_paths.append(img_path)
        
        # Create metadata
        metadata = [
            {
                "context": ctx,
                "prompt": prompts[idx]
            }
            for idx, ctx in enumerate(context_variations)
        ]
        
        # Create ZIP package
        zip_path = create_creative_package(
            output_path=output_dir,
            images=image_paths,
            captions=captions,
            metadata=metadata,
            package_name=f"{brand_name.lower().replace(' ', '_')}_creatives"
        )
        
        # Return ZIP file
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=os.path.basename(zip_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
