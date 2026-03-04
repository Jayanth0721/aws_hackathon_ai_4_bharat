#!/bin/bash

echo "🛡️  Ashoka Platform - Startup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Check and install FFmpeg
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n 1 | awk '{print $3}')
    echo "✓ FFmpeg $ffmpeg_version detected"
else
    echo "⚠️  FFmpeg not found. Installing..."
    
    # Detect OS and install FFmpeg
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "Installing FFmpeg using apt..."
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            echo "Installing FFmpeg using yum..."
            sudo yum install -y ffmpeg
        elif command -v dnf &> /dev/null; then
            echo "Installing FFmpeg using dnf..."
            sudo dnf install -y ffmpeg
        else
            echo "✗ Could not detect package manager. Please install FFmpeg manually:"
            echo "  Ubuntu/Debian: sudo apt install ffmpeg"
            echo "  CentOS/RHEL: sudo yum install ffmpeg"
            echo "  Fedora: sudo dnf install ffmpeg"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "Installing FFmpeg using Homebrew..."
            brew install ffmpeg
        else
            echo "✗ Homebrew not found. Please install FFmpeg manually:"
            echo "  Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "  Then run: brew install ffmpeg"
            exit 1
        fi
    else
        echo "✗ Unsupported OS. Please install FFmpeg manually."
        exit 1
    fi
    
    # Verify installation
    if command -v ffmpeg &> /dev/null; then
        echo "✓ FFmpeg installed successfully"
    else
        echo "✗ FFmpeg installation failed"
        exit 1
    fi
fi
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
    echo "⚠️  Please edit .env and add your GOOGLE_API_KEY"
else
    echo "✓ .env file exists"
fi
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo ""

# Run tests (if test_setup.py exists)
if [ -f test_setup.py ]; then
    echo "Running setup tests..."
    python test_setup.py
    if [ $? -ne 0 ]; then
        echo "✗ Setup tests failed"
        exit 1
    fi
    echo ""
fi

echo "======================================"
echo "🚀 Launching dashboard..."
echo "======================================"
echo ""
python run_dashboard.py
