#!/bin/bash
# Backend Setup Script

echo "🚀 Setting up LettaXRAG Backend..."

# Check if Python 3.9+ is available
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your API keys to .env"
echo "3. Start MongoDB"
echo "4. Run: python main.py"
