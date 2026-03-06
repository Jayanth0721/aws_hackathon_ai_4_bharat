# Implementation Plan: YouTube Video Analysis

## Overview

This implementation plan breaks down the YouTube Video Analysis feature into discrete coding tasks. The feature extends the Ashoka platform's Content Intelligence capabilities by enabling users to analyze YouTube videos directly from URLs. The implementation leverages existing services (Whisper AI, Gemini AI) while adding new YouTube-specific components.

The implementation follows this sequence:
1. Database schema setup
2. Core YouTube processing components
3. Analysis orchestration layer
4. UI integration
5. Caching and rate limiting
6. Error handling and monitoring
7. Testing and validation

## Tasks

- [x] 1. Set up database schema for YouTube analysis
  - Create `youtube_query_history` table with all required fields (query_id, user_id, youtube_url, video_id, analysis_mode, video metadata, analysis results, timestamps)
  - Create `youtube_transcription_cache` table with video_id, transcript, language, timestamps, and access tracking
  - Create `youtube_rate_limits` table with user_id and request_timestamp
  - Add indexes: (user_id, created_at), (video_id), (user_id, request_timestamp)
  - _Requirements: 8.1-8.7, 11.7, 12.6_

- [ ] 2. Enhance YouTubeProcessor with validation and metadata extraction
  - [x] 2.1 Implement URL validation and video ID extraction
    - Update `validate_youtube_url()` to handle standard URLs (youtube.com/watch?v=VIDEO_ID)
    - Support shortened URLs (youtu.be/VIDEO_ID)
    - Support URLs with query parameters and timestamps
    - Implement `extract_video_id()` with regex patterns for all URL formats
    - Add URL sanitization to prevent injection attacks (max 2048 chars, whitelist domains)
    - _Requirements: 1.2-1.6, 12.3, 12.7_

  - [ ]* 2.2 Write property test for URL validation
    - **Property 1: URL Validation Accepts Valid Formats**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6**
    - Generate random valid YouTube URLs in all formats and verify video ID extraction

  - [ ]* 2.3 Write property test for URL rejection
    - **Property 2: URL Validation Rejects Invalid Formats**
    - **Validates: Requirements 1.7, 12.3, 12.7**
    - Generate random invalid URLs and verify rejection with appropriate error messages

  - [x] 2.4 Implement video metadata extraction
    - Update `get_video_info()` to extract title, duration, uploader, view_count, thumbnail URL, and description
    - Add error handling for unavailable/restricted videos
    - Add validation for video duration (reject if >2 hours / 7200 seconds)
    - Return structured metadata dictionary with all required fields
    - _Requirements: 2.1-2.6, 3.5, 3.6_

  - [ ]* 2.5 Write property test for metadata completeness
    - **Property 3: Metadata Extraction Completeness**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**
    - For any valid video, verify all required metadata fields are present and non-empty

  - [x] 2.6 Implement audio extraction with temporary file management
    - Update `download_audio_only()` to extract audio in MP3 format (192kbps)
    - Store audio in secure temporary directory with restricted permissions
    - Return file path, video_id, title, and duration
    - Add error handling for network issues, disk space, and download timeouts
    - _Requirements: 3.1-3.4, 11.6_

  - [ ]* 2.7 Write property test for audio format compatibility
    - **Property 4: Audio Extraction Format Compatibility**
    - **Validates: Requirements 3.2, 3.3, 3.4**
    - Verify extracted audio files are valid MP3 format with audio stream

  - [ ]* 2.8 Write unit tests for YouTubeProcessor error cases
    - Test invalid URL formats return appropriate errors
    - Test unavailable video handling
    - Test video too long rejection (>2 hours)
    - Test network error handling
    - _Requirements: 1.7, 2.9, 3.5, 3.6_

- [ ] 3. Implement temporary file cleanup mechanism
  - [x] 3.1 Add cleanup method to YouTubeProcessor
    - Implement `cleanup_temp_files()` method to delete audio files
    - Add automatic cleanup after transcription completes
    - Add cleanup on error conditions
    - Schedule cleanup after 5 minutes as fallback
    - _Requirements: 3.7, 11.2_

  - [ ]* 3.2 Write property test for temporary file cleanup
    - **Property 5: Temporary File Cleanup**
    - **Validates: Requirements 3.7, 11.2**
    - Verify temp files are deleted after processing or on error

