
# **The AI Creative Studio** 🎨

A **location-aware creative generation engine** that transforms a brand's logo, product image, and contextual signals into **10+ hyper-personalized ad creatives** with AI-generated captions — all in under **60 seconds**.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## **✨ Features**

- 🤖 **AI-Powered Audience Analysis** - LLM analyzes your brand to identify target demographics and recommend best cities
- 🌍 **Hierarchical Location Selection** - Country → Region → City for precise targeting
- 🎨 **Brand Color Extraction** - Automatic brand palette detection and enforcement
- 🖼️ **AI Image Generation** - DALL-E 3 for professional ad-quality creatives
- 💬 **Smart Caption Generation** - Gemini 2-5 Flash for context-aware, engaging captions
- 🌤️ **Weather Integration** - Real-time weather data for contextual relevance
- 🎭 **Cultural Personalization** - Festival-aware, region-specific content
- 🎯 **Creative Refinement** - Select favorites and get AI-powered refinement suggestions
- 📊 **Design Rationale** - Understand why each creative works (colors, positioning, context)
- 📦 **One-Click Download** - All creatives packaged in a ZIP with metadata
- 💎 **Beautiful UI** - Modern, gradient-based Streamlit interface
- 🐳 **Multiple Deployment Options** - Streamlit, FastAPI, or Docker

---

## **1. Problem Overview**

Marketing teams spend days producing minor variations of the same creative for different **regions**, **weather conditions**, **seasons**, and **audience segments**.
This repetitive workflow — changing backgrounds, colors, themes, and localized text — is slow and not scalable. As a result, brands miss contextual opportunities like:

* A monsoon-themed beverage ad for Bangalore
* A sunny-day skincare creative for Chennai
* A mall-footfall weekend ad for Gurgaon

Traditional tools generate *pretty images*, but not *contextually relevant ad creatives*.

---

## **2. My Solution**

**The AI Creative Studio** automatically generates a full set of hyperlocal, context-driven creatives using:

* **Location intelligence for targeted audience**
* **Weather & time signals**
* **Nearby POIs & local culture themes**
* **Brand color extraction + guided brand consistency prompts**
* **Text + visuals fused into creative metadata**

### **What the user gets (inside a ZIP):**

* 10+ high-resolution creatives
* Brand-aligned, context-aware captions
* Metadata showing which context influenced each creative

All generated in under a minute.

---

## **3. What Makes It Innovative**

### **a. Context Engine Inspired by GroundTruth**

Each creative uses:

* Current weather
* Temperature & time-of-day
* Seasonality
* POIs within radius
* City-specific culture or festivals
* Hyperlocal mood signals (e.g., "Bangalore monsoon vibes")

### **b. Brand Intelligence Layer**

I extract:

* Brand colors
* Logo palette
* Product category

…and enforce them inside prompts using:

* Structured prompt templates
* Palette-aware image conditioning
* Hard logo placement instructions

### **c. Local Culture Personalization**

Using LLM extraction + (future) web-scraping, the system can incorporate:

* Region-specific preferences
* Local shopping behavior
* Festival season (Diwali, Pongal, Durga Puja, Onam)
* City vibes (e.g., Chennai coastal, Delhi nightlife, Bangalore café culture)

This makes each creative not just visually correct, but *culturally relevant*.

### **d. Caption Engine (Gemini for Text)**

Captions are generated using:

* Tone consistency
* Regionally relevant vocabulary
* Weather/time references
* Category-specific CTAs

With quality checks for:

* Length
* Hallucination-free claims
* Brand-safe language

### **e. Image Generation (OpenAI DALL-E)**

Using:

* **OpenAI DALL·E 3** for cleaner ad-quality compositions
* **Stable Diffusion XL** support (placeholder for future integration)

Each prompt blends:

* Product image
* Logo
* Context data
* Brand palette enforcement
* POI & local culture theme

---

## **4. Smart Targeting & Refinement**

### **a. AI-Powered Audience Analysis**

Before generating creatives, the system can analyze your brand using LLM to:

* **Identify target demographics** - Age groups, income levels, lifestyle preferences
* **Recommend best cities** - Based on product category and brand positioning
* **Understand customer behavior** - Shopping patterns, preferences, cultural alignment
* **Suggest optimal regions** - Country → Region → City hierarchy for precise targeting

