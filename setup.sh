#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "  agencIA — Setup"
echo "========================================="
echo

# Check Python
if command -v python3 &>/dev/null; then
    PY=$(python3 --version)
    echo -e "${GREEN}[OK]${NC} $PY"
elif command -v python &>/dev/null; then
    PY=$(python --version)
    echo -e "${GREEN}[OK]${NC} $PY"
else
    echo -e "${RED}[!]${NC} Python not found."
    echo
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing Python 3 via apt..."
        sudo apt update && sudo apt install -y python3 python3-pip python3-venv
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing Python 3 via Homebrew..."
        brew install python@3.12
    else
        echo "Please install Python 3.12+ from https://www.python.org/downloads/"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} $(python3 --version)"
fi

echo

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
else
    echo -e "${GREEN}[OK]${NC} Virtual environment exists"
fi

# Activate venv
source venv/bin/activate
echo -e "${GREEN}[OK]${NC} Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}[OK]${NC} Dependencies installed"

echo

# Check .env
if [ -f ".env" ]; then
    if grep -q "your-api-key-here" .env; then
        echo -e "${YELLOW}[!]${NC} .env exists but API key is still the placeholder."
        echo "    Edit .env and replace 'your-api-key-here' with your actual key."
    else
        echo -e "${GREEN}[OK]${NC} .env configured"
    fi
else
    cp .env.example .env
    echo -e "${YELLOW}[!]${NC} Created .env from .env.example"
    echo "    Edit .env and add your Google Places API key."
fi

echo
echo "========================================="
echo -e "  ${GREEN}Setup complete!${NC}"
echo "========================================="
echo
echo "Next steps:"
echo "  1. Edit .env with your GOOGLE_PLACES_API_KEY"
echo "  2. Activate the venv:  source venv/bin/activate"
echo "  3. Use /sales-finding-leads in Claude Code"
echo