- [ ] 4. Integrate transcription pipeline with MediaProcessor
  - [x] 4.1 Connect YouTubeProcessor audio output to MediaProcessor
    - Pass extracted audio file path to `MediaProcessor.process_audio()`
    - Handle transcription response and extract transcript text
    - Add error handling for transcription failures
    - Verify transcript is non-empty before proceeding
    - _Requirements: 4.1-4.4_

  - [ ]* 4.2 Write property test for transcription pipeline integration
    - **Property 6: Transcription Pipeline Integration**
    - **Validates: Requirements 4.1, 4.2, 4.3**
    - For any valid audio file, verify transcript is returned with non-empty text

  - [ ]* 4.3 Write unit tests for transcription error handling
    - Test empty audio file handling
    - Test transcription timeout handling
    - Test Whisper unavailable error
    - _Requirements: 4.5_

- [ ] 5. Integrate content analysis pipeline with ContentAnalyzer
  - [x] 5.1 Connect transcription output to ContentAnalyzer
    - Pass transcript to `ContentAnalyzer.analyze_content()`
    - Extract summary, sentiment, sentiment_confidence, keywords, topics, and takeaways
    - Structure analysis results in standardized format
    - Add error handling for analysis failures
    - _Requirements: 5.1-5.7_

  - [ ]* 5.2 Write property test for analysis result completeness
    - **Property 7: Analysis Result Completeness**
    - **Validates: Requirements 5.2, 5.3, 5.4, 5.5, 5.6, 5.7**
    - For any successful analysis, verify all required components are present

  - [ ]* 5.3 Write unit tests for content analysis error handling
    - Test empty transcript handling
    - Test Gemini API unavailable error
    - Test API quota exceeded error
    - Test analysis timeout handling
    - _Requirements: 5.7_

- [ ] 6. Checkpoint - Ensure core pipeline components work end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement YouTubeAnalyzer orchestration layer
  - [x] 7.1 Implement quick summary mode
    - Create `get_quick_summary()` method that calls YouTubeProcessor.get_video_info()
    - Return metadata only (no transcription or analysis)
    - Add authentication verification before processing
    - Structure response with success flag and error handling
    - _Requirements: 6.1, 6.3, 12.1, 12.2_

  - [x] 7.2 Implement full analysis pipeline orchestration
    - Create `analyze_youtube_video()` method that coordinates all pipeline stages
    - Stage 1: Authentication verification (SecurityService)
    - Stage 2: Rate limit check (SecurityService)
    - Stage 3: URL validation (YouTubeProcessor)
    - Stage 4: Cache check (query transcription cache by video_id)
    - Stage 5: Metadata retrieval (YouTubeProcessor)
    - Stage 6: Audio download (YouTubeProcessor)
    - Stage 7: Transcription (MediaProcessor)
    - Stage 8: Content analysis (ContentAnalyzer)
    - Stage 9: Database storage (query_history table)
    - Stage 10: Cache update (transcription_cache table)
    - Stage 11: Cleanup (temporary files)
    - Return structured result with metadata, transcript, and analysis
    - _Requirements: 6.2, 6.4, 12.1, 12.2_

  - [ ]* 7.3 Write property test for analysis mode behavior
    - **Property 8: Analysis Mode Behavior**
    - **Validates: Requirements 6.3, 6.4**
    - Verify Quick Summary returns only metadata, Full Analysis executes all stages

  - [ ] 7.4 Add progress tracking and updates
    - Implement progress callback mechanism
    - Emit progress updates every 10 seconds during transcription
    - Include current stage and estimated time remaining
    - Add timeout handling (10 minutes max)
    - _Requirements: 11.4, 11.5_

  - [ ]* 7.5 Write unit tests for YouTubeAnalyzer orchestration
    - Test quick summary mode execution
    - Test full analysis pipeline execution
    - Test progress update emission
    - Test timeout behavior
    - _Requirements: 6.1-6.4, 11.4, 11.5_