**How it works:**
1. Enter brand name and product category
2. (Optional) Add company description for better insights
3. Click "Analyze Target Audience"
4. Review AI recommendations
5. Select from recommended cities

**Example Output:**
```json
{
  "age_group": "25-35 years",
  "demographics": "Urban millennials, health-conscious, tech-savvy",
  "insights": "Target audience values premium quality and sustainability",
  "recommended_cities": ["Bangalore", "Mumbai", "Pune"]
}
```

### **b. Hierarchical Location Targeting**

Instead of a flat city list, the app now uses:

**Country → Region → City**

This allows for:
* Better geographic organization
* Regional cultural understanding
* Scalability to multiple countries
* AI recommendations within selected region

**Supported Locations:**
- **India**: South, North, West, East, Central regions
- **United States**: West Coast, East Coast, Midwest, South
- **United Kingdom**: England, Scotland, Wales, Northern Ireland

**Future Scope:**
- Web scraping to analyze actual customer distribution
- Integration with Google Analytics for real customer data
- Footfall data integration for location-based insights
- Social media sentiment analysis by region

### **c. Creative Refinement & Explanation**

After generation, users can:

**1. View Design Rationale** for each creative:
- Color palette choices and reasoning
- Logo positioning strategy
- Context integration explanation
- Why specific elements were chosen
- Suggested use cases

**2. Select Favorites** (3-4 recommended):
- Checkbox selection for each creative
- Visual highlighting of selected creatives
- Batch analysis of selected set

**3. Get Refinement Suggestions**:
- Color adjustment recommendations
- Composition change ideas
- Context variation options
- Style modification suggestions
- A/B testing guidance

**Example Explanation:**
```
Creative #3 - Design Rationale

Color Palette:
- Primary Brand Color: #667eea
- Reasoning: Extracted from logo for brand consistency

Positioning & Layout:
- Logo: Top-right for visibility without overwhelming
- Style: Energetic morning theme

Context Integration:
- Location: Bangalore
- Weather: Pleasant at 24°C
- Theme: Morning energy

Why This Works:
- Aligns with Bangalore café culture
- Perfect for morning social media posts
- Brand colors ensure recognition
```

---

## **17. Expected Output**

Input:

* Brand logo
* Product image
* (Optional) Brand colors

Output ZIP contains:

```
/images          → all generated creatives  
/captions.txt    → caption set  
/metadata.json   → context signals per image
/README.md       → package information
```

---

## **17. Technical Architecture**

### **Core Layers**

1. **Upload Module (Streamlit/FastAPI)**
2. **Context Enrichment Engine**
   * Weather API
   * Geolocation API
   * POI API
   * Time/Season logic
3. **Brand Intelligence Extractor**
   * LLM-based color/theme extraction
   * (Future) Web scraping for brand tone & campaigns
4. **Prompt Builder**
   * Adaptive prompt templates
   * Logo placement instructions
   * Palette conditioning
5. **Image Generator**
   * DALL·E 3 (OpenAI)
   * SDXL (placeholder)
6. **Caption Generator**
   * Gemini 1.5 Pro
7. **Packaging**
   * Pillow
   * zipfile

---

## **17. Repository Structure**

```
ai-creative-studio/
│
├── app/
│   ├── api/                    # API endpoints (future)
│   ├── core/
│   │   ├── context_engine.py   # Context gathering
│   │   ├── brand_extractor.py  # Brand intelligence
│   │   ├── prompt_builder.py   # Prompt generation
│   │   └── caption_generator.py # Caption creation
│   ├── services/
│   │   ├── dalle_service.py    # DALL-E integration
│   │   ├── sdxl_service.py     # SDXL placeholder
│   │   └── weather_service.py  # Weather API
│   ├── utils/
│   │   ├── image_utils.py      # Image processing
│   │   ├── palette_utils.py    # Color extraction
│   │   └── zip_utils.py        # Package creation
│   └── main.py                 # FastAPI app
│
├── streamlit_app.py            # Streamlit UI
├── run.sh                      # Interactive run script
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## **17. How to Run**

### **Quick Start (Recommended)**

```bash
# 1. Clone repository
git clone https://github.com/username/ai-creative-studio.git
cd ai-creative-studio

