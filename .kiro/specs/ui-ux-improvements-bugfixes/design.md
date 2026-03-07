# Design Document: UI/UX Improvements and Bug Fixes

## Overview

This design document specifies the technical approach for implementing UI/UX improvements and critical bug fixes for the Ashoka GenAI Governance Dashboard. The dashboard is built using NiceGUI (a Python-based web framework) and provides content analysis, transformation, and monitoring capabilities powered by Google's Gemini AI.

### Scope

The design addresses eight distinct requirements organized into three categories:

1. **UI Simplification** (Requirements 1, 4, 5, 6): Remove unnecessary UI elements to streamline the user experience
2. **Critical Bug Fixes** (Requirements 2, 3, 7): Fix broken functionality affecting core features
3. **Preservation** (Requirement 8): Ensure all existing functionality continues to work

### Goals

- Simplify the user interface by removing redundant controls and displays
- Fix critical bugs preventing users from analyzing content and copying results
- Improve error handling for YouTube video processing
- Maintain backward compatibility with all existing features

### Non-Goals

- Adding new features or capabilities
- Redesigning the overall dashboard layout
- Changing the authentication system
- Modifying database schema or data models

## Architecture

### System Context

The Ashoka Dashboard follows a layered architecture:

```
┌─────────────────────────────────────────────────────┐
│              NiceGUI Web Interface                  │
│         (src/ui/dashboard.py)                       │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│              Service Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ GeminiClient │  │ContentAnalyzer│  │YouTube   │ │
│  │              │  │               │  │Processor │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│              Data Layer                             │
│         DuckDB + DynamoDB                           │
└─────────────────────────────────────────────────────┘
```

### Affected Components

This design impacts the following components:

1. **UI Layer** (`src/ui/dashboard.py`)
   - Theme toggle removal
   - Usage count display removal
   - Image generation button cleanup
   - Clipboard operation fixes

2. **Service Layer**
   - `src/services/gemini_client.py`: Add missing `generate_text` method
   - `src/services/content_analyzer.py`: Update to use corrected GeminiClient API
   - `src/services/youtube_processor.py`: Enhance error detection and handling

3. **No Database Changes**: All changes are at the UI and service layers

## Components and Interfaces

### 1. Theme Management (Requirement 1)

**Current Implementation:**
- `AshokaGovDashboard` class has `dark_mode` boolean state variable
- `theme_toggle` button in header navigation
- `_toggle_theme()` method that manipulates DOM classes
- CSS includes dark mode styles

**Design Changes:**
- Remove `self.dark_mode` state variable from `__init__`
- Remove `self.theme_toggle` button creation in header
- Remove `_toggle_theme()` method
- Remove dark mode CSS classes from embedded styles
- Keep only light theme CSS variables

**Interface Impact:**
- No external API changes
- Internal state simplified

### 2. GeminiClient API Fix (Requirement 2)

**Current Implementation:**
```python
class GeminiClient:
    def generate_content(self, prompt, system_instruction, temperature) -> Dict
    def analyze_content(self, content, analysis_type) -> Dict
    def transform_content(self, content, target_platform, ...) -> Dict
    # Missing: generate_text method
```

**Design Changes:**
Add `generate_text` method to GeminiClient:

```python
def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
    """
    Generate text using Gemini (simple text generation)
    
    Args:
        prompt: User prompt
        temperature: Sampling temperature (0.0-2.0)
        
    Returns:
        Generated text string
        
    Raises:
        Exception: If client not initialized or API error occurs
    """
```

**Implementation Strategy:**
- Delegate to existing `generate_content` method
- Extract and return only the text field from response
- Maintain consistent error handling with other methods

**Interface Contract:**
- Input: `prompt` (str), `temperature` (float, default 0.7)
- Output: `str` (generated text)
- Errors: Raises `Exception` with descriptive message

### 3. Clipboard Functionality (Requirement 3)

**Current Implementation:**
```python
def _copy_to_clipboard(self, text: str):
    payload = json.dumps(text)
    ui.run_javascript(
        f"navigator.clipboard.writeText({payload}).then(...);"
    )
    ui.notify('Copied to clipboard!', type='positive')
```

