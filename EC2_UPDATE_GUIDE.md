# EC2 Update Guide

This guide explains how to push local changes to GitHub and update your EC2 instance.

## Problem: WebSocket Connection Error on EC2

If you see this error on EC2:
```
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes
websockets.exceptions.ConnectionClosedError: sent 1000 (OK); no close frame received
```

This means your EC2 has old code without the WebSocket fix. Follow the steps below to update.

---

## Step 1: Push Changes from Windows to GitHub

**On your Windows machine**, open PowerShell in the project directory:

```powershell
# Check what files have changed
git status

# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "Fix WebSocket connection bug and add EC2 deployment guide"

# Push to GitHub (replace 'main' with your branch name if different)
git push origin main
```

If you haven't set up Git yet:
```powershell
# Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository (if not already done)
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git add .
git commit -m "Initial commit with WebSocket fix"
git push -u origin main
```

---

## Step 2: Update EC2 Instance

**SSH into your EC2 instance:**

```bash
ssh -i "your-key.pem" ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com
```

**Stop the running dashboard:**

```bash
# Kill the process
pkill -f run_dashboard.py

# Verify it's stopped
ps aux | grep python
```

**Pull latest changes from GitHub:**

```bash
# Navigate to project directory
cd ~/aws_hackathon_ai_4_bharat

# Pull latest code
git pull origin main

# If you get merge conflicts or errors, you can force pull:
# git fetch origin
# git reset --hard origin/main
```

**Update dependencies and restart:**

```bash
# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Verify .env file has STORAGE_SECRET
cat .env | grep STORAGE_SECRET

# If STORAGE_SECRET is missing, add it:
echo "STORAGE_SECRET=$(openssl rand -hex 32)" >> .env

# Start dashboard in screen
# Start dashboard in background
nohup python run_dashboard.py > dashboard.log 2>&1 &

# Verify it's running
ps aux | grep run_dashboard
```

**Verify it's running:**

```bash
# Check process is running
ps aux | grep run_dashboard

# Check port 8080 is listening
sudo ss -tlnp | grep 8080

# Get your public IP
curl http://checkip.amazonaws.com

# Test local access
curl http://localhost:8080

# View logs
tail -f dashboard.log
```

---

## Step 3: Access Dashboard from Windows

Open your browser and go to:
```
http://YOUR_EC2_PUBLIC_IP:8080
```

For example: `http://100.52.210.236:8080`

---

## Quick Reference Commands

**Windows (Push to GitHub):**
```powershell
git add .
git commit -m "Your commit message"
git push origin main
```

**EC2 (Pull and Restart):**
```bash
cd ~/aws_hackathon_ai_4_bharat
pkill -f run_dashboard.py
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
nohup python run_dashboard.py > dashboard.log 2>&1 &
```

---

## Troubleshooting

### Git Push Fails (Authentication)

If you get authentication errors when pushing to GitHub:

1. **Use Personal Access Token (PAT):**
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Use token as password when pushing

2. **Or use SSH keys:**
   - Generate SSH key: `ssh-keygen -t ed25519 -C "your.email@example.com"`
   - Add to GitHub: Settings → SSH and GPG keys
   - Change remote URL: `git remote set-url origin git@github.com:USERNAME/REPO.git`

### Git Pull Fails (Merge Conflicts)

If you have local changes on EC2 that conflict:

```bash
# Save your local changes
git stash

# Pull latest code
git pull origin main

# Apply your local changes back (if needed)
git stash pop
```

Or force overwrite local changes:
```bash
git fetch origin
git reset --hard origin/main
```

### Dashboard Still Shows Old Code

Make sure you:
1. Killed the old process: `pkill -f run_dashboard.py`
2. Pulled latest code: `git pull origin main`
3. Restarted dashboard: `nohup python run_dashboard.py > dashboard.log 2>&1 &`
4. Cleared browser cache: Ctrl+Shift+R (hard refresh)

### WebSocket Error Persists

Check `.env` file has STORAGE_SECRET:
```bash
cat .env | grep STORAGE_SECRET
```

If missing, add it:
```bash
echo "STORAGE_SECRET=$(openssl rand -hex 32)" >> .env
```

Then restart the dashboard.

---

## Automated Update Script

Create a script to automate EC2 updates:

```bash
# Create update script
cat > ~/update_dashboard.sh << 'EOF'
#!/bin/bash
cd ~/aws_hackathon_ai_4_bharat
pkill -f run_dashboard.py
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
nohup python run_dashboard.py > dashboard.log 2>&1 &
echo "Dashboard updated and restarted!"
echo "Access at: http://$(curl -s http://checkip.amazonaws.com):8080"
EOF

# Make it executable
chmod +x ~/update_dashboard.sh

# Run it anytime you need to update
~/update_dashboard.sh
```

---

## Production Deployment (Optional)

For production, use Supervisor to auto-restart on crashes:

```bash
# Install Supervisor
sudo apt install supervisor

# Copy config
sudo cp deployment_scripts/supervisor_ashoka.conf /etc/supervisor/conf.d/ashoka.conf

# Update and start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ashoka

# Check status
sudo supervisorctl status ashoka
```

Now the dashboard will auto-restart if it crashes!
