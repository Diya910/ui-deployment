
# **The AI Creative Studio**

A **location-aware creative generation engine** that transforms a brand’s logo, product image, and contextual signals into **10+ hyper-personalized ad creatives** with AI-generated captions — all in under **60 seconds**.

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

* **Location intelligence**
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
* Hyperlocal mood signals (e.g., “Bangalore monsoon vibes”)

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

### **e. Image Generation (OpenAI / SDXL)**

Using:

* **OpenAI DALL·E** for cleaner ad-quality compositions
* **Stable Diffusion XL** for custom styles

Each prompt blends:

* Product image
* Logo
* Context data
* Brand palette enforcement
* POI & local culture theme

---

## **4. Expected Output**

Input:

* Brand logo
* Product image
* (Optional) Brand colors

Output ZIP contains:

```
/images          → all generated creatives  
/captions.txt    → caption set  
/metadata.json   → context signals per image  
```

---

## **5. Technical Architecture**

### **Core Layers**

1. **Upload Module (FastAPI)**
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
   * SDXL (local)
6. **Caption Generator**

   * Gemini 1.5 Pro
7. **Packaging**

   * Pillow
   * zipfile

---

## **6. Repository Structure**

```
ai-creative-studio/
│
├── app/
│   ├── api/
│   │   ├── upload.py
│   │   ├── generate.py
│   │   └── health.py
│   ├── core/
│   │   ├── context_engine.py
│   │   ├── brand_extractor.py
│   │   ├── prompt_builder.py
│   │   └── caption_generator.py
│   ├── services/
│   │   ├── dalle_service.py
│   │   ├── sdxl_service.py
│   │   └── weather_service.py
│   ├── utils/
│   │   ├── image_utils.py
│   │   ├── palette_utils.py
│   │   └── zip_utils.py
│   └── main.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## **7. How to Run**

### **1. Clone Repository**

```
git clone https://github.com/username/ai-creative-studio.git
cd ai-creative-studio
```

### **2. Add Keys**

```
export IMAGE_API_KEY="your_openai_key"
export TEXT_API_KEY="your_gemini_key"
export WEATHER_API_KEY="your_weather_key"
```

### **3. Build & Run**

```
docker-compose up --build
```

### **4. Test**

Visit:

```
http://localhost:8000
```

Upload logo + product image.

---

## **8. Why I Picked This Problem**

This challenge aligns perfectly with my interest in **Generative AI applied to AdTech**.
GroundTruth’s strength lies in mobility and location intelligence — and I wanted to extend that to creative production.

Instead of making yet another design generator, I built something that creates **context-intelligent, culturally aligned, brand-safe ad creatives** at scale.

---

## **9. Future Enhancements**

* Automatic festival-based creative sets
* Category-aware design templates
* Multilingual captioning
* Brand font detection & typography matching
* Batch mode (100+ creatives)
* Footfall-likelihood scoring
* “Campaign-ready pack” with multiple banner sizes
