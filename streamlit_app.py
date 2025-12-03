"""
AI Creative Studio - Streamlit Application
Beautiful, modern UI for generating hyper-personalized ad creatives.
"""
import streamlit as st
from PIL import Image
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Import core modules
from app.core.context_engine import ContextEngine
from app.core.brand_extractor import BrandExtractor
from app.core.prompt_builder import PromptBuilder
from app.core.caption_generator import CaptionGenerator
from app.services.dalle_service import DalleService
from app.utils.image_utils import create_composite, ensure_rgb
from app.utils.zip_utils import create_creative_package

# Initialize Gemini for audience analysis
TEXT_API_KEY = os.getenv("TEXT_API_KEY")
if TEXT_API_KEY and TEXT_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=TEXT_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
else:
    gemini_model = None

# Page configuration
st.set_page_config(
    page_title="AI Creative Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container adjustments */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
        max_width: 100%;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .header-container {
            padding: 1rem;
        }
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 300;
    }
    
    /* Cards */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        color: white;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_creatives' not in st.session_state:
    st.session_state.generated_creatives = []
if 'generated_captions' not in st.session_state:
    st.session_state.generated_captions = []
if 'zip_path' not in st.session_state:
    st.session_state.zip_path = None
if 'selected_for_refinement' not in st.session_state:
    st.session_state.selected_for_refinement = []
if 'audience_insights' not in st.session_state:
    st.session_state.audience_insights = None
if 'context_variations' not in st.session_state:
    st.session_state.context_variations = []
if 'brand_info' not in st.session_state:
    st.session_state.brand_info = {}