- [ ] 8. Implement query history persistence
  - [x] 8.1 Create database operations for query history
    - Implement `save_query_history()` to insert records into youtube_query_history table
    - Store user_id, youtube_url, video_id, analysis_mode, metadata, analysis results, timestamp
    - Implement `get_user_query_history()` to retrieve records filtered by user_id
    - Order results by created_at DESC (reverse chronological)
    - Add pagination support (limit/offset)
    - _Requirements: 8.1-8.7, 8.9_

  - [ ]* 8.2 Write property test for query history persistence
    - **Property 9: Query History Persistence**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7**
    - For any analysis, verify storing and retrieving preserves all data (round-trip)

  - [ ]* 8.3 Write property test for query history ordering
    - **Property 10: Query History Ordering**
    - **Validates: Requirements 8.9**
    - For any set of records, verify retrieval returns reverse chronological order

  - [ ]* 8.4 Write property test for user isolation
    - **Property 11: User Isolation**
    - **Validates: Requirements 12.4, 12.5**
    - For any user, verify only their records are returned, no cross-user access

- [ ] 9. Implement transcription caching system
  - [x] 9.1 Create cache operations for transcriptions
    - Implement `get_cached_transcription()` to query by video_id
    - Check cache timestamp (reject if >24 hours old)
    - Update access_count and last_accessed_at on cache hit
    - Implement `save_transcription_to_cache()` to store new transcriptions
    - Implement cache eviction (LRU policy, max 1000 entries)
    - _Requirements: 11.7_

  - [x] 9.2 Integrate caching into YouTubeAnalyzer pipeline
    - Check cache before audio download in full analysis mode
    - Return cached transcript if available and fresh (<24 hours)
    - Update cache after new transcription completes
    - Track cache hit rate in monitoring logs
    - _Requirements: 11.7_

  - [ ]* 9.3 Write property test for transcription caching
    - **Property 14: Transcription Caching**
    - **Validates: Requirements 11.7**
    - For any video analyzed twice within 24 hours, verify cached transcript is reused

  - [ ]* 9.4 Write unit tests for cache operations
    - Test cache hit returns cached transcript
    - Test cache miss triggers new transcription
    - Test cache expiration (>24 hours)
    - Test cache eviction (LRU policy)
    - _Requirements: 11.7_

- [ ] 10. Implement rate limiting system
  - [ ] 10.1 Create rate limit operations
    - Implement `check_rate_limit()` to query youtube_rate_limits table
    - Use sliding window algorithm (count requests in last 1 hour)
    - Limit to 10 requests per hour per user
    - Exempt admin users from rate limits
    - Implement `record_rate_limit_request()` to log new requests
    - _Requirements: 12.6_

  - [ ] 10.2 Integrate rate limiting into YouTubeAnalyzer
    - Check rate limit before processing in full analysis mode
    - Return error if rate limit exceeded
    - Record request timestamp after successful analysis
    - _Requirements: 12.6_

  - [ ]* 10.3 Write property test for rate limiting enforcement
    - **Property 13: Rate Limiting Enforcement**
    - **Validates: Requirements 12.6**
    - For any user exceeding 10 requests in 1 hour, verify subsequent requests are rejected

  - [ ]* 10.4 Write unit tests for rate limiting
    - Test rate limit allows 10 requests per hour
    - Test rate limit rejects 11th request
    - Test sliding window behavior
    - Test admin exemption
    - _Requirements: 12.6_

- [ ] 11. Implement concurrent download limiting
  - [ ] 11.1 Add semaphore-based concurrency control to YouTubeProcessor
    - Create semaphore with max 3 concurrent downloads
    - Acquire semaphore before audio download
    - Release semaphore after download completes or on error
    - Queue additional requests when limit reached
    - _Requirements: 11.1_

  - [ ]* 11.2 Write property test for concurrent download limiting
    - **Property 15: Concurrent Download Limiting**
    - **Validates: Requirements 11.1**
    - For any set of concurrent requests, verify at most 3 simultaneous downloads

