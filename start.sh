#!/bin/bash

echo "🛡️  Ashoka Platform - Startup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create data directory
echo "Creating data directory..."
mkdir -p data
echo "✓ Data directory ready"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file exists"
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo ""

# Run tests
echo "Running setup tests..."
python test_setup.py
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "🚀 Launching dashboard..."
    echo "======================================"
    echo ""
    python run_dashboard.py
else
    echo "✗ Setup tests failed"
    exit 1
fi
