# Ashoka - GenAI Governance Platform

A comprehensive AI-powered content governance platform built for the AWS Hackathon. Ashoka provides intelligent content analysis, multi-platform transformation, real-time monitoring, and security features.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Run the dashboard
python run_dashboard.py
```

Open http://localhost:8080 in your browser.

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
- Real-time alerts from content analysis
- Quality-based warnings
- Risk assessments
- Transformation success notifications

### 6. Security Dashboard (Admin Only)
- Login activity monitoring
- Security event tracking
- User session management
- Geographic and device information

### 7. Role-Based Access Control
- **User Role**: Standard access (default for signup)
- **Creator Role**: Content creation access (selectable during signup)
- **Admin Role**: Full access including Security tab (pre-configured)

## 🛠️ Technology Stack

- **Frontend**: NiceGUI (Python-based web framework)
- **AI/ML**: Google Gemini API (gemini-2.5-flash)
- **Database**: DuckDB (persistent local storage)
- **Authentication**: OTP-based with session management
- **Styling**: Tailwind CSS with custom brown theme

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

- **Primary Color**: Skinish Brown (#78350f, #92400e)
- **Background**: Cream/Beige gradients (#fff8f0, #f5e6d3)
- **Accents**: Amber for warnings, Red for errors, Green for success

## 📝 Environment Variables

Required in `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key_here
USE_GEMINI=true
MOCK_MODE=false
```

## 🔄 Data Persistence

All data is stored in `data/ashoka.duckdb`:
- User accounts and sessions
- Content analysis history
- Transform history
- Security logs
- Monitoring metrics

## 🚧 Coming Soon Features

- Audio analysis
- Image analysis
- Video analysis
- Document analysis
- Image generation
- Video generation

## 📄 License

Built for AWS Hackathon 2024

## 🤝 Support

For issues or questions, please refer to SETUP.md and FEATURES.md for detailed documentation.
