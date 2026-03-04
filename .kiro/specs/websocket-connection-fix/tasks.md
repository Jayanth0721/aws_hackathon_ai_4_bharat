# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Fault Condition** - WebSocket Connection Failure Without Storage Secret
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: Scope the property to concrete failing cases - WebSocket connection attempts when storage_secret is not configured
  - Test that WebSocket connections are accepted when storage_secret is properly configured
  - Test implementation details: Start dashboard, attempt WebSocket connection, verify connection is accepted and UI loads
  - The test assertions should match: websocket_connection_accepted(result) AND ui_loads_successfully(result)
  - Run test on UNFIXED code (without storage_secret parameter in ui.run())
  - **EXPECTED OUTCOME**: Test FAILS with "Expected ASGI message 'websocket.accept' or 'websocket.close', but got 'http.response.start'"
  - Document counterexamples found: WebSocket protocol mismatch error, UI does not load, blank page displayed
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Existing Functionality Unchanged
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-WebSocket functionality (authentication, session management, UI components)
  - Write property-based tests capturing observed behavior patterns:
    - Authentication flow (login/logout) works correctly
    - Session tokens are stored and retrieved from app.storage.general
    - User preferences (language, username, user_id) are persisted
    - UI components render and interact correctly
    - Database operations execute successfully
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 3. Fix for WebSocket connection crash due to missing storage_secret

  - [x] 3.1 Add storage_secret to environment configuration
    - Generate a cryptographically secure random string (minimum 32 characters)
    - Add STORAGE_SECRET to .env file
    - Update .env.example with STORAGE_SECRET placeholder and documentation
    - _Bug_Condition: isBugCondition(input) where input.protocol == 'websocket' AND storage_secret_configured() == false_
    - _Expected_Behavior: websocket_connection_accepted(result) AND ui_loads_successfully(result)_
    - _Preservation: Authentication flow, session management, UI functionality, database operations remain unchanged_
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4_

  - [x] 3.2 Update run_dashboard.py to load and use storage_secret
    - Import os module if not already present
    - Load STORAGE_SECRET from environment: storage_secret = os.getenv('STORAGE_SECRET')
    - Add validation to check STORAGE_SECRET is set before starting server
    - Add storage_secret parameter to ui.run() call (after existing parameters)
    - _Bug_Condition: isBugCondition(input) where storage_secret_configured() == false_
    - _Expected_Behavior: websocket_connection_accepted(result) AND ui_loads_successfully(result)_
    - _Preservation: Server startup, authentication, session management, UI features remain unchanged_
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4_

  - [x] 3.3 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - WebSocket Connection Acceptance
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed - WebSocket connections are accepted and UI loads)
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.4 Verify preservation tests still pass
    - **Property 2: Preservation** - Existing Functionality Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions in authentication, session management, UI, database operations)
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Checkpoint - Ensure all tests pass
  - Verify bug condition exploration test passes (WebSocket connections work)
  - Verify preservation tests pass (existing functionality unchanged)
  - Test full user flow: open browser → load login page → authenticate → navigate to dashboard → verify UI loads
  - Test session persistence across page refreshes
  - Test concurrent users in multiple browser tabs
  - Ensure all tests pass, ask the user if questions arise
