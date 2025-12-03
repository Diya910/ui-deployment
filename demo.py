import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
load_dotenv()

# Import modules
from app.core.context_engine import ContextEngine
from app.core.brand_extractor import BrandExtractor
from app.core.prompt_builder import PromptBuilder
from app.core.caption_generator import CaptionGenerator
from app.services.dalle_service import DalleService
from app.utils.image_utils import create_composite, ensure_rgb
from app.utils.zip_utils import create_creative_package


def create_sample_logo():
    """Create a sample logo for testing."""
    img = Image.new('RGB', (300, 300), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple logo
    draw.ellipse([50, 50, 250, 250], fill='white', outline='#764ba2', width=5)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()
    
    text = "DEMO"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    draw.text(
        ((300 - text_width) // 2, (300 - text_height) // 2),
        text,
        fill='#667eea',
        font=font
    )
    
    return img


def create_sample_product():
    """Create a sample product image for testing."""
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple product (bottle shape)
    # Bottle body
    draw.rectangle([150, 100, 250, 300], fill='#f093fb', outline='#764ba2', width=3)
    # Bottle neck
    draw.rectangle([175, 80, 225, 100], fill='#f093fb', outline='#764ba2', width=3)
    # Bottle cap
    draw.rectangle([170, 60, 230, 80], fill='#667eea', outline='#764ba2', width=3)
    
    return img


def main():
    """Main demo function."""
    print("🎨 AI Creative Studio - Demo Script")
    print("=" * 50)
    print()
    
    # Configuration
    brand_name = "DemoBrend"
    product_category = "Beverage"
    city = "Bangalore"
    num_creatives = 5
    
    print(f"📋 Configuration:")
    print(f"   Brand: {brand_name}")
    print(f"   Category: {product_category}")
    print(f"   City: {city}")
    print(f"   Creatives: {num_creatives}")
    print()
    
    # Create sample images
    print("🎨 Creating sample brand assets...")
    logo_img = create_sample_logo()
    product_img = create_sample_product()
    print("✅ Sample assets created")
    print()
    
    # Initialize services
    print("🔧 Initializing AI services...")
    context_engine = ContextEngine()
    brand_extractor = BrandExtractor()
    prompt_builder = PromptBuilder()
    caption_generator = CaptionGenerator()
    dalle_service = DalleService()
    print("✅ Services initialized")
    print()
    
    # Extract brand information
    print("🎨 Analyzing brand identity...")
    brand_info = brand_extractor.extract_brand_info(
        logo_image=logo_img,
        product_image=product_img,
        brand_name=brand_name,
        product_category=product_category
    )
    print(f"✅ Brand colors extracted: {brand_info['brand_palette']['hex_colors'][:3]}")
    print()
    
    # Get context
    print(f"🌍 Gathering context for {city}...")
    base_context = context_engine.get_context(
        city=city,
        product_category=product_category
    )
    print(f"✅ Weather: {base_context['weather']['description']}, {base_context['weather']['temperature']}°C")
    print(f"✅ Season: {base_context['season']}, Time: {base_context['time_of_day']}")
    print()
    
    # Create variations
    print(f"🎯 Creating {num_creatives} context variations...")
    context_variations = context_engine.create_context_variations(
        base_context,
        num_variations=num_creatives
    )
    print(f"✅ Variations created with themes: {[v['theme'] for v in context_variations]}")
    print()
    
    # Build prompts
    print("📝 Building AI prompts...")
    prompts = prompt_builder.build_multiple_prompts(
        brand_info=brand_info,
        context_variations=context_variations
    )
    print(f"✅ {len(prompts)} prompts generated")
    print(f"   Sample: {prompts[0][:100]}...")
    print()
    
    # Generate images
    print("🎨 Generating images with DALL-E...")
    print("   (This may take a minute...)")
    generated_images = []
    for idx, prompt in enumerate(prompts):
        print(f"   Generating image {idx + 1}/{len(prompts)}...", end='\r')
        image = dalle_service.generate_image(prompt)
        if image:
            # Add logo
            image = create_composite(image, logo_img)
            generated_images.append(image)
    print()
    print(f"✅ {len(generated_images)} images generated")
    print()
    
    # Generate captions
    print("💬 Creating engaging captions...")
    captions = caption_generator.generate_multiple_captions(
        brand_info=brand_info,
        context_variations=context_variations,
        tone="engaging"
    )
    print(f"✅ {len(captions)} captions generated")
    print(f"   Sample: {captions[0]}")
    print()
    
    # Save and package
    print("📦 Packaging creatives...")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save images
    image_paths = []
    for idx, img in enumerate(generated_images):
        img_path = os.path.join(output_dir, f"demo_creative_{idx+1:02d}.png")
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
        package_name=f"{brand_name.lower()}_demo_creatives"
    )
    
    print(f"✅ Package created: {zip_path}")
    print()
    
    # Summary
    print("=" * 50)
    print("🎉 Demo Complete!")
    print()
    print(f"📦 Output:")
    print(f"   ZIP Package: {zip_path}")
    print(f"   Images: {len(generated_images)}")
    print(f"   Captions: {len(captions)}")
    print()
    print("💡 Next steps:")
    print("   1. Extract the ZIP file to view all creatives")
    print("   2. Check metadata.json for context details")
    print("   3. Review captions.txt for all captions")
    print("   4. Run the Streamlit app for the full UI experience:")
    print("      streamlit run streamlit_app.py")
    print()


if __name__ == "__main__":
    main()
