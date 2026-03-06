# Design Document: YouTube Video Analysis

## Overview

The YouTube Video Analysis feature extends the Ashoka platform's Content Intelligence capabilities by enabling users to analyze YouTube videos directly from URLs. The feature integrates with existing services (Whisper AI for transcription, Gemini AI for content analysis) while adding new components for YouTube-specific processing.

### Key Capabilities

- YouTube URL validation and normalization (multiple URL formats)
- Video metadata extraction (title, duration, uploader, views, thumbnail)
- Audio extraction from YouTube videos using yt-dlp
- Audio transcription using existing Whisper AI integration
- Content analysis using existing Gemini AI integration
- Two analysis modes: Quick Summary (metadata only) and Full Analysis (transcription + AI analysis)
- Query history tracking for user analysis requests
- Admin monitoring and cost tracking
- Caching for performance optimization

### Integration Points

The feature integrates with:
- **Existing Services**: media_processor (Whisper), content_analyzer (Gemini), auth_service, monitoring_service
- **New Services**: youtube_processor (URL validation, video download), youtube_analyzer (orchestration)
- **Database**: DuckDB for query history and analysis results
- **UI**: Dashboard Content Intelligence panel with new YouTube input tab

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Dashboard UI                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Content Intelligence Panel                               │  │
│  │  ├─ TEXT Tab                                             │  │
│  │  ├─ AUDIO Tab                                            │  │
│  │  ├─ VIDEO Tab                                            │  │
│  │  ├─ DOCUMENT Tab                                         │  │
│  │  └─ YOUTUBE Tab (NEW)                                    │  │
│  │      ├─ URL Input Field                                  │  │
│  │      ├─ Analysis Mode Selector (Quick/Full)              │  │
│  │      ├─ Metadata Preview                                 │  │
│  │      └─ Analysis Results Display                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   YouTube Analyzer (Orchestrator)                │
│  - Coordinates the analysis pipeline                             │
│  - Manages analysis modes (Quick vs Full)                        │
│  - Handles caching and deduplication                             │
│  - Creates query history records                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────┐
│   YouTube Processor       │   │   Security Service       │
│  - URL validation         │   │  - Auth verification     │
│  - Video metadata         │   │  - URL sanitization      │
│  - Audio extraction       │   │  - Rate limiting         │
│  - Temporary file mgmt    │   └──────────────────────────┘
└───────────────────────────┘
                │
                ▼
┌───────────────────────────┐
│   Media Processor         │
│  - Whisper AI             │
│  - Audio transcription    │
└───────────────────────────┘
                │
                ▼
┌───────────────────────────┐
│   Content Analyzer        │
│  - Gemini AI              │
│  - Summary generation     │
│  - Sentiment analysis     │
│  - Keyword extraction     │
│  - Topic identification   │
└───────────────────────────┘
                │
                ▼
┌───────────────────────────┐
│   Database (DuckDB)       │
│  - Query history          │
│  - Analysis results       │
│  - Transcription cache    │
└───────────────────────────┘
```

### Component Interactions

#### Analysis Flow - Quick Summary Mode

```
User → Dashboard → YouTubeAnalyzer.get_quick_summary()
                         │
                         ├─→ SecurityService.verify_auth()
                         ├─→ YouTubeProcessor.validate_youtube_url()
                         ├─→ YouTubeProcessor.get_video_info()
                         └─→ Dashboard (display metadata)
```

#### Analysis Flow - Full Analysis Mode

```
User → Dashboard → YouTubeAnalyzer.analyze_youtube_video()
                         │
                         ├─→ SecurityService.verify_auth()
                         ├─→ SecurityService.check_rate_limit()
                         ├─→ YouTubeProcessor.validate_youtube_url()
                         ├─→ YouTubeProcessor.get_video_info()
                         ├─→ Check cache (video_id + 24h)
                         │   └─→ If cached: return cached result
                         ├─→ YouTubeProcessor.download_audio_only()
                         ├─→ MediaProcessor.process_audio()
                         ├─→ ContentAnalyzer.analyze_content()
                         ├─→ Store in database (query_history)
                         ├─→ Store in cache
                         ├─→ Cleanup temporary files
                         └─→ Dashboard (display results)