**Problem:**
- Special characters in text (quotes, newlines, backslashes) break JSON encoding
- JavaScript injection vulnerability if text contains malicious content
- No error handling for clipboard API failures

**Design Changes:**

```python
def _copy_to_clipboard(self, text: str):
    """
    Copy text to clipboard with proper escaping and error handling
    
    Args:
        text: Text content to copy
    """
    try:
        # Double-encode: json.dumps handles escaping, then we pass to JS
        payload = json.dumps(text)
        
        # Execute clipboard operation with error handling
        ui.run_javascript(f"""
            navigator.clipboard.writeText({payload})
                .then(() => {{
                    console.log('Clipboard copy successful');
                }})
                .catch((err) => {{
                    console.error('Clipboard copy failed:', err);
                }});
        """)
        
        ui.notify('Copied to clipboard!', type='positive')
        
    except Exception as e:
        logger.error(f"Clipboard operation failed: {e}")
        ui.notify('Failed to copy to clipboard', type='negative')
```

**Security Considerations:**
- `json.dumps()` properly escapes special characters
- No direct string interpolation of user content into JavaScript
- Error handling prevents silent failures

**Browser Compatibility:**
- Requires HTTPS or localhost (Clipboard API restriction)
- Fallback notification if operation fails

### 4. Usage Count Display (Requirement 4)

**Current Implementation:**
```python
def _get_recently_used_features(self):
    # Returns list with 'usage_count' field
    return [
        {
            'name': 'Feature Name',
            'icon': 'icon_name',
            'color': 'color',
            'usage_count': 42,  # This field displayed in UI
            'last_used': 'timestamp',
            'tab': 'tab_name'
        }
    ]

# In UI rendering:
ui.label(f"{feat['usage_count']} times used")
```

**Design Changes:**
- Keep `usage_count` in data structure (used for sorting/analytics)
- Remove UI rendering of usage count
- Display only: feature name, icon, last used timestamp

**Updated UI Rendering:**
```python
with ui.column().classes('gap-2 mt-auto text-center'):
    ui.label(f"Last used: {feat['last_used']}").classes('text-sm')
    # Remove: ui.label(f"{feat['usage_count']} times used")
```

**Data Flow:**
- Database query unchanged (still tracks usage count)
- Service layer unchanged (still returns usage count)
- UI layer filters out usage count display

### 5. Image Generation Refresh Button (Requirement 5)

**Current Implementation:**
- After image generation, UI shows download button and refresh button
- Refresh button is redundant (main form can generate new images)

**Design Changes:**
- Locate refresh button in image generation result display
- Remove button creation code
- Keep download button functionality

**Impact:**
- Cleaner UI with single action button
- Users generate new images via main prompt form

### 6. Generate Another Button (Requirement 6)

**Current Implementation:**
```python
with ui.row().classes('gap-2 mt-3'):
    ui.button(
        'Generate Another',
        icon='auto_awesome',
        on_click=lambda: self._generate_ai_content()
    ).props('color=primary')
```

**Design Changes:**
- Remove "Generate Another" button from image generation results
- Keep download button
- Users can generate additional images using main generation form

**UI Flow:**
1. User enters prompt and clicks generate
2. Image displays with download button only
3. User can modify prompt and generate again using main form

### 7. YouTube Bot Detection (Requirement 7)

**Current Implementation:**
```python
def download_audio_only(self, url, output_path):
    try:
        # yt-dlp download logic
        return {"success": True, "file_path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Problem:**
- Generic error handling doesn't distinguish bot detection
- Users see cryptic yt-dlp error messages
- No guidance on what to do when blocked

**Design Changes:**

Add bot detection logic:

```python
def download_audio_only(self, url, output_path):
    try:
        # ... existing download logic ...
        return {"success": True, "file_path": path}
        
    except Exception as e:
        error_msg = str(e).lower()
        
        # Detect bot/blocking errors
        if self._is_bot_detection_error(error_msg):
            return {
                "success": False,
                "error": "YouTube has detected automated access and blocked this request. Please try again in a few minutes or use a different video.",
                "error_code": "BOT_DETECTION",
                "file_path": None
            }
        
        # ... other error handling ...

