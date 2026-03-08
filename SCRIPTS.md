# Ashoka Platform - Scripts & Technical Documentation

> **Complete technical reference for scripts, automation, and platform architecture**

---

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [Startup Scripts](#startup-scripts)
3. [Deployment Scripts](#deployment-scripts)
4. [Database Scripts](#database-scripts)
5. [Service Architecture](#service-architecture)
6. [API Integration](#api-integration)
7. [Automation & Maintenance](#automation--maintenance)

---

## Platform Overview

### What is Ashoka?

Ashoka is an enterprise-grade GenAI governance platform that provides:

**Core Capabilities:**
- 🧠 **AI Content Intelligence**: Multi-format content analysis with quality scoring
- 🎨 **AI Content Generation**: Text and image creation using state-of-the-art AI
- 🔄 **Multi-Platform Transformation**: Automated content adaptation for social media
- 📊 **Real-Time Monitoring**: Performance tracking and quality metrics
- 🚨 **Intelligent Alerts**: Proactive quality and risk notifications
- 🔒 **Security & Governance**: RBAC, audit trails, and content restrictions

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Ashoka Platform                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Frontend   │  │   Services   │  │   Database   │       │
│  │   (NiceGUI)  │◄─┤  (Python)    │◄─┤  (DuckDB)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                                │
│         │                  ▼                                │
│         │          ┌──────────────┐                         │
│         │          │  AI Services │                         │
│         │          ├──────────────┤                         │
│         │          │ Multi-Engine │ (Gemini + Sarvam AI)    │
│         └─────────►│ Son of Ashoka│ (Image Gen - FREE)      │
│                    └──────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend Layer:**
- NiceGUI (Python web framework)
- Tailwind CSS (styling)
- JavaScript (client-side interactions)

**Service Layer:**
- Python 3.8+
- Async/await for non-blocking operations
- RESTful API patterns

**AI/ML Layer:**
- Multi-Engine AI System:
  - Google Gemini API (gemini-2.0-flash) - Primary engine (50 requests/day)
  - Sarvam AI (sarvam-m) - Fallback for Indian languages (1000 requests/day)
  - Gemini Engine 3 - Additional fallback (50 requests/day)
- API Usage Tracking System:
  - Real-time quota monitoring
  - 24-hour reset cycle
  - Automatic engine fallback
  - Per-user tracking
- Son of Ashoka API (Cloudflare Workers) - Image generation (FREE, unlimited)

**Data Layer:**
- DuckDB (local, file-based)
- DynamoDB (optional, cloud)

**Security Layer:**
- OTP authentication
- Session management
- Role-based access control (RBAC)

---

## Startup Scripts

### 1. start.sh (Linux/Mac)

**Purpose**: Automated setup and launch for Unix-based systems

**Location**: `./start.sh`

**What it does:**
1. Checks Python version (requires 3.8+)
2. Detects and installs FFmpeg if missing
3. Installs Python dependencies from requirements.txt
4. Creates .env file from template
5. Launches the dashboard

**Usage:**
```bash
chmod +x start.sh
./start.sh
```

**Script Breakdown:**
```bash
#!/bin/bash

# Color codes for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

# Install FFmpeg based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ffmpeg
fi

# Install Python dependencies
pip3 install -r requirements.txt

# Create .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env and add your GOOGLE_API_KEY"
fi

# Launch dashboard
python3 run_dashboard.py
```

**Error Handling:**
- Exits if Python < 3.8
- Warns if FFmpeg installation fails
- Prompts for API key if missing

---

### 2. start.bat (Windows)

**Purpose**: Automated setup and launch for Windows systems

**Location**: `./start.bat`

**What it does:**
1. Checks Python installation
2. Installs FFmpeg via winget
3. Installs Python dependencies
4. Creates .env file
5. Launches the dashboard

**Usage:**
```cmd
start.bat
```

**Script Breakdown:**
```batch
@echo off
echo Ashoka Platform - Windows Setup

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    exit /b 1
)

REM Install FFmpeg
winget install --id=Gyan.FFmpeg -e

REM Install dependencies
pip install -r requirements.txt

REM Create .env
if not exist .env (
    copy .env.example .env
    echo Please edit .env and add your GOOGLE_API_KEY
)

REM Launch
python run_dashboard.py
```

---

### 3. run_dashboard.py

**Purpose**: Main application entry point

**Location**: `./run_dashboard.py`

**What it does:**
1. Initializes database schema
2. Creates default users (admin, demo)
3. Configures NiceGUI server
4. Sets up routing
5. Starts web server

**Key Components:**

```python
# Database initialization
from src.database.duckdb_schema import db_schema
db_schema.connect()
db_schema.initialize_schema()

# Create default users
from src.services.auth_service import auth_service
auth_service.signup("admin", "admin@ashoka.ai", "admin123", "admin")
auth_service.signup("creator", "creator@ashoka.ai", "creator123", "creator")
auth_service.signup("guruji", "guruji@ashoka.ai", "guru1", "user")
auth_service.signup("demo", "demo@ashoka.ai", "demo123", "user")

# Setup routes
@ui.page('/')
def index():
    create_auth_page()

@ui.page('/dashboard')
def dashboard():
    # Check authentication
    session_token = app.storage.general.get('session_token')
    if not session_token:
        ui.navigate.to('/')
        return
    
    # Show dashboard
    dashboard_instance = AshokaGovDashboard()
    dashboard_instance.create_dashboard()

# Start server
ui.run(
    title='Ashoka - GenAI Governance Platform',
    host='0.0.0.0',
    port=8080,
    storage_secret=storage_secret
)
```

**Configuration:**
- Host: 0.0.0.0 (accessible from network)
- Port: 8080
- Storage: Requires STORAGE_SECRET in .env
- Reload: Disabled in production

---

## Deployment Scripts

### 1. deploy.sh

**Purpose**: Automated deployment to production server

**Location**: `./deployment_scripts/deploy.sh`

**What it does:**
1. Pulls latest code from repository
2. Installs/updates dependencies
3. Runs database migrations
4. Restarts services
5. Verifies deployment

**Usage:**
```bash
cd deployment_scripts
chmod +x deploy.sh
./deploy.sh
```

**Script Flow:**
```bash
#!/bin/bash

# Pull latest code
git pull origin main

# Backup database
cp data/ashoka.duckdb data/ashoka_backup_$(date +%Y%m%d).duckdb

# Install dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo supervisorctl restart ashoka

# Check status
sudo supervisorctl status ashoka

# Verify
curl -f http://localhost:8080 || echo "Deployment verification failed"
```

---

### 2. setup_ec2.sh

**Purpose**: Initial EC2 instance setup

**Location**: `./deployment_scripts/setup_ec2.sh`

**What it does:**
1. Updates system packages
2. Installs Python, FFmpeg, Nginx, Supervisor
3. Clones repository
4. Configures services
5. Sets up firewall

**Usage:**
```bash
chmod +x setup_ec2.sh
./setup_ec2.sh
```

**Key Steps:**
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3 python3-pip ffmpeg nginx supervisor

# Clone repository
git clone <repository-url> /home/ubuntu/ashoka
cd /home/ubuntu/ashoka

# Install Python packages
pip3 install -r requirements.txt

# Configure Supervisor
sudo cp deployment_scripts/supervisor_ashoka.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update

# Configure Nginx
sudo cp deployment_scripts/nginx_ashoka.conf /etc/nginx/sites-available/ashoka
sudo ln -s /etc/nginx/sites-available/ashoka /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Start services
sudo supervisorctl start ashoka
```

---

### 3. Supervisor Configuration

**Purpose**: Process management and auto-restart

**Location**: `./deployment_scripts/supervisor_ashoka.conf`

**Configuration:**
```ini
[program:ashoka]
command=/usr/bin/python3 /home/ubuntu/ashoka/run_dashboard.py
directory=/home/ubuntu/ashoka
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ashoka/dashboard.log
environment=PATH="/usr/bin",HOME="/home/ubuntu"
```

**Features:**
- Auto-start on boot
- Auto-restart on crash
- Log rotation
- Environment variables

**Management Commands:**
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

---

### 4. Nginx Configuration

**Purpose**: Reverse proxy and HTTPS termination

**Location**: `./deployment_scripts/nginx_ashoka.conf`

**Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Features:**
- WebSocket support
- Real IP forwarding
- Connection upgrade handling
- Cache bypass

---

## Database Scripts

### 1. Database Schema Initialization

**Purpose**: Create all required tables

**Location**: `src/database/duckdb_schema.py`

**Tables Created:**
```sql
-- Content Analysis
CREATE TABLE ashoka_contentint (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    content_type VARCHAR,
    content_text TEXT,
    summary TEXT,
    sentiment VARCHAR,
    quality_score FLOAT,
    keywords JSON,
    topics JSON,
    analyzed_at TIMESTAMP
);

-- Transform History
CREATE TABLE transform_history (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    original_content TEXT,
    platforms JSON,
    tone VARCHAR,
    transformed_results JSON,
    created_at TIMESTAMP
);

-- Users
CREATE TABLE ashoka_users (
    user_id VARCHAR PRIMARY KEY,
    username VARCHAR UNIQUE,
    password_hash VARCHAR,
    email VARCHAR,
    role VARCHAR,
    created_at TIMESTAMP
);

-- Security Events
CREATE TABLE security_events (
    event_id INTEGER PRIMARY KEY,
    username VARCHAR,
    event_type VARCHAR,
    event_description TEXT,
    timestamp TIMESTAMP
);

-- And more...
```

**Usage:**
```python
from src.database.duckdb_schema import db_schema

# Connect
db_schema.connect()

# Initialize
db_schema.initialize_schema()

# Query
results = db_schema.conn.execute("SELECT * FROM ashoka_contentint").fetchall()
```

---

### 2. Database Backup Script

**Purpose**: Backup DuckDB database

**Create**: `scripts/backup_db.sh`

```bash
#!/bin/bash

# Configuration
DB_PATH="data/ashoka.duckdb"
BACKUP_DIR="data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ashoka_$DATE.duckdb"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup
cp $DB_PATH $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup created: $BACKUP_FILE.gz"
```

**Usage:**
```bash
chmod +x scripts/backup_db.sh
./scripts/backup_db.sh
```

**Cron Setup (Daily at 2 AM):**
```bash
crontab -e
# Add line:
0 2 * * * /path/to/ashoka/scripts/backup_db.sh
```

---

## Service Architecture

### 1. Authentication Service

**Location**: `src/services/auth_service.py`

**Responsibilities:**
- User registration
- Password hashing
- OTP generation and verification
- Session management

**Key Methods:**
```python
class AuthService:
    def signup(username, email, password, role):
        # Create user account
        
    def authenticate(username, password):
        # Verify credentials
        
    def generate_otp(user_id):
        # Create time-limited OTP
        
    def verify_otp(user_id, code):
        # Validate OTP
        
    def create_session(user_id):
        # Generate session token
```

---

### 2. Content Analyzer Service

**Location**: `src/services/content_analyzer.py`

**Responsibilities:**
- Content analysis using Multi-Engine AI (Gemini + Sarvam AI)
- Quality score calculation
- Sentiment detection
- Keyword extraction

**Key Methods:**
```python
class ContentAnalyzer:
    def analyze_text(text):
        # Analyze text content
        # Returns: sentiment, keywords, topics, quality_score
        
    def analyze_image(image_path):
        # Analyze image content
        
    def analyze_audio(audio_path):
        # Transcribe and analyze audio
        
    def analyze_video(video_path):
        # Extract audio, transcribe, analyze
```

**Quality Score Calculation:**
```python
def _calculate_quality_score(analysis):
    score = 100
    
    # Sentiment penalty
    if sentiment == 'negative':
        score -= 15
    elif sentiment == 'neutral':
        score -= 5
    
    # Confidence penalty
    if confidence < 0.7:
        score -= 10
    
    # Length penalty
    if word_count < 20:
        score -= 20
    elif word_count < 50:
        score -= 10
    
    # Keyword penalty
    if len(keywords) < 3:
        score -= 10
    
    # Topic penalty
    if len(topics) < 2:
        score -= 5
    
    return max(0, score)
```

---

### 3. API Usage Tracker Service (NEW)

**Location**: `src/services/api_usage_tracker.py`

**Responsibilities:**
- Track AI engine API requests per user per day
- Monitor quota usage in real-time
- Enforce daily limits
- Provide usage statistics
- Automatic 24-hour reset cycle

**Key Methods:**
```python
class APIUsageTracker:
    DAILY_LIMITS = {
        'gemini': 50,      # Gemini Engine 1
        'sarvam': 1000,    # Sarvam AI
        'gemini3': 50,     # Gemini Engine 3
    }
    
    def track_request(user_id, engine_name, model_name, success=True):
        # Track an API request (success or failure)
        # Updates or creates daily usage record
        
    def get_usage_today(user_id, engine_name):
        # Get today's usage for specific engine
        # Returns: used, limit, remaining, percentage
        
    def get_all_usage_today(user_id):
        # Get usage for all engines
        # Returns: dict mapping engine names to stats
        
    def can_use_engine(user_id, engine_name):
        # Check if user has quota remaining
        # Returns: Boolean
        
    def get_recommended_engine(user_id):
        # Get engine with available quota
        # Priority: gemini → sarvam → gemini3
```

**Database Schema:**
```sql
CREATE TABLE ai_engine_usage (
    usage_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    engine_name VARCHAR NOT NULL,
    model_name VARCHAR NOT NULL,
    request_date DATE NOT NULL,
    request_count INTEGER DEFAULT 1,
    last_request_at TIMESTAMP NOT NULL,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0
)

CREATE INDEX idx_ai_engine_usage_user_date 
ON ai_engine_usage(user_id, request_date, engine_name)
```

**Usage Example:**
```python
from src.services.api_usage_tracker import api_usage_tracker

# Check quota before request
if api_usage_tracker.can_use_engine('user_guruji', 'gemini'):
    # Make API request
    result = ai_client.generate_content(prompt, user_id='user_guruji')
    
    # Track successful request
    api_usage_tracker.track_request(
        user_id='user_guruji',
        engine_name='gemini',
        model_name='gemini-2.0-flash',
        success=True
    )
else:
    print("Quota exceeded for Gemini")
```

**24-Hour Reset Logic:**
- Tracking uses `request_date` field (DATE type)
- Each day at midnight, new date begins
- Previous day's data preserved in database
- New day starts with 0 usage
- Automatic reset, no cron jobs needed

---

### 4. Image Generator Service

**Location**: `src/services/image_generator.py`

**Responsibilities:**
- Image generation via Son of Ashoka API
- Base64 encoding for display
- Error handling and retries

**Key Methods:**
```python
class ImageGenerator:
    def generate_image(prompt):
        # Call Cloudflare Workers API
        # Returns: base64 image data
        
    def save_image(image_bytes, filepath):
        # Save to local storage
```

**API Integration:**
```python
def generate_image(self, prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {self.api_token}",
        "Content-Type": "application/json"
    }
    
    data = {"prompt": prompt}
    
    response = requests.post(
        self.api_url,
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return {
            'success': True,
            'image_data': image_base64
        }
```

**Why Son of Ashoka (Cloudflare Workers)?**

1. **Cost Optimization**: FREE vs $0.02-0.10 per image
2. **Better Performance**: Global edge network distribution
3. **Scalability**: Automatic load balancing
4. **Reliability**: Built-in redundancy
5. **Computational Power**: Optimized resource allocation

---

### 4. Content Transformer Service

**Location**: `src/services/content_transformer.py`

**Responsibilities:**
- Multi-platform content adaptation
- Tone adjustment
- Hashtag generation
- Character limit compliance

**Key Methods:**
```python
class ContentTransformer:
    def transform_content(content, platforms, tone, include_hashtags):
        # Transform for each platform
        # Returns: dict of platform-specific content
```

**Platform Specifications:**
```python
PLATFORM_SPECS = {
    'LinkedIn': {
        'max_length': 3000,
        'style': 'Professional',
        'hashtags': 3-5
    },
    'Twitter': {
        'max_length': 280,
        'style': 'Concise',
        'hashtags': 1-2
    },
    'Instagram': {
        'max_length': 2200,
        'style': 'Visual-first',
        'hashtags': 10-15
    },
    'Facebook': {
        'max_length': 63206,
        'style': 'Conversational',
        'hashtags': 1-3
    }
}
```

---

### 5. Monitoring Service

**Location**: `src/services/monitoring_service.py`

**Responsibilities:**
- Metrics collection
- Performance tracking
- System health checks
- Alert generation

**Key Methods:**
```python
class MonitoringService:
    def get_quality_metrics():
        # Calculate quality statistics
        
    def get_performance_trends():
        # Generate 24-hour trend data
        
    def check_system_health():
        # Verify API, database, AI status
```

---

## API Integration

### 1. Multi-Engine AI System

**Purpose**: Content analysis, generation, transformation with automatic fallback

**Configuration:**
```python
# .env
GOOGLE_API_KEY=your_gemini_key_here
GOOGLE_API_KEY_2=your_second_gemini_key  # Optional backup
SARVAM_API_KEY=your_sarvam_key_here      # Optional fallback
```

**Engine Priority:**
1. Gemini Engine 1 (primary)
2. Sarvam AI (fallback for Indian languages)
3. Gemini Engine 3 (additional fallback)

**Usage:**
```python
from src.services.ai_engine import multi_engine_client

# Automatic engine selection with fallback
result = multi_engine_client.generate_content(prompt)

# Analyze content
analysis = multi_engine_client.analyze_content(text)
```

**Cost**: ~$0.001-0.002 per request (Gemini), FREE tier available

---

### 2. Son of Ashoka API (Cloudflare Workers)

**Purpose**: AI image generation

**Endpoint**: `https://son-of-ashoka.guymovie89.workers.dev/`

**Authentication**: Bearer token (hardcoded)

**Usage:**
```python
from src.services.image_generator import image_generator

result = image_generator.generate_image("robot cooking breakfast")

if result['success']:
    image_data = result['image_data']  # base64
    image_bytes = result['image_bytes']  # raw bytes
```

**Cost**: FREE (Cloudflare Workers)

**Benefits:**
- No per-image charges
- Global CDN distribution
- Automatic scaling
- 10-30 second generation time

---



## Automation & Maintenance

### 1. Auto-Refresh System

**Purpose**: Keep dashboard data current without page reload

**Implementation:**
```python
# Monitoring auto-refresh (10 minutes)
ui.timer(600, self._refresh_monitoring_metrics)

# Alerts auto-refresh (10 minutes)
ui.timer(600, lambda: self._refresh_alerts(show_notification=False))

# Security auto-refresh (10 minutes)
ui.timer(600, self._refresh_security_logs)
```

---

### 2. Session Management

**Purpose**: Automatic session timeout and cleanup

**Configuration:**
```python
# .env
SESSION_TIMEOUT_MINUTES=30
```

**Implementation:**
```python
def _start_session_timer(self):
    self.session_timer = ui.timer(1, self._update_session_timer)
    
def _update_session_timer(self):
    elapsed = datetime.now() - self.session_start_time
    remaining = self.session_duration - elapsed.total_seconds()
    
    if remaining <= 0:
        self._handle_session_timeout()
```

---

### 3. Database Maintenance

**Daily Tasks:**
```bash
# Backup database
./scripts/backup_db.sh

# Vacuum database (optimize)
duckdb data/ashoka.duckdb "VACUUM;"

# Check database size
du -h data/ashoka.duckdb
```

**Weekly Tasks:**
```bash
# Clean old backups (keep 30 days)
find data/backups -name "*.gz" -mtime +30 -delete

# Analyze database statistics
duckdb data/ashoka.duckdb "ANALYZE;"
```

---

### 4. Log Management

**Log Locations:**
```
/var/log/ashoka/dashboard.log    # Application logs
/var/log/nginx/access.log        # Nginx access
/var/log/nginx/error.log         # Nginx errors
/var/log/supervisor/ashoka.log   # Supervisor logs
```

**Log Rotation:**
```bash
# /etc/logrotate.d/ashoka
/var/log/ashoka/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 ubuntu ubuntu
}
```

---

## Performance Optimization

### 1. Database Query Optimization

**Use Indexes:**
```sql
CREATE INDEX idx_user_id ON ashoka_contentint(user_id);
CREATE INDEX idx_analyzed_at ON ashoka_contentint(analyzed_at);
CREATE INDEX idx_created_at ON transform_history(created_at);
```

**Use Prepared Statements:**
```python
# Good
db_schema.conn.execute("SELECT * FROM ashoka_contentint WHERE user_id = ?", [user_id])

# Bad
db_schema.conn.execute(f"SELECT * FROM ashoka_contentint WHERE user_id = '{user_id}'")
```

---

### 2. Caching Strategy

**Metrics Cache:**
```python
self._metrics_cache = {}
self._metrics_cache_ttl_seconds = 45

def _get_cached_metrics(self):
    if 'metrics' in self._metrics_cache:
        age = time.time() - self._metrics_cache['timestamp']
        if age < self._metrics_cache_ttl_seconds:
            return self._metrics_cache['metrics']
    
    # Fetch fresh data
    metrics = self._fetch_metrics()
    self._metrics_cache = {
        'metrics': metrics,
        'timestamp': time.time()
    }
    return metrics
```

---

### 3. Async Operations

**Non-Blocking AI Calls:**
```python
async def _generate_ai_content(self):
    loop = asyncio.get_event_loop()
    
    result = await loop.run_in_executor(
        None,
        gemini_client.generate_content,
        prompt
    )
```

---

## Conclusion

This technical documentation covers all scripts, services, and automation in the Ashoka platform. For user-facing workflows, see [WORKFLOW.md](WORKFLOW.md).

For setup instructions, see [SETUP.md](SETUP.md).

---

**Built with precision for enterprise-grade content governance**