```

## Components and Interfaces

### 1. YouTubeProcessor

**Purpose**: Handle YouTube-specific operations (URL validation, metadata extraction, audio download)

**Location**: `src/services/youtube_processor.py` (already implemented)

**Key Methods**:

```python
class YouTubeProcessor:
    def validate_youtube_url(self, url: str) -> bool:
        """Validate if URL is a valid YouTube URL"""
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video metadata without downloading
        Returns: {
            "success": bool,
            "title": str,
            "duration": int,  # seconds
            "uploader": str,
            "view_count": int,
            "thumbnail": str,  # URL
            "description": str,
            "error": Optional[str]
        }
        """
        
    def download_audio_only(self, url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Download only audio from YouTube video
        Returns: {
            "success": bool,
            "file_path": str,
            "video_id": str,
            "title": str,
            "duration": int,
            "error": Optional[str]
        }
        """
```

**Dependencies**:
- yt-dlp: YouTube video download library
- tempfile: Temporary file management
- re: URL pattern matching

**Error Handling**:
- Invalid URL format → return error with message
- Video unavailable/restricted → return error with message
- Video too long (>2 hours) → return error with message
- Network errors → return error with message

### 2. YouTubeAnalyzer

**Purpose**: Orchestrate the complete YouTube analysis pipeline

**Location**: `src/services/youtube_analyzer.py` (already implemented)

**Key Methods**:

```python
class YouTubeAnalyzer:
    def get_quick_summary(self, url: str) -> Dict[str, Any]:
        """Get quick summary (metadata only)
        Returns: {
            "success": bool,
            "title": str,
            "uploader": str,
            "duration": int,
            "view_count": int,
            "description": str,
            "thumbnail": str,
            "error": Optional[str]
        }
        """
        
    def analyze_youtube_video(self, url: str, user_id: str, audio_only: bool = True) -> Dict[str, Any]:
        """Complete YouTube video analysis pipeline
        Returns: {
            "success": bool,
            "url": str,
            "metadata": {
                "title": str,
                "duration": int,
                "uploader": str,
                "view_count": int,
                "language": str
            },
            "transcript": str,
            "analysis": {
                "summary": str,
                "sentiment": str,
                "sentiment_confidence": float,
                "keywords": List[str],
                "topics": List[str],
                "takeaways": List[str]
            },
            "word_count": int,
            "char_count": int,
            "error": Optional[str],
            "stage": Optional[str]  # For error tracking
        }
        """
```

**Pipeline Stages**:
1. Authentication verification
2. Rate limit check
3. URL validation
4. Cache check (video_id + timestamp)
5. Metadata retrieval
6. Audio download
7. Transcription
8. Content analysis
9. Database storage
10. Cache update
11. Cleanup

### 3. Dashboard UI Integration

**Location**: `src/ui/dashboard.py`

**New UI Components**:

```python
# Add YOUTUBE tab to Content Intelligence Panel
with ui.tab_panel(youtube_tab):
    # URL Input Section
    youtube_url_input = ui.input(
        label='YouTube URL',
        placeholder='https://www.youtube.com/watch?v=...'
    )
    
    # Analysis Mode Selector
    analysis_mode = ui.radio(
        ['Quick Summary', 'Full Analysis'],
        value='Quick Summary'
    )
    
    # Metadata Preview Container
    metadata_preview_container = ui.column()
    
    # Analyze Button
    ui.button(
        'Analyze Video',
        on_click=lambda: _handle_youtube_analysis(
            youtube_url_input.value,
            analysis_mode.value
        )
    )
    
    # Results Container
    youtube_results_container = ui.column()
```

**Handler Methods**:

```python
def _handle_youtube_analysis(self, url: str, mode: str):
    """Handle YouTube video analysis request"""
    # 1. Validate URL
    # 2. Show loading indicator
    # 3. Call appropriate analyzer method
    # 4. Display results
    # 5. Handle errors
    
def _display_youtube_metadata(self, metadata: Dict):
    """Display video metadata preview"""
    # Show thumbnail, title, duration, uploader, views
    
def _display_youtube_analysis(self, result: Dict):
    """Display full analysis results"""
    # Show metadata + transcript + analysis
