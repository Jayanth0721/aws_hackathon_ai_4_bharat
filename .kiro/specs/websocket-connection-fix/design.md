# WebSocket Connection Fix Bugfix Design

## Overview

The NiceGUI dashboard application crashes when WebSocket connections are attempted because the `storage_secret` parameter is missing from the `ui.run()` call. The application uses `app.storage.general` for session management (storing session tokens, user IDs, usernames, and language preferences), which requires a storage secret to properly negotiate WebSocket connections. Without this parameter, the ASGI middleware sends HTTP responses instead of accepting WebSocket connections, causing a protocol mismatch error. The fix is straightforward: add the `storage_secret` parameter to the `ui.run()` call in `run_dashboard.py`, using a secure value from environment variables.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when WebSocket connections are attempted without `storage_secret` configured
- **Property (P)**: The desired behavior when WebSocket connections are attempted - connections should be accepted and the UI should load
- **Preservation**: Existing authentication flow, session management, and UI functionality that must remain unchanged by the fix
- **ui.run()**: The NiceGUI function in `run_dashboard.py` that starts the web server and configures the application
- **app.storage.general**: NiceGUI's general storage mechanism used for session management across the application
- **storage_secret**: A required parameter for `ui.run()` when using `app.storage.general`, used to encrypt session data
- **ASGI middleware**: The underlying web server layer that handles HTTP and WebSocket protocol negotiation

## Bug Details

### Fault Condition

The bug manifests when a browser attempts to establish a WebSocket connection to the NiceGUI dashboard. The `ui.run()` function is called without the `storage_secret` parameter, but the application uses `app.storage.general` throughout the codebase for session management. This causes the ASGI middleware to fail WebSocket negotiation and send HTTP responses instead.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type WebSocketConnectionAttempt
  OUTPUT: boolean
  
  RETURN input.protocol == 'websocket'
         AND app_uses_storage_general() == true
         AND storage_secret_configured() == false
         AND websocket_accept_not_sent()
