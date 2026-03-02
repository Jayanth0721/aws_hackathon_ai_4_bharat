# Deployment Scripts

This directory contains scripts and configuration files for deploying Ashoka Platform to AWS.

## Files

### Shell Scripts
- `setup_ec2.sh` - Initial EC2 instance setup (run on EC2)
- `deploy.sh` - Automated deployment from local machine to EC2

### Configuration Files
- `supervisor_ashoka.conf` - Supervisor process manager configuration
- `nginx_ashoka.conf` - Nginx reverse proxy configuration

## Usage

### On Linux/Mac

Make scripts executable:
```bash
chmod +x deployment_scripts/*.sh
```

### On Windows

Scripts will be executable when uploaded to EC2. No action needed locally.

## Quick Start

1. **Setup EC2** (run on EC2 instance):
   ```bash
   ./setup_ec2.sh
   ```

2. **Deploy Application** (run from local machine):
   ```bash
   # Edit deploy.sh first to set EC2_HOST and KEY_FILE
   ./deploy.sh
   ```

3. **Configure Supervisor** (run on EC2):
   ```bash
   sudo cp supervisor_ashoka.conf /etc/supervisor/conf.d/ashoka.conf
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start ashoka
   ```

4. **Configure Nginx** (run on EC2):
   ```bash
   sudo cp nginx_ashoka.conf /etc/nginx/sites-available/ashoka
   sudo ln -s /etc/nginx/sites-available/ashoka /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## See Also

- `../AWS_DEPLOYMENT.md` - Complete deployment guide
- `../QUICK_START_AWS.md` - Quick deployment guide
- `../AWS_DEPLOYMENT_SUMMARY.md` - Deployment overview