```

## Data Models

### YouTube Query History

**Table**: `youtube_query_history`

```sql
CREATE TABLE IF NOT EXISTS youtube_query_history (
    query_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    youtube_url TEXT NOT NULL,
    video_id TEXT NOT NULL,
    analysis_mode TEXT NOT NULL,  -- 'quick' or 'full'
    
    -- Video Metadata
    video_title TEXT,
    video_duration INTEGER,  -- seconds
    video_uploader TEXT,
    video_view_count INTEGER,
    video_thumbnail_url TEXT,
    
    -- Analysis Results (NULL for quick mode)
    transcript TEXT,
    transcript_language TEXT,
    summary TEXT,
    sentiment TEXT,
    sentiment_confidence REAL,
    keywords TEXT,  -- JSON array
    topics TEXT,  -- JSON array
    takeaways TEXT,  -- JSON array
    
    -- Metadata
    created_at TIMESTAMP NOT NULL,
    processing_time_seconds REAL,
    
    -- Indexing
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_video_id (video_id)
);
```

### Transcription Cache

**Table**: `youtube_transcription_cache`

```sql
CREATE TABLE IF NOT EXISTS youtube_transcription_cache (
    video_id TEXT PRIMARY KEY,
    transcript TEXT NOT NULL,
    transcript_language TEXT,
    cached_at TIMESTAMP NOT NULL,
    access_count INTEGER DEFAULT 1,
    last_accessed_at TIMESTAMP NOT NULL,
    
    INDEX idx_cached_at (cached_at)
);
```

**Cache Policy**:
- TTL: 24 hours
- Eviction: LRU (Least Recently Used)
- Max size: 1000 entries

### Rate Limiting

**Table**: `youtube_rate_limits`

```sql
CREATE TABLE IF NOT EXISTS youtube_rate_limits (
    user_id TEXT NOT NULL,
    request_timestamp TIMESTAMP NOT NULL,
    
    INDEX idx_user_timestamp (user_id, request_timestamp)
);
```

**Rate Limit Policy**:
- 10 analyses per hour per user
- Sliding window implementation
- Admin users: unlimited

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: URL Validation Accepts Valid Formats

*For any* valid YouTube URL (standard, shortened, with parameters, with timestamps), the YouTube_URL_Processor should successfully validate and extract the video ID.

**Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6**

### Property 2: URL Validation Rejects Invalid Formats

*For any* invalid URL (non-YouTube domains, malformed URLs, missing video IDs), the YouTube_URL_Processor should reject the URL and return an appropriate error message.

**Validates: Requirements 1.7, 12.3, 12.7**

### Property 3: Metadata Extraction Completeness

*For any* valid YouTube URL, when metadata is retrieved, the result should contain all required fields: title, duration, uploader, view_count, and thumbnail URL.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

### Property 4: Audio Extraction Format Compatibility

*For any* successfully extracted audio file, the format should be compatible with the Whisper AI transcription service (MP3 format, valid audio stream).

**Validates: Requirements 3.2, 3.3, 3.4**

### Property 5: Temporary File Cleanup

*For any* audio extraction operation, temporary files should be cleaned up after transcription completes or if an error occurs.

**Validates: Requirements 3.7, 11.2**

### Property 6: Transcription Pipeline Integration

*For any* valid audio file, when passed to the transcription service, a transcript should be returned with non-empty text content.

**Validates: Requirements 4.1, 4.2, 4.3**

### Property 7: Analysis Result Completeness

*For any* successful content analysis, the result should contain all required components: summary, sentiment, keywords, topics, and takeaways.

**Validates: Requirements 5.2, 5.3, 5.4, 5.5, 5.6, 5.7**

### Property 8: Analysis Mode Behavior

*For any* YouTube URL, when Quick Summary mode is selected, only metadata should be retrieved (no transcription or analysis), and when Full Analysis mode is selected, all pipeline stages should execute.

**Validates: Requirements 6.3, 6.4**

### Property 9: Query History Persistence

*For any* completed Full Analysis, a query history record should be created in the database containing user_id, URL, timestamp, metadata, and analysis results, and retrieving the record should return the same data (round-trip property).

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7**

### Property 10: Query History Ordering

*For any* set of query history records for a user, when retrieved, they should be ordered in reverse chronological order (most recent first).

**Validates: Requirements 8.9**

### Property 11: User Isolation

*For any* user, when retrieving query history, only records associated with that user's user_id should be returned, and no other users' records should be accessible.

**Validates: Requirements 12.4, 12.5**

### Property 12: Authentication Requirement

*For any* YouTube analysis request, the system should verify user authentication before processing, and reject unauthenticated requests.

**Validates: Requirements 12.1, 12.2**

### Property 13: Rate Limiting Enforcement

*For any* user with rate limiting enabled, when the user exceeds 10 analyses within a 1-hour sliding window, subsequent requests should be rejected until the window slides.

**Validates: Requirements 12.6**

### Property 14: Transcription Caching

*For any* video analyzed twice within 24 hours, the second analysis should reuse the cached transcription rather than re-transcribing the audio.

**Validates: Requirements 11.7**

### Property 15: Concurrent Download Limiting

*For any* set of concurrent YouTube download requests, the system should process at most 3 simultaneous downloads, queuing additional requests.

**Validates: Requirements 11.1**

### Property 16: Progress Updates During Processing

*For any* Full Analysis operation, progress updates should be provided at regular intervals (every 10 seconds) during the transcription stage.

**Validates: Requirements 11.4**

### Property 17: Admin Monitoring Logging

*For any* YouTube analysis request, monitoring logs should be created containing user_id, video duration, processing time, and any errors that occurred.

**Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7**

## Error Handling

### Error Categories

1. **URL Validation Errors**
   - Invalid URL format
   - Non-YouTube URL
   - Missing video ID

2. **Video Access Errors**
   - Video unavailable (deleted, private, restricted)
   - Video too long (>2 hours)
   - Geographic restrictions
   - Age restrictions

3. **Download Errors**
   - Network connectivity issues
   - yt-dlp not installed
   - Insufficient disk space
   - Download timeout

4. **Transcription Errors**
   - Whisper not available
   - Audio format incompatible
   - Transcription timeout
   - Empty audio file

5. **Analysis Errors**
   - Gemini API unavailable
   - API quota exceeded
   - Analysis timeout
   - Empty transcript

6. **Authentication/Authorization Errors**
   - User not authenticated
   - Session expired
   - Rate limit exceeded
   - Insufficient permissions

### Error Response Format

```python
{
    "success": False,
    "error": "Human-readable error message",
    "error_code": "ERROR_CODE",
    "stage": "download|transcription|analysis",
    "details": {
        # Additional context for debugging
    }
}
```

### Error Messages (User-Facing)

| Error Code | User Message |
|------------|--------------|
| INVALID_URL | "Invalid YouTube URL format. Please enter a valid YouTube link." |
| VIDEO_UNAVAILABLE | "Video unavailable. The video may be private, deleted, or restricted in your region." |
| VIDEO_TOO_LONG | "Video duration exceeds the 2-hour limit. Please select a shorter video." |
| DOWNLOAD_FAILED | "Failed to extract audio from video. Please try again or contact support." |
| TRANSCRIPTION_FAILED | "Transcription failed. Please try again or contact support." |
| ANALYSIS_FAILED | "Content analysis failed. Please try again or contact support." |
| AUTH_REQUIRED | "Authentication required. Please log in to continue." |
| RATE_LIMIT_EXCEEDED | "Rate limit exceeded. You can perform 10 analyses per hour. Please try again later." |
| TIMEOUT | "Analysis timed out after 10 minutes. Please try a shorter video." |

### Error Recovery Strategies

1. **Automatic Retry**: Network errors, temporary API failures (max 3 retries with exponential backoff)
2. **Graceful Degradation**: If analysis fails, still return transcript
3. **Cleanup on Error**: Always cleanup temporary files, even on error
4. **User Notification**: Clear error messages with actionable guidance
5. **Logging**: Detailed error logs for debugging and monitoring

## Testing Strategy

### Dual Testing Approach

The testing strategy combines unit tests for specific examples and edge cases with property-based tests for comprehensive coverage of universal properties.

**Unit Tests**: Focus on specific examples, edge cases, and error conditions
- Specific URL format examples (standard, shortened, with parameters)
- Error handling for unavailable videos
- Timeout behavior
- Cleanup verification
- UI component rendering

**Property Tests**: Verify universal properties across all inputs
- URL validation across randomly generated URLs
- Metadata completeness for any valid video
- Transcription pipeline for any audio file
- Query history persistence (round-trip)
- User isolation across random user sets
- Rate limiting enforcement

### Property-Based Testing Configuration

**Library**: Use `hypothesis` for Python property-based testing

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with: `Feature: youtube-video-analysis, Property {number}: {property_text}`
- Generators for: YouTube URLs, video IDs, user IDs, timestamps, metadata objects

**Example Property Test Structure**:

```python
from hypothesis import given, strategies as st
import pytest

