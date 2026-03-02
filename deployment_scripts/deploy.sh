#!/bin/bash
# Deployment script for Ashoka Platform
# Run this from your local machine to deploy to EC2

set -e

# Configuration
EC2_USER="ubuntu"
EC2_HOST=""  # Set your EC2 public IP or hostname
KEY_FILE=""  # Set path to your .pem key file
APP_DIR="/opt/ashoka"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if configuration is set
if [ -z "$EC2_HOST" ] || [ -z "$KEY_FILE" ]; then
    echo -e "${RED}Error: Please set EC2_HOST and KEY_FILE in this script${NC}"
    echo "Edit this file and set:"
    echo "  EC2_HOST=\"your-ec2-public-ip\""
    echo "  KEY_FILE=\"path/to/your-key.pem\""
    exit 1
fi

echo -e "${GREEN}=========================================="
echo "Ashoka Platform - Deployment Script"
echo "==========================================${NC}"

# Step 1: Create deployment package
echo -e "${YELLOW}Step 1: Creating deployment package...${NC}"
tar -czf ashoka-deploy.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='data/*.duckdb' \
    --exclude='.env' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    .

echo -e "${GREEN}✓ Deployment package created${NC}"

# Step 2: Upload to EC2
echo -e "${YELLOW}Step 2: Uploading to EC2...${NC}"
scp -i "$KEY_FILE" ashoka-deploy.tar.gz "$EC2_USER@$EC2_HOST:/tmp/"
echo -e "${GREEN}✓ Upload complete${NC}"

# Step 3: Extract and setup on EC2
echo -e "${YELLOW}Step 3: Extracting and setting up on EC2...${NC}"
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_HOST" << 'ENDSSH'
    set -e
    
    # Extract
    cd /opt/ashoka
    tar -xzf /tmp/ashoka-deploy.tar.gz
    rm /tmp/ashoka-deploy.tar.gz
    
    # Install/update dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "Deployment extracted and dependencies updated"
ENDSSH

echo -e "${GREEN}✓ Setup complete${NC}"

# Step 4: Restart application
echo -e "${YELLOW}Step 4: Restarting application...${NC}"
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_HOST" << 'ENDSSH'
    sudo supervisorctl restart ashoka
    sleep 3
    sudo supervisorctl status ashoka
ENDSSH

echo -e "${GREEN}✓ Application restarted${NC}"

# Cleanup
rm ashoka-deploy.tar.gz

echo -e "${GREEN}=========================================="
echo "Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Access your application at: http://$EC2_HOST"
echo ""
echo "To view logs:"
echo "  ssh -i $KEY_FILE $EC2_USER@$EC2_HOST 'sudo tail -f /var/log/ashoka/app.log'"
