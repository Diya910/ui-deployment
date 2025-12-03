#!/bin/bash

# AI Creative Studio - Run Script
# This script helps you run the application in different modes

echo "🎨 AI Creative Studio - Setup & Run"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please add your API keys before running."
    echo ""
fi

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    echo "✅ Python 3 found: $(python3 --version)"
}

# Function to create virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
        echo "✅ Virtual environment created"
    else
        echo "✅ Virtual environment already exists"
    fi
}

# Function to install dependencies
install_deps() {
    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
}

# Function to run Streamlit
run_streamlit() {
    echo ""
    echo "🚀 Starting Streamlit application..."
    echo "📍 URL: http://localhost:8501"
    echo ""
    source venv/bin/activate
    streamlit run streamlit_app.py
}

# Function to run FastAPI
run_fastapi() {
    echo ""
    echo "🚀 Starting FastAPI server..."
    echo "📍 URL: http://localhost:8000"
    echo "📍 Docs: http://localhost:8000/docs"
    echo ""
    source venv/bin/activate
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to run with Docker
run_docker() {
    echo ""
    echo "🐳 Starting with Docker..."
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    docker-compose up --build
}

# Main menu
echo "Select run mode:"
echo "1) Streamlit (Recommended - Beautiful UI)"
echo "2) FastAPI (API Server)"
echo "3) Docker (Containerized)"
echo "4) Setup only (Install dependencies)"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        check_python
        setup_venv
        install_deps
        run_streamlit
        ;;
    2)
        check_python
        setup_venv
        install_deps
        run_fastapi
        ;;
    3)
        run_docker
        ;;
    4)
        check_python
        setup_venv
        install_deps
        echo "✅ Setup complete!"
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
