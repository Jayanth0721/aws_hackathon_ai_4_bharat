# Bugfix Requirements Document

## Introduction

The NiceGUI dashboard application crashes when WebSocket connections are attempted, preventing the UI from loading in the browser. The error occurs because the application uses `app.storage.general` for session management but does not provide the required `storage_secret` parameter to `ui.run()`. This causes the ASGI middleware to send HTTP responses instead of accepting WebSocket connections, resulting in a protocol mismatch error: "Expected ASGI message 'websocket.accept' or 'websocket.close', but got 'http.response.start'."

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN the dashboard starts and a WebSocket connection is attempted THEN the system crashes with RuntimeError: "Expected ASGI message 'websocket.accept' or 'websocket.close', but got 'http.response.start'"

1.2 WHEN `app.storage.general` is used without `storage_secret` configured THEN the ASGI middleware fails to properly negotiate WebSocket connections

1.3 WHEN the WebSocket connection fails THEN the UI does not load in the browser despite the server starting successfully at http://localhost:8080

### Expected Behavior (Correct)

2.1 WHEN the dashboard starts and a WebSocket connection is attempted THEN the system SHALL accept the WebSocket connection without errors

2.2 WHEN `app.storage.general` is used with `storage_secret` configured THEN the ASGI middleware SHALL properly negotiate WebSocket connections

2.3 WHEN the WebSocket connection succeeds THEN the UI SHALL load properly in the browser

### Unchanged Behavior (Regression Prevention)

3.1 WHEN the dashboard starts successfully THEN the system SHALL CONTINUE TO display startup messages and listen on http://localhost:8080

3.2 WHEN session tokens are stored in `app.storage.general` THEN the system SHALL CONTINUE TO maintain authentication state across requests

3.3 WHEN users authenticate and navigate to /dashboard THEN the system SHALL CONTINUE TO check session tokens and redirect unauthenticated users to login

3.4 WHEN the application uses other NiceGUI features (ui.page, ui.notify, ui.navigate) THEN the system SHALL CONTINUE TO function correctly
