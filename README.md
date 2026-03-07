# Ashoka - GenAI Governance & Observability Platform

> **Intelligent Content Governance with AI-Powered Analysis, Generation, and Multi-Platform Transformation**

A comprehensive enterprise-grade platform that combines AI content intelligence, automated quality monitoring, multi-platform content transformation, and robust security governance—all in one unified dashboard.

---

## 🌟 What is Ashoka?

Ashoka is a next-generation GenAI governance platform designed to help organizations, content creators, and enterprises manage their AI-generated and user-created content with confidence. It provides real-time content analysis, quality scoring, risk assessment, and automated transformation for multiple social media platforms—while maintaining strict governance and security controls.

### Why Ashoka?

In today's AI-driven content landscape, organizations face critical challenges:
- **Quality Control**: Ensuring AI-generated content meets standards
- **Risk Management**: Detecting policy violations, toxicity, and inappropriate content
- **Multi-Platform Publishing**: Adapting content for different social media platforms
- **Cost Optimization**: Managing AI API costs effectively
- **Security & Compliance**: Maintaining audit trails and access controls

Ashoka addresses all these challenges in a single, intuitive platform.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio/video processing)
- Google Gemini API key

### Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

The script will automatically:
- Check Python version
- Install FFmpeg (if needed)
- Install Python dependencies
- Create .env file
- Launch the dashboard

### Manual Setup

```bash
# 1. Install FFmpeg (required for audio/video processing)
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
# Windows: winget install --id=Gyan.FFmpeg -e

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Run the dashboard
python run_dashboard.py
```

Open http://localhost:8080 in your browser.

---

## 🔐 Default Credentials

- **Admin User**: `admin` / `admin123` (full access including Security tab)
- **Demo User**: `demo` / `demo123` (standard user access)
- **Creator Role**: Available during signup for content creation access

---

## ✨ Core Features

### 1. 🧠 Content Intelligence & Analysis
**AI-powered content analysis with comprehensive insights**

- **Multi-Format Support**: Text, Audio, Video, Images, Documents (PDF, DOCX)
- **Sentiment Analysis**: Positive, Negative, Neutral with confidence scores
- **Quality Scoring**: 0-100% quality metrics based on multiple factors
- **Keyword Extraction**: Automatic identification of key terms
- **Topic Detection**: Content categorization and theme identification
- **Analysis History**: Track all analyzed content with reload capability

**Quality Score Factors:**
- Sentiment (negative content reduces score)
- Confidence levels
- Content length and completeness
- Keyword richness
- Topic diversity

### 2. 🎨 AI Content Generator
**Create professional content using Google Gemini AI**

- **Text Generation**: Professional emails, articles, social posts, notes
- **Image Generation**: AI-powered image creation using Son of Ashoka API
  - **Cost-Optimized**: Cloudflare Workers wrapper for efficient processing
  - **Scalable**: Better computational power distribution
  - **Fast**: 10-30 second generation time
  - **Download**: Save generated images locally
- **Prompt-Based**: Natural language descriptions
- **Content Restrictions**: Admin-controlled keyword blocking for governance
- **Integration**: Use generated content directly in transformer

**Image Generation Benefits:**
- No direct API costs (uses Cloudflare Workers)
- Automatic load balancing
- Global edge network distribution
- Reduced latency

### 3. 🔄 Multi-Platform Content Transformer
**Transform content for different social media platforms**

- **Supported Platforms**: LinkedIn, Twitter/X, Instagram, Facebook, Threads, Blog
- **Tone Customization**: Professional, Casual, Storytelling
- **Hashtag Generation**: Optional platform-specific hashtags
- **Batch Processing**: Transform for multiple platforms simultaneously
- **Transform History**: Track and reload previous transformations
- **Role-Based Access**: Admin and Creator roles only

**Use Cases:**
- Repurpose blog posts for social media
- Adapt professional content for casual platforms
- Create platform-specific campaigns from single source
- Maintain consistent messaging across channels

### 4. 📊 Real-Time Monitoring
**Comprehensive system and content performance tracking**

