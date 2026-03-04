# Ashoka - GenAI Governance Platform

A comprehensive AI-powered content governance platform built for the AWS Hackathon. Ashoka provides intelligent content analysis, multi-platform transformation, real-time monitoring, and security features.

## 🚀 Quick Start

### Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```
This will automatically:
- Check Python version
- Install FFmpeg (Linux: `sudo apt install ffmpeg`, Mac: `brew install ffmpeg`)
- Install Python dependencies
- Create .env file
- Launch the dashboard

**Windows:**
```bash
start.bat
```
This will:
- Check Python version
- Check for FFmpeg and offer to install it using winget
- Install Python dependencies
- Create .env file
- Launch the dashboard

### Manual Setup

```bash
# 1. Install FFmpeg (required for audio/video processing)
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
# Windows: winget install --id=Gyan.FFmpeg -e
# See INSTALL_FFMPEG_WINDOWS.md for detailed Windows instructions

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run the dashboard
python run_dashboard.py
```

Open http://localhost:8080 in your browser.

**Note:** If you get audio/video processing errors, you need to install FFmpeg. See [INSTALL_FFMPEG_WINDOWS.md](INSTALL_FFMPEG_WINDOWS.md) for Windows instructions.

## 🔐 Default Credentials

- **Admin User**: `admin` / `admin123` (has access to Security tab)
- **Demo User**: `demo` / `demo123` (standard user)

## ✨ Key Features

### 1. Content Intelligence & Analysis
- **Text Analysis**: AI-powered content analysis with sentiment, keywords, and quality scoring
- **File Upload Support**: Audio, Image, Video, and Document uploads (with remove functionality)
- **Analysis History**: Track all analyzed content with preview and reload options

### 2. AI Content Generator
- **Text/Notes Generation**: Generate professional content using Google Gemini AI
- **Coming Soon**: Image and Video generation features

### 3. Multi-Platform Content Transformer
- Transform content for different platforms (Twitter, LinkedIn, Instagram, Facebook, Blog)
- Customize tone (Professional, Casual, Formal, Friendly)
- Optional hashtag generation
- **Transform History**: View and reload past transformations

### 4. Real-Time Monitoring
- Operation metrics and success rates
- System performance tracking
- Error monitoring and alerts

### 5. Alerts & Notifications
- Real-time alerts from Content Intelligence analysis history
- Real-time alerts from Multi-Platform Transformer history
- Quality-based warnings (< 60% quality score)
- Sentiment-based warnings (negative sentiment > 70% confidence)
- Risk assessments (policy violations, toxicity)
- Transformation success notifications
- Filter by type: All, Critical, Warning, Info, Success
- Auto-refresh every 10 minutes

### 6. Security Dashboard (Admin Only)
- Login activity monitoring
- Security event tracking
- User session management
- Geographic and device information
- **NEW: AI Content Generation Restrictions**
  - Define keywords/phrases that block AI content generation
  - Prevent inappropriate, illegal, or policy-violating content
  - Toggle restrictions on/off without deleting
  - Reduces AI API costs by blocking invalid prompts before API calls
  - Admin-only access for content governance

### 7. Role-Based Access Control
- **User Role**: Standard access (default for signup)
- **Creator Role**: Content creation access (selectable during signup)
- **Admin Role**: Full access including Security tab (pre-configured)

## 🛠️ Technology Stack

- **Frontend**: NiceGUI (Python-based web framework)
- **AI/ML**: 
  - Google Gemini API (gemini-2.5-flash) - Content analysis, generation, transformation
  - OpenAI Whisper (local) - Audio/video transcription
- **Document Processing**:
  - pdfplumber - PDF text extraction
  - python-docx - DOCX text extraction
- **Audio/Video Processing**:
  - openai-whisper - Speech-to-text transcription (runs locally)
  - moviepy - Video processing and audio extraction
  - pydub - Audio format conversion
  - **FFmpeg** (required) - Multimedia framework for audio/video handling
- **Database**: DuckDB (local) or DynamoDB (AWS cloud)
- **Authentication**: OTP-based with session management
- **Styling**: Tailwind CSS with custom teal theme

### 🎯 Which Tool Does What?

When you use different features, here's what processes your content:

| Feature | Tool Used | Type | Cost |
|---------|-----------|------|------|
| **Text Analysis** | **Google Gemini** | Cloud API | Paid per request |
| **Content Generation** | **Google Gemini** | Cloud API | Paid per request |
| **Content Transformation** | **Google Gemini** | Cloud API | Paid per request |
| **Audio Transcription** | **OpenAI Whisper** | Local AI | FREE |
| **Video Transcription** | **OpenAI Whisper + MoviePy** | Local AI | FREE |
| **PDF Text Extraction** | **pdfplumber** | Local Library | FREE |
| **DOCX Text Extraction** | **python-docx** | Local Library | FREE |
| **TXT/MD Reading** | **Python Built-in** | Local | FREE |

**Note:** The UI shows which tool is processing your content in real-time!

## 📁 Project Structure

