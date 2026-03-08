# API Usage Tracking System

Real-time API quota monitoring and management for all AI engines in the Ashoka platform.

## Overview

The API Usage Tracking system provides comprehensive monitoring of AI engine usage with automatic 24-hour reset cycles. It helps manage API costs, prevent quota exhaustion, and provides visibility into AI resource consumption.

## Features

### 1. Real-Time Usage Dashboard

Located in the **Content Intelligence & Analysis** section, the dashboard displays:

- **3 Engine Cards**: Visual representation of each AI engine
  - Engine 1: Gemini (50 requests/day)
  - Engine 2: Sarvam AI (1000 requests/day)  
  - Engine 3: Gemini Backup (50 requests/day)

- **Usage Metrics**:
  - Badge: "X/Y" format (used/total limit)
  - Used: Total requests made today
  - Left: Remaining requests for today
  - Progress Bar: Visual percentage with color coding

- **Color Coding**:
  - 🟢 Green: < 70% used (healthy)
  - 🟠 Orange: 70-90% used (warning)
  - 🔴 Red: ≥ 90% used (critical)

### 2. Engine Selection

**Manual Selection**:
- 🤖 Auto (Recommended): System automatically chooses best available engine
- ⚡ Engine 1: Gemini: Manually select Gemini
- 🌏 Engine 2: Sarvam AI: Manually select Sarvam AI
- 🔄 Engine 3: Gemini Backup: Manually select backup Gemini

**Auto-Selection Logic**:
1. Checks quota for each engine in priority order
2. Skips engines with exceeded quota
3. Uses first available engine
4. Falls back to next engine if current fails

### 3. Automatic Tracking

Every AI request is automatically tracked:

**Tracked Operations**:
- ✅ Content Analysis (text, image, video, audio)
- ✅ Content Generation (text, notes)
- ✅ Content Transformation (multi-platform)
- ✅ Image Analysis (Gemini Vision)

**What's Tracked**:
- Request count (total)
- Success count
- Failure count
- Last request timestamp
- Request date

### 4. 24-Hour Reset Cycle

**How It Works**:
- Tracking is based on `request_date` field
- Each day at midnight, a new date begins
- Previous day's data is preserved in database
- New day starts with 0 usage
- Daily limits are reset automatically

**Example**:
- March 8, 2026: Used 45/50 Gemini requests
- March 9, 2026 00:00: Counter resets to 0/50
- March 8 data remains in database for historical tracking

### 5. Quota Management

**Automatic Quota Checking**:
- Before each request, system checks remaining quota
- If quota exceeded, engine is skipped
- System tries next available engine
- User sees clear error if all engines exhausted

**Quota Exceeded Behavior**:
```
Engine 1 (Gemini): 50/50 used → Skip
Engine 2 (Sarvam): 15/1000 used → Use this
Engine 3 (Gemini3): 50/50 used → Skip
```

### 6. Real-Time Updates

**Auto-Refresh**:
- Stats update automatically after each AI request
- No manual refresh needed
- Immediate feedback on usage

**Manual Refresh**:
- Refresh button available for manual updates
- Updates all engine cards simultaneously
- Updates dropdown options with current counts

## Database Schema

### Table: `ai_engine_usage`

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
```

### Index

```sql
CREATE INDEX idx_ai_engine_usage_user_date 
ON ai_engine_usage(user_id, request_date, engine_name)
```

## API Reference

### APIUsageTracker Class

Located in `src/services/api_usage_tracker.py`

#### Methods

**`track_request(user_id, engine_name, model_name, success=True)`**
- Tracks an API request
- Updates or creates usage record for today
- Increments success/failure counters

**`get_usage_today(user_id, engine_name)`**
- Returns today's usage stats for specific engine
- Returns: Dict with used, limit, remaining, percentage, etc.

**`get_all_usage_today(user_id)`**
- Returns today's usage for all engines
- Returns: Dict mapping engine names to usage stats

**`can_use_engine(user_id, engine_name)`**
- Checks if user has quota remaining
- Returns: Boolean (True if quota available)

**`get_recommended_engine(user_id)`**
- Returns engine name with available quota
- Priority: gemini → sarvam → gemini3
- Returns: Engine name or None

### Daily Limits

```python
DAILY_LIMITS = {
    'gemini': 50,      # Gemini Engine 1
    'sarvam': 1000,    # Sarvam AI
    'gemini3': 50,     # Gemini Engine 3
}
```

## Usage Examples

### Check Current Usage

```python
from src.services.api_usage_tracker import api_usage_tracker

