# Ashoka Platform - Production Hosting Guide

> **Complete guide for hosting Ashoka on AWS EC2 with custom domain and HTTPS**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [EC2 Instance Setup](#ec2-instance-setup)
3. [Application Deployment](#application-deployment)
4. [HTTP Access Setup](#http-access-setup)
5. [Custom Domain Configuration](#custom-domain-configuration)
6. [HTTPS/SSL Setup](#httpsssl-setup)
7. [Process Management](#process-management)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Resources
- AWS EC2 instance (t2.medium or larger recommended)
- Ubuntu 20.04 LTS or newer
- Domain name: `ashoka-ai.hopto.org` (No-IP free domain)
- SSH access to EC2 instance

### Security Group Configuration
Ensure your EC2 security group allows:
- Port 22 (SSH)
- Port 80 (HTTP)
- Port 443 (HTTPS)
- Port 8080 (Application - for testing only)

---

## EC2 Instance Setup

### 1. Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2. Update System Packages

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### 3. Install Required Dependencies

```bash
# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Install FFmpeg (required for audio/video processing)
sudo apt-get install -y ffmpeg

# Install Nginx
sudo apt-get install -y nginx

# Install Supervisor (for process management)
sudo apt-get install -y supervisor

# Install Certbot (for SSL certificates)
sudo apt-get install -y certbot python3-certbot-nginx
```

---

## Application Deployment

### 1. Clone Repository

```bash
cd /home/ubuntu
git clone https://github.com/Jayanth0721/aws_hackathon_ai_4_bharat.git ashoka
cd ashoka
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit environment file
nano .env
```

Add your configuration:
```bash
# AI Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
USE_GEMINI=true

# Database Configuration
USE_REAL_DYNAMODB=false
DUCKDB_PATH=data/ashoka.duckdb

# Session Configuration
SESSION_TIMEOUT_MINUTES=30
STORAGE_SECRET=your_secure_random_string_here
```

### 4. Initialize Database

```bash
python3 run_dashboard.py
# Press Ctrl+C after database initialization completes
```

---

## HTTP Access Setup

### 1. Configure Nginx for HTTP

Clear the default Nginx configuration:
```bash
sudo sh -c 'echo -n > /etc/nginx/sites-available/default'
```

Open the Nginx config file:
```bash
sudo nano /etc/nginx/sites-available/default
```

Paste the following configuration:
```nginx
# WebSocket upgrade configuration
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

# Backend server (Ashoka runs on port 8080)
upstream ashoka_backend {
    server 127.0.0.1:8080;
    keepalive 64;
}

# HTTP server
server {
    listen 80;
    server_name _;

    # Increase timeouts for long-running operations
    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;

    location / {
        proxy_pass http://ashoka_backend;
        proxy_http_version 1.1;
        
        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        
        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Disable caching for dynamic content
        proxy_cache_bypass $http_upgrade;
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }
}
```

### 2. Test and Restart Nginx

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo service nginx restart
```

### 3. Start Ashoka Application

```bash
# Run in background
nohup python3 run_dashboard.py > dashboard.log 2>&1 &
```

### 4. Test HTTP Access

Visit: `http://your-ec2-public-ip`

You should see the Ashoka login page!

---

## Custom Domain Configuration

### 1. Sign Up for No-IP

1. Go to [https://www.noip.com](https://www.noip.com)
2. Create a free account
3. Confirm your email

### 2. Create Hostname

1. Login to No-IP dashboard
2. Click "Dynamic DNS" → "No-IP Hostnames"
3. Click "Create Hostname"
4. Enter hostname: `ashoka-ai`
5. Select domain: `hopto.org`
6. Full domain: `ashoka-ai.hopto.org`
7. Enter your EC2 public IP address (e.g., `3.91.241.72`)
8. Click "Create Hostname"

### 3. Test Custom Domain

Visit: `http://ashoka-ai.hopto.org`

Your Ashoka platform should now be accessible via custom domain!

---

## HTTPS/SSL Setup

### 1. Stop Nginx

```bash
sudo service nginx stop
```

### 2. Obtain SSL Certificate

```bash
sudo certbot certonly --standalone -d ashoka-ai.hopto.org
```

Follow the prompts:
- Enter your email address
- Agree to terms of service
- Choose whether to share email with EFF

Certificate will be saved to:
- Certificate: `/etc/letsencrypt/live/ashoka-ai.hopto.org/fullchain.pem`
- Private Key: `/etc/letsencrypt/live/ashoka-ai.hopto.org/privkey.pem`

### 3. Configure Nginx for HTTPS

Clear the current configuration:
```bash
sudo sh -c 'echo -n > /etc/nginx/sites-available/default'
```

Open the config file:
```bash
sudo nano /etc/nginx/sites-available/default
```

Paste the following configuration:
```nginx
# WebSocket upgrade configuration
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

# Backend server (Ashoka runs on port 8080)
upstream ashoka_backend {
    server 127.0.0.1:8080;
    keepalive 64;
}

# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name ashoka-ai.hopto.org;

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name ashoka-ai.hopto.org;

    # SSL certificate configuration
    ssl_certificate /etc/letsencrypt/live/ashoka-ai.hopto.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ashoka-ai.hopto.org/privkey.pem;

    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Increase timeouts for long-running operations
    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://ashoka_backend;
        proxy_http_version 1.1;
        
        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        
        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Disable caching for dynamic content
        proxy_cache_bypass $http_upgrade;
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }
}
```

### 4. Test and Restart Nginx

```bash
# Test configuration
sudo nginx -t

# Start Nginx
sudo service nginx start
```

### 5. Test HTTPS Access

Visit: `https://ashoka-ai.hopto.org`

You should see:
- 🔒 Secure connection (padlock icon)
- Valid SSL certificate
- Ashoka login page

### 6. Setup Auto-Renewal

Certbot certificates expire after 90 days. Setup auto-renewal:

```bash
# Test renewal process
sudo certbot renew --dry-run

# Add cron job for auto-renewal
sudo crontab -e
```

Add this line:
```bash
0 3 * * * certbot renew --quiet --post-hook "service nginx reload"
```

This will check for renewal daily at 3 AM and reload Nginx if renewed.

---

## Process Management

### Option 1: Using Supervisor (Recommended)

#### 1. Create Supervisor Configuration

```bash
sudo nano /etc/supervisor/conf.d/ashoka.conf
```

Paste:
```ini
[program:ashoka]
command=/usr/bin/python3 /home/ubuntu/ashoka/run_dashboard.py
directory=/home/ubuntu/ashoka
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ashoka/dashboard.log
stderr_logfile=/var/log/ashoka/dashboard_error.log
environment=PATH="/usr/bin",HOME="/home/ubuntu"
```

#### 2. Create Log Directory

```bash
sudo mkdir -p /var/log/ashoka
sudo chown ubuntu:ubuntu /var/log/ashoka
```

#### 3. Update Supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ashoka
```

#### 4. Supervisor Commands

```bash
# Start
sudo supervisorctl start ashoka

# Stop
sudo supervisorctl stop ashoka

# Restart
sudo supervisorctl restart ashoka

# Status
sudo supervisorctl status ashoka

# View logs
sudo tail -f /var/log/ashoka/dashboard.log
```

### Option 2: Using systemd

#### 1. Create Service File

```bash
sudo nano /etc/systemd/system/ashoka.service
```

Paste:
```ini
[Unit]
Description=Ashoka GenAI Governance Platform
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ashoka
ExecStart=/usr/bin/python3 /home/ubuntu/ashoka/run_dashboard.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/ashoka/dashboard.log
StandardError=append:/var/log/ashoka/dashboard_error.log

[Install]
WantedBy=multi-user.target
```

#### 2. Enable and Start Service

```bash
# Create log directory
sudo mkdir -p /var/log/ashoka
sudo chown ubuntu:ubuntu /var/log/ashoka

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable ashoka

# Start service
sudo systemctl start ashoka
```

#### 3. systemd Commands

```bash
# Start
sudo systemctl start ashoka

# Stop
sudo systemctl stop ashoka

# Restart
sudo systemctl restart ashoka

# Status
sudo systemctl status ashoka

# View logs
sudo journalctl -u ashoka -f
```

---

## Troubleshooting

### Issue: Cannot Connect to Domain

**Check DNS propagation:**
```bash
nslookup ashoka-ai.hopto.org
```

**Check Nginx status:**
```bash
sudo service nginx status
```

**Check Nginx logs:**
```bash
sudo tail -f /var/log/nginx/error.log
```

### Issue: Application Not Starting

**Check application logs:**
```bash
# If using Supervisor
sudo tail -f /var/log/ashoka/dashboard.log

# If using systemd
sudo journalctl -u ashoka -f

# If running manually
tail -f dashboard.log
```

**Check if port 8080 is in use:**
```bash
sudo netstat -tulpn | grep 8080
```

**Kill existing process:**
```bash
sudo pkill -f run_dashboard.py
```

### Issue: SSL Certificate Errors

**Check certificate validity:**
```bash
sudo certbot certificates
```

**Renew certificate manually:**
```bash
sudo certbot renew --force-renewal
sudo service nginx reload
```

### Issue: WebSocket Connection Failed

**Check Nginx configuration:**
```bash
sudo nginx -t
```

**Verify WebSocket headers:**
```bash
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" https://ashoka-ai.hopto.org
```

### Issue: 502 Bad Gateway

**Possible causes:**
1. Application not running
2. Wrong port in Nginx config
3. Firewall blocking port 8080

**Solutions:**
```bash
# Check if application is running
ps aux | grep run_dashboard

# Check if port 8080 is listening
sudo netstat -tulpn | grep 8080

# Restart application
sudo supervisorctl restart ashoka

# Restart Nginx
sudo service nginx restart
```

### Issue: High Memory Usage

**Check memory usage:**
```bash
free -h
htop
```

**Restart application:**
```bash
sudo supervisorctl restart ashoka
```

**Consider upgrading EC2 instance type** if memory is consistently high.

---

## Maintenance Tasks

### Daily
- Monitor application logs
- Check system resources (CPU, memory, disk)

### Weekly
- Review security logs
- Check for application updates
- Backup database

### Monthly
- Review SSL certificate expiration
- Update system packages
- Analyze performance metrics

---

## Quick Reference

### URLs
- **HTTP**: `http://ashoka-ai.hopto.org`
- **HTTPS**: `https://ashoka-ai.hopto.org`
- **Direct IP**: `http://your-ec2-ip:8080` (testing only)

### Important Paths
- Application: `/home/ubuntu/ashoka`
- Nginx config: `/etc/nginx/sites-available/default`
- SSL certificates: `/etc/letsencrypt/live/ashoka-ai.hopto.org/`
- Application logs: `/var/log/ashoka/dashboard.log`
- Nginx logs: `/var/log/nginx/`

### Key Commands
```bash
# Restart everything
sudo supervisorctl restart ashoka
sudo service nginx restart

# View logs
sudo tail -f /var/log/ashoka/dashboard.log
sudo tail -f /var/log/nginx/error.log

# Check status
sudo supervisorctl status ashoka
sudo service nginx status
```

---

## Security Best Practices

1. **Keep system updated:**
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Use strong passwords** for admin accounts

3. **Enable firewall:**
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

4. **Regular backups:**
   ```bash
   cp data/ashoka.duckdb data/ashoka_backup_$(date +%Y%m%d).duckdb
   ```

5. **Monitor logs** for suspicious activity

6. **Keep SSL certificates updated** (auto-renewal configured)

---

## Support

For issues or questions:
1. Check logs first
2. Review troubleshooting section
3. Consult [SCRIPTS.md](SCRIPTS.md) for technical details
4. Check [AWS_DEPLOYMENT_SUMMARY.md](AWS_DEPLOYMENT_SUMMARY.md)

---

**Your Ashoka platform is now live at https://ashoka-ai.hopto.org! 🚀**