```
ashoka/
├── src/
│   ├── ui/
│   │   ├── dashboard.py      # Main dashboard UI
│   │   └── auth_page.py      # Login/Signup UI
│   ├── services/
│   │   ├── gemini_client.py  # Google Gemini integration
│   │   ├── auth_service.py   # Authentication logic
│   │   ├── content_analyzer.py
│   │   ├── content_transformer.py
│   │   ├── security_service.py
│   │   └── monitoring_service.py
│   ├── database/
│   │   ├── duckdb_schema.py  # Database schema
│   │   └── mock_storage.py   # Storage implementations
│   └── models/
│       ├── auth.py           # User/Session models
│       ├── monitoring.py
│       └── audit.py
├── data/
│   ├── ashoka.duckdb         # Main database
│   └── uploads/              # Uploaded files
├── run_dashboard.py          # Main entry point
├── requirements.txt
└── .env                      # Environment configuration
```

## 🎨 UI Theme

### Light Mode
- **Primary Color**: Teal/Turquoise (#2d8a84, #176a66)
- **Background**: Warm Beige/Cream (#ded5c4, #efeeeb)
- **Card Background**: Off-white (#f8f6f2)
- **Text**: Dark Teal (#102d32, #4e6b71)
- **Accent**: Teal (#2d8a84) and Soft Blue (#5b93c9)

### Dark Mode
- **Primary Color**: Teal (#1f7d78, #145f5b)
- **Background**: Dark Teal/Gray (#102124, #173037)
- **Card Background**: Dark Teal (#1c3438)
- **Text**: Light Cyan (#e7f3f4, #b5cfd1)
- **Accent**: Light Teal (#70b8b2) and Light Blue (#7caede)

### Status Colors
- **Success**: Green
- **Warning**: Orange/Amber
- **Error**: Red
- **Info**: Blue

## 📝 Environment Variables

Required in `.env`:
```
# AI Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
USE_GEMINI=true

# Database Configuration
USE_REAL_DYNAMODB=false          # Set to 'true' to use AWS DynamoDB, 'false' for local DuckDB
DUCKDB_PATH=data/ashoka.duckdb   # Path to local DuckDB file (used when USE_REAL_DYNAMODB=false)

# AWS Configuration (only needed if USE_REAL_DYNAMODB=true)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DYNAMODB_TABLE=ashoka_contentint  # Your DynamoDB table name

# Other
MOCK_MODE=false
```

### Database Mode Selection

**Local Mode (Default - Recommended for Development):**
```bash
USE_REAL_DYNAMODB=false
```
- Uses DuckDB (local file-based database)
- No AWS credentials needed
- No cloud costs
- Perfect for development and testing
- Data stored in `data/ashoka.duckdb`

**Cloud Mode (Optional - For Production):**
```bash
USE_REAL_DYNAMODB=true
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
DYNAMODB_TABLE=ashoka_contentint
```
- Uses AWS DynamoDB
- Requires AWS credentials
- Costs ~$3-90/year depending on usage
- Provides scalability and high availability
- Managed infrastructure

## 🔄 Data Persistence

All data is stored in `data/ashoka.duckdb`:
- User accounts and sessions
- Content analysis history
- Transform history
- Security logs
- Monitoring metrics

### Database Storage Architecture

| Database | Tables/Data Stored | Purpose | Cost Impact |
|----------|-------------------|---------|-------------|
| **DuckDB** (Local) | • `ashoka_contentint` - Content analysis results<br>• `transform_history` - Platform transformations<br>• `ashoka_users` - User accounts (local mode)<br>• `ashoka_sessions` - User sessions (local mode)<br>• `security_login_logs` - Login attempts<br>• `security_events` - Security events<br>• `content_restrictions` - AI generation restrictions<br>• `operation_metrics` - System metrics<br>• `quality_metrics` - Content quality scores<br>• `risk_assessments` - Risk analysis results<br>• `engagement_analysis` - Engagement metrics<br>• `reactions` - User reactions | Fast local storage for all application data, analysis results, and user information. Used in development and can be used in production. | **FREE** - No cloud costs |
| **DynamoDB** (AWS Cloud) | • `ashoka_contentint` - Single-table design storing:<br>&nbsp;&nbsp;- Users (diff_data = user_id)<br>&nbsp;&nbsp;- Sessions (diff_data = session_token)<br>&nbsp;&nbsp;- Content (diff_data = content_id)<br>&nbsp;&nbsp;- Audit logs (diff_data = audit_id)<br>&nbsp;&nbsp;- Alerts (diff_data = alert_id)<br>• Uses generic partition key `diff_data` for flexible storage | Cloud-based NoSQL database for production deployments. Provides scalability, high availability, and managed infrastructure. Optional - can use DuckDB instead. | **PAID** - AWS charges:<br>• On-demand: $1.25/million writes, $0.25/million reads<br>• Provisioned: $0.00065/hour per WCU<br>• Storage: $0.25/GB/month<br>**Estimated: $5-20/month for small-medium usage** |
| **Google Gemini API** | N/A - API calls only | AI content analysis, sentiment detection, content generation, transformation | **PAID** - Per API call:<br>• Input: $0.00025 per 1K chars<br>• Output: $0.00075 per 1K chars |
| **Whisper AI** (Local) | N/A - Local model | Audio/video transcription | **FREE** - Runs locally |

**Note:** You can choose between DuckDB (local, free) or DynamoDB (cloud, paid) by setting `USE_REAL_DYNAMODB=true/false` in `.env`. Both work identically from the application's perspective.

### Cost Optimization Strategy

**How Content Restrictions Reduce AI Costs:**

1. **Prevents Unnecessary API Calls**
   - Blocks restricted prompts BEFORE calling Gemini API
   - No API charges for blocked content
   - Example: If "violence" is restricted, prompt "write about violence" is blocked locally without API call

2. **Pre-validation Layer**
   - Checks happen in Python code (free)
   - Only valid prompts reach Gemini API (paid)
   - Reduces wasted API calls by 10-30% depending on restrictions

3. **Admin Control**
   - Admins define what content should never be generated
   - Prevents users from generating inappropriate content that would waste API credits
   - Protects against malicious or accidental expensive API usage

4. **Example Cost Savings:**
   ```
   Without Restrictions:
   - 1000 prompts/day × $0.00025/prompt = $0.25/day
   - Including 200 inappropriate prompts that get blocked after API call
   
   With Restrictions:
   - 800 valid prompts/day × $0.00025/prompt = $0.20/day
   - 200 blocked locally (no API call) = $0.00
   - Savings: $0.05/day = $1.50/month = $18/year
   ```

5. **Additional Benefits**
   - Prevents policy violations (saves review costs)
   - Reduces content moderation needs
   - Protects brand reputation
   - Ensures compliance with regulations

**Current AI Usage:**
- **Gemini API**: Content analysis, sentiment detection, keyword extraction, content generation, transformation
- **Whisper AI (Local)**: Audio/video transcription (no API costs)
- **pdfplumber/python-docx (Local)**: Document processing (no API costs)

**Cost Control Features:**
- ✅ Content restrictions (blocks before API call)
- ✅ Local processing for media files (Whisper, pdfplumber)
- ✅ DuckDB local storage (no cloud database costs)
- ✅ Cached analysis results (avoid re-analyzing same content)

📊 **See [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) for detailed cost analysis and savings calculations.**

## 🚧 Coming Soon Features

- Audio analysis
- Image analysis
- Video analysis
- Document analysis
- Image generation
- Video generation

## ☁️ AWS EC2 Deployment

### Quick EC2 Access Guide

After deploying to EC2, you need to access the dashboard using the EC2 instance's **public IP address**, not localhost.

**Step 1: Get your EC2 Public IP**

Run this command **on your EC2 instance** (via SSH):
```bash
curl http://checkip.amazonaws.com
```

This will return your public IP, for example: `54.123.45.67`

**Step 2: Access the Dashboard**

Open your browser and go to:
```
http://YOUR_EC2_PUBLIC_IP:8080
```

For example: `http://54.123.45.67:8080`

**Step 3: Verify Security Group**

Make sure your EC2 security group allows inbound traffic on port 8080:
- Type: Custom TCP
- Port: 8080
- Source: 0.0.0.0/0 (or your specific IP for better security)

### Common Issues

**Problem**: "Can't reach this page" or "Connection refused"

**Solutions**:
1. ✅ Use EC2 public IP, not `localhost` or private IP (172.x.x.x)
2. ✅ Check security group has port 8080 open
3. ✅ Verify dashboard is running: `ps aux | grep python`
4. ✅ Check dashboard logs for errors

**Problem**: Dashboard stops when SSH session closes

**Solution**: Use `screen` or `tmux` to keep it running:
```bash
# Install screen
sudo apt install screen

# Start a screen session
screen -S ashoka

# Run the dashboard
python run_dashboard.py

# Detach: Press Ctrl+A then D
# Reattach later: screen -r ashoka
```

### Production Deployment

For production, use Supervisor and Nginx (see `deployment_scripts/README.md`):
- Supervisor: Keeps the app running and auto-restarts on crashes
- Nginx: Reverse proxy for better performance and HTTPS support

### Updating EC2 After Code Changes

If you've made changes locally and need to update EC2:

**On Windows (push changes):**
```bash
# Stage all changes
git add .

# Commit with a message
git commit -m "Fix WebSocket connection and add EC2 deployment guide"

# Push to GitHub
git push origin main
```

**On EC2 (pull changes):**
```bash
# Navigate to project directory
cd ~/aws_hackathon_ai_4_bharat

# Stop the dashboard (if running in screen)
screen -r ashoka
# Press Ctrl+C to stop
# Press Ctrl+A then D to detach

# Or kill the process
pkill -f run_dashboard.py

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Start dashboard in screen
screen -S ashoka
python run_dashboard.py

# Wait for "Ready!" then detach: Ctrl+A, then D
```

## 📄 License

Built for AWS Hackathon 2026

## 🤝 Support

For issues or questions, please refer to SETUP.md and FEATURES.md for detailed documentation.
