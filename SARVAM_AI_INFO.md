# Sarvam AI - Complete Guide

## What is Sarvam AI?

**Sarvam AI** is an Indian AI company focused on building AI models for Indian languages and contexts. It's a great alternative to international AI providers, especially for Indian content.

Website: https://www.sarvam.ai

---

## Capabilities

### ✅ Supported Features

1. **Text Generation**
   - Create content in multiple languages
   - Generate articles, posts, emails
   - Creative writing

2. **Text Analysis**
   - Sentiment analysis (Positive/Negative/Neutral)
   - Keyword extraction
   - Topic identification
   - Content summarization

3. **Content Transformation**
   - Multi-platform adaptation
   - Tone conversion (Professional/Casual/Formal)
   - Language translation

4. **Multilingual Support**
   - **Strong support for Indian languages:**
     - Hindi
     - Tamil
     - Kannada
     - Telugu
     - Malayalam
     - Bengali
     - Marathi
     - Gujarati
   - English

### ✅ All Ashoka Features Supported

Sarvam AI supports ALL the analysis types in Ashoka:
- ✅ Content Intelligence & Analysis
- ✅ AI Content Generation
- ✅ Multi-Platform Content Transformation
- ✅ Sentiment Analysis
- ✅ Quality Scoring
- ✅ Keyword & Topic Extraction

---

## Why Use Sarvam AI?

### Advantages:

1. **Indian Language Support**
   - Better understanding of Indian context
   - Native support for regional languages
   - Cultural nuances handled well

2. **Cost-Effective**
   - Competitive pricing
   - Free tier available
   - Good for Indian market

3. **Data Privacy**
   - Indian company, data stays in India
   - Better compliance with Indian regulations

4. **Optimized for Indian Content**
   - Understands Indian names, places, culture
   - Better at analyzing Indian social media content
   - Handles code-mixing (Hinglish, Tanglish, etc.)

---

## Getting Started

### Step 1: Get API Key

1. Visit: https://www.sarvam.ai
2. Sign up for an account
3. Navigate to API section
4. Generate API key
5. Copy the key

### Step 2: Add to Ashoka

Edit your `.env` file:

```bash
# Sarvam AI Configuration
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_MODEL=sarvam-m
```

### Step 3: Test

```bash
# Restart Ashoka
pkill -f run_dashboard.py
python run_dashboard.py

# Check Settings → AI Engine Status
# You should see "sarvam" in active engines
```

---

## Available Models

| Model | Description | Use Case |
|-------|-------------|----------|
| **sarvam-m** | Medium model (recommended) | Balanced performance and speed |
| **sarvam-30b** | 30 billion parameters | High-quality responses |
| **sarvam-30b-16k** | 30B with 16k context | Long-form content |
| **sarvam-105b** | 105 billion parameters | Best quality |
| **sarvam-105b-32k** | 105B with 32k context | Maximum context length |

---

## API Endpoints

Sarvam AI uses REST API (no SDK needed):

### Chat Completions
```
POST https://api.sarvam.ai/v1/chat/completions
```

### Translation
```
POST https://api.sarvam.ai/v1/translate
```

### Text-to-Speech
```
POST https://api.sarvam.ai/v1/text-to-speech
```

---

## Pricing & Rate Limits

### Free Tier
- Check https://www.sarvam.ai/pricing for current limits
- Typically includes:
  - Limited requests per day
  - Basic models access
  - Standard support

### Paid Tier
- Higher rate limits
- Access to advanced models
- Priority support
- Custom solutions

**Note:** Pricing is competitive with international providers and optimized for Indian market.

---

## Integration with Ashoka

### How It Works

1. **Primary Engine**: Gemini (50 free requests/day)
2. **Backup Engine**: Sarvam AI (kicks in when Gemini fails)

### Automatic Fallback

```
User Request
    ↓
Try Gemini (50 free/day)
    ↓
Failed? → Try Sarvam AI
    ↓
Success! → Return Result
```

### Configuration

