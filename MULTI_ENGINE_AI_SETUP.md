# Multi-Engine AI Implementation Guide

## Overview

The Ashoka platform now supports **3 AI engines** with automatic fallback:
1. **Engine 1: Google Gemini AI** (Primary)
2. **Engine 2: Sarvam AI** (Secondary - Indian AI, great for Indian languages)
3. **Engine 3: Google Gemini AI Backup** (Tertiary - Additional Gemini API key)

When one engine fails or hits rate limits, the system automatically falls back to the next available engine.

---

## What Was Implemented

### 1. New Multi-Engine AI Client (`src/services/ai_engine.py`)
- Unified interface for all 3 AI engines
- Automatic fallback mechanism (Gemini → Sarvam AI → Gemini Engine 3)
- Rate limit tracking and display
- Engine priority configuration

### 2. Updated Services
- `src/services/content_analyzer.py` - Now uses multi-engine client
- `src/services/content_transformer.py` - Now uses multi-engine client

### 3. Updated Dependencies (`requirements.txt`)
```bash
google-genai>=0.2.0      # Gemini AI
# Sarvam AI uses REST API (no package needed)
```

### 4. Environment Configuration (`.env`)
```bash
# AI Engine Configuration
PRIMARY_AI_ENGINE=gemini

# Gemini Engine 1 (Primary)
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash
# Rate Limit: 50 requests/day (free tier)

# Sarvam AI Engine 2 (Secondary - Backup)
SARVAM_API_KEY=your_key_here
SARVAM_MODEL=sarvam-m
# Rate Limit: Check https://www.sarvam.ai
# Excellent for Indian languages

# Gemini Engine 3 (Tertiary - Additional Gemini Backup)
GEMINI_ENGINE3=your_second_gemini_key_here
GEMINI_MODEL_ENGINE3=gemini-2.0-flash
# Rate Limit: 50 requests/day (free tier)
# Use a different Gemini API key for additional quota
```

### 5. UI Enhancements
- **Settings Dialog**: New "AI Engine Status" card showing:
  - Active engines
  - Rate limits for each engine
  - Current availability status

### 6. Other Fixes
- ✅ OTP input speed set to 1 second (was 0.5 seconds)
- ✅ Topic chip icons removed (no more up/down arrows)
- ✅ Calendar icon kept in Command Center
- ✅ Date-time and role text made black and bold

---

## Installation Steps

### Step 1: No New Dependencies Needed!
Sarvam AI uses REST API, so no additional packages required.

### Step 2: Update Environment Variables
Edit your `.env` file and add:

```bash
# Switch to gemini-2.0-flash (50 requests/day instead of 20)
GEMINI_MODEL=gemini-2.0-flash

# Add Sarvam AI key (get from https://www.sarvam.ai)
SARVAM_API_KEY=your-sarvam-key-here
SARVAM_MODEL=sarvam-m

# Add Gemini Engine 3 (optional - for additional quota)
GEMINI_ENGINE3=your-second-gemini-key-here
GEMINI_MODEL_ENGINE3=gemini-2.0-flash

# Set primary engine (gemini or sarvam)
PRIMARY_AI_ENGINE=gemini
```

### Step 3: Restart Application
```bash
# Stop current process
pkill -f run_dashboard.py

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Start application
python run_dashboard.py
```

---

## How It Works

### Automatic Fallback Flow

```
User Request
    ↓
Try Engine 1 (Gemini)
    ↓
Success? → Return Result ✓
    ↓
Failed? → Try Engine 2 (Sarvam AI)
    ↓
Success? → Return Result ✓
    ↓
Failed? → Try Engine 3 (Gemini Backup)
    ↓
Success? → Return Result ✓
    ↓
All Failed? → Return Error ✗
```

### Engine Priority

The default engine priority is: **Gemini → Sarvam AI → Gemini Engine 3**

You can set the primary engine in `.env`:

```bash
# Use Gemini first (recommended)
PRIMARY_AI_ENGINE=gemini

# Use Sarvam first (for Indian languages)
PRIMARY_AI_ENGINE=sarvam
```

**Note:** Gemini Engine 3 is always used as the final fallback regardless of PRIMARY_AI_ENGINE setting.

---

## Rate Limits (Free Tier)

| Engine | Model | Free Tier Limit | Cost After |
|--------|-------|----------------|------------|
| **Gemini Engine 1** | gemini-2.0-flash | 50 requests/day | Free |
| **Gemini Engine 1** | gemini-2.5-flash | 20 requests/day | Free |
| **Sarvam AI** | sarvam-m | Check website | Competitive |
| **Sarvam AI** | sarvam-2b-v0.5 | Free tier available | Competitive |
| **Gemini Engine 3** | gemini-2.0-flash | 50 requests/day | Free |

**Note:** Sarvam AI is an Indian AI company with excellent support for Indian languages.

### Recommended Configuration

**For Maximum Free Usage (100 requests/day):**
```bash
PRIMARY_AI_ENGINE=gemini
GEMINI_API_KEY=your_first_key       # 50 requests/day
GEMINI_MODEL=gemini-2.0-flash
SARVAM_API_KEY=your_key             # Backup
GEMINI_ENGINE3=your_second_key      # 50 more requests/day
GEMINI_MODEL_ENGINE3=gemini-2.0-flash
```

