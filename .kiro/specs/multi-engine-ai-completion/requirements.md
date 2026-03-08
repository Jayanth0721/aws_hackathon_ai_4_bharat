# Requirements Document

## Introduction

This document specifies requirements for completing the multi-engine AI system implementation in the Ashoka platform. The system currently supports three AI engines: Gemini (Engine 1), Sarvam AI (Engine 2), and Gemini Engine 3 (backup Gemini). Two critical issues prevent full functionality: (1) Sarvam AI returns 400 Bad Request errors when making API calls, and (2) the Gemini Engine 3 implementation is incomplete because the `_generate_gemini` method does not accept an engine parameter to differentiate between Gemini Engine 1 and Engine 3 clients.

## Glossary

- **AI_Engine_System**: The multi-engine AI client in `src/services/ai_engine.py` that manages three AI engines with automatic fallback
- **Gemini_Engine_1**: Primary Gemini AI engine using GEMINI_API_KEY (currently exhausted quota)
- **Sarvam_Engine**: Secondary AI engine using Sarvam AI API for Indian language support
- **Gemini_Engine_3**: Tertiary backup Gemini AI engine using GEMINI_ENGINE3 API key
- **Engine_Fallback**: Automatic switching to next available engine when current engine fails
- **API_Request_Format**: The structure of HTTP requests sent to Sarvam AI API including headers, payload, and authentication
- **Engine_Parameter**: Method parameter that specifies which engine client to use for generation
- **Round_Trip_Property**: Property test that verifies parse(format(x)) == x or equivalent inverse operations

## Requirements

### Requirement 1: Fix Sarvam AI 400 Bad Request Error

**User Story:** As a developer, I want Sarvam AI to successfully process requests, so that the system can fall back to Sarvam AI when Gemini Engine 1 is unavailable.

#### Acceptance Criteria

1. WHEN the AI_Engine_System sends a request to Sarvam_Engine, THE Sarvam_Engine SHALL return a successful response (HTTP 200)
2. WHEN Sarvam_Engine receives an invalid request format, THE AI_Engine_System SHALL log the detailed error response from the API
3. THE AI_Engine_System SHALL use the correct API request format as specified in Sarvam AI documentation
4. WHEN Sarvam_Engine successfully generates content, THE AI_Engine_System SHALL return a response containing the generated text and engine metadata
5. IF Sarvam_Engine returns a 400 error, THEN THE AI_Engine_System SHALL log both the HTTP status code and the complete error response body for debugging

### Requirement 2: Complete Gemini Engine 3 Implementation

**User Story:** As a developer, I want Gemini Engine 3 to function as a backup engine, so that the system has a third fallback option when both Gemini Engine 1 and Sarvam AI fail.

#### Acceptance Criteria

1. THE _generate_gemini method SHALL accept an engine parameter to specify which Gemini client to use
2. WHEN _generate_gemini is called with AIEngine.GEMINI, THE method SHALL use the Gemini_Engine_1 client
3. WHEN _generate_gemini is called with AIEngine.GEMINI3, THE method SHALL use the Gemini_Engine_3 client
4. WHEN generate_content attempts to use Gemini_Engine_3, THE AI_Engine_System SHALL successfully generate content using the GEMINI_ENGINE3 API key
5. THE _generate_gemini method SHALL retrieve the correct client and model from the engines dictionary based on the engine parameter

### Requirement 3: Verify Three-Engine Fallback System

**User Story:** As a user, I want the system to automatically try all three engines in order, so that I can get AI-generated content even when some engines are unavailable.

#### Acceptance Criteria

1. WHEN Gemini_Engine_1 fails, THE AI_Engine_System SHALL attempt to use Sarvam_Engine
2. WHEN both Gemini_Engine_1 and Sarvam_Engine fail, THE AI_Engine_System SHALL attempt to use Gemini_Engine_3
3. WHEN all three engines fail, THE AI_Engine_System SHALL raise an exception with details about the last error
4. THE AI_Engine_System SHALL log each engine attempt with success or failure status
5. WHEN any engine succeeds, THE AI_Engine_System SHALL return the result immediately without trying remaining engines

### Requirement 4: Update Documentation for Three-Engine Setup

**User Story:** As a developer, I want accurate documentation of the three-engine system, so that I can understand the configuration and troubleshooting steps.

#### Acceptance Criteria

1. THE MULTI_ENGINE_AI_SETUP.md file SHALL document all three engines including Gemini_Engine_3
2. THE .env.example file SHALL include configuration examples for GEMINI_ENGINE3 and GEMINI_MODEL_ENGINE3
3. THE documentation SHALL specify the engine priority order: Gemini → Sarvam AI → Gemini3
4. THE documentation SHALL include troubleshooting steps for Sarvam AI 400 errors
5. THE documentation SHALL explain how to configure and test Gemini_Engine_3

### Requirement 5: Validate API Request Format for Sarvam AI

**User Story:** As a developer, I want to ensure the Sarvam AI request format matches the API specification, so that requests are accepted by the Sarvam API.

#### Acceptance Criteria

1. THE AI_Engine_System SHALL send requests to the endpoint https://api.sarvam.ai/v1/chat/completions
2. THE request headers SHALL include Authorization with format "Bearer {api_key}"
3. THE request headers SHALL include Content-Type with value "application/json"
4. THE request payload SHALL include the model field with the configured model name
5. THE request payload SHALL include the messages field as an array of message objects with role and content
6. THE request payload SHALL include temperature and max_tokens fields with numeric values
7. WHEN system_instruction is provided, THE messages array SHALL include a system role message before the user message
8. THE AI_Engine_System SHALL parse the response to extract text from data['choices'][0]['message']['content']

### Requirement 6: Implement Error Handling and Logging

**User Story:** As a developer, I want detailed error logging for API failures, so that I can diagnose and fix issues quickly.

#### Acceptance Criteria

1. WHEN an engine fails, THE AI_Engine_System SHALL log the engine name and error message at warning level
2. WHEN an engine succeeds, THE AI_Engine_System SHALL log the engine name at info level
3. WHEN Sarvam_Engine returns an HTTP error, THE AI_Engine_System SHALL attempt to parse and log the JSON error response
4. IF the error response is not valid JSON, THEN THE AI_Engine_System SHALL log the raw response text
5. THE AI_Engine_System SHALL include the HTTP status code in error messages for HTTP failures

### Requirement 7: Maintain Backward Compatibility

**User Story:** As a developer, I want existing code to continue working after the fixes, so that no functionality is broken by the changes.

#### Acceptance Criteria

1. THE generate_content method signature SHALL remain unchanged
2. THE return value format from generate_content SHALL remain unchanged
3. THE engine_priority list SHALL maintain the order: Gemini → Sarvam AI → Gemini3
4. THE existing initialization methods SHALL continue to work without modification
5. WHEN an engine is not configured, THE AI_Engine_System SHALL skip that engine without errors