- **Performance Trends**: AWS EC2-style line graphs for 24-hour metrics
- **Quality Metrics**: Average scores, distribution, trends
- **Risk Assessment**: Toxicity detection, policy violations
- **Operation Metrics**: Success rates, error tracking
- **System Health**: API status, database connectivity, AI model performance
- **Auto-Refresh**: Updates every 10 minutes

**Monitored Metrics:**
- Content processing rate
- Quality score trends
- Risk alert frequency
- API response times
- Storage utilization

### 5. 🚨 Alerts & Notifications
**Intelligent alerting system with quality-based warnings**

- **Quality Alerts**:
  - Critical: < 60% quality score (immediate review)
  - Warning: < 80% quality score (review recommended)
  - Success: ≥ 85% quality score (high quality)
- **Sentiment Alerts**: Negative sentiment with high confidence
- **Risk Alerts**: Policy violations, toxicity, backlash risk
- **Filter Options**: All, Critical, Warning, Info, Success
- **Real-Time Updates**: Auto-refresh every 10 minutes
- **24-Hour Window**: Recent alerts with time tracking

**Alert Insights:**
- Platform health indicators
- Content quality trends
- Risk exposure levels
- Successful operations count

### 6. 🔒 Security Dashboard (Admin Only)
**Comprehensive security monitoring and governance**

- **Login Activity**: Track all authentication attempts
- **Security Events**: Monitor password changes, OTP generation, session creation
- **User Session Management**: Active session tracking
- **AI Content Restrictions**:
  - Define blocked keywords/phrases
  - Prevent inappropriate content generation
  - Reduce AI API costs by blocking invalid prompts
  - Admin-only configuration for governance
- **Audit Trail**: Complete security event history
- **Access Control**: Role-based permissions

**Security Benefits:**
- Prevent policy violations before they happen
- Reduce wasted AI API calls
- Maintain compliance with content policies
- Track user behavior and access patterns

### 7. 👥 Role-Based Access Control (RBAC)
**Granular permissions for different user types**

- **User Role**: Standard access to analysis and viewing
- **Creator Role**: Content creation and transformation access
- **Admin Role**: Full access including security and restrictions
- **Feature Locking**: Visual indicators for restricted features
- **Personalized Dashboard**: Role-specific content and metrics

---

## 🛠️ Complete Technology Stack

### Frontend Layer
- **NiceGUI** v2.5.0+ - Python-based reactive web framework
- **Tailwind CSS** - Modern utility-first styling
- **JavaScript** - Client-side interactions and WebSocket support
- **Custom Theme** - Teal/cyan gradient with dark mode

### Backend Layer
- **Python** 3.8+ - Core application language
- **Async/Await** - Non-blocking operations
- **RESTful API** - Standard API patterns

### AI & Machine Learning
- **Google Gemini API** (gemini-2.5-flash)
  - Content analysis and sentiment detection
  - Text generation and transformation
  - Quality scoring and keyword extraction
  - Audio/video transcription and analysis
  - SDK: `google-genai` v1.66.0+
- **Son of Ashoka API** (Cloudflare Workers)
  - AI image generation (FREE)
  - Global edge distribution
  - Automatic load balancing

### Document Processing
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX document processing
- **moviepy** - Video processing
- **FFmpeg** - Audio/video codec support
- **Pillow** - Image processing

### Database & Storage
- **DuckDB** - Local file-based database (default)
- **DynamoDB** - AWS cloud database (optional)
- **File Storage** - Local uploads directory

### Cloud & Infrastructure
- **AWS EC2** - Application hosting and deployment
- **AWS DynamoDB** - Optional cloud database for production
- **Cloudflare Workers** - Image generation API (Son of Ashoka)
- **No-IP / Dynamic DNS** - Domain management for EC2

### Authentication & Security
- **OTP-based Authentication**: Secure login with time-limited codes
- **Session Management**: Token-based with configurable timeout
- **Password Hashing**: Secure credential storage
- **Role-Based Access**: Granular permission system

---

## ☁️ AWS Services Used

This project leverages the following AWS services:

### Core Services