```bash
# In .env file
PRIMARY_AI_ENGINE=gemini  # Use Gemini first
SARVAM_API_KEY=your_key   # Sarvam as backup
```

Or switch to Sarvam as primary:

```bash
PRIMARY_AI_ENGINE=sarvam  # Use Sarvam first
```

---

## Comparison: Gemini vs Sarvam AI

| Feature | Gemini | Sarvam AI |
|---------|--------|-----------|
| **Free Tier** | 50 requests/day | Check website |
| **Indian Languages** | Good | Excellent |
| **English** | Excellent | Good |
| **Cultural Context** | Good | Excellent |
| **Speed** | Fast | Fast |
| **Cost** | Free tier | Competitive |
| **Data Location** | Global | India |

### When to Use Sarvam AI:

- ✅ Content in Indian languages
- ✅ Indian cultural context important
- ✅ Data privacy concerns (India-based)
- ✅ Code-mixed content (Hinglish, etc.)
- ✅ Regional content analysis

### When to Use Gemini:

- ✅ English content
- ✅ Technical/scientific content
- ✅ Global context
- ✅ Maximum free tier (50/day)

---

## Example Usage

### Content Analysis (Hindi)

```python
from src.services.ai_engine import ai_client

# Analyze Hindi content
result = ai_client.analyze_content(
    "यह एक बहुत अच्छा उत्पाद है। मुझे यह बहुत पसंद आया।"
)

print(result['sentiment'])  # positive
print(result['keywords'])   # ['उत्पाद', 'अच्छा', 'पसंद']
```

### Content Generation (Tamil)

```python
result = ai_client.generate_content(
    prompt="தமிழில் ஒரு வலைப்பதிவு இடுகை எழுதுங்கள்",
    preferred_engine="sarvam"
)

print(result['text'])
```

---

## Testing Sarvam AI

### Quick Test Script

Create `test_sarvam.py`:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('SARVAM_API_KEY')
endpoint = 'https://api.sarvam.ai/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'sarvam-1',
    'messages': [
        {'role': 'user', 'content': 'Say hello in Hindi'}
    ]
}

response = requests.post(endpoint, headers=headers, json=payload)

if response.status_code == 200:
    print("✓ Sarvam AI is working!")
    print(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(response.text)
```

Run:
```bash
python test_sarvam.py
```

---

## Troubleshooting

### Issue: "Sarvam AI: API key not set"

**Solution:**
1. Check `.env` file has `SARVAM_API_KEY=...`
2. Verify key is correct (no extra spaces)
3. Restart application

### Issue: "Connection failed"

**Solution:**
1. Check internet connection
2. Verify API endpoint is correct
3. Check if Sarvam AI service is up
4. Try again after a few minutes

### Issue: "Invalid API key"

**Solution:**
1. Generate new key from https://www.sarvam.ai
2. Update `.env` file
3. Restart application

### Issue: "Rate limit exceeded"

**Solution:**
1. Wait for rate limit reset
2. Upgrade to paid tier
3. Use Gemini as primary (Sarvam as backup)

---

## Best Practices

1. **Use Gemini as Primary**
   - Gemini has 50 free requests/day
   - Sarvam as backup saves your Sarvam quota

2. **Choose Right Engine for Content**
   - Indian languages → Sarvam AI
   - English/Technical → Gemini

3. **Monitor Usage**
   - Check Settings → AI Engine Status
   - Track which engine is being used

4. **Set Spending Limits**
   - Configure in Sarvam AI dashboard
   - Avoid unexpected charges

---

## Support & Resources

- **Website**: https://www.sarvam.ai
- **Documentation**: https://docs.sarvam.ai
- **API Reference**: https://api.sarvam.ai/docs
- **Support**: support@sarvam.ai

---

## Summary

✅ **Sarvam AI supports ALL Ashoka features**
✅ **Excellent for Indian languages and context**
✅ **Cost-effective alternative to international providers**
✅ **Automatic fallback from Gemini**
✅ **No additional SDK needed (REST API)**

**Perfect for Indian content creators and businesses!** 🇮🇳

---

**Last Updated:** March 2026