def _is_bot_detection_error(self, error_msg: str) -> bool:
    """
    Detect if error is due to bot detection/blocking
    
    Args:
        error_msg: Error message from yt-dlp (lowercased)
        
    Returns:
        True if error indicates bot detection
    """
    bot_keywords = [
        'bot',
        'blocked',
        'captcha',
        'too many requests',
        'rate limit',
        'forbidden',
        '429',
        'sign in to confirm',
        'unusual traffic'
    ]
    
    return any(keyword in error_msg for keyword in bot_keywords)
```

**Error Response Structure:**
```python
{
    "success": False,
    "error": "User-friendly error message",
    "error_code": "BOT_DETECTION",  # Machine-readable code
    "file_path": None
}
```

**UI Integration:**
Dashboard checks `error_code` field and displays appropriate message:

```python
if result.get("error_code") == "BOT_DETECTION":
    ui.notify(
        "YouTube blocked this request. Try again later or use a different video.",
        type='warning',
        timeout=5000
    )
else:
    ui.notify(result.get("error"), type='negative')
```

**Logging:**
- Log bot detection events for monitoring
- Track frequency to identify rate limiting issues
- Include video URL (sanitized) for debugging

### 8. Functionality Preservation (Requirement 8)

**Strategy:**
- All changes are additive or subtractive (no modifications to existing logic)
- No database schema changes
- No API contract changes (except adding `generate_text`)
- Comprehensive testing of existing features

**Verification Approach:**
- Manual testing of all major features
- Verify no regressions in:
  - Content analysis (text, image, video, document)
  - Content transformation
  - Monitoring panels
  - Alerts and security
  - Authentication and sessions
  - History tracking

## Data Models

### No Schema Changes

This design does not modify any database schemas or data models. All changes are at the UI and service layers.

### Existing Models Used

1. **ContentAnalysis** (unchanged)
   - Used by GeminiClient and ContentAnalyzer
   - No modifications needed

2. **Feature Usage Tracking** (unchanged)
   - `usage_count` still tracked in database
   - Only UI display changes

3. **YouTube Processing** (unchanged)
   - Return structure enhanced with `error_code` field
   - Backward compatible (existing code ignores new field)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Before defining properties, let me analyze each acceptance criterion for testability:


### Property Reflection

After analyzing all acceptance criteria, I've identified the following redundancies and consolidation opportunities:

**Redundancies Identified:**

1. **Dark Mode Removal (1.1-1.5)**: All five criteria test different aspects of removing dark mode. These are all examples testing specific implementation details rather than properties. They can be consolidated into verification that dark mode is completely removed.

2. **GeminiClient Method (2.1-2.3, 2.5)**: Criteria 2.1, 2.2, 2.3, and 2.5 are all examples testing specific behaviors. Only 2.4 is a true property about all valid inputs.

3. **Clipboard Operations (3.1, 3.3, 3.4, 3.5)**: These are all examples testing specific scenarios. Criteria 3.2 and 3.6 are the true properties about escaping and preservation.

4. **Recently Used Section (4.1-4.5)**: All are examples testing specific UI elements. No true properties here.

5. **Image Generation Buttons (5.1-5.4, 6.1-6.4)**: All are examples testing presence/absence of specific buttons. No properties.

6. **YouTube Bot Detection (7.1, 7.2, 7.5, 7.6)**: Criteria 7.1, 7.5, and 7.6 are properties about error handling. Criteria 7.2 overlaps with 7.6. We can consolidate into fewer properties.

7. **Preservation (8.1-8.6)**: These are all examples. Only 8.7 is a true property about preservation.

**Consolidation Decisions:**

- **Property 1** (from 2.4): For any valid prompt and temperature, generate_text returns non-empty string
- **Property 2** (from 3.2 + 3.6): For any text with special characters, clipboard operation preserves content
- **Property 3** (from 7.6): For any exception containing bot keywords, classification is bot detection
- **Property 4** (from 7.1 + 7.5): For any bot detection error, response includes error_code field
- **Property 5** (from 8.7): For any existing feature not in removal list, functionality is preserved

All other criteria will be tested as specific examples rather than properties.

### Correctness Properties

### Property 1: Text Generation Returns Non-Empty Content

*For any* valid prompt string and temperature value (0.0-2.0), when generate_text is called on an initialized GeminiClient, the method should return a non-empty string response.

**Validates: Requirements 2.4**

### Property 2: Clipboard Preserves Special Characters

*For any* text content containing special characters (quotes, newlines, backslashes, unicode), when copied to clipboard via _copy_to_clipboard, the JSON encoding should properly escape all characters such that the clipboard receives the exact original text without corruption or injection vulnerabilities.

**Validates: Requirements 3.2, 3.6**

### Property 3: Bot Detection Keyword Classification

*For any* yt-dlp exception message containing bot detection keywords ('bot', 'blocked', 'captcha', 'too many requests', 'rate limit', 'forbidden', '429', 'sign in to confirm', 'unusual traffic'), the YouTube_Processor should classify the error as a bot detection error.

**Validates: Requirements 7.6**

### Property 4: Bot Detection Error Response Structure

*For any* bot detection error encountered during YouTube processing, the response dictionary should include an 'error_code' field set to 'BOT_DETECTION', a user-friendly 'error' message, 'success' set to False, and 'file_path' set to None.

**Validates: Requirements 7.1, 7.5**

### Property 5: Feature Preservation

*For any* existing dashboard feature not explicitly mentioned in removal requirements (dark theme, usage count display, image generation buttons), the feature's functionality should remain unchanged after implementing the improvements, including all inputs producing the same outputs and all UI elements behaving identically.

**Validates: Requirements 8.7**

## Error Handling

### GeminiClient Error Handling

**API Initialization Errors:**
- If `GEMINI_API_KEY` not set: Log warning, set `client = None`
- If `google-genai` package not installed: Log warning, set `GEMINI_AVAILABLE = False`
- If client initialization fails: Log error, set `client = None`

**Runtime Errors:**
- `generate_text` called on uninitialized client: Raise `Exception` with message "Gemini client not initialized. Check API key and installation."
- API timeout: Raise `Exception` with timeout details
- API rate limit: Raise `Exception` with rate limit message
- Invalid response format: Raise `Exception` with parsing error details

**Error Response Format:**
```python
{
    'error': 'User-friendly error message',
    'raw_response': 'Original API response (if available)',
    '_metadata': {
        'model': 'model_name',
        'latency': 0.0
    }
}
```

### Clipboard Error Handling

**JavaScript Execution Errors:**
- JSON encoding fails: Catch exception, log error, show negative notification
- Clipboard API not available (HTTP context): Silent failure, notification shown
- User denies clipboard permission: Browser handles, notification shown

**Error Flow:**
```python
try:
    payload = json.dumps(text)
    ui.run_javascript(f"navigator.clipboard.writeText({payload})...")
    ui.notify('Copied to clipboard!', type='positive')
