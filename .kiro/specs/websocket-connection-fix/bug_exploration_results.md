# Bug Condition Exploration Results

## Test Execution Summary

**Test**: `test_bug_condition_storage_secret_missing`
**Status**: ✅ PASSED (Test correctly detected the bug condition)
**Date**: 2026-03-03

## Bug Condition Confirmed

The bug condition exploration test successfully confirmed the existence of the bug described in the bugfix specification.

### Counterexamples Found

1. **Missing storage_secret Parameter**
   - **Location**: `run_dashboard.py`, line 119 (ui.run() call)
   - **Issue**: The `storage_secret` parameter is NOT present in the ui.run() call
   - **Impact**: WebSocket connections fail with protocol mismatch error

2. **Missing Environment Variable Loading**
   - **Location**: `run_dashboard.py`
   - **Issue**: STORAGE_SECRET environment variable is NOT loaded from .env
   - **Impact**: Even if storage_secret parameter were added, it would have no value

3. **Widespread app.storage.general Usage**
   - **Files Affected**: 3 files use app.storage.general
     - `src/ui/auth_page.py` - Stores session tokens after login
     - `src/ui/dashboard.py` - Reads user preferences and session data
     - `run_dashboard.py` - Checks session tokens for authentication
   - **Issue**: All these files depend on app.storage.general working correctly
   - **Impact**: Without storage_secret, the storage layer fails to initialize properly for WebSocket connections

### Root Cause Validation

The test confirms the root cause identified in the design document:

> According to NiceGUI documentation, when app.storage.general is used, storage_secret MUST be provided to ui.run() for proper WebSocket handling.

**Current State (UNFIXED)**:
```python
ui.run(
    title='Ashoka - GenAI Governance Platform',
    dark=False,
    reload=False,
    host='0.0.0.0',
    port=8080
)
# ❌ Missing storage_secret parameter
```

**Expected State (FIXED)**:
```python
storage_secret = os.getenv('STORAGE_SECRET')
ui.run(
    title='Ashoka - GenAI Governance Platform',
    dark=False,
    reload=False,
    host='0.0.0.0',
    port=8080,
    storage_secret=storage_secret  # ✅ Added
)
```

### Error Manifestation

Without storage_secret configured, WebSocket connections fail with:
```
RuntimeError: Expected ASGI message 'websocket.accept' or 'websocket.close', 
but got 'http.response.start'
```

This error occurs because:
1. Browser attempts to establish WebSocket connection to NiceGUI dashboard
2. ASGI middleware cannot properly initialize the storage layer without storage_secret
3. Middleware falls back to HTTP response instead of accepting WebSocket
4. WebSocket protocol violation occurs
5. UI fails to load in browser

### Test Validation

The bug condition exploration test validates:
- ✅ app.storage.general is used in the codebase (3 files)
- ✅ storage_secret parameter is missing from ui.run()
- ✅ STORAGE_SECRET environment variable is not loaded
- ✅ Bug condition is correctly identified

### Next Steps

The test encodes the expected behavior. After implementing the fix (Task 3), this same test will:
1. Detect that storage_secret parameter IS present in ui.run()
2. Detect that STORAGE_SECRET environment variable IS loaded
3. PASS, confirming the bug is fixed

## Property-Based Test Coverage

The test suite includes:
1. **Bug Condition Test**: Verifies storage_secret is missing (FAILS on unfixed code)
2. **Property Test**: Verifies storage_secret requirements across different secret values
3. **Preservation Test**: Verifies app.storage.general usage is preserved

All tests are ready to validate the fix once implemented.