# Feature: youtube-video-analysis, Property 1: URL Validation Accepts Valid Formats
@given(
    video_id=st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')), min_size=11, max_size=11),
    url_format=st.sampled_from(['standard', 'shortened', 'with_params', 'with_timestamp'])
)
@pytest.mark.property_test
def test_url_validation_accepts_valid_formats(video_id, url_format):
    """Property 1: For any valid YouTube URL format, validation should succeed"""
    # Generate URL based on format
    # Validate URL
    # Assert video_id extracted correctly
    pass

# Feature: youtube-video-analysis, Property 9: Query History Persistence
@given(
    user_id=st.text(min_size=1, max_size=50),
    url=st.text(min_size=10),
    metadata=st.fixed_dictionaries({
        'title': st.text(min_size=1),
        'duration': st.integers(min_value=1, max_value=7200),
        'uploader': st.text(min_size=1)
    })
)
@pytest.mark.property_test
def test_query_history_round_trip(user_id, url, metadata):
    """Property 9: For any analysis, storing and retrieving history should preserve data"""
    # Create query history record
    # Store in database
    # Retrieve from database
    # Assert all fields match (round-trip)
    pass
```

### Test Coverage Goals

- **Unit Test Coverage**: 80% code coverage
- **Property Test Coverage**: All 17 correctness properties implemented
- **Integration Tests**: End-to-end pipeline tests for both analysis modes
- **UI Tests**: Component rendering and interaction tests
- **Performance Tests**: Verify timeout behavior, concurrent limits

### Test Organization

```
tests/
├── unit/
│   ├── test_youtube_processor.py
│   ├── test_youtube_analyzer.py
│   ├── test_youtube_ui.py
│   └── test_youtube_error_handling.py
├── property/
│   ├── test_youtube_properties.py
│   └── generators.py
├── integration/
│   ├── test_youtube_pipeline.py
│   └── test_youtube_caching.py
└── fixtures/
    ├── sample_urls.py
    └── mock_responses.py