except Exception as e:
    logger.error(f"Clipboard operation failed: {e}")
    ui.notify('Failed to copy to clipboard', type='negative')
```

### YouTube Processing Error Handling

**Error Categories:**

1. **Bot Detection** (error_code: `BOT_DETECTION`)
   - Keywords: bot, blocked, captcha, rate limit, 429, etc.
   - Message: "YouTube has detected automated access and blocked this request. Please try again in a few minutes or use a different video."
   - Action: Log event, suggest retry

2. **Video Unavailable** (error_code: `VIDEO_UNAVAILABLE`)
   - Keywords: private, unavailable, deleted, restricted
   - Message: "Video unavailable. The video may be private, deleted, or restricted in your region."
   - Action: Suggest different video

3. **Network Errors** (error_code: `NETWORK_ERROR`)
   - Keywords: network, connection, timeout
   - Message: "Network error. Please check your connection and try again."
   - Action: Suggest retry

4. **Invalid URL** (error_code: `INVALID_URL`)
   - Validation fails before download
   - Message: "Invalid YouTube URL format. Please enter a valid YouTube link."
   - Action: Show URL format examples

5. **Video Too Long** (error_code: `VIDEO_TOO_LONG`)
   - Duration > 7200 seconds (2 hours)
   - Message: "Video duration exceeds the 2-hour limit. Please select a shorter video."
   - Action: Show duration limit

6. **Generic Errors** (error_code: `DOWNLOAD_FAILED`)
   - All other exceptions
   - Message: "Failed to download video: {error_details}"
   - Action: Log full error, suggest support contact

**Error Detection Logic:**
```python
def _categorize_error(self, exception: Exception) -> Dict[str, Any]:
    error_msg = str(exception).lower()
    
    if self._is_bot_detection_error(error_msg):
        return {
            "error_code": "BOT_DETECTION",
            "error": "YouTube blocked this request...",
            "success": False
        }
    elif any(kw in error_msg for kw in ['private', 'unavailable', 'deleted']):
        return {
            "error_code": "VIDEO_UNAVAILABLE",
            "error": "Video unavailable...",
            "success": False
        }
    # ... other categories ...