1. **Amazon EC2 (Elastic Compute Cloud)**
   - **Purpose**: Application hosting and deployment
   - **Instance Type**: t2.micro or t2.small (Free Tier eligible)
   - **Configuration**: Ubuntu Server with Python 3.8+
   - **Access**: Public IP with port 8080 exposed
   - **Cost**: Free Tier: 750 hours/month, After: ~$8-15/month

2. **Amazon DynamoDB** (Optional)
   - **Purpose**: Cloud-based NoSQL database for production
   - **Tables**: Users, content analysis, transform history, security events
   - **Mode**: On-demand pricing
   - **Alternative**: DuckDB (local, file-based) for development
   - **Cost**: Free Tier: 25 GB storage, After: ~$5-20/month

### Supporting Infrastructure

3. **Cloudflare Workers** (Not AWS, but integrated)
   - **Purpose**: AI image generation (Son of Ashoka API)
   - **Benefit**: FREE image generation (no AWS costs)
   - **Performance**: Global edge network distribution
   - **Cost**: $0/month

### Deployment Tools

4. **AWS Security Groups**
   - **Purpose**: Firewall rules for EC2 instance
   - **Configuration**: Port 8080 (HTTP), Port 22 (SSH)
   - **Cost**: Free

5. **AWS Elastic IP** (Optional)
   - **Purpose**: Static IP address for EC2 instance
   - **Benefit**: Prevents IP changes on instance restart
   - **Cost**: Free while attached to running instance

### Third-Party Integrations

6. **No-IP / Dynamic DNS**
   - **Purpose**: Domain name mapping (e.g., ashoka-ai.hopto.org)
   - **Benefit**: Human-readable URL instead of IP address
   - **Cost**: Free tier available

### Cost Summary

**Minimum Setup (Free Tier):**
- EC2 t2.micro: Free (750 hours/month)
- DuckDB (local): Free
- Cloudflare Workers: Free
- **Total: $0/month** (within Free Tier limits)

**Production Setup:**
- EC2 t2.small: ~$15/month
- DynamoDB: ~$10/month
- Elastic IP: Free (when attached)
- **Total: ~$25/month**

**With AI API Costs:**
- Google Gemini API: ~$5-15/month (based on usage)
- **Grand Total: ~$30-40/month**

For detailed cost breakdown, see [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md).

---

## 💰 Cost Optimization

### AI Processing Cost Breakdown

| Feature | Tool Used | Type | Cost | Notes |
|---------|-----------|------|------|-------|
| Text Analysis | Google Gemini | Cloud API | ~$0.001/request | Paid |
| Content Generation | Google Gemini | Cloud API | ~$0.002/request | Paid |
| Content Transformation | Google Gemini | Cloud API | ~$0.001/platform | Paid |
| **Image Generation** | **Son of Ashoka** | **Cloudflare Workers** | **FREE** | **Cost-optimized** |
| Audio Transcription | Google Gemini | Cloud API | ~$0.001/request | Paid |
| Video Transcription | Gemini + MoviePy | Cloud API | ~$0.001/request | Paid |
| PDF Extraction | pdfplumber | Local | FREE | No API calls |
| DOCX Extraction | python-docx | Local | FREE | No API calls |

### Why Son of Ashoka for Image Generation?

**Traditional Approach:**
- Direct API calls to image generation services
- Pay per image ($0.02-0.10 per image)
- Rate limits and throttling
- Single point of failure

**Son of Ashoka Approach (Cloudflare Workers):**
- ✅ **FREE**: No per-image costs
- ✅ **Scalable**: Automatic load distribution
- ✅ **Fast**: Global edge network (10-30s generation)
- ✅ **Reliable**: Built-in redundancy and failover
- ✅ **Optimized**: Better computational power allocation

**Monthly Cost Estimate:**
- **Local Mode** (DuckDB): $5-15/month (Gemini API only)
- **Cloud Mode** (DynamoDB): $10-30/month (Gemini + AWS)
- **Image Generation**: $0/month (Cloudflare Workers)

For detailed cost analysis, see [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md).

---

## 📁 Project Structure