```

## Security Considerations

### Input Validation

1. **URL Sanitization**
   - Remove potentially malicious characters
   - Validate against whitelist of YouTube domains
   - Prevent URL injection attacks
   - Limit URL length (max 2048 characters)

2. **Video ID Validation**
   - Validate format (11 characters, alphanumeric + - and _)
   - Prevent directory traversal attempts
   - Sanitize before using in file paths

### Authentication & Authorization

1. **User Authentication**
   - Verify active session before processing
   - Check session expiration
   - Require re-authentication for sensitive operations

2. **User Isolation**
   - Query history filtered by user_id
   - Prevent cross-user data access
   - Admin-only access to monitoring data

3. **Rate Limiting**
   - Per-user rate limits (10/hour)
   - Sliding window implementation
   - Admin users exempt from limits
   - Rate limit bypass for testing

### Data Protection

1. **Temporary File Security**
   - Store in secure temporary directory
   - Restrict file permissions (owner-only)
   - Cleanup after processing
   - Automatic cleanup on error

2. **Database Security**
   - Parameterized queries (prevent SQL injection)
   - User_id validation
   - Encrypted connections (if remote DB)

3. **API Key Protection**
   - Store API keys in environment variables
   - Never log API keys
   - Rotate keys regularly
   - Use separate keys for dev/prod

### Network Security

1. **HTTPS Only**
   - All YouTube API calls over HTTPS
   - Validate SSL certificates
   - Timeout for network requests

2. **Content Security**
   - Validate downloaded content type
   - Scan for malicious content (if applicable)
   - Limit file sizes

## Performance Optimizations

### Caching Strategy

1. **Transcription Cache**
   - Cache key: video_id
   - TTL: 24 hours
   - Storage: DuckDB table
   - Eviction: LRU policy
   - Max size: 1000 entries
   - Cache hit rate target: >50%

2. **Metadata Cache**
   - Cache key: video_id
   - TTL: 1 hour
   - Storage: In-memory (dict)
   - Max size: 500 entries

### Resource Management

1. **Concurrent Download Limiting**
   - Max 3 simultaneous downloads
   - Queue additional requests
   - Priority: authenticated users > anonymous

2. **Temporary File Management**
   - Use system temp directory
   - Cleanup after 5 minutes
   - Automatic cleanup on process exit
   - Monitor disk space

3. **Memory Management**
   - Stream large files (don't load entirely in memory)
   - Limit transcript size (max 1MB)
   - Garbage collection for large objects

### Async Processing

1. **Background Tasks**
   - Audio download: async
   - Transcription: async with progress updates
   - Analysis: async
   - Cleanup: async

2. **Progress Indicators**
   - Real-time progress updates
   - Estimated time remaining
   - Current stage display
   - Cancel operation support

### Database Optimization

1. **Indexing**
   - Index on (user_id, created_at) for history queries
   - Index on video_id for cache lookups
   - Index on (user_id, request_timestamp) for rate limiting

2. **Query Optimization**
   - Limit result sets (pagination)
   - Use prepared statements
   - Batch inserts where possible

### Performance Targets

| Operation | Target Time |
|-----------|-------------|
| URL Validation | <100ms |
| Metadata Retrieval | <5s |
| Audio Download (5min video) | <30s |
| Transcription (5min video) | <60s |
| Content Analysis | <10s |
| Total (Full Analysis, 5min video) | <2min |
| Cache Hit Response | <500ms |

## Cost Optimization

### API Usage Tracking

1. **Whisper AI**
   - Track audio duration processed
   - Monitor transcription costs
   - Alert on high usage

2. **Gemini AI**
   - Track token usage (input + output)
   - Monitor analysis costs
   - Alert on quota approaching

### Cost Reduction Strategies

1. **Caching**
   - Reuse transcriptions (24h cache)
   - Avoid re-processing same videos
   - Target: 50% cache hit rate

2. **Audio Quality Optimization**
   - Use lower quality audio for transcription
   - Balance quality vs file size
   - Target: 192kbps MP3

3. **Batch Processing**
   - Batch multiple analyses if possible
   - Optimize API calls

4. **Rate Limiting**
   - Prevent abuse
   - Limit per-user usage
   - Monitor heavy users

### Cost Monitoring

**Metrics to Track**:
- Total analyses per day/week/month
- Cache hit rate
- Average processing time
- API costs per analysis
- Cost per user
- Heavy users (top 10%)

**Alerts**:
- Daily cost exceeds threshold
- Cache hit rate drops below 40%
- Individual user exceeds 50 analyses/day
- API quota approaching limit

## Deployment Considerations

### Dependencies

**New Dependencies**:
```
yt-dlp>=2023.10.13
```

**Existing Dependencies**:
```
openai-whisper>=20230918
google-generativeai>=0.3.0
duckdb>=0.9.0
nicegui>=1.4.0
```

### Environment Variables

```bash
# YouTube Analysis Configuration
YOUTUBE_MAX_DURATION=7200  # 2 hours in seconds
YOUTUBE_MAX_CONCURRENT_DOWNLOADS=3
YOUTUBE_CACHE_TTL_HOURS=24
YOUTUBE_RATE_LIMIT_PER_HOUR=10

