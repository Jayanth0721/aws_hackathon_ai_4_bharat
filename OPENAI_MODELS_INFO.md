# OpenAI Models Information

## ⚠️ DEPRECATED - OpenAI Removed from Ashoka Platform

**As of March 2026, OpenAI has been removed from the Ashoka platform.**

### Why OpenAI Was Removed

1. **Cost Optimization**: OpenAI charges per request (~$0.002-0.03 per request)
2. **Free Alternatives**: Gemini provides 50 free requests/day per API key
3. **Multi-Key Strategy**: Using multiple Gemini keys (100 free requests/day total)
4. **Sarvam AI Backup**: Indian AI with competitive pricing and free tier

### Current AI Engine Stack

Ashoka now uses a three-tier fallback system:

1. **Gemini Engine 1** (Primary)
   - Model: gemini-2.0-flash
   - Cost: FREE (50 requests/day)
   - Speed: Very fast
   - Quality: Excellent

2. **Sarvam AI** (Secondary)
   - Model: sarvam-m
   - Cost: FREE tier available
   - Speed: Fast
   - Quality: Good (excellent for Indian languages)

3. **Gemini Engine 3** (Tertiary)
   - Model: gemini-2.0-flash
   - Cost: FREE (50 requests/day with second API key)
   - Speed: Very fast
   - Quality: Excellent

### Total Free Quota

- **100 Gemini requests/day** (50 + 50 from two keys)
- **Sarvam AI backup** (free tier)
- **$0/month** for AI processing (excluding AWS costs)

### Migration Guide

If you were using OpenAI:

1. **Remove OpenAI configuration** from `.env`:
   ```bash
   # Remove these lines:
   # OPENAI_API_KEY=...
   # OPENAI_MODEL=...
   ```

2. **Add Gemini configuration**:
   ```bash
   # Primary Gemini Engine
   GEMINI_API_KEY=your_first_key
   GEMINI_MODEL=gemini-2.0-flash
   
   # Backup Gemini Engine (optional)
   GEMINI_ENGINE3=your_second_key
   GEMINI_MODEL_ENGINE3=gemini-2.0-flash
   
   # Sarvam AI (optional)
   SARVAM_API_KEY=your_sarvam_key
   SARVAM_MODEL=sarvam-m
   ```

3. **Restart the application**:
   ```bash
   python run_dashboard.py
   ```

### Cost Comparison

**Old Setup (with OpenAI):**
- Gemini: $0/month (50 requests/day)
- OpenAI: $5-15/month (backup)
- **Total: $5-15/month**

**New Setup (without OpenAI):**
- Gemini Engine 1: $0/month (50 requests/day)
- Sarvam AI: $0/month (free tier)
- Gemini Engine 3: $0/month (50 requests/day)
- **Total: $0/month**

### Benefits of Removal

✅ **Zero AI costs** - All engines use free tiers
✅ **Better reliability** - Three engines instead of two
✅ **More requests** - 100 free Gemini requests/day
✅ **Simpler setup** - One SDK (google-genai) instead of two
✅ **Indian language support** - Sarvam AI excels at Hindi, Tamil, etc.

### If You Still Want OpenAI

OpenAI is no longer supported in Ashoka. However, you can:

1. Use the old codebase (before March 2026)
2. Fork the project and add OpenAI support yourself
3. Use Gemini instead - it's free and performs just as well

### Recommended Configuration

For maximum free usage:

```bash
# .env configuration
PRIMARY_AI_ENGINE=gemini

# Gemini Engine 1 (Primary)
GEMINI_API_KEY=your_first_gemini_key
GEMINI_MODEL=gemini-2.0-flash

# Sarvam AI (Secondary - Backup)
SARVAM_API_KEY=your_sarvam_key
SARVAM_MODEL=sarvam-m

# Gemini Engine 3 (Tertiary - Additional Backup)
GEMINI_ENGINE3=your_second_gemini_key
GEMINI_MODEL_ENGINE3=gemini-2.0-flash
```

### Getting Gemini API Keys

1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key
4. Repeat for second key (use different Google account if needed)

### Getting Sarvam AI Key

1. Go to https://www.sarvam.ai
2. Sign up for free account
3. Get API key from dashboard

---

## Historical Information (For Reference Only)

### OpenAI Models That Were Supported

- gpt-3.5-turbo (~$0.002 per request)
- gpt-4-turbo (~$0.01 per request)
- gpt-4o (~$0.005 per request)

### Why We Chose Gemini Over OpenAI

1. **Cost**: Gemini is free (50 requests/day), OpenAI charges per request
2. **Performance**: Gemini 2.0-flash is comparable to GPT-3.5-turbo
3. **Quota**: Multiple Gemini keys = 100 free requests/day
4. **Simplicity**: One SDK instead of two

---

**Last Updated:** March 2026
**Status:** DEPRECATED - OpenAI removed from platform

For current AI engine documentation, see [MULTI_ENGINE_AI_SETUP.md](MULTI_ENGINE_AI_SETUP.md)