# Location data hierarchy
LOCATION_DATA = {
    "India": {
        "South India": ["Bangalore", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
        "North India": ["Delhi", "Gurgaon", "Noida", "Chandigarh", "Jaipur"],
        "West India": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nagpur"],
        "East India": ["Kolkata", "Bhubaneswar", "Patna", "Ranchi"],
        "Central India": ["Indore", "Bhopal", "Raipur", "Nagpur"]
    },
    "United States": {
        "West Coast": ["Los Angeles", "San Francisco", "Seattle", "San Diego"],
        "East Coast": ["New York", "Boston", "Miami", "Washington DC"],
        "Midwest": ["Chicago", "Detroit", "Minneapolis", "St. Louis"],
        "South": ["Houston", "Dallas", "Atlanta", "Austin"]
    },
    "United Kingdom": {
        "England": ["London", "Manchester", "Birmingham", "Liverpool"],
        "Scotland": ["Edinburgh", "Glasgow", "Aberdeen"],
        "Wales": ["Cardiff", "Swansea"],
        "Northern Ireland": ["Belfast", "Derry"]
    }
}


def analyze_target_audience(brand_name: str, product_category: str, company_description: str = "") -> dict:
    """Use LLM to analyze target audience and suggest best locations."""
    if not gemini_model:
        # Fallback analysis
        return {
            "age_group": "25-45 years",
            "demographics": "Urban professionals and young families",
            "regions": ["Metropolitan cities", "Tier 1 cities"],
            "insights": "Target audience likely consists of urban professionals interested in quality products.",
            "recommended_cities": ["Bangalore", "Mumbai", "Delhi"]
        }
    
    try:
        prompt = f"""Analyze the target audience for this brand:

Brand Name: {brand_name}
Product Category: {product_category}
Company Description: {company_description if company_description else "Not provided"}

Provide a detailed analysis in JSON format with:
1. Primary age group (e.g., "18-25", "25-35", "35-50")
2. Demographics (lifestyle, income level, interests)
3. Best regions/cities for marketing (be specific)
4. Key insights about customer behavior
5. Recommended top 3 cities in India for this product

Return ONLY valid JSON, no other text."""

        response = gemini_model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Try to parse JSON
        import json
        # Remove markdown code blocks if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        analysis = json.loads(result_text)
        return analysis
        
    except Exception as e:
        print(f"Audience analysis error: {e}")
        return {
            "age_group": "25-45 years",
            "demographics": "Urban professionals",
            "regions": ["Metropolitan areas"],
            "insights": f"Target audience for {product_category} in urban markets.",
            "recommended_cities": ["Bangalore", "Mumbai", "Delhi"]
        }


def explain_creative_choices(brand_info: dict, context: dict, creative_index: int) -> str:
    """Generate explanation for creative design choices."""
    explanation = f"""### 🎨 Creative #{creative_index} - Design Rationale

**Color Palette:**
- Primary Brand Color: {brand_info.get('brand_palette', {}).get('primary_hex', '#667eea')}
- Color Scheme: {', '.join(brand_info.get('brand_palette', {}).get('hex_colors', [])[:3])}
- Reasoning: Colors extracted from your brand logo to maintain consistency and recognition.

**Positioning & Layout:**
- Logo Placement: Top-right corner for brand visibility without overwhelming the creative
- Composition: Professional ad layout optimized for social media engagement
- Style: {context.get('mood', 'Engaging and contextual')}

**Context Integration:**
- Location: {context.get('city', 'Target city')}
- Weather: {context.get('weather', {}).get('description', 'Current conditions')} at {context.get('weather', {}).get('temperature', 'N/A')}°C
- Time: {context.get('time_of_day', 'Day')} during {context.get('season', 'season')}
- Theme: {context.get('theme', 'Lifestyle-focused')}

**Why This Works:**
- Contextually relevant to {context.get('city', 'the target location')}'s current conditions
- Aligns with {context.get('local_vibes', 'local culture and preferences')}
- Optimized for {context.get('mood', 'target audience engagement')}
- Brand colors ensure immediate recognition

**Suggested Use Cases:**
- Social media posts (Instagram, Facebook)
- Digital advertising campaigns
- Location-specific promotions
- {context.get('season', 'Seasonal')} campaigns
"""
    return explanation


def get_refinement_suggestions(selected_indices: list, brand_info: dict) -> str:
    """Generate suggestions for refining selected creatives."""
    if not selected_indices:
        return "Please select creatives to refine."
    
    suggestions = f"""### 🎯 Refinement Suggestions for Selected Creatives

You've selected {len(selected_indices)} creative(s) for refinement.

**Possible Refinements:**

1. **Color Adjustments:**
   - Enhance brand color prominence
   - Adjust brightness/contrast for better visibility
   - Try different color temperature (warmer/cooler)

2. **Composition Changes:**
   - Reposition logo (top-left, bottom-right, center)
   - Adjust logo size (larger for brand focus, smaller for product focus)
   - Change background elements

3. **Context Variations:**
   - Different time of day (morning energy vs evening relaxation)
   - Alternative weather scenarios
   - Different local cultural themes

4. **Style Modifications:**
   - More vibrant/energetic vs calm/sophisticated
   - Lifestyle-focused vs product-focused
   - Minimalist vs detailed composition

**Next Steps:**
1. Note which specific changes you want
2. Generate new variations with adjusted parameters
3. A/B test different versions with your audience

**Pro Tip:** The selected creatives show strong {brand_info.get('product_category', 'product')} appeal. Consider testing them in different regions to see which performs best!
"""
    return suggestions

def main():
    """Main application function."""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🎨 AI Creative Studio</h1>
        <p class="subtitle">Transform your brand into hyper-personalized, context-aware ad creatives in under 60 seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Brand name (moved to top as it's most important)
        brand_name = st.text_input("🏷️ Brand Name", placeholder="Enter your brand name")
        
        # Product category
        categories = [
            "Beverage", "Skincare", "Fashion", "Food",
            "Technology", "Fitness", "Home", "Automotive", "Other"
        ]
        product_category = st.selectbox("📦 Product Category", categories)
        
        # Company description for better targeting
        with st.expander("📝 Company Description (Optional but Recommended)"):
            company_description = st.text_area(
                "Describe your company and target customers",
                placeholder="E.g., We sell premium organic beverages targeting health-conscious millennials in urban areas...",
                height=100
            )
        
        st.markdown("---")
        st.markdown("### 🎯 Target Audience Analysis")
        
        # Analyze audience button
        if brand_name and st.button("🔍 Analyze Target Audience"):
            with st.spinner("Analyzing target audience with AI..."):
                st.session_state.audience_insights = analyze_target_audience(
                    brand_name, product_category, company_description
                )
        
        # Display audience insights
        if st.session_state.audience_insights:
            insights = st.session_state.audience_insights
            st.success("✅ Audience Analysis Complete!")
            
            with st.expander("👥 View Audience Insights", expanded=True):
                st.markdown(f"**Age Group:** {insights.get('age_group', 'N/A')}")
                st.markdown(f"**Demographics:** {insights.get('demographics', 'N/A')}")
                st.markdown(f"**Key Insights:** {insights.get('insights', 'N/A')}")
                
                if 'recommended_cities' in insights:
                    st.markdown("**Recommended Cities:**")
                    for city in insights['recommended_cities']:
                        st.markdown(f"- {city}")
        
        st.markdown("---")
        st.markdown("### 📍 Location Targeting")
        
        # Hierarchical location selection
        country = st.selectbox("🌍 Select Country", list(LOCATION_DATA.keys()), index=0)
        
        regions = list(LOCATION_DATA[country].keys())
        region = st.selectbox("🗺️ Select Region", regions, index=0)
        
        cities = LOCATION_DATA[country][region]
        
        # If we have audience insights, highlight recommended cities
        if st.session_state.audience_insights and 'recommended_cities' in st.session_state.audience_insights:
            recommended = st.session_state.audience_insights['recommended_cities']
            # Filter recommended cities that are in the selected region
            available_recommended = [c for c in recommended if c in cities]
            if available_recommended:
                st.info(f"💡 AI recommends: {', '.join(available_recommended)}")
        
        city = st.selectbox("🏙️ Select City", cities, index=0)
        
        st.markdown("---")
        st.markdown("### 🎨 Creative Settings")
        
        # Number of creatives
        num_creatives = st.slider("🎯 Number of Creatives", min_value=1, max_value=15, value=3)
        
        # Tone selection
        tones = ["Engaging", "Professional", "Playful", "Inspirational", "Casual"]
        caption_tone = st.selectbox("💬 Caption Tone", tones)
        
        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        - ✅ AI-powered audience analysis
        - ✅ Location-aware context
        - ✅ Weather integration
        - ✅ Brand color extraction
        - ✅ Cultural personalization
        - ✅ Creative refinement options
        - ✅ ZIP package download
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        1. **Analyze audience first** for better targeting
        2. **Add company description** for smarter insights
        3. **Select recommended cities** from AI analysis
        4. **Review creative explanations** to understand choices
        5. **Select favorites** for refinement
        """)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Upload Brand Logo")
        logo_file = st.file_uploader(
            "Upload your brand logo (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            key="logo"
        )
        
        if logo_file:
            logo_image = Image.open(logo_file)
            st.image(logo_image, caption="Brand Logo", use_column_width=True)
    
    with col2:
        st.markdown("### 📸 Upload Product Image")
        product_file = st.file_uploader(
            "Upload your product image (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            key="product"
        )
        
        if product_file:
            product_image = Image.open(product_file)
            st.image(product_image, caption="Product Image", use_column_width=True)
    
    # Generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_button = st.button("🚀 Generate Creatives")
    
    # Generation process
    if generate_button:
        if not brand_name:
            st.error("⚠️ Please enter a brand name")
            return
        
        # Start generation
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎬 Generating Your Creatives...")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Initialize services
            status_text.text("🔧 Initializing AI services...")
            progress_bar.progress(10)
            
            context_engine = ContextEngine()
            brand_extractor = BrandExtractor()
            prompt_builder = PromptBuilder()
            caption_generator = CaptionGenerator()
            dalle_service = DalleService()
            
            time.sleep(0.5)
            
            # Step 2: Extract brand information
            status_text.text("🎨 Analyzing brand identity...")
            progress_bar.progress(20)
            
            logo_img = Image.open(logo_file) if logo_file else None
            product_img = Image.open(product_file) if product_file else None
            
            brand_info = brand_extractor.extract_brand_info(
                logo_image=logo_img,
                product_image=product_img,
                brand_name=brand_name,
                product_category=product_category
            )
            
            time.sleep(0.5)
            
            # Step 3: Get context
            status_text.text(f"🌍 Gathering context for {city}...")
            progress_bar.progress(30)
            
            base_context = context_engine.get_context(
                city=city,
                product_category=product_category
            )
            
            # Create variations
            context_variations = context_engine.create_context_variations(
                base_context,
                num_variations=num_creatives
            )
            
            time.sleep(0.5)
            
            # Step 4: Build prompts
            status_text.text("📝 Creating AI prompts...")
            progress_bar.progress(40)
            
            prompts = prompt_builder.build_multiple_prompts(
                brand_info=brand_info,
                context_variations=context_variations
            )
            
            time.sleep(0.5)
            
            # Step 5: Generate images
            status_text.text("🎨 Generating images with DALL-E...")
            progress_bar.progress(50)
            
            generated_images = []
            for idx, prompt in enumerate(prompts):
                progress = 50 + int((idx / len(prompts)) * 30)
                progress_bar.progress(progress)
                status_text.text(f"🎨 Generating image {idx + 1}/{len(prompts)}...")
                
                image = dalle_service.generate_image(prompt)
                if image:
                    # Add logo if provided
                    if logo_img:
                        image = create_composite(image, logo_img)
                    generated_images.append(image)
            
            # Step 6: Generate captions
            status_text.text("💬 Creating engaging captions...")
            progress_bar.progress(85)
            
            captions = caption_generator.generate_multiple_captions(
                brand_info=brand_info,
                context_variations=context_variations,
                tone=caption_tone.lower()
            )
            
            time.sleep(0.5)
            
            # Step 7: Save and package
            status_text.text("📦 Packaging your creatives...")
            progress_bar.progress(95)
            
            # Create output directory
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Save images
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
            
            # Store in session state (including context for explanations)
            st.session_state.generated_creatives = generated_images
            st.session_state.generated_captions = captions
            st.session_state.zip_path = zip_path
            st.session_state.context_variations = context_variations
            st.session_state.brand_info = brand_info
            
            progress_bar.progress(100)
            status_text.text("✅ Generation complete!")
            
            time.sleep(0.5)
            
            # Success message
            st.markdown(f"""
            <div class="success-box">
                🎉 Successfully generated {len(generated_images)} hyper-personalized creatives!
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")
            return
    
    # Display results
    if st.session_state.generated_creatives:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎨 Your Generated Creatives")
        
        # Download button
        if st.session_state.zip_path and os.path.exists(st.session_state.zip_path):
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download All Creatives (ZIP)",
                    data=f,
                    file_name=os.path.basename(st.session_state.zip_path),
                    mime="application/zip"
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Creative refinement section
        st.markdown("### 🎯 Select Creatives for Refinement")
        st.info("💡 Select your favorite creatives (3-4 recommended) to get refinement suggestions and understand the design choices.")
        
        # Selection checkboxes
        selected_creatives = []
        cols_select = st.columns(min(5, len(st.session_state.generated_creatives)))
        for idx in range(len(st.session_state.generated_creatives)):
            col_idx = idx % len(cols_select)
            with cols_select[col_idx]:
                if st.checkbox(f"Creative {idx + 1}", key=f"select_{idx}"):
                    selected_creatives.append(idx)
        
        # Show refinement suggestions if creatives are selected
        if selected_creatives:
            st.markdown("<br>", unsafe_allow_html=True)
            brand_info = st.session_state.get('brand_info', {})
            
            with st.expander("🎯 View Refinement Suggestions", expanded=True):
                st.markdown(get_refinement_suggestions(selected_creatives, brand_info))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display creatives in grid with explanations
        cols_per_row = 3
        for i in range(0, len(st.session_state.generated_creatives), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx < len(st.session_state.generated_creatives):
                    with cols[j]:
                        # Highlight if selected
                        if idx in selected_creatives:
                            st.markdown("⭐ **SELECTED**")
                        
                        st.image(
                            st.session_state.generated_creatives[idx],
                            caption=f"Creative {idx + 1}",
                            use_column_width=True
                        )
                        
                        # Caption
                        with st.expander("📝 View Caption"):
                            st.write(st.session_state.generated_captions[idx])
                        
                        # Design explanation
                        if 'context_variations' in st.session_state and 'brand_info' in st.session_state:
                            with st.expander("🎨 Design Rationale"):
                                context = st.session_state.context_variations[idx]
                                brand_info = st.session_state.brand_info
                                explanation = explain_creative_choices(brand_info, context, idx + 1)
                                st.markdown(explanation)

if __name__ == "__main__":
    main()

