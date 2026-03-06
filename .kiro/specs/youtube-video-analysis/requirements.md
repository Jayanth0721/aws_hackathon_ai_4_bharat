# Requirements Document

## Introduction

The YouTube Video Analysis feature enables users of the Ashoka platform to analyze YouTube videos directly from URLs without manual download. This feature extends the existing video analysis capabilities by integrating YouTube video extraction, leveraging the existing Whisper AI transcription and Gemini AI content analysis infrastructure. Users can paste a YouTube URL and receive comprehensive analysis including transcription, summary, sentiment, keywords, topics, and key takeaways.

## Glossary

- **YouTube_URL_Processor**: Component that validates and normalizes YouTube URLs
- **Video_Downloader**: Component that extracts audio from YouTube videos using yt-dlp
- **Transcription_Service**: Existing Whisper AI service that converts audio to text
- **Content_Analyzer**: Existing Gemini AI service that analyzes transcribed content
- **Analysis_Result**: Data structure containing summary, sentiment, keywords, topics, and takeaways
- **Video_Metadata**: Data structure containing title, duration, uploader, view count, and thumbnail URL
- **Quick_Summary**: Analysis mode that retrieves only video metadata without transcription
- **Full_Analysis**: Analysis mode that includes transcription and AI content analysis
- **Query_History**: Database record of user analysis requests with timestamps
- **Content_Intelligence_Panel**: UI component where users interact with content analysis features
- **Analysis_Pipeline**: End-to-end process from URL input to result display

## Requirements

### Requirement 1: YouTube URL Input and Validation

**User Story:** As a user, I want to input YouTube URLs in various formats, so that I can analyze videos without worrying about URL format differences

#### Acceptance Criteria

1. THE Content_Intelligence_Panel SHALL display a text input field for YouTube URLs
2. WHEN a user enters a URL, THE YouTube_URL_Processor SHALL validate the URL format
3. THE YouTube_URL_Processor SHALL accept standard YouTube URLs (youtube.com/watch?v=VIDEO_ID)
4. THE YouTube_URL_Processor SHALL accept shortened YouTube URLs (youtu.be/VIDEO_ID)
5. THE YouTube_URL_Processor SHALL accept YouTube URLs with additional query parameters
6. THE YouTube_URL_Processor SHALL accept YouTube URLs with timestamps
7. IF an invalid URL is provided, THEN THE YouTube_URL_Processor SHALL return an error message indicating the URL format is not supported
8. WHEN a valid URL is detected, THE Content_Intelligence_Panel SHALL enable the analysis button

### Requirement 2: Video Metadata Retrieval and Preview

**User Story:** As a user, I want to see video information before analyzing, so that I can confirm I selected the correct video

#### Acceptance Criteria

1. WHEN a valid YouTube URL is provided, THE Video_Downloader SHALL retrieve Video_Metadata
2. THE Video_Downloader SHALL extract the video title from YouTube
3. THE Video_Downloader SHALL extract the video duration from YouTube
4. THE Video_Downloader SHALL extract the uploader name from YouTube
5. THE Video_Downloader SHALL extract the view count from YouTube
6. THE Video_Downloader SHALL extract the thumbnail URL from YouTube
7. WHEN Video_Metadata is retrieved, THE Content_Intelligence_Panel SHALL display the thumbnail image
8. WHEN Video_Metadata is retrieved, THE Content_Intelligence_Panel SHALL display the title, duration, uploader, and view count
9. IF metadata retrieval fails, THEN THE Content_Intelligence_Panel SHALL display an error message indicating the video is unavailable

### Requirement 3: Audio Extraction from YouTube Videos

**User Story:** As a user, I want the system to automatically extract audio from YouTube videos, so that I don't need to download videos manually

#### Acceptance Criteria

1. WHEN a user initiates Full_Analysis, THE Video_Downloader SHALL download audio from the YouTube URL using yt-dlp
2. THE Video_Downloader SHALL extract audio in a format compatible with the Transcription_Service
3. THE Video_Downloader SHALL store the extracted audio in a temporary location
4. WHEN audio extraction completes, THE Video_Downloader SHALL return the audio file path
5. IF the video is unavailable or restricted, THEN THE Video_Downloader SHALL return an error message indicating the video cannot be accessed
6. IF the video is too long (exceeds 2 hours), THEN THE Video_Downloader SHALL return an error message indicating the video duration exceeds the limit
7. WHEN audio extraction completes, THE Video_Downloader SHALL clean up temporary files after transcription

