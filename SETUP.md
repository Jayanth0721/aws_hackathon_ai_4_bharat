# Setup Guide - Ashoka Platform

Complete setup instructions for the Ashoka GenAI Governance Platform.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
cd C:\_Personal_Project\aws_hackathon
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- nicegui>=2.5.0 (CRITICAL: upgraded from 1.4.0 for WebSocket support)
- google-genai>=0.2.0 (NEW SDK - replaces deprecated google-generativeai)
- duckdb>=0.9.0
- bcrypt>=4.0.0
- python-dotenv>=1.0.0
- Pillow>=10.0.0

**IMPORTANT SDK MIGRATION:**
- OLD SDK: `google-generativeai` (deprecated, causes "Gemini client not initialized" errors)
- NEW SDK: `google-genai` (required for proper functionality)
- If you have the old SDK installed, uninstall it first: `pip uninstall google-generativeai`

### 3. Get Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key

### 4. Configure Environment Variables

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
# Google Gemini Configuration
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-flash
USE_GEMINI=true

# NiceGUI Storage Secret (required for WebSocket connections)
STORAGE_SECRET=your_random_secret_key_here

# Database Configuration
DUCKDB_PATH=data/ashoka.duckdb

# Session Configuration
SESSION_TIMEOUT_MINUTES=30
OTP_EXPIRATION_MINUTES=5

# DynamoDB Configuration (optional - for AWS deployment)
USE_REAL_DYNAMODB=false
DYNAMODB_TABLE=ashoka_contentint
```

### 5. Initialize Database

The database will be automatically created on first run at `data/ashoka.duckdb`.

Default users are created automatically:
- **admin** / **admin123** (role: admin)
- **demo** / **demo123** (role: user)

### 6. Run the Application

```bash
python run_dashboard.py
```

Expected output:
```
🛡️  Starting Ashoka GenAI Governance Dashboard...
📊 Dashboard will be available at: http://localhost:8080
🔐 Authentication required - Login with OTP
🔄 Setting up default users...
✅ Admin user exists: admin / admin123 (role: admin)
✅ Demo user exists: demo / demo123 (role: user)
📊 Total users in database: 2
🤖 AI: Google Gemini (gemini-2.5-flash)
Ready! Open http://localhost:8080 in your browser
```

### 7. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8080
```

### 8. (Optional) Install Media Processing Dependencies

To enable audio and video analysis features:

#### Install yt-dlp

```bash
pip install yt-dlp
```

#### Install FFmpeg (Required for audio extraction)

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

#### Install Whisper AI (Required for transcription)

```bash
pip install openai-whisper
```

**Note**: Whisper requires PyTorch. It will be installed automatically, but may take some time.

#### Verify Media Processing Setup

After installing dependencies, restart the application:
```bash
python run_dashboard.py
```

Check the console for:
```
✅ yt-dlp is available for video processing
✅ Whisper model loaded successfully (base)
```

If you see these messages, media processing is ready to use!

## Login Process

1. Enter username and password
2. Click "Login"
3. Check console for OTP code (displayed in terminal)
4. Enter the 5-digit OTP
5. Click "Verify OTP"

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Make sure `.env` file exists and contains valid API key (use GEMINI_API_KEY, not GOOGLE_API_KEY)

### Issue: "Gemini client not initialized" or "ContentAnalyzer initialized without AI"
**Solution**: 
- Make sure you have the NEW `google-genai` package installed (not the old `google-generativeai`)
- Run: `pip uninstall google-generativeai && pip install google-genai`
- Verify: `pip show google-genai` should show version 1.66.0 or higher
- Restart the application completely (kill all Python processes)
- Clear Python cache: `find . -type d -name "__pycache__" -exec rm -rf {} +`

**Why this happens:**
- The old `google-generativeai` SDK (v0.8.6) is deprecated
- The new `google-genai` SDK (v1.66.0+) uses different imports: `from google import genai`
- Having the wrong SDK causes silent import failures, setting `GEMINI_AVAILABLE = False`

### Issue: "Model not found" or "404 NOT_FOUND"
**Solution**:
- Use a valid model name in `.env`: `GEMINI_MODEL=gemini-2.5-flash`
- Available models: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash, gemini-2.0-flash-001
- Do NOT use: gemini-2.0-flash-exp (experimental model, not available in production API)