END FUNCTION
```

### Examples

- **Example 1**: User opens http://localhost:8080 in browser → Browser attempts WebSocket connection → Server crashes with "Expected ASGI message 'websocket.accept' or 'websocket.close', but got 'http.response.start'" → UI does not load
- **Example 2**: User successfully logs in and navigates to /dashboard → Browser attempts WebSocket connection for real-time updates → Server crashes with protocol mismatch error → Dashboard does not render
- **Example 3**: Authenticated user refreshes the dashboard page → Browser re-establishes WebSocket connection → Server crashes again → User sees blank page
- **Edge Case**: Server starts successfully and listens on port 8080, HTTP requests work initially, but any WebSocket upgrade request triggers the crash

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Server startup messages and listening on http://localhost:8080 must continue to work
- Session token storage in `app.storage.general` for authentication state must continue to work
- Authentication flow (login, session validation, redirect logic) must continue to work
- All NiceGUI UI features (ui.page, ui.notify, ui.navigate, ui.dialog, etc.) must continue to work
- User preferences stored in `app.storage.general` (language, username, user_id) must continue to work
- Dashboard functionality (content analysis, transformation, monitoring, security panels) must continue to work

**Scope:**
All functionality that does NOT involve the initial WebSocket connection establishment should be completely unaffected by this fix. This includes:
- HTTP request handling for page routes
- Authentication and authorization logic
- Database operations (DynamoDB, DuckDB)
- AI service integrations (Gemini)
- Session management logic (token validation, user context loading)
- UI component rendering and interactions

## Hypothesized Root Cause

Based on the bug description and code analysis, the root cause is clear:

1. **Missing Configuration Parameter**: The `ui.run()` call in `run_dashboard.py` (line 119) does not include the `storage_secret` parameter, which is required when using `app.storage.general`

2. **Widespread Storage Usage**: The application extensively uses `app.storage.general` throughout the codebase:
   - `src/ui/auth_page.py`: Stores session_token, user_id, username after login
   - `run_dashboard.py`: Reads session_token for authentication checks
   - `src/ui/dashboard.py`: Reads user_id, username, language preferences; stores language changes; clears storage on logout

3. **NiceGUI Requirement**: NiceGUI's documentation states that when using `app.storage.general` or `app.storage.user`, a `storage_secret` must be provided to `ui.run()` for secure session encryption and proper WebSocket handling

4. **ASGI Middleware Behavior**: Without the storage secret, the ASGI middleware cannot properly initialize the storage layer, causing it to fail WebSocket protocol negotiation and fall back to HTTP responses, which violates the WebSocket protocol

## Correctness Properties

Property 1: Fault Condition - WebSocket Connection Acceptance

_For any_ WebSocket connection attempt when the application uses `app.storage.general` and `storage_secret` is properly configured, the fixed `ui.run()` function SHALL accept the WebSocket connection without errors, allowing the UI to load successfully in the browser.

**Validates: Requirements 2.1, 2.2, 2.3**

Property 2: Preservation - Existing Functionality

_For any_ application functionality that does NOT involve the initial WebSocket connection establishment (authentication flow, session management, UI rendering, database operations, AI services), the fixed code SHALL produce exactly the same behavior as the original code, preserving all existing functionality.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

## Fix Implementation

### Changes Required

The root cause analysis confirms that the fix requires adding the `storage_secret` parameter to `ui.run()`.

**File**: `run_dashboard.py`

**Function**: `ui.run()` call (lines 119-125)

**Specific Changes**:
1. **Add Environment Variable**: Add `STORAGE_SECRET` to `.env` file with a secure random value (minimum 32 characters)
   - Use a cryptographically secure random string
   - Document in `.env.example` for other developers

2. **Load Environment Variable**: Import and read `STORAGE_SECRET` from environment at the top of `run_dashboard.py`
   - Add `import os` if not already present
   - Read value: `storage_secret = os.getenv('STORAGE_SECRET')`

3. **Add Parameter to ui.run()**: Add `storage_secret` parameter to the `ui.run()` call
   - Insert after existing parameters (title, dark, reload, host, port)
   - Pass the loaded environment variable value

4. **Add Validation**: Optionally add a check to ensure `STORAGE_SECRET` is set before starting the server
   - Print warning if not set
   - Provide clear error message with setup instructions

5. **Update Documentation**: Update `.env.example` and any setup documentation to include the new required environment variable

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code, then verify the fix works correctly and preserves existing behavior.

### Exploratory Fault Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm that the missing `storage_secret` parameter is indeed the root cause.

**Test Plan**: Start the dashboard without `storage_secret` configured and attempt to load the UI in a browser. Observe the WebSocket connection failure and capture the exact error message. Run these tests on the UNFIXED code to confirm the bug manifestation.

**Test Cases**:
1. **Initial Page Load Test**: Start server, open http://localhost:8080 in browser (will fail on unfixed code with WebSocket protocol error)
2. **Dashboard Navigation Test**: Login successfully, navigate to /dashboard (will fail on unfixed code when WebSocket connection is attempted)
3. **Page Refresh Test**: Refresh an already-loaded page (will fail on unfixed code on reconnection attempt)
4. **Multiple Browser Test**: Open dashboard in multiple browser tabs simultaneously (will fail on unfixed code for each WebSocket connection)

**Expected Counterexamples**:
- RuntimeError: "Expected ASGI message 'websocket.accept' or 'websocket.close', but got 'http.response.start'"
- Browser console shows WebSocket connection failed
- UI does not render, blank page displayed
- Possible causes: missing storage_secret parameter, ASGI middleware misconfiguration, WebSocket protocol negotiation failure

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds (WebSocket connection attempts), the fixed function produces the expected behavior (successful connection and UI loading).

**Pseudocode:**
```
FOR ALL input WHERE isBugCondition(input) DO
  result := ui_run_with_storage_secret(input)
  ASSERT websocket_connection_accepted(result)
  ASSERT ui_loads_successfully(result)
END FOR
```

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold (non-WebSocket functionality), the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL input WHERE NOT isBugCondition(input) DO
  ASSERT original_behavior(input) = fixed_behavior(input)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the input domain
- It catches edge cases that manual unit tests might miss
- It provides strong guarantees that behavior is unchanged for all non-WebSocket functionality

**Test Plan**: Observe behavior on UNFIXED code first for authentication, session management, and UI interactions, then write property-based tests capturing that behavior.

**Test Cases**:
1. **Authentication Flow Preservation**: Observe that login/logout works on unfixed code (before WebSocket connection), then verify this continues after fix
2. **Session Storage Preservation**: Observe that session tokens are stored and retrieved correctly, then verify this continues after fix
3. **UI Component Preservation**: Observe that UI components (buttons, dialogs, notifications) work correctly, then verify this continues after fix
4. **Database Operations Preservation**: Observe that database queries work correctly, then verify this continues after fix

### Unit Tests

- Test that `storage_secret` is loaded from environment variables
- Test that `ui.run()` is called with the correct parameters including `storage_secret`
- Test that WebSocket connections are accepted when `storage_secret` is configured
- Test that missing `storage_secret` produces a clear error message (if validation is added)

### Property-Based Tests

- Generate random WebSocket connection scenarios and verify all are accepted with `storage_secret` configured
- Generate random session management operations and verify behavior is preserved after fix
- Generate random UI interaction sequences and verify behavior is unchanged
- Test that authentication flow works correctly across many scenarios

### Integration Tests

- Test full user flow: open browser → load login page → authenticate → navigate to dashboard → verify UI loads
- Test session persistence: login → close browser → reopen → verify session is maintained
- Test concurrent users: multiple browsers connecting simultaneously → verify all WebSocket connections succeed
- Test page refresh: load dashboard → refresh page → verify WebSocket reconnection succeeds
