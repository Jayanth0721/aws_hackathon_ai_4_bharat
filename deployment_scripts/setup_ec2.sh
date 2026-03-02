#!/bin/bash
# EC2 Setup Script for Ashoka Platform
# Run this script on your EC2 instance after SSH connection

set -e  # Exit on error

echo "=========================================="
echo "Ashoka Platform - EC2 Setup Script"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
echo "Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y git nginx supervisor postgresql-client unzip curl

# Install AWS CLI
echo "Installing AWS CLI..."
if ! command -v aws &> /dev/null; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
fi

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /opt/ashoka
sudo chown ubuntu:ubuntu /opt/ashoka

# Create log directory
echo "Creating log directory..."
sudo mkdir -p /var/log/ashoka
sudo chown ubuntu:ubuntu /var/log/ashoka

echo "=========================================="
echo "Basic setup complete!"
echo ""
echo "Next steps:"
echo "1. Upload your application code to /opt/ashoka"
echo "2. Configure AWS credentials: aws configure"
echo "3. Create .env file with your configuration"
echo "4. Run: cd /opt/ashoka && python3.11 -m venv venv"
echo "5. Run: source venv/bin/activate && pip install -r requirements.txt"
echo "=========================================="