```
ashoka/
├── src/
│   ├── ui/
│   │   ├── dashboard.py           # Main dashboard UI
│   │   └── auth_page.py           # Login/Signup UI
│   ├── services/
│   │   ├── gemini_client.py       # Google Gemini integration
│   │   ├── image_generator.py     # Son of Ashoka image generation
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── content_analyzer.py    # Content analysis engine
│   │   ├── content_transformer.py # Multi-platform transformation
│   │   ├── security_service.py    # Security and restrictions
│   │   ├── monitoring_service.py  # Metrics and monitoring
│   │   ├── document_processor.py  # PDF/DOCX processing
│   │   └── media_processor.py     # Audio/video processing
│   ├── database/
│   │   ├── duckdb_schema.py       # Database schema
│   │   ├── db_factory.py          # Database factory
│   │   └── mock_storage.py        # Storage implementations
│   ├── models/
│   │   ├── auth.py                # User/Session models
│   │   ├── monitoring.py          # Monitoring models
│   │   └── audit.py               # Audit models
│   └── utils/
│       ├── logging.py             # Logging configuration
│       ├── timestamp.py           # Time utilities
│       └── id_generator.py        # ID generation
├── data/
│   ├── ashoka.duckdb              # Main database
│   └── uploads/                   # Uploaded files
├── deployment_scripts/
│   ├── deploy.sh                  # Deployment script
│   ├── setup_ec2.sh               # EC2 setup
│   ├── nginx_ashoka.conf          # Nginx configuration
│   └── supervisor_ashoka.conf     # Supervisor configuration
├── tests/
│   ├── test_preservation_properties.py
│   └── test_websocket_connection_bugfix.py
├── run_dashboard.py               # Main entry point
├── requirements.txt               # Python dependencies
├── start.sh / start.bat           # Automated setup scripts
└── .env                           # Environment configuration
```

---

## 🎨 UI Theme & Design

### Modern Teal/Turquoise Theme