### Requirement 4: Video Transcription Integration

**User Story:** As a user, I want YouTube videos to be transcribed automatically, so that I can analyze the spoken content

#### Acceptance Criteria

1. WHEN audio extraction completes, THE Analysis_Pipeline SHALL pass the audio file to the Transcription_Service
2. THE Transcription_Service SHALL transcribe the audio using the existing Whisper AI integration
3. WHEN transcription completes, THE Transcription_Service SHALL return the full transcript text
4. THE Content_Intelligence_Panel SHALL display the transcript to the user
5. IF transcription fails, THEN THE Analysis_Pipeline SHALL return an error message indicating transcription failed
6. THE Analysis_Pipeline SHALL preserve the existing transcription quality and accuracy standards

### Requirement 5: Content Analysis Integration

**User Story:** As a user, I want YouTube video transcripts to be analyzed automatically, so that I can quickly understand the video content

#### Acceptance Criteria

1. WHEN transcription completes, THE Analysis_Pipeline SHALL pass the transcript to the Content_Analyzer
2. THE Content_Analyzer SHALL generate a summary using the existing Gemini AI integration
3. THE Content_Analyzer SHALL extract sentiment analysis from the transcript
4. THE Content_Analyzer SHALL extract keywords from the transcript
5. THE Content_Analyzer SHALL identify main topics from the transcript
6. THE Content_Analyzer SHALL extract key takeaways from the transcript
7. WHEN analysis completes, THE Content_Analyzer SHALL return an Analysis_Result
8. THE Content_Intelligence_Panel SHALL display all components of the Analysis_Result to the user

### Requirement 6: Analysis Mode Selection

**User Story:** As a user, I want to choose between quick metadata preview and full analysis, so that I can save time when I only need basic information

#### Acceptance Criteria

1. THE Content_Intelligence_Panel SHALL provide a Quick_Summary option
2. THE Content_Intelligence_Panel SHALL provide a Full_Analysis option
3. WHEN Quick_Summary is selected, THE Analysis_Pipeline SHALL retrieve only Video_Metadata
4. WHEN Full_Analysis is selected, THE Analysis_Pipeline SHALL perform audio extraction, transcription, and content analysis
5. THE Content_Intelligence_Panel SHALL display the selected analysis mode to the user
6. THE Content_Intelligence_Panel SHALL indicate estimated processing time for each mode

### Requirement 7: Results Display and Formatting

**User Story:** As a user, I want analysis results displayed in a clear and organized format, so that I can easily understand the video content

#### Acceptance Criteria

1. THE Content_Intelligence_Panel SHALL display Video_Metadata at the top of the results section
2. THE Content_Intelligence_Panel SHALL display the video thumbnail with the metadata
3. THE Content_Intelligence_Panel SHALL display the full transcript in a scrollable text area
4. THE Content_Intelligence_Panel SHALL display the summary in a prominent section
5. THE Content_Intelligence_Panel SHALL display sentiment analysis with visual indicators
6. THE Content_Intelligence_Panel SHALL display keywords as a list or tag cloud
7. THE Content_Intelligence_Panel SHALL display topics as a structured list
8. THE Content_Intelligence_Panel SHALL display key takeaways as bullet points
9. THE Content_Intelligence_Panel SHALL provide options to copy or export the results

### Requirement 8: Query History Tracking

**User Story:** As a user, I want my YouTube analysis requests to be saved in history, so that I can review past analyses

#### Acceptance Criteria