# Existing AI Configuration
GEMINI_API_KEY=your_api_key_here
USE_GEMINI=true
```

### Database Migrations

```sql
-- Migration: Add YouTube tables
-- Run this migration to add YouTube-specific tables

CREATE TABLE IF NOT EXISTS youtube_query_history (
    -- See Data Models section for full schema
);

CREATE TABLE IF NOT EXISTS youtube_transcription_cache (
    -- See Data Models section for full schema
);

CREATE TABLE IF NOT EXISTS youtube_rate_limits (
    -- See Data Models section for full schema
);
```

### Installation Steps

1. Install yt-dlp: `pip install yt-dlp`
2. Run database migrations
3. Configure environment variables
4. Restart application
5. Verify YouTube tab appears in dashboard

### Monitoring & Alerts

**Metrics to Monitor**:
- Analysis success rate
- Average processing time
- Cache hit rate
- Error rate by type
- API usage and costs
- User adoption rate

**Alerts**:
- Error rate >10%
- Processing time >5min
- Cache hit rate <40%
- API quota >80%
- Disk space <10%

## Future Enhancements

1. **Playlist Support**: Analyze entire YouTube playlists
2. **Subtitle Integration**: Use existing subtitles if available (faster than transcription)
3. **Multi-Language Support**: Translate transcripts to user's preferred language
4. **Video Summarization**: Generate video summaries with timestamps
5. **Comparison Mode**: Compare multiple videos side-by-side
6. **Export Options**: Export analysis to PDF, DOCX, or JSON
7. **Scheduled Analysis**: Schedule recurring analysis of channels
8. **Collaborative Features**: Share analysis results with team members
9. **Advanced Filtering**: Filter history by date, duration, topic
10. **Analytics Dashboard**: Visualize analysis trends over time