**Light Mode:**
- Warm beige/cream backgrounds (#f3efe8)
- Teal accents (#0f766e, #0b4f6c)
- Clean card-based layout
- Glassmorphism effects

**Dark Mode:**
- Dark teal/gray backgrounds (#0f172a, #1e293b)
- Light cyan text (#e2e8f0)
- High contrast for readability
- Smooth transitions

**Status Colors:**
- 🟢 Green: Success, high quality
- 🟠 Orange: Warnings, review needed
- 🔴 Red: Critical, immediate action
- 🔵 Blue: Information, neutral

### Recent UI/UX Improvements (March 2026)

**Command Center Enhancements:**
- Session timer moved to header (top-right) with clock icon
- Date-time display in Command Center with calendar icon (07-Mar-2026 10:05 PM IST)
- Role badge display (USER/CREATOR/ADMIN) in Command Center
- Purple "Workspace for {username}" text (#a855f7) for personalization
- Cleaner, more intuitive layout

**Help & Support:**
- Renamed "Help & Support" to "Help" for brevity
- Quick Help sections (Getting Started, Common Issues, Feature Access) now use full width
- Contact Support cards changed to horizontal layout for better space utilization

**Content Intelligence:**
- Analysis section headers changed from white to black for better visibility
- Clear button now clears both text input AND analysis results
- Improved user feedback and interaction flow

**Monitoring & Alerts:**
- Monitoring section hidden for user role (visible only for creator/admin)
- Removed "Refresh Metrics" button from Monitoring panel (auto-refresh only)
- Removed "Refresh Alerts" button from Alerts panel (auto-refresh only)
- System Health moved from Overview to Alerts & Notifications panel
- Minimum warning count set to 1 for better alert visibility

**Overview Panel:**
- System Health section removed from Overview (now in Alerts panel)
- Enhanced platform details with Core Services and How It Works sections
- Cleaner focus on content metrics and platform capabilities

**Authentication:**
- OTP input speed reduced by 0.5 seconds for better user experience
- Smoother authentication flow

---

## 📝 Environment Variables

Create a `.env` file with:

```bash
# AI Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
USE_GEMINI=true

# Database Configuration
USE_REAL_DYNAMODB=false          # false = DuckDB (local), true = DynamoDB (AWS)
DUCKDB_PATH=data/ashoka.duckdb

# AWS Configuration (only if USE_REAL_DYNAMODB=true)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Session Configuration
SESSION_TIMEOUT_MINUTES=30
STORAGE_SECRET=your_secure_random_string_here

# Image Generation (Son of Ashoka API)
# No configuration needed - uses Cloudflare Workers
```

**IMPORTANT NOTES:**
- Use `GEMINI_API_KEY` (not `GOOGLE_API_KEY`) for the Gemini API key
- Use `GEMINI_MODEL=gemini-2.5-flash` (available models: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash)
- Do NOT use `gemini-2.0-flash-exp` (experimental model, not available in production)
- `STORAGE_SECRET` is REQUIRED for NiceGUI WebSocket connections

### Database Options

**Local Mode (Default - Recommended):**
- ✅ Uses DuckDB (file-based database)
- ✅ No AWS credentials needed
- ✅ No cloud costs
- ✅ Perfect for development
- ✅ Data stored in `data/ashoka.duckdb`

**Cloud Mode (Optional - Production):**
- Uses AWS DynamoDB
- Requires AWS credentials
- Provides scalability and high availability
- Estimated cost: $5-20/month

---

## 🔄 Data Persistence

All data is stored in `data/ashoka.duckdb`:
- ✅ User accounts and sessions
- ✅ Content analysis history
- ✅ Transform history
- ✅ Security logs and events
- ✅ Monitoring metrics
- ✅ Alert history
- ✅ Quality scores and trends

**Backup Recommendation:**
```bash
# Backup database
cp data/ashoka.duckdb data/ashoka_backup_$(date +%Y%m%d).duckdb

# Restore database
cp data/ashoka_backup_20260306.duckdb data/ashoka.duckdb
```

---

## 🔧 Common Issues & Quick Fixes

### WebSocket Connection Failed
**Symptom**: Page loads but buttons don't work

**Fix**: Upgrade NiceGUI to 2.5.0+
```bash
pip uninstall nicegui && pip install "nicegui>=2.5.0"
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Gemini API Not Working
**Symptom**: "Gemini client not initialized" error

**Fix**: Install correct SDK
```bash
pip uninstall google-generativeai -y
pip install google-genai
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Model Not Found Error
**Symptom**: 404 NOT_FOUND when generating content

**Fix**: Use correct model name in `.env`
```bash
GEMINI_MODEL=gemini-2.5-flash
```

For detailed troubleshooting, see [SETUP.md](SETUP.md) and [HOSTING.md](HOSTING.md).

---

## ☁️ AWS EC2 Deployment

### Quick Access Guide

After deploying to EC2, access the dashboard using your EC2 instance's public IP:

**Get your EC2 Public IP:**
```bash
curl http://checkip.amazonaws.com
```

**Access the Dashboard:**
```
http://YOUR_EC2_PUBLIC_IP:8080
```

**Security Group Requirements:**
- Type: Custom TCP
- Port: 8080
- Source: 0.0.0.0/0 (or your specific IP)

### Running Dashboard on EC2

**Start in background:**
```bash
nohup python run_dashboard.py > dashboard.log 2>&1 &
```

**View logs:**
```bash
tail -f dashboard.log
```

**Stop dashboard:**
```bash
pkill -f run_dashboard.py
```

### Production Deployment

For production, use Supervisor and Nginx (see `deployment_scripts/README.md`):
- Supervisor: Auto-restart on crashes
- Nginx: Reverse proxy for HTTPS support

### Updating EC2 After Code Changes

See [EC2_UPDATE_GUIDE.md](EC2_UPDATE_GUIDE.md) for detailed instructions on pushing changes from local to EC2.

---

## 📚 Documentation

### User Guides
- **[WORKFLOW.md](WORKFLOW.md)** - Complete workflows, use cases, and best practices
  - User roles and permissions
  - Step-by-step workflows for all features
  - Real-world scenarios (Social Media Manager, Compliance Officer, Marketing Team)
  - Troubleshooting and optimization tips

### Technical Documentation
- **[SCRIPTS.md](SCRIPTS.md)** - Complete technical reference
  - Platform architecture overview
  - Startup scripts (start.sh, start.bat, run_dashboard.py)
  - Deployment scripts and configurations
  - Service architecture and API integration
  - Database management and automation
  - Performance optimization strategies

### Setup & Deployment
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[EC2_UPDATE_GUIDE.md](EC2_UPDATE_GUIDE.md)** - EC2 deployment and updates
- **[AWS_DEPLOYMENT_SUMMARY.md](AWS_DEPLOYMENT_SUMMARY.md)** - AWS deployment overview
- **[HOSTING.md](HOSTING.md)** - Hosting and domain configuration

### Feature Documentation
- **[FEATURES.md](FEATURES.md)** - Complete feature documentation
- **[COST_OPTIMIZATION.md](COST_OPTIMIZATION.md)** - Cost analysis and optimization
- **[RECENT_FIXES.md](RECENT_FIXES.md)** - Latest updates and bug fixes

---

## 🎯 Use Cases

### For Content Creators
- Analyze content quality before publishing
- Transform blog posts for multiple social platforms
- Generate AI images for content illustration (FREE via Cloudflare)
- Monitor content performance and quality trends
- **Example**: Social Media Manager creating daily posts across LinkedIn, Twitter, and Instagram in 30 minutes

### For Marketing Teams
- Ensure brand consistency across platforms
- Detect policy violations before publishing
- Track content quality metrics
- Automate multi-platform content distribution
- **Example**: Marketing team launching multi-channel campaign with quality assurance in 2 hours

### For Enterprises
- Govern AI-generated content
- Maintain security and compliance
- Monitor user activity and access
- Control content generation with restrictions
- **Example**: Compliance Officer conducting weekly audits with complete audit trails

### For Startups
- Create professional content on a budget
- Cost-optimized image generation (FREE)
- Scale content production efficiently
- **Example**: Founder creating weekly content for <$1/year

### For Developers
- Integrate AI capabilities into applications
- Build content governance workflows
- Monitor AI API usage and costs
- Implement role-based access control

**For detailed workflows and scenarios, see [WORKFLOW.md](WORKFLOW.md)**

---

## 🚀 Performance & Scalability

- **Fast Load Times**: Optimized database queries with caching
- **Async Processing**: Non-blocking AI operations
- **Auto-Refresh**: Background updates without page reload
- **Session Management**: Configurable timeout (15-120 minutes)
- **Scalable Architecture**: Ready for cloud deployment

---

## 🔒 Security Features

- **OTP Authentication**: Time-limited one-time passwords
- **Session Tokens**: Secure token-based sessions
- **Password Hashing**: Industry-standard encryption
- **Role-Based Access**: Granular permissions
- **Audit Logging**: Complete activity tracking
- **Content Restrictions**: Admin-controlled blocking
- **WebSocket Security**: Secure real-time connections

---

## 📄 License

Built for AWS Hackathon 2026

---

## 🤝 Support & Contributing

### Getting Help
1. **Documentation**: Check the comprehensive docs in the repository
   - [WORKFLOW.md](WORKFLOW.md) - User workflows and best practices
   - [SCRIPTS.md](SCRIPTS.md) - Technical reference and automation
   - [SETUP.md](SETUP.md) - Setup and troubleshooting
2. **Common Issues**: See troubleshooting sections in documentation
3. **Use Cases**: Review real-world scenarios in [WORKFLOW.md](WORKFLOW.md)

### Quick Links
- **User Workflows**: [WORKFLOW.md](WORKFLOW.md) - Complete guide for all user roles
- **Technical Details**: [SCRIPTS.md](SCRIPTS.md) - Architecture, scripts, and automation
- **Cost Analysis**: [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) - Detailed cost breakdown

---

## 🌟 What Makes Ashoka Special?

1. **All-in-One Platform**: Analysis, generation, transformation, and monitoring in one place
2. **Cost-Optimized**: Smart use of local processing and Cloudflare Workers
3. **Enterprise-Ready**: RBAC, security, audit trails, and governance
4. **User-Friendly**: Intuitive UI with dark mode and responsive design
5. **Scalable**: Works locally or in the cloud
6. **Open Architecture**: Easy to extend and customize

---

**Built with ❤️ for intelligent content governance**
