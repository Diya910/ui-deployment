# 🚀 Run Instructions - AI Creative Studio

Complete guide to running the AI Creative Studio application.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running Options](#running-options)
4. [API Keys Configuration](#api-keys-configuration)
5. [Using the Application](#using-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## 🔧 Prerequisites

### Required Software

- **Python 3.8 or higher**
  - Check: `python3 --version`
  - Install from: https://www.python.org/downloads/

- **pip** (Python package manager)
  - Usually comes with Python
  - Check: `pip --version`

### Optional (for Docker)

- **Docker** and **Docker Compose**
  - Install from: https://www.docker.com/get-started

---

## ⚙️ Initial Setup

### Step 1: Clone or Navigate to Project

```bash
cd /path/to/ai_hackathon
```

### Step 2: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 3: Add Your API Keys

Edit the `.env` file and add your API keys:

```env
# Required Keys
IMAGE_API_KEY=sk-your-openai-api-key-here
TEXT_API_KEY=your-google-gemini-api-key-here

# Optional Keys
WEATHER_API_KEY=your-openweathermap-api-key-here
```

**Where to get API keys:**

1. **OpenAI (DALL-E)**: https://platform.openai.com/api-keys
2. **Google Gemini**: https://makersuite.google.com/app/apikey
3. **OpenWeatherMap** (optional): https://openweathermap.org/api

---

## 🎯 Running Options

### Option 1: Interactive Script (Recommended)

The easiest way to run the application:

```bash
# Make script executable (first time only)
chmod +x run.sh

# Run the interactive script
./run.sh
```

The script will present you with options:
1. **Streamlit** - Beautiful UI (Recommended)
2. **FastAPI** - API Server
3. **Docker** - Containerized deployment
4. **Setup only** - Just install dependencies

### Option 2: Manual Streamlit (Beautiful UI)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

**Access at:** http://localhost:8501

### Option 3: Manual FastAPI (API Server)

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Option 4: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

**Access at:** http://localhost:8000

### Option 5: Demo Script (Testing)

Run a programmatic demo without UI:

```bash
# Activate virtual environment
source venv/bin/activate

# Run demo
python demo.py
```

This will generate sample creatives and save them to the `output/` directory.

---

## 🔑 API Keys Configuration

### Required Keys (Only 2!)

#### 1. OpenAI API Key (IMAGE_API_KEY)

**Purpose:** Generate images using DALL-E 3

**How to get:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to `.env`: `IMAGE_API_KEY=sk-your-key-here`

**Cost:** Pay-per-use (~$0.04 per 1024x1024 image)

#### 2. Google Gemini API Key (TEXT_API_KEY)

**Purpose:** Generate captions and analyze target audience

**How to get:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`: `TEXT_API_KEY=your-key-here`

**Cost:** Free tier available (generous limits)

---

### ❌ NOT Required: Weather API

**Important:** You do **NOT** need a weather API key!

**Why?** The app automatically determines weather based on the target city you select:
- **Location-Based Weather**: Uses the city you choose for your ad campaign
- **Season-Aware**: Adjusts weather based on current season
- **Realistic Data**: Provides accurate weather patterns for each location
- **No API Needed**: Works perfectly without any weather API key

**Example:**
- Select "Bangalore" → Gets Bangalore's typical weather for current season
- Select "Mumbai" → Gets Mumbai's typical weather (monsoon, humidity, etc.)
- Select "New York" → Gets New York's weather (cold winters, hot summers)

**Optional:** If you want **real-time** weather data instead of location-based patterns, you can add:

```env
WEATHER_API_KEY=your_openweathermap_key_here
```

But this is **completely optional**! The app works great without it.

---

### Summary: What You Actually Need

```env
# REQUIRED (2 keys only)
IMAGE_API_KEY=sk-your-openai-key-here
TEXT_API_KEY=your-gemini-key-here

# OPTIONAL (app works perfectly without these)
# WEATHER_API_KEY=your-weather-key-here  # Not needed!
```

That's it! Just 2 API keys and you're ready to go.

---

## 📱 Using the Application

### Streamlit UI Workflow

1. **Start the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Configure in Sidebar**
   - Enter brand name
   - Select product category
   - (Optional) Add company description
   - Click "Analyze Target Audience"

3. **Review Audience Insights**
   - Check AI-recommended cities
   - Review demographics and age groups
   - Understand target audience behavior

4. **Select Location**
   - Choose country
   - Select region
   - Pick city (AI recommendations highlighted)

5. **Upload Assets**
   - Upload brand logo (optional)
   - Upload product image (optional)

6. **Generate Creatives**
   - Click "Generate Creatives"
   - Wait 30-60 seconds
   - Review generated creatives

7. **Analyze Results**
   - View each creative
   - Read captions
   - Check design rationale
   - Select favorites (3-4 recommended)

8. **Get Refinement Suggestions**
   - Select creatives using checkboxes
   - View refinement suggestions
   - Understand design choices

9. **Download**
   - Click "Download All Creatives (ZIP)"
   - Extract ZIP to view all files

### FastAPI Usage

#### Using cURL:

```bash
curl -X POST "http://localhost:8000/generate" \
  -F "brand_name=MyBrand" \
  -F "product_category=Beverage" \
  -F "city=Bangalore" \
  -F "num_creatives=10" \
  -F "caption_tone=engaging" \
  -F "logo=@/path/to/logo.png" \
  -F "product_image=@/path/to/product.png" \
  --output creatives.zip
```

#### Using Python:

```python
import requests

url = "http://localhost:8000/generate"

files = {
    'logo': open('logo.png', 'rb'),
    'product_image': open('product.png', 'rb')
}

data = {
    'brand_name': 'MyBrand',
    'product_category': 'Beverage',
    'city': 'Bangalore',
    'num_creatives': 10,
    'caption_tone': 'engaging'
}

response = requests.post(url, files=files, data=data)

with open('creatives.zip', 'wb') as f:
    f.write(response.content)
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" Error

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. "No valid API key found"

**Solution:**
- Check `.env` file exists in project root
- Verify API keys are correctly formatted
- Restart the application after adding keys

#### 3. "Port already in use"

**For Streamlit:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**For FastAPI:**
```bash
uvicorn app.main:app --port 8001
```

#### 4. Images Not Generating

**Possible causes:**
- Invalid OpenAI API key
- Insufficient API credits
- Network issues

**Solution:**
- Verify API key is valid
- Check OpenAI account credits
- App will use placeholder images if API fails

#### 5. Slow Generation

**Normal behavior:**
- 5 creatives: ~30 seconds
- 10 creatives: ~60 seconds
- 15 creatives: ~90 seconds

**To speed up:**
- Reduce number of creatives
- Use faster internet connection
- Consider caching (advanced)

#### 6. Audience Analysis Not Working

**Possible causes:**
- Invalid Gemini API key
- Network issues

**Solution:**
- Verify Gemini API key
- App will use fallback analysis if API fails

---

## 🎓 Advanced Usage

### Custom Configuration

Edit `.env` for custom settings:

```env
# Image settings
IMAGE_SIZE=1024x1024
IMAGE_QUALITY=hd
MAX_CREATIVES=15

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### Running in Production

#### Using Streamlit Cloud:

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Deploy from repository
4. Add secrets in Streamlit Cloud dashboard

#### Using Docker in Production:

```bash
# Build production image
docker build -t ai-creative-studio:prod .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  -e IMAGE_API_KEY=$IMAGE_API_KEY \
  -e TEXT_API_KEY=$TEXT_API_KEY \
  --name creative-studio \
  ai-creative-studio:prod
```

### Batch Processing

For generating creatives for multiple brands:

```python
# Create a script: batch_generate.py
from demo import main as generate_creatives

brands = [
    {"name": "Brand1", "category": "Beverage", "city": "Bangalore"},
    {"name": "Brand2", "category": "Skincare", "city": "Mumbai"},
    # Add more brands
]

for brand in brands:
    generate_creatives(**brand)
```

### Performance Optimization

#### Enable Caching:

Add to your code:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_context(city):
    return context_engine.get_context(city)
```

#### Parallel Generation:

Use `concurrent.futures` for faster generation:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    images = list(executor.map(dalle_service.generate_image, prompts))
```

---

## 📊 Output Structure

After generation, you'll get:

```
output/
├── brand_name_creatives.zip
│   ├── images/
│   │   ├── creative_01.png
│   │   ├── creative_02.png
│   │   └── ...
│   ├── captions.txt
│   ├── metadata.json
│   └── README.md
└── individual image files
```

---

## 🆘 Getting Help

### Check Logs

**Streamlit:**
- Logs appear in terminal where you ran the command

**FastAPI:**
```bash
# View logs
tail -f logs/app.log
```

**Docker:**
```bash
docker-compose logs -f
```

### Debug Mode

Run in debug mode for more information:

```bash
# Set in .env
DEBUG=True

# Or run with debug flag
streamlit run streamlit_app.py --logger.level=debug
```

### Common Questions

**Q: Can I run without API keys?**
A: Yes, but with limited functionality. The app will use placeholder images and fallback captions.

**Q: How much do API calls cost?**
A: 
- OpenAI DALL-E: ~$0.04 per image (1024x1024)
- Google Gemini: Free tier available
- OpenWeatherMap: Free tier available

**Q: Can I use my own images instead of AI generation?**
A: Yes, modify the code to skip DALL-E and use your own images.

**Q: How do I add more cities?**
A: Edit `LOCATION_DATA` in `streamlit_app.py`

---

## 📞 Support

For issues:
1. Check this guide
2. Review error messages
3. Check GitHub issues
4. Create new issue with details

---

**Happy Creating! 🎨**

Last updated: 2025-12-03