```

**Logging Strategy:**
- Log all errors with full exception details
- Include sanitized URL (video ID only)
- Track error frequency for monitoring
- Alert on high bot detection rates

### UI Error Display

**Notification Types:**
- `positive`: Success messages (green)
- `negative`: Error messages (red)
- `warning`: Bot detection, rate limits (orange)
- `info`: Informational messages (blue)

**Timeout Strategy:**
- Success notifications: 3 seconds
- Error notifications: 5 seconds
- Warning notifications: 5 seconds
- Critical errors: 10 seconds or manual dismiss

## Testing Strategy

### Dual Testing Approach

This feature requires both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests** focus on:
- Specific examples of dark mode removal
- GeminiClient method existence and basic functionality
- Clipboard operation with known test strings
- UI element presence/absence verification
- Specific error scenarios (bot detection, network errors)
- Integration between components

**Property-Based Tests** focus on:
- Text generation with random prompts and temperatures
- Clipboard operations with randomly generated special characters
- Bot detection with various error message patterns
- Error response structure validation
- Feature preservation across random inputs

### Property-Based Testing Configuration

**Library Selection:**
- Python: Use `hypothesis` library (industry standard for Python PBT)
- Installation: `pip install hypothesis`

**Test Configuration:**
- Minimum 100 iterations per property test
- Each test tagged with feature name and property reference
- Tag format: `# Feature: ui-ux-improvements-bugfixes, Property {number}: {property_text}`

**Example Property Test Structure:**
```python
from hypothesis import given, strategies as st
import hypothesis

@given(
    prompt=st.text(min_size=1, max_size=1000),
    temperature=st.floats(min_value=0.0, max_value=2.0)
)
@hypothesis.settings(max_examples=100)
def test_property_1_text_generation_returns_non_empty():
    """
    Feature: ui-ux-improvements-bugfixes, Property 1: 
    For any valid prompt and temperature, generate_text returns non-empty string
    """
    client = GeminiClient()
    if not client.is_available():
        pytest.skip("Gemini client not available")
    
    result = client.generate_text(prompt, temperature)
    assert isinstance(result, str)
    assert len(result) > 0
```

### Unit Test Coverage

**Requirement 1: Dark Theme Removal**
- Test: `test_dark_mode_state_removed` - Verify `dark_mode` attribute doesn't exist
- Test: `test_theme_toggle_button_removed` - Verify `theme_toggle` attribute is None
- Test: `test_dark_mode_css_removed` - Verify CSS doesn't contain `.dark-mode` classes
- Test: `test_no_dark_mode_on_init` - Verify no dark mode classes applied during initialization

**Requirement 2: GeminiClient Fix**
- Test: `test_generate_text_method_exists` - Verify method exists with correct signature
- Test: `test_generate_text_returns_string` - Verify return type is string
- Test: `test_generate_text_calls_api` - Mock API and verify it's called
- Test: `test_generate_text_error_handling` - Verify exceptions raised on API errors
- Property Test: `test_property_1_text_generation` - Random prompts return non-empty strings

**Requirement 3: Clipboard Functionality**
- Test: `test_clipboard_basic_text` - Copy simple text
- Test: `test_clipboard_with_quotes` - Copy text with quotes
- Test: `test_clipboard_with_newlines` - Copy text with newlines
- Test: `test_clipboard_with_backslashes` - Copy text with backslashes
- Test: `test_clipboard_success_notification` - Verify positive notification
- Test: `test_clipboard_error_notification` - Verify negative notification on error
- Property Test: `test_property_2_clipboard_preservation` - Random special characters preserved

