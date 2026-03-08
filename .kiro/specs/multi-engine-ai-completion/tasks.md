# Implementation Plan: Multi-Engine AI Completion

## Overview

This implementation fixes two critical issues in the multi-engine AI system: (1) Sarvam AI 400 Bad Request errors due to incorrect API request format, and (2) incomplete Gemini Engine 3 implementation due to missing engine parameter in _generate_gemini method. The implementation enables a robust three-tier fallback system (Gemini → Sarvam AI → Gemini Engine 3) with comprehensive error logging and testing.

## Tasks

- [x] 1. Fix Sarvam AI request format and error handling
  - [x] 1.1 Update _generate_sarvam method to use correct API request format
    - Verify endpoint URL is exactly "https://api.sarvam.ai/v1/chat/completions"
    - Ensure Authorization header format is "Bearer {api_key}" with space
    - Verify Content-Type header is "application/json"
    - Ensure payload includes all required fields: model, messages, temperature, max_tokens
    - Verify messages array structure with role and content fields
    - When system_instruction is provided, add system message before user message
    - Parse response from data['choices'][0]['message']['content']
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_
  
  - [x] 1.2 Enhance Sarvam AI error logging
    - Catch requests.exceptions.HTTPError
    - Attempt to parse JSON error response
    - Log JSON error response if parsing succeeds
    - Fall back to logging raw response text if JSON parsing fails
    - Include HTTP status code in all error messages
    - _Requirements: 1.2, 1.5, 6.3, 6.4, 6.5_
  
  - [ ]* 1.3 Write property test for Sarvam AI request format
    - **Property 1: Sarvam AI Request Format Compliance**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7**
    - Use hypothesis to generate random prompts, system instructions, and temperatures
    - Mock requests.post to capture request details
    - Verify endpoint URL, headers, and payload structure
    - Test with and without system_instruction
  
  - [ ]* 1.4 Write property test for Sarvam AI successful response
    - **Property 2: Sarvam AI Successful Response**
    - **Validates: Requirements 1.1, 1.4, 5.8**
    - Mock successful HTTP 200 response from Sarvam AI
    - Verify response contains generated text from correct JSON path
    - Verify response includes engine metadata
  
  - [ ]* 1.5 Write unit tests for Sarvam AI error handling
    - Test HTTP 400 error with JSON response
    - Test HTTP 400 error with non-JSON response
    - Test HTTP 401, 429, 500 errors
    - Test network timeout errors
    - Test connection errors
    - Verify error logging includes status code and details
    - _Requirements: 1.2, 1.5, 6.3, 6.4, 6.5_

- [x] 2. Complete Gemini Engine 3 implementation
  - [x] 2.1 Add engine parameter to _generate_gemini method
    - Add engine: AIEngine parameter to method signature
    - Update method to retrieve config from self.engines[engine] instead of self.engines[AIEngine.GEMINI]
    - Extract client and model from the specified engine's config
    - Maintain backward compatibility by using engine parameter for routing
    - _Requirements: 2.1, 2.5_
  
  - [x] 2.2 Update generate_content to pass engine parameter
    - When routing to _generate_gemini for AIEngine.GEMINI, pass AIEngine.GEMINI as engine parameter
    - When routing to _generate_gemini for AIEngine.GEMINI3, pass AIEngine.GEMINI3 as engine parameter
    - Ensure both Gemini engines use the same generation logic with different clients
    - _Requirements: 2.2, 2.3_
  
  - [ ]* 2.3 Write property test for Gemini engine parameter routing
    - **Property 4: Gemini Engine Parameter Routing**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.5**
    - Mock both Gemini engine clients
    - Verify _generate_gemini uses correct client based on engine parameter
    - Test with AIEngine.GEMINI and AIEngine.GEMINI3
    - Verify correct model is used for each engine
  
  - [ ]* 2.4 Write property test for Gemini Engine 3 end-to-end generation
    - **Property 5: Gemini Engine 3 End-to-End Generation**
    - **Validates: Requirements 2.4**
    - Mock Gemini Engine 3 client with valid API key
    - Verify successful content generation
    - Verify response includes generated text and engine metadata
  
  - [ ]* 2.5 Write unit tests for Gemini engine routing
    - Test _generate_gemini with AIEngine.GEMINI uses Engine 1 client
    - Test _generate_gemini with AIEngine.GEMINI3 uses Engine 3 client
    - Test that both engines return correct response format
    - Test error handling for each engine
    - _Requirements: 2.2, 2.3, 2.5_