### GPT-3.5 Series (Recommended for Cost)
- **gpt-3.5-turbo** 
  - Cost: ~$0.002 per request
  - Speed: Very fast
  - Quality: Good for most tasks
  - Best for: Content analysis, transformation, general tasks

### GPT-4 Series (Recommended for Quality)
- **gpt-4-turbo**
  - Cost: ~$0.01 per request
  - Speed: Fast (optimized)
  - Quality: Excellent
  - Best for: Complex analysis, high-quality content generation

- **gpt-4o** (Optimized)
  - Cost: ~$0.005 per request
  - Speed: Faster than GPT-4
  - Quality: Excellent
  - Best for: Balanced performance and cost

- **gpt-4**
  - Cost: ~$0.03 per request
  - Speed: Slower
  - Quality: Excellent
  - Best for: Most complex tasks (rarely needed)

## GPT-5 Status

**GPT-5 is NOT available yet.**

There is no:
- ❌ GPT-5.3
- ❌ GPT-5.2
- ❌ GPT-5.0
- ❌ GPT-5

OpenAI has not released GPT-5 to the public as of March 2026.

## How to Check Your API Access

### Method 1: Check OpenAI Dashboard
1. Go to https://platform.openai.com/account/limits
2. View your available models
3. Check your usage limits

### Method 2: Test via API
```python
import openai

openai.api_key = "your-api-key"

# List available models
models = openai.models.list()
for model in models.data:
    print(model.id)
```

### Method 3: Check in Ashoka Dashboard
1. Login to Ashoka
2. Go to Settings
3. View "AI Engine Status" card
4. See which OpenAI models are accessible

## Recommended Configuration

### For Development/Testing
```bash
OPENAI_MODEL=gpt-3.5-turbo
```
- Cheapest option
- Fast responses
- Good quality for testing

### For Production (Cost-Effective)
```bash
OPENAI_MODEL=gpt-3.5-turbo
```
- Best cost/performance ratio
- Handles 95% of use cases well

### For Production (High Quality)
```bash
OPENAI_MODEL=gpt-4o
```
- Better quality than GPT-3.5
- Faster than GPT-4
- Reasonable cost

### For Production (Maximum Quality)
```bash
OPENAI_MODEL=gpt-4-turbo
```
- Best quality
- Optimized speed
- Higher cost but worth it for critical tasks

## Cost Comparison

For 1000 requests:

| Model | Cost | Use Case |
|-------|------|----------|
| gpt-3.5-turbo | $2 | General tasks, high volume |
| gpt-4o | $5 | Balanced quality/cost |
| gpt-4-turbo | $10 | High quality needed |
| gpt-4 | $30 | Maximum quality (overkill) |

## Free Tier

OpenAI provides:
- **$5 credit** for new accounts
- Valid for **3 months**
- After that, you need to add payment method

### How Long Will $5 Last?

With gpt-3.5-turbo:
- ~2,500 requests
- ~83 requests/day for 30 days
- Perfect for testing!

With gpt-4-turbo:
- ~500 requests
- ~16 requests/day for 30 days

## Checking Your API Key Access

### Quick Test Script

Create `test_openai.py`:

```python
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Test available models
print("Testing OpenAI API access...\n")

models_to_test = [
    'gpt-3.5-turbo',
    'gpt-4-turbo',
    'gpt-4o',
    'gpt-4'
]

for model in models_to_test:
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print(f"✓ {model}: ACCESSIBLE")
        print(f"  Response: {response.choices[0].message.content}\n")
    except Exception as e:
        print(f"✗ {model}: NOT ACCESSIBLE")
        print(f"  Error: {str(e)}\n")
```

Run:
```bash
python test_openai.py
```

## Common Issues

### Issue: "Model not found"
**Cause:** Your API key doesn't have access to that model
**Solution:** Use gpt-3.5-turbo (available to all accounts)

### Issue: "Insufficient quota"
**Cause:** You've used your $5 credit or hit rate limits
**Solution:** Add payment method at https://platform.openai.com/account/billing

### Issue: "Invalid API key"
**Cause:** API key is wrong or expired
**Solution:** Generate new key at https://platform.openai.com/api-keys

## Best Practices

1. **Start with gpt-3.5-turbo** - Test everything first
2. **Monitor costs** - Check usage at https://platform.openai.com/usage
3. **Set spending limits** - Configure at https://platform.openai.com/account/billing/limits
4. **Use Gemini as primary** - Save OpenAI for fallback
5. **Upgrade model only if needed** - gpt-3.5-turbo is usually sufficient

## Integration with Ashoka

Ashoka automatically:
- ✅ Tries Gemini first (free 50 requests/day)
- ✅ Falls back to OpenAI if Gemini fails
- ✅ Uses your configured model (gpt-3.5-turbo by default)
- ✅ Logs which engine was used
- ✅ Shows rate limits in Settings

## Summary

- **No GPT-5 yet** - Latest is GPT-4 Turbo and GPT-4o
- **Use gpt-3.5-turbo** - Best for most use cases
- **Check your access** - Run test script above
- **Monitor costs** - OpenAI dashboard
- **Let Gemini be primary** - OpenAI as backup

---

**Last Updated:** March 2026