# Get usage for specific engine
usage = api_usage_tracker.get_usage_today('user_guruji', 'gemini')
print(f"Used: {usage['used']}/{usage['limit']}")
print(f"Remaining: {usage['remaining']}")
print(f"Percentage: {usage['percentage']}%")

# Get usage for all engines
all_usage = api_usage_tracker.get_all_usage_today('user_guruji')
for engine, stats in all_usage.items():
    print(f"{engine}: {stats['used']}/{stats['limit']}")
```

### Track a Request

```python
# Track successful request
api_usage_tracker.track_request(
    user_id='user_guruji',
    engine_name='gemini',
    model_name='gemini-2.0-flash',
    success=True
)

# Track failed request
api_usage_tracker.track_request(
    user_id='user_guruji',
    engine_name='sarvam',
    model_name='sarvam-m',
    success=False
)
```

### Check Quota Before Request

```python
# Check if engine has quota
if api_usage_tracker.can_use_engine('user_guruji', 'gemini'):
    # Make API request
    result = ai_client.generate_content(prompt, user_id='user_guruji')
else:
    print("Quota exceeded for Gemini")
```

## Integration Points

### 1. AI Engine (`src/services/ai_engine.py`)

**`generate_content()` method**:
- Checks quota before trying each engine
- Tracks successful requests
- Tracks failed requests
- Automatically skips engines with exceeded quota

**`analyze_content()` method**:
- Calls `generate_content()` internally
- Inherits all tracking behavior

**`transform_content()` method**:
- Calls `generate_content()` internally
- Tracks transformation requests

### 2. Gemini Client (`src/services/gemini_client.py`)

**`analyze_image()` method**:
- Checks Gemini quota before processing
- Tracks successful image analysis
- Tracks failed image analysis

### 3. Dashboard (`src/ui/dashboard.py`)

**Engine Usage Dashboard**:
- Creates UI elements with references
- Displays real-time usage stats
- Provides engine selector dropdown
- Refresh button for manual updates

**Auto-Refresh Points**:
- After content analysis completes
- After content generation completes
- After content transformation completes
- After image analysis completes

## Troubleshooting

### Issue: Usage shows 0/0

**Cause**: Database connection not initialized or error loading stats

**Solution**:
1. Check database connection: `db_schema.conn`
2. Verify table exists: `SELECT * FROM ai_engine_usage LIMIT 1`
3. Check logs for errors

### Issue: Usage not updating

**Cause**: `current_user_id` not set or tracking not called

**Solution**:
1. Verify `self.current_user_id` is set in dashboard
2. Check that `user_id` parameter is passed to AI methods
3. Verify `_refresh_engine_usage()` is called after operations

### Issue: Quota exceeded but still making requests

**Cause**: Tracking not integrated or quota check bypassed

**Solution**:
1. Verify `can_use_engine()` is called before requests
2. Check that tracking is enabled in AI engine
3. Ensure `user_id` is passed to all AI methods

## Best Practices

1. **Always pass `user_id`**: Ensure all AI operations include user_id parameter
2. **Check quota first**: Use `can_use_engine()` before making requests
3. **Track all requests**: Both successful and failed requests should be tracked
4. **Monitor usage**: Regularly check usage stats to avoid quota exhaustion
5. **Use auto-selection**: Let system choose best available engine
6. **Plan for limits**: Design workflows considering daily limits

## Future Enhancements

Potential improvements for the tracking system:

1. **Historical Analytics**: View usage trends over time
2. **Usage Alerts**: Email notifications when quota reaches threshold
3. **Custom Limits**: Allow admins to set custom daily limits
4. **Cost Tracking**: Calculate API costs based on usage
5. **User Quotas**: Set per-user limits instead of global limits
6. **Export Reports**: Download usage reports in CSV/PDF
7. **Predictive Alerts**: Warn users before quota exhaustion
8. **Multi-Timezone Support**: Handle different timezone resets

## Support

For issues or questions about API usage tracking:
1. Check this documentation
2. Review database schema
3. Check application logs
4. Verify API keys are configured
5. Test with manual refresh button

---

**Last Updated**: March 8, 2026
**Version**: 1.0.0
