#!/bin/bash
# EC2 Dashboard Update Script
# Run this on EC2 to pull latest changes and restart dashboard

set -e  # Exit on error

echo "🔄 Updating Ashoka Dashboard on EC2..."
echo ""

# Navigate to project directory
cd ~/aws_hackathon_ai_4_bharat

# Stop running dashboard
echo "⏹️  Stopping dashboard..."
pkill -f run_dashboard.py || true
sleep 2

# Pull latest changes
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check for STORAGE_SECRET
if ! grep -q "STORAGE_SECRET" .env; then
    echo "🔐 Adding STORAGE_SECRET to .env..."
    echo "STORAGE_SECRET=$(openssl rand -hex 32)" >> .env
fi

# Start dashboard in screen
echo "🚀 Starting dashboard in screen session..."
screen -dmS ashoka bash -c 'source venv/bin/activate && python run_dashboard.py'

# Wait a moment for startup
sleep 3

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

# Verify it's running
if ps aux | grep -q "[r]un_dashboard.py"; then
    echo ""
    echo "✅ Dashboard updated and running!"
    echo "📊 Access at: http://$PUBLIC_IP:8080"
    echo ""
    echo "To view logs: screen -r ashoka"
    echo "To detach from logs: Ctrl+A then D"
else
    echo ""
    echo "❌ Dashboard failed to start!"
    echo "Check logs: screen -r ashoka"
fi