- [ ] 12. Implement authentication and security checks
  - [ ] 12.1 Add authentication verification to YouTubeAnalyzer
    - Call SecurityService.verify_auth() before processing
    - Check session validity and expiration
    - Return authentication error if not authenticated
    - _Requirements: 12.1, 12.2_

  - [ ]* 12.2 Write property test for authentication requirement
    - **Property 12: Authentication Requirement**
    - **Validates: Requirements 12.1, 12.2**
    - For any analysis request, verify authentication is checked and unauthenticated requests are rejected

  - [ ]* 12.3 Write unit tests for security checks
    - Test unauthenticated request rejection
    - Test expired session rejection
    - Test URL sanitization
    - Test video ID validation
    - _Requirements: 12.1, 12.2, 12.3, 12.7_

- [ ] 13. Checkpoint - Ensure all backend components are integrated and tested
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Implement Dashboard UI integration
  - [x] 14.1 Add YouTube tab to Content Intelligence Panel
    - Add YOUTUBE tab to existing tabs (TEXT, AUDIO, VIDEO, DOCUMENT)
    - Create tab panel container for YouTube-specific UI
    - _Requirements: 1.1_

  - [x] 14.2 Create YouTube URL input section
    - Add text input field with label "YouTube URL" and placeholder
    - Add analysis mode radio selector (Quick Summary / Full Analysis)
    - Add "Analyze Video" button
    - Display estimated processing time for each mode
    - _Requirements: 1.1, 6.1, 6.2, 6.6_

  - [x] 14.3 Implement metadata preview display
    - Create container for video metadata preview
    - Display thumbnail image
    - Display title, duration (formatted), uploader, and view count
    - Show metadata after URL validation or quick summary
    - _Requirements: 2.7, 2.8_

  - [x] 14.4 Implement analysis results display
    - Create scrollable container for full analysis results
    - Display video metadata at top with thumbnail
    - Display full transcript in scrollable text area
    - Display summary in prominent section
    - Display sentiment with visual indicators (positive/negative/neutral)
    - Display keywords as tags or list
    - Display topics as structured list
    - Display key takeaways as bullet points
    - Add copy/export buttons for results
    - _Requirements: 7.1-7.9_

  - [x] 14.5 Implement progress indicator
    - Display loading spinner during processing
    - Show current stage (Downloading, Transcribing, Analyzing)
    - Display progress percentage if available
    - Show estimated time remaining
    - Add cancel button for long-running operations
    - _Requirements: 10.8_

  - [x] 14.6 Implement error message display
    - Create error notification component
    - Display user-friendly error messages based on error codes
    - Map error codes to messages (INVALID_URL, VIDEO_UNAVAILABLE, etc.)
    - Show error with appropriate styling (red/warning)
    - _Requirements: 10.1-10.6_

  - [x] 14.7 Create YouTube analysis handler method
    - Implement `_handle_youtube_analysis()` to process user requests
    - Validate URL input before processing
    - Show loading indicator
    - Call YouTubeAnalyzer.get_quick_summary() or analyze_youtube_video() based on mode
    - Display results or errors
    - Handle exceptions and show user-friendly messages
    - _Requirements: 1.1-10.8_

  - [ ]* 14.8 Write unit tests for UI components
    - Test YouTube tab rendering
    - Test URL input validation
    - Test analysis mode selection
    - Test metadata display
    - Test results display
    - Test error message display
    - _Requirements: 1.1-10.8_

- [ ] 15. Implement query history UI
  - [ ] 15.1 Add history view to YouTube tab
    - Create "View History" button or section
    - Display past analyses in reverse chronological order
    - Show video thumbnail, title, and timestamp for each entry
    - Add click handler to load full analysis results
    - Implement pagination (10 entries per page)
    - _Requirements: 8.8, 8.9_

  - [ ]* 15.2 Write unit tests for history UI
    - Test history list rendering
    - Test chronological ordering
    - Test pagination
    - Test loading historical analysis
    - _Requirements: 8.8, 8.9_