**To verify available models:**
```python
python -c "from google import genai; import os; from dotenv import load_dotenv; load_dotenv(); client = genai.Client(api_key=os.getenv('GEMINI_API_KEY')); models = client.models.list(); [print(f'  - {m.name}') for m in models if 'gemini' in m.name.lower()]"
```

### Issue: "Module not found"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: "Port 8080 already in use"
**Solution**: 
- Stop other applications using port 8080
- Or modify port in `run_dashboard.py` (line with `ui.run(port=8080)`)

### Issue: "Database locked"
**Solution**: 
- Close all instances of the application
- Delete `data/ashoka.duckdb.wal` file
- Restart the application

### Issue: "OTP expired"
**Solution**: 
- OTP expires after 5 minutes
- Click "Login" again to generate new OTP

### Issue: "Users not persisting"
**Solution**: 
- Check that `data/` directory exists
- Verify `data/ashoka.duckdb` file is being created
- Check file permissions

### Issue: "yt-dlp not installed"
**Solution**:
- Run `pip install yt-dlp`
- Restart the application
- Verify installation: `yt-dlp --version`

### Issue: "Whisper not available"
**Solution**:
- Run `pip install openai-whisper`
- This will also install PyTorch (may take 5-10 minutes)
- Restart the application

### Issue: "FFmpeg not found"
**Solution**:
- Install FFmpeg (see step 8 above)
- Add FFmpeg to system PATH
- Verify: `ffmpeg -version`
- Restart terminal/application

### Issue: "Video processing failed"
**Solution**:
- Check if video file is corrupted or in unsupported format
- Ensure FFmpeg is installed and in PATH
- Try with a smaller video file first
- Try a different video
- Verify URL format is correct

### Issue: "Video too long"
**Solution**:
- Maximum supported duration is 2 hours
- Select a shorter video
- Or split long videos into segments

### Issue: "Rate limit exceeded"
**Solution**:
- Users can analyze 10 videos per hour
- Wait for the rate limit window to reset
- Admin users have unlimited access

## Creating New Users

### Via Signup Page

1. Click "Sign Up" on login page
2. Enter username, email, password
3. Select role (User or Creator)
4. Click "Sign Up"
5. Login with new credentials

### Via Python Console

```python
from src.services.auth_service import auth_service

# Create new user
success, message = auth_service.signup(
    username="newuser",
    email="newuser@ashoka.ai",
    password="password123",
    role="user"  # or "creator"
)
print(message)
```

## Database Management

### View Database Contents

```python
import duckdb

conn = duckdb.connect('data/ashoka.duckdb')

# View all users
print(conn.execute("SELECT * FROM ashoka_users").fetchall())

# View all sessions
print(conn.execute("SELECT * FROM ashoka_sessions").fetchall())

# View content analysis history
print(conn.execute("SELECT * FROM ashoka_contentint").fetchall())

conn.close()
```

### Reset Database

```bash
# Stop the application
# Delete database file
rm data/ashoka.duckdb
rm data/ashoka.duckdb.wal

# Restart application (will recreate database)
python run_dashboard.py
```

## Configuration Options

### Change Session Timeout

Edit `.env`:
```
SESSION_TIMEOUT_MINUTES=60  # Change from 30 to 60 minutes
```

### Change OTP Expiration

Edit `.env`:
```
OTP_EXPIRATION_MINUTES=10  # Change from 5 to 10 minutes
```

### Change Port

Edit `run_dashboard.py`:
```python
ui.run(
    title='Ashoka - GenAI Governance Platform',
    favicon='🛡️',
    dark=False,
    reload=False,
    port=8081  # Change from 8080 to 8081
)
```

## Development Mode

For development with auto-reload:

```python
ui.run(
    title='Ashoka - GenAI Governance Platform',
    favicon='🛡️',
    dark=False,
    reload=True,  # Enable auto-reload
    port=8080
)
```

## Production Deployment

For production deployment:

1. Set strong passwords for default users
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Set `reload=False` in `ui.run()`
5. Use a production-grade database (PostgreSQL, MySQL)
6. Implement proper logging and monitoring
7. Set up backup strategy for database

## Next Steps

- Read FEATURES.md for detailed feature documentation
- Read CREDENTIALS.md for user management
- Start using the platform!
