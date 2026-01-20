#!/bin/bash
# Frontend Quick Start Script

echo "🚀 Setting up LettaXRAG Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✓ Dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "To start the development server, run:"
echo "  npm run dev"