**For Indian Language Content:**
```bash
PRIMARY_AI_ENGINE=sarvam            # Best for Hindi, Tamil, Kannada, etc.
GEMINI_API_KEY=your_key             # Backup
GEMINI_ENGINE3=your_second_key      # Additional backup
```

---

## Viewing AI Engine Status

1. Login to dashboard
2. Click **Settings** icon (top-right)
3. View **AI Engine Status** card at the top
4. See:
   - Active engines
   - Rate limits for each engine
   - Current availability

---

## Supported Features

All 3 engines support:
- ✅ Text analysis (sentiment, keywords, topics)
- ✅ Content generation
- ✅ Content transformation (multi-platform)
- ✅ Summarization
- ✅ Quality scoring

---

## Troubleshooting

### Issue: Sarvam AI 400 Bad Request Error

**Symptoms:**
- Error message: "400 Bad Request" when using Sarvam AI
- System falls back to Gemini Engine 3

**Root Cause:**
Sarvam AI API requires exact request format with specific headers and payload structure.

**Solution:**
The system now uses the correct format:
```bash
# Endpoint
POST https://api.sarvam.ai/v1/chat/completions

# Headers
Authorization: Bearer {api_key}
Content-Type: application/json

# Payload
{
  "model": "sarvam-m",
  "messages": [
    {"role": "system", "content": "system instruction"},
    {"role": "user", "content": "user prompt"}
  ],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Testing with curl:**
```bash
curl -X POST https://api.sarvam.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sarvam-m",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

If you still get 400 errors:
1. Verify your API key is valid
2. Check Sarvam AI documentation for API changes
3. Ensure model name is correct (use "sarvam-m")
4. System will automatically fall back to Gemini Engine 3

### Issue: "No AI engines available"

**Solution:**
1. Check API keys are set in `.env`
2. Verify keys are valid
3. Install required packages: `pip install openai google-genai`
4. Restart application

### Issue: "All AI engines failed"

**Possible Causes:**
1. All engines hit rate limits
2. Invalid API keys
3. Network connectivity issues

**Solution:**
1. Wait for rate limit reset (check logs for retry time)
2. Verify API keys are correct
3. Check internet connection
4. Try switching primary engine

### Issue: OpenAI not working

**Solution:**
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Ensure you have credits: https://platform.openai.com/usage
4. Restart application

### Issue: Sarvam AI not working

**Solution:**
1. Get API key from https://www.sarvam.ai
2. Add to `.env`: `SARVAM_API_KEY=...`
3. Check API endpoint is correct in `src/services/ai_engine.py`
4. Verify Sarvam AI API documentation for latest changes

---

## Testing the Setup

### Test 1: Check Available Engines
```python
from src.services.ai_engine import ai_client

print("Available engines:", ai_client.get_available_engines())
print("Rate limits:", ai_client.get_rate_limits())
```

### Test 2: Test Content Analysis
1. Login to dashboard
2. Go to Content Intelligence
3. Enter text: "This is a test"
4. Click "Analyze Text"
5. Check logs to see which engine was used

### Test 3: Force Fallback
1. Set invalid Gemini key
2. Try analysis
3. Should automatically use OpenAI
4. Check logs for fallback message

---

## Logs to Monitor

Watch for these log messages:

```
✓ Gemini initialized: gemini-2.0-flash
✓ Sarvam AI initialized: sarvam-m
✓ Gemini Engine 3 initialized: gemini-2.0-flash

Multi-engine AI initialized. Priority: ['gemini', 'sarvam', 'gemini3']
Available engines: [AIEngine.GEMINI, AIEngine.SARVAM, AIEngine.GEMINI3]

Attempting generation with gemini
✓ Generation successful with gemini

✗ gemini failed: 429 RESOURCE_EXHAUSTED
Attempting generation with sarvam
✓ Generation successful with sarvam

✗ sarvam failed: 400 Bad Request
Attempting generation with gemini3
✓ Generation successful with gemini3
```

---

## Cost Optimization Tips

1. **Use Gemini 2.0-flash** (50 free requests/day)
2. **Set OpenAI as backup** (only used when Gemini fails)
3. **Monitor usage** in Settings → AI Engine Status
4. **Upgrade to paid tier** when needed for production

---

## Migration from Old System

The old `gemini_client.py` is still available but no longer used. The new `ai_engine.py` provides:
- ✅ Multiple engine support
- ✅ Automatic fallback
- ✅ Better error handling
- ✅ Rate limit tracking
- ✅ Engine switching

No code changes needed in your application - the services automatically use the new multi-engine client.

---

## Future Enhancements

Potential additions:
- [ ] Add more AI engines (Anthropic Claude, Cohere, etc.)
- [ ] Implement request caching to reduce API calls
- [ ] Add usage analytics dashboard
- [ ] Implement smart engine selection based on task type
- [ ] Add cost tracking per engine

---

## Support

For issues or questions:
1. Check logs: `tail -f dashboard.log`
2. Verify API keys in `.env`
3. Test each engine individually
4. Check rate limits in Settings

---

**Built with ❤️ for intelligent content governance**
