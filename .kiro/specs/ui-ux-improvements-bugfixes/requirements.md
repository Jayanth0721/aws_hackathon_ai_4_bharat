# Requirements Document

## Introduction

This document specifies requirements for UI/UX improvements and bug fixes for the Ashoka GenAI Governance Dashboard. The dashboard is built using NiceGUI and provides content analysis, transformation, and monitoring capabilities. This specification addresses critical bugs affecting analysis functionality, YouTube video downloads, and clipboard operations, while also streamlining the user interface by removing unnecessary features and controls.

## Glossary

- **Dashboard**: The Ashoka GenAI Governance Dashboard web application
- **GeminiClient**: Service class that interfaces with Google's Gemini AI API for content analysis and generation
- **Content_Analyzer**: Service that uses GeminiClient to analyze text, images, videos, and documents
- **YouTube_Processor**: Service that downloads and processes YouTube videos using yt-dlp
- **Theme_Toggle**: UI button that switches between light and dark display modes
- **Clipboard_Operation**: Browser-based operation to copy text to the system clipboard
- **Recently_Used_Section**: Dashboard panel displaying the three most recently accessed features
- **Image_Generation_Section**: Dashboard panel for AI-powered image generation
- **Usage_Count**: Numeric display showing how many times a feature has been used
- **Bot_Detection_Error**: Error from yt-dlp when YouTube blocks automated video downloads

## Requirements

### Requirement 1: Remove Dark Theme Support

**User Story:** As a product owner, I want to remove the dark theme option, so that the dashboard maintains a consistent light theme appearance for all users.

#### Acceptance Criteria

1. THE Dashboard SHALL remove the theme toggle button from the header navigation
2. THE Dashboard SHALL remove all dark mode CSS classes and styles from the application
3. THE Dashboard SHALL remove the dark_mode state variable and related toggle logic
4. THE Dashboard SHALL display only in light theme mode for all users
5. WHEN the Dashboard initializes, THE Dashboard SHALL NOT apply any dark mode styling

### Requirement 2: Fix GeminiClient Analysis Method

**User Story:** As a user, I want content analysis to work correctly, so that I can analyze text, images, videos, and documents without errors.

#### Acceptance Criteria

1. THE GeminiClient SHALL provide a generate_text method that accepts a prompt string and temperature parameter
2. WHEN Content_Analyzer calls generate_text on GeminiClient, THE GeminiClient SHALL return generated text without AttributeError
3. THE generate_text method SHALL use the Gemini API to generate text responses
4. WHEN generate_text is called with valid parameters, THE GeminiClient SHALL return a non-empty string response
5. IF generate_text encounters an API error, THEN THE GeminiClient SHALL raise an appropriate exception with error details

### Requirement 3: Fix Clipboard Functionality

**User Story:** As a user, I want to copy analysis results and generated content to my clipboard, so that I can easily use the content in other applications.

#### Acceptance Criteria

1. WHEN a user clicks a copy button, THE Dashboard SHALL execute the browser's clipboard API to copy the specified text
2. THE Clipboard_Operation SHALL properly escape special characters in JSON payloads before executing JavaScript
3. WHEN clipboard copy succeeds, THE Dashboard SHALL display a success notification to the user
4. IF clipboard copy fails, THEN THE Dashboard SHALL display an error notification with failure details
5. THE Dashboard SHALL provide copy buttons for all analysis results, transcripts, and generated content
6. FOR ALL text content copied to clipboard, the operation SHALL preserve formatting and special characters

### Requirement 4: Remove Usage Count Display

**User Story:** As a product owner, I want to remove usage count displays from the Recently Used section, so that the interface is cleaner and focuses on recency rather than frequency.

#### Acceptance Criteria

1. THE Recently_Used_Section SHALL display feature name, icon, and last used timestamp
2. THE Recently_Used_Section SHALL NOT display usage count or "times used" text
3. WHEN rendering recently used features, THE Dashboard SHALL query usage data for sorting but not display counts
4. THE Dashboard SHALL maintain usage tracking in the database for analytics purposes
5. THE Recently_Used_Section SHALL continue to display the three most recently used features

### Requirement 5: Remove Image Generation Refresh Button

**User Story:** As a user, I want a cleaner image generation interface, so that I can focus on the essential download action without confusion from redundant buttons.

#### Acceptance Criteria

1. THE Image_Generation_Section SHALL display only a download button next to generated images
2. THE Image_Generation_Section SHALL NOT display a refresh button next to the download button
3. WHEN an image is generated, THE Dashboard SHALL provide download functionality through a single button
4. THE Dashboard SHALL maintain the ability to generate new images through the main generation form

### Requirement 6: Remove Generate Another Button

**User Story:** As a user, I want a streamlined image generation workflow, so that I can download images without unnecessary action buttons cluttering the interface.

#### Acceptance Criteria

1. THE Image_Generation_Section SHALL NOT display a "Generate Another" button after image generation
2. WHEN an image is generated, THE Dashboard SHALL display only the image and download button
3. THE Dashboard SHALL allow users to generate additional images by using the main prompt input and generate button
4. THE Image_Generation_Section SHALL maintain the download button for saving generated images

### Requirement 7: Handle YouTube Bot Detection Gracefully

**User Story:** As a user, I want clear feedback when YouTube blocks video downloads, so that I understand why the download failed and what alternatives are available.

#### Acceptance Criteria

1. WHEN YouTube_Processor encounters a bot detection error from yt-dlp, THE YouTube_Processor SHALL return a structured error response
2. THE YouTube_Processor SHALL detect bot detection errors by checking for specific error messages in yt-dlp exceptions
3. WHEN a bot detection error occurs, THE Dashboard SHALL display a user-friendly error message explaining the issue
4. THE error message SHALL suggest alternative approaches such as trying again later or using a different video
5. THE YouTube_Processor SHALL include an error_code field in the response to distinguish bot detection from other errors
6. IF yt-dlp raises an exception containing "bot" or "blocked" keywords, THEN THE YouTube_Processor SHALL classify it as a bot detection error
7. THE Dashboard SHALL log bot detection errors for monitoring and rate limiting purposes

### Requirement 8: Preserve Existing Functionality

**User Story:** As a user, I want all existing features to continue working after the improvements, so that my workflow is not disrupted.

#### Acceptance Criteria

1. THE Dashboard SHALL maintain all content analysis capabilities for text, images, videos, and documents
2. THE Dashboard SHALL maintain all content transformation capabilities
3. THE Dashboard SHALL maintain monitoring, alerts, and security panels
4. THE Dashboard SHALL maintain user authentication and session management
5. THE Dashboard SHALL maintain history tracking and analysis preview functionality
6. THE Dashboard SHALL maintain AI content generation for both text and images
7. FOR ALL existing features not mentioned in removal requirements, functionality SHALL remain unchanged