**Requirement 4: Usage Count Removal**
- Test: `test_usage_count_not_displayed` - Verify "times used" text absent from UI
- Test: `test_recently_used_shows_timestamp` - Verify timestamp displayed
- Test: `test_recently_used_shows_three_features` - Verify exactly 3 features shown
- Test: `test_usage_count_still_tracked` - Verify database still records usage

**Requirement 5: Refresh Button Removal**
- Test: `test_no_refresh_button_in_image_results` - Verify refresh button absent
- Test: `test_download_button_present` - Verify download button exists
- Test: `test_main_form_generates_images` - Verify main form still works

**Requirement 6: Generate Another Button Removal**
- Test: `test_no_generate_another_button` - Verify button absent
- Test: `test_only_download_button_shown` - Verify only download button present
- Test: `test_multiple_generations_via_form` - Verify can generate multiple images

**Requirement 7: YouTube Bot Detection**
- Test: `test_bot_detection_with_bot_keyword` - Test "bot" keyword detection
- Test: `test_bot_detection_with_blocked_keyword` - Test "blocked" keyword detection
- Test: `test_bot_detection_with_captcha_keyword` - Test "captcha" keyword detection
- Test: `test_bot_detection_error_message` - Verify user-friendly message
- Test: `test_bot_detection_error_code` - Verify error_code field
- Test: `test_bot_detection_logging` - Verify errors logged
- Property Test: `test_property_3_bot_keyword_classification` - Random keywords classified correctly
- Property Test: `test_property_4_bot_error_structure` - Error responses have correct structure

**Requirement 8: Preservation**
- Test: `test_content_analysis_text` - Verify text analysis works
- Test: `test_content_analysis_image` - Verify image analysis works
- Test: `test_content_transformation` - Verify transformation works
- Test: `test_monitoring_panel_renders` - Verify monitoring panel exists
- Test: `test_alerts_panel_renders` - Verify alerts panel exists
- Test: `test_authentication_works` - Verify login/logout works
- Property Test: `test_property_5_feature_preservation` - Random feature inputs produce same outputs

### Integration Testing

**End-to-End Scenarios:**
1. User analyzes content → copies result → verifies clipboard
2. User generates image → downloads image → generates another via form
3. User attempts YouTube download → encounters bot detection → sees friendly error
4. User navigates all panels → verifies no dark mode toggle → all features work

### Manual Testing Checklist

- [ ] Dark mode toggle button not visible in header
- [ ] No dark mode CSS classes in page source
- [ ] Light theme displays correctly
- [ ] Content analysis works for all content types
- [ ] Copy buttons work for analysis results
- [ ] Copy buttons work for transcripts
- [ ] Copy buttons work for generated content
- [ ] Special characters copy correctly (test: quotes, newlines, emojis)
- [ ] Recently used section shows 3 features
- [ ] Recently used section shows timestamps
- [ ] Recently used section does NOT show usage counts
- [ ] Image generation shows only download button
- [ ] No refresh button after image generation
- [ ] No "Generate Another" button after image generation
- [ ] Can generate multiple images via main form
- [ ] YouTube bot detection shows friendly error
- [ ] YouTube bot detection suggests alternatives
- [ ] All monitoring panels render correctly
- [ ] All alert panels render correctly
- [ ] Authentication and sessions work
- [ ] History tracking works

### Test Execution

**Running Tests:**
```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/ -m "not property"

# Run property tests only
pytest tests/ -m property

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific requirement tests
pytest tests/test_ui_ux_improvements.py::TestDarkModeRemoval
```

**Continuous Integration:**
- Run all tests on every commit
- Require 100% property test pass rate
- Require 90%+ unit test coverage
- Block merge if tests fail

## Implementation Plan

### Phase 1: Bug Fixes (Priority: Critical)

**Task 1.1: Fix GeminiClient.generate_text**
- Add `generate_text` method to `GeminiClient` class
- Implement delegation to `generate_content`
- Add error handling
- Write unit tests
- Update `ContentAnalyzer` to use new method

**Task 1.2: Fix Clipboard Functionality**
- Update `_copy_to_clipboard` method with proper escaping
- Add try-catch error handling
- Add error notifications
- Write unit and property tests
- Test with various special characters