- [ ] 16. Implement admin monitoring and logging
  - [ ] 16.1 Add monitoring logs to YouTubeAnalyzer
    - Log analysis request with user_id, video_id, timestamp
    - Log video duration for each analysis
    - Log processing time for each pipeline stage
    - Log errors with full context (stage, error type, details)
    - Track Whisper API usage (audio duration)
    - Track Gemini API usage (token count)
    - _Requirements: 9.1-9.7_

  - [ ]* 16.2 Write property test for admin monitoring logging
    - **Property 17: Admin Monitoring Logging**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7**
    - For any analysis request, verify monitoring logs contain required fields

  - [ ]* 16.3 Write unit tests for monitoring
    - Test log creation for successful analysis
    - Test log creation for failed analysis
    - Test API usage tracking
    - Test error logging with context
    - _Requirements: 9.1-9.7_

- [ ] 17. Implement comprehensive error handling
  - [ ] 17.1 Add error handling to all pipeline stages
    - Wrap each stage in try-except blocks
    - Return structured error responses with error codes
    - Include stage information in error responses
    - Log errors with full context for debugging
    - Ensure cleanup happens even on error
    - _Requirements: 10.1-10.7_

  - [ ] 17.2 Implement automatic retry logic
    - Add retry decorator for network errors (max 3 retries, exponential backoff)
    - Add retry for temporary API failures
    - Skip retry for permanent errors (invalid URL, video unavailable)
    - _Requirements: 10.7_

  - [ ]* 17.3 Write unit tests for error handling
    - Test error response structure
    - Test error code mapping
    - Test cleanup on error
    - Test retry logic
    - Test graceful degradation (return transcript if analysis fails)
    - _Requirements: 10.1-10.8_

- [ ] 18. Integration testing for complete pipeline
  - [ ]* 18.1 Write integration test for quick summary mode
    - Test end-to-end flow: URL input → validation → metadata retrieval → display
    - Verify no transcription or analysis occurs
    - Verify response time <5 seconds
    - _Requirements: 6.1, 6.3, 11.3_

  - [ ]* 18.2 Write integration test for full analysis mode
    - Test end-to-end flow: URL input → validation → metadata → download → transcription → analysis → storage → display
    - Verify all pipeline stages execute in order
    - Verify query history is created
    - Verify cache is updated
    - Verify temporary files are cleaned up
    - _Requirements: 6.2, 6.4_

  - [ ]* 18.3 Write integration test for caching behavior
    - Analyze same video twice within 24 hours
    - Verify second analysis uses cached transcription
    - Verify cache hit is faster than cache miss
    - _Requirements: 11.7_

  - [ ]* 18.4 Write integration test for rate limiting
    - Submit 11 analysis requests within 1 hour
    - Verify first 10 succeed, 11th is rejected
    - Wait for sliding window to advance
    - Verify new request succeeds
    - _Requirements: 12.6_

  - [ ]* 18.5 Write integration test for error scenarios
    - Test invalid URL handling
    - Test unavailable video handling
    - Test video too long handling
    - Test network error handling
    - Verify appropriate error messages displayed
    - _Requirements: 10.1-10.6_

- [ ] 19. Update documentation
  - [x] 19.1 Update FEATURES.md with YouTube analysis capability
    - Document YouTube URL support
    - Document analysis modes (Quick Summary vs Full Analysis)
    - Document query history feature
    - Document rate limits and constraints
    - _Requirements: All_

  - [x] 19.2 Update SETUP.md with installation instructions
    - Add yt-dlp installation step
    - Document environment variables for YouTube configuration
    - Document database migration steps
    - _Requirements: All_

  - [x] 19.3 Create user guide for YouTube analysis
    - Document how to use YouTube tab
    - Provide examples of supported URL formats
    - Explain analysis modes and when to use each
    - Document error messages and troubleshooting
    - _Requirements: All_

- [ ] 20. Final checkpoint - Complete system validation
  - Run all unit tests, property tests, and integration tests
  - Verify all 17 correctness properties pass
  - Test UI functionality manually
  - Verify monitoring and logging work correctly
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end pipeline behavior
- The implementation leverages existing services (MediaProcessor, ContentAnalyzer, SecurityService) to minimize new code
- Database schema must be created before implementing any features that depend on it
- UI integration should happen after backend components are complete and tested
- All 17 correctness properties from the design document are covered by property tests