1. WHEN a Full_Analysis completes, THE Analysis_Pipeline SHALL create a Query_History record
2. THE Query_History record SHALL include the user_id of the requesting user
3. THE Query_History record SHALL include the YouTube URL
4. THE Query_History record SHALL include the timestamp of the analysis
5. THE Query_History record SHALL include the Video_Metadata
6. THE Query_History record SHALL include the Analysis_Result
7. THE Analysis_Pipeline SHALL store the Query_History record in the database
8. THE Content_Intelligence_Panel SHALL allow users to view their analysis history
9. WHEN a user views history, THE Content_Intelligence_Panel SHALL display past analyses in reverse chronological order

### Requirement 9: Admin Monitoring and Tracking

**User Story:** As an administrator, I want to monitor YouTube analysis usage, so that I can track platform usage and costs

#### Acceptance Criteria

1. WHEN a YouTube analysis is initiated, THE Analysis_Pipeline SHALL log the request with user_id
2. THE Analysis_Pipeline SHALL log the video duration for each analysis
3. THE Analysis_Pipeline SHALL log the processing time for each analysis stage
4. THE Analysis_Pipeline SHALL log any errors or failures during analysis
5. WHERE admin monitoring is enabled, THE Analysis_Pipeline SHALL track API usage for Whisper AI
6. WHERE admin monitoring is enabled, THE Analysis_Pipeline SHALL track API usage for Gemini AI
7. THE Analysis_Pipeline SHALL make monitoring data available to administrators through the dashboard

### Requirement 10: Error Handling and User Feedback

**User Story:** As a user, I want clear error messages when analysis fails, so that I understand what went wrong and how to fix it

#### Acceptance Criteria

1. IF the YouTube URL is invalid, THEN THE Content_Intelligence_Panel SHALL display "Invalid YouTube URL format. Please enter a valid YouTube link."
2. IF the video is unavailable, THEN THE Content_Intelligence_Panel SHALL display "Video unavailable. The video may be private, deleted, or restricted in your region."
3. IF the video is too long, THEN THE Content_Intelligence_Panel SHALL display "Video duration exceeds the 2-hour limit. Please select a shorter video."
4. IF audio extraction fails, THEN THE Content_Intelligence_Panel SHALL display "Failed to extract audio from video. Please try again or contact support."
5. IF transcription fails, THEN THE Content_Intelligence_Panel SHALL display "Transcription failed. Please try again or contact support."
6. IF content analysis fails, THEN THE Content_Intelligence_Panel SHALL display "Content analysis failed. Please try again or contact support."
7. WHEN an error occurs, THE Analysis_Pipeline SHALL log the error details for debugging
8. WHEN processing is in progress, THE Content_Intelligence_Panel SHALL display a progress indicator with the current stage

### Requirement 11: Performance and Resource Management

**User Story:** As a platform operator, I want YouTube analysis to use resources efficiently, so that the platform remains responsive for all users

#### Acceptance Criteria

1. THE Video_Downloader SHALL limit concurrent YouTube downloads to 3 simultaneous requests
2. WHEN audio extraction completes, THE Video_Downloader SHALL delete temporary audio files within 5 minutes
3. THE Analysis_Pipeline SHALL complete metadata retrieval within 5 seconds
4. THE Analysis_Pipeline SHALL provide progress updates every 10 seconds during transcription
5. IF analysis takes longer than 10 minutes, THEN THE Analysis_Pipeline SHALL timeout and return an error
6. THE Video_Downloader SHALL limit audio quality to balance file size and transcription accuracy
7. THE Analysis_Pipeline SHALL reuse existing transcriptions if the same video is analyzed within 24 hours

### Requirement 12: Security and Access Control

**User Story:** As a platform operator, I want YouTube analysis to respect user permissions and security policies, so that the platform remains secure

#### Acceptance Criteria

1. THE Analysis_Pipeline SHALL verify user authentication before processing YouTube URLs
2. THE Analysis_Pipeline SHALL validate that the user has active session credentials
3. THE Analysis_Pipeline SHALL prevent analysis of URLs containing malicious patterns
4. THE Query_History SHALL associate each analysis with the authenticated user_id
5. THE Analysis_Pipeline SHALL prevent users from accessing other users' analysis history
6. WHERE rate limiting is enabled, THE Analysis_Pipeline SHALL limit each user to 10 YouTube analyses per hour
7. THE Video_Downloader SHALL sanitize YouTube URLs to prevent injection attacks