# 2. Copy environment file and add your API keys
cp .env.example .env
# Edit .env and add your keys:
# - IMAGE_API_KEY (OpenAI)
# - TEXT_API_KEY (Google Gemini)
# - WEATHER_API_KEY (OpenWeatherMap)

# 3. Run the interactive script
chmod +x run.sh
./run.sh
```

The script will guide you through:
- **Option 1**: Streamlit (Beautiful UI) - **Recommended**
- **Option 2**: FastAPI (API Server)
- **Option 3**: Docker (Containerized)
- **Option 4**: Setup only

### **Manual Setup**

#### **A. Streamlit (Beautiful UI)**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run streamlit_app.py
```

Visit: `http://localhost:8501`

#### **B. FastAPI (API Server)**

```bash
# Activate virtual environment
source venv/bin/activate

# Run FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

#### **C. Docker**

```bash
# Build and run with Docker Compose
docker-compose up --build
```

Visit: `http://localhost:8000`

---

## **17. API Keys Setup**

You need the following API keys:

### **Required:**

1. **OpenAI API Key** (for DALL-E 3)
   - Get it from: https://platform.openai.com/api-keys
   - Add to `.env` as `IMAGE_API_KEY`

2. **Google Gemini API Key** (for captions)
   - Get it from: https://makersuite.google.com/app/apikey
   - Add to `.env` as `TEXT_API_KEY`

### **Optional:**

3. **OpenWeatherMap API Key** (for weather data)
   - Get it from: https://openweathermap.org/api
   - Add to `.env` as `WEATHER_API_KEY`
   - *Note: App works with mock weather data if not provided*

### **Example .env file:**

```env
IMAGE_API_KEY=sk-your-openai-key-here
TEXT_API_KEY=your-gemini-key-here
WEATHER_API_KEY=your-weather-key-here
```

---

## **17. Usage Guide**

### **Streamlit UI:**

1. **Select Configuration:**
   - Choose city (Bangalore, Chennai, Mumbai, etc.)
   - Set number of creatives (1-15)
   - Select product category
   - Enter brand name
   - Choose caption tone

2. **Upload Assets:**
   - Upload brand logo (optional)
   - Upload product image (optional)

3. **Generate:**
   - Click "Generate Creatives"
   - Wait ~30-60 seconds
   - Download ZIP package

### **API Usage:**

```bash
curl -X POST "http://localhost:8000/generate" \
  -F "brand_name=MyBrand" \
  -F "product_category=Beverage" \
  -F "city=Bangalore" \
  -F "num_creatives=10" \
  -F "caption_tone=engaging" \
  -F "logo=@logo.png" \
  -F "product_image=@product.png" \
  --output creatives.zip
```

---

## **17. Screenshots**

### **Streamlit UI**
Beautiful gradient interface with modern design:
- 🎨 Drag-and-drop file uploads
- 📊 Real-time progress tracking
- 🖼️ Interactive creative gallery
- 📥 One-click ZIP download

---

## **17. Why I Picked This Problem**

This challenge aligns perfectly with my interest in **Generative AI applied to AdTech**.
GroundTruth's strength lies in mobility and location intelligence — and I wanted to extend that to creative production.

Instead of making yet another design generator, I built something that creates **context-intelligent, culturally aligned, brand-safe ad creatives** at scale.

---

## **17. Future Enhancements**

* ✅ Automatic festival-based creative sets
* ✅ Category-aware design templates
* ✅ Multilingual captioning
* ✅ Brand font detection & typography matching
* ✅ Batch mode (100+ creatives)
* ✅ Footfall-likelihood scoring
* ✅ "Campaign-ready pack" with multiple banner sizes
* ✅ A/B testing recommendations
* ✅ Performance analytics integration
* ✅ Real-time POI data integration

---

## **17. Tech Stack**

- **Frontend**: Streamlit (Beautiful gradient UI)
- **Backend**: FastAPI
- **AI/ML**: 
  - OpenAI DALL-E 3 (Image generation)
  - Google Gemini 1.5 Pro (Caption generation)
- **Image Processing**: Pillow, OpenCV
- **Color Extraction**: ColorThief, scikit-learn
- **Weather**: OpenWeatherMap API
- **Deployment**: Docker, Docker Compose

---

## **17. Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

---

## **17. License**

MIT License - feel free to use this project for your own purposes.

---

## **17. Contact**

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for GroundTruth AI Hackathon**