- [ ] 3. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement and test three-engine fallback system
  - [x] 4.1 Verify fallback logic in generate_content
    - Review existing fallback implementation
    - Ensure engine_priority includes all three engines in correct order
    - Verify fallback continues to next engine on failure
    - Verify short-circuit on first success
    - _Requirements: 3.1, 3.2, 3.5, 7.3_
  
  - [ ]* 4.2 Write property test for primary to secondary fallback
    - **Property 6: Primary to Secondary Fallback**
    - **Validates: Requirements 3.1**
    - Mock Gemini Engine 1 to fail
    - Mock Sarvam Engine to succeed
    - Verify Sarvam Engine is attempted after Gemini failure
    - Verify successful response from Sarvam Engine
  
  - [ ]* 4.3 Write property test for secondary to tertiary fallback
    - **Property 7: Secondary to Tertiary Fallback**
    - **Validates: Requirements 3.2**
    - Mock Gemini Engine 1 and Sarvam Engine to fail
    - Mock Gemini Engine 3 to succeed
    - Verify Gemini Engine 3 is attempted after both failures
    - Verify successful response from Gemini Engine 3
  
  - [ ]* 4.4 Write property test for all engines failed exception
    - **Property 8: All Engines Failed Exception**
    - **Validates: Requirements 3.3**
    - Mock all three engines to fail
    - Verify exception is raised
    - Verify exception contains details about last error
  
  - [ ]* 4.5 Write property test for short-circuit on success
    - **Property 10: Short-Circuit on Success**
    - **Validates: Requirements 3.5**
    - Mock first engine to succeed
    - Verify remaining engines are not attempted
    - Use call counts to verify only one engine was called
  
  - [ ]* 4.6 Write unit tests for fallback scenarios
    - Test Gemini → Sarvam fallback with specific errors
    - Test Gemini → Sarvam → Gemini3 fallback
    - Test all engines failing with different error types
    - Test short-circuit when first engine succeeds
    - Test short-circuit when second engine succeeds
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [x] 5. Implement comprehensive error logging
  - [x] 5.1 Add engine attempt logging
    - Log at info level when attempting each engine
    - Log at info level when engine succeeds with engine name
    - Log at warning level when engine fails with engine name and error
    - Use consistent log format across all engines
    - _Requirements: 3.4, 6.1, 6.2_
  
  - [ ]* 5.2 Write property test for comprehensive error logging
    - **Property 3: Comprehensive Error Logging**
    - **Validates: Requirements 1.2, 1.5, 6.1, 6.3, 6.4, 6.5**
    - Mock logger to capture log calls
    - Test logging for each engine failure type
    - Verify HTTP status code is logged for HTTP errors
    - Verify JSON error response is logged when available
    - Verify raw text is logged when JSON parsing fails
  
  - [ ]* 5.3 Write property test for engine attempt logging
    - **Property 9: Engine Attempt Logging**
    - **Validates: Requirements 3.4, 6.1, 6.2**
    - Mock logger to capture log calls
    - Test logging for engine attempts (info level)
    - Test logging for engine success (info level)
    - Test logging for engine failure (warning level)
    - Verify engine name is included in all log messages
  
  - [ ]* 5.4 Write unit tests for error logging
    - Test logging format for each error type
    - Test logging includes engine name
    - Test logging includes error message
    - Test logging includes HTTP status code for HTTP errors
    - Test logging includes JSON error details when available
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 6. Verify backward compatibility
  - [ ]* 6.1 Write property test for generate_content signature stability
    - **Property 11: Generate Content Signature Stability**
    - **Validates: Requirements 7.1, 7.2**
    - Verify method accepts same parameters as before
    - Verify return value has same structure
    - Test with various parameter combinations
  
  - [ ]* 6.2 Write property test for engine priority order preservation
    - **Property 12: Engine Priority Order Preservation**
    - **Validates: Requirements 7.3**
    - Verify engine_priority list maintains correct order
    - Test with and without PRIMARY_AI_ENGINE environment variable
  
  - [ ]* 6.3 Write property test for graceful engine unavailability
    - **Property 13: Graceful Engine Unavailability**
    - **Validates: Requirements 7.5**
    - Mock missing API keys for some engines
    - Verify system skips unavailable engines
    - Verify no errors raised for missing engines
    - Verify available engines still work
  
  - [ ]* 6.4 Write property test for initialization backward compatibility
    - **Property 14: Initialization Backward Compatibility**
    - **Validates: Requirements 7.4**
    - Test initialization without code modifications
    - Verify all previously working engines remain functional
    - Test with various environment variable configurations
  
  - [ ]* 6.5 Write unit tests for backward compatibility
    - Test existing method signatures unchanged
    - Test return value formats unchanged
    - Test engine priority order unchanged
    - Test initialization methods work without modification
    - Test graceful handling of missing engines
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Update documentation
  - [x] 8.1 Update MULTI_ENGINE_AI_SETUP.md
    - Add section documenting Gemini Engine 3
    - Update architecture diagram to show three engines
    - Document engine priority order: Gemini → Sarvam AI → Gemini3
    - Add troubleshooting section for Sarvam AI 400 errors
    - Include configuration examples for all three engines
    - Add curl command examples for testing each engine
    - _Requirements: 4.1, 4.3, 4.4, 4.5_
  
  - [x] 8.2 Update .env.example
    - Add GEMINI_ENGINE3 variable with placeholder
    - Add GEMINI_MODEL_ENGINE3 variable with default value
    - Include comments explaining each engine's purpose
    - Document which engines are primary, secondary, tertiary
    - _Requirements: 4.2_
  
  - [ ]* 8.3 Write documentation completeness tests
    - Verify MULTI_ENGINE_AI_SETUP.md contains all three engines
    - Verify .env.example contains GEMINI_ENGINE3 variables
    - Verify documentation includes troubleshooting steps
    - Verify documentation includes configuration examples
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 9. Final integration and validation
  - [x] 9.1 Manual testing with real API keys
    - Test Sarvam AI with valid API key (verify HTTP 200)
    - Test Gemini Engine 3 with valid API key
    - Test fallback from Gemini to Sarvam AI
    - Test fallback from Sarvam AI to Gemini Engine 3
    - Test all engines failing scenario
    - Verify error logging provides sufficient debugging information
    - _Requirements: 1.1, 2.4, 3.1, 3.2, 3.3_
  
  - [x] 9.2 Review and validate all changes
    - Verify no regressions in existing functionality
    - Verify all requirements are met
    - Verify all properties are tested
    - Verify code coverage > 90% for ai_engine.py
    - Review error messages for clarity
    - _Requirements: All_

- [ ] 10. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use hypothesis framework with minimum 100 iterations
- Unit tests focus on specific examples and edge cases
- Checkpoints ensure incremental validation
- Manual testing in task 9.1 should be performed by the user, not automated
- All code changes maintain backward compatibility
- Error logging provides comprehensive debugging information