**Task 1.3: Enhance YouTube Bot Detection**
- Add `_is_bot_detection_error` method
- Update error handling in `download_audio_only`
- Add `error_code` field to responses
- Update UI to display friendly messages
- Add logging for bot detection events
- Write unit and property tests

### Phase 2: UI Cleanup (Priority: High)

**Task 2.1: Remove Dark Theme**
- Remove `self.dark_mode` from `__init__`
- Remove `self.theme_toggle` button creation
- Remove `_toggle_theme` method
- Remove dark mode CSS classes
- Write unit tests
- Manual testing

**Task 2.2: Remove Usage Count Display**
- Update recently used features UI rendering
- Remove usage count label
- Keep timestamp display
- Verify database tracking still works
- Write unit tests

**Task 2.3: Remove Image Generation Buttons**
- Remove refresh button from image results
- Remove "Generate Another" button
- Keep download button
- Verify main form still works
- Write unit tests

### Phase 3: Testing & Validation (Priority: High)

**Task 3.1: Write Property-Based Tests**
- Set up hypothesis framework
- Write Property 1: Text generation
- Write Property 2: Clipboard preservation
- Write Property 3: Bot detection classification
- Write Property 4: Bot error structure
- Write Property 5: Feature preservation
- Run with 100+ iterations each

**Task 3.2: Write Unit Tests**
- Write tests for all requirements
- Achieve 90%+ coverage
- Test edge cases
- Test error scenarios

**Task 3.3: Manual Testing**
- Execute manual testing checklist
- Test on different browsers
- Test clipboard on HTTPS
- Test YouTube with various videos
- Verify all existing features work

### Phase 4: Documentation & Deployment (Priority: Medium)

**Task 4.1: Update Documentation**
- Update README with changes
- Document new error codes
- Update API documentation
- Add troubleshooting guide

**Task 4.2: Deployment**
- Deploy to staging environment
- Run smoke tests
- Deploy to production
- Monitor for errors

## Rollback Plan

If critical issues are discovered after deployment:

1. **Immediate Rollback:**
   - Revert to previous commit
   - Redeploy previous version
   - Notify users of temporary rollback

2. **Issue Investigation:**
   - Identify root cause
   - Reproduce in development
   - Fix and test thoroughly

3. **Redeployment:**
   - Deploy fixed version
   - Monitor closely
   - Verify all functionality

## Monitoring & Metrics

**Key Metrics to Track:**

1. **Error Rates:**
   - GeminiClient API errors
   - Clipboard operation failures
   - YouTube bot detection frequency

2. **Performance:**
   - Page load time (should improve without dark mode CSS)
   - API response times
   - YouTube download success rate

3. **User Behavior:**
   - Clipboard usage frequency
   - Image generation frequency
   - YouTube processing attempts

**Alerting:**
- Alert if bot detection rate > 20%
- Alert if clipboard failure rate > 5%
- Alert if GeminiClient error rate > 10%

## Security Considerations

### Clipboard Operations

**Threat:** JavaScript injection via clipboard content
**Mitigation:** Use `json.dumps()` for proper escaping, never interpolate user content directly into JavaScript

**Threat:** Sensitive data exposure via clipboard
**Mitigation:** No automatic clipboard operations, user must click button

### YouTube Processing

**Threat:** Malicious URLs causing SSRF attacks
**Mitigation:** Validate URLs against YouTube domain whitelist, limit URL length

**Threat:** Large file downloads causing DoS
**Mitigation:** Enforce 2-hour video duration limit, use temporary directories with cleanup

### API Keys

**Threat:** Gemini API key exposure
**Mitigation:** Store in environment variables, never log API keys, rotate regularly

## Conclusion

This design provides a comprehensive approach to implementing UI/UX improvements and critical bug fixes for the Ashoka Dashboard. The changes are focused, well-tested, and preserve all existing functionality while improving user experience and fixing critical issues.

Key benefits:
- Cleaner, simpler UI without unnecessary controls
- Fixed content analysis and clipboard functionality
- Better error handling for YouTube processing
- Comprehensive testing strategy with property-based tests
- No breaking changes to existing features

The implementation can be completed in phases, with critical bug fixes deployed first, followed by UI cleanup and thorough testing.
