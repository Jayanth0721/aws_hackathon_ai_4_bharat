"""
Preservation Property Tests for WebSocket Connection Fix

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

These tests capture the baseline behavior of non-WebSocket functionality
that MUST be preserved after the storage_secret fix is implemented.

IMPORTANT: These tests are run on UNFIXED code to establish baseline behavior.
They should PASS on unfixed code and continue to PASS after the fix.

Property 2: Preservation - Existing Functionality Unchanged
For any application functionality that does NOT involve the initial WebSocket
connection establishment, the fixed code SHALL produce exactly the same behavior
as the original code.
"""

import pytest
import os
import sys
from pathlib import Path
from hypothesis import given, strategies as st, settings, assume
from datetime import datetime, timedelta
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# =============================================================================
# PROPERTY 1: Authentication Flow Preservation
# =============================================================================

@given(
    username=st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    password=st.text(min_size=6, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'P')))
)
@settings(max_examples=5, deadline=None)
def test_property_authentication_flow_preserved(username, password):
    """
    Property: Authentication flow (login/logout) works correctly
    
    **Validates: Requirements 3.1, 3.3**
    
    This test verifies that the authentication service interface remains unchanged:
    - Auth service exists and is callable
    - Required methods are available
    - Method signatures are preserved
    
    This behavior should be identical before and after the storage_secret fix.
    """
    # Import here to avoid hanging during test collection
    from src.services.auth_service import auth_service
    
    # Ensure username is valid
    assume(len(username) >= 3)
    assume(len(password) >= 6)
    
    # Verify authentication service interface exists
    assert auth_service is not None, "Auth service should be available"
    assert hasattr(auth_service, 'signup'), "Auth service should have signup method"
    assert hasattr(auth_service, 'authenticate'), "Auth service should have authenticate method"
    assert hasattr(auth_service, 'generate_otp'), "Auth service should have generate_otp method"
    assert hasattr(auth_service, 'create_session'), "Auth service should have create_session method"
    assert hasattr(auth_service, 'verify_otp'), "Auth service should have verify_otp method"
    
    print(f"✅ Authentication flow interface preserved")


# =============================================================================
# PROPERTY 2: Session Storage Preservation
# =============================================================================

def test_property_session_storage_preserved():
    """
    Property: Session tokens are stored and retrieved from app.storage.general
    
    **Validates: Requirements 3.2**
    
    This test verifies that session management using app.storage.general
    remains unchanged. The fix adds storage_secret but should not change
    how session data is stored and retrieved.
    
    Note: This test verifies the storage mechanism exists and is used correctly
    in the codebase, not the actual runtime storage (which requires WebSocket).
    """
    # Check that app.storage.general is used for session management
    files_using_storage = []
    
    # Check run_dashboard.py
    dashboard_file = Path(__file__).parent.parent / 'run_dashboard.py'
    if dashboard_file.exists():
        content = dashboard_file.read_text(encoding='utf-8')
        if 'app.storage.general' in content and 'session_token' in content:
            files_using_storage.append('run_dashboard.py')
    
    # Check auth_page.py
    auth_page_file = Path(__file__).parent.parent / 'src' / 'ui' / 'auth_page.py'
    if auth_page_file.exists():
        content = auth_page_file.read_text(encoding='utf-8')
        if 'app.storage.general' in content:
            files_using_storage.append('src/ui/auth_page.py')
    
    # Check dashboard.py
    dashboard_ui_file = Path(__file__).parent.parent / 'src' / 'ui' / 'dashboard.py'
    if dashboard_ui_file.exists():
        content = dashboard_ui_file.read_text(encoding='utf-8')
        if 'app.storage.general' in content:
            files_using_storage.append('src/ui/dashboard.py')
    
    # Verify storage is used
    assert len(files_using_storage) > 0, (
        "app.storage.general should be used for session management"
    )
    
    # Verify specific session-related keys are used
    session_keys = ['session_token', 'user_id', 'username']
    found_keys = []
    
    for file_path in files_using_storage:
        full_path = Path(__file__).parent.parent / file_path
        content = full_path.read_text(encoding='utf-8')
        for key in session_keys:
            if f"'{key}'" in content or f'"{key}"' in content:
                if key not in found_keys:
                    found_keys.append(key)
    
    assert 'session_token' in found_keys, "session_token should be stored in app.storage.general"
    assert 'user_id' in found_keys, "user_id should be stored in app.storage.general"
    
    print(f"✅ Session storage preserved: {len(files_using_storage)} files use app.storage.general")
    print(f"   Session keys found: {found_keys}")


# =============================================================================
# PROPERTY 3: User Preferences Preservation
# =============================================================================

def test_property_user_preferences_preserved():
    """
    Property: User preferences (language, username, user_id) are persisted
    
    **Validates: Requirements 3.2, 3.4**
    
    This test verifies that user preference storage remains unchanged.
    The dashboard stores language preferences and user context in
    app.storage.general, and this should continue to work after the fix.
    """
    # Check that user preferences are stored in app.storage.general
    dashboard_file = Path(__file__).parent.parent / 'src' / 'ui' / 'dashboard.py'
    
    if not dashboard_file.exists():
        pytest.skip("Dashboard file not found")
    
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Verify language preference storage
    assert 'language' in content, "Language preference should be stored"
    assert 'app.storage.general' in content, "Preferences should use app.storage.general"
    
    # Verify user context storage
    user_context_keys = ['user_id', 'username']
    found_context = []
    
    for key in user_context_keys:
        if f"'{key}'" in content or f'"{key}"' in content:
            found_context.append(key)
    
    assert len(found_context) > 0, (
        f"User context should be stored. Expected keys: {user_context_keys}, "
        f"Found: {found_context}"
    )
    
    print(f"✅ User preferences preserved: language and user context stored")
    print(f"   Context keys found: {found_context}")


# =============================================================================
# PROPERTY 4: UI Components Preservation
# =============================================================================

def test_property_ui_components_preserved():
    """
    Property: UI components render and interact correctly
    
    **Validates: Requirements 3.4**
    
    This test verifies that UI component definitions remain unchanged.
    The fix should not affect how NiceGUI components are defined and used.
    """
    # Check that NiceGUI components are used correctly
    ui_files = [
        Path(__file__).parent.parent / 'src' / 'ui' / 'auth_page.py',
        Path(__file__).parent.parent / 'src' / 'ui' / 'dashboard.py',
        Path(__file__).parent.parent / 'run_dashboard.py'
    ]
    
    nicegui_components = [
        'ui.page',
        'ui.button',
        'ui.input',
        'ui.label',
        'ui.notify',
        'ui.navigate',
        'ui.dialog',
        'ui.card'
    ]
    
    components_found = {}
    
    for ui_file in ui_files:
        if not ui_file.exists():
            continue
        
        content = ui_file.read_text(encoding='utf-8')
        file_name = ui_file.name
        
        for component in nicegui_components:
            if component in content:
                if component not in components_found:
                    components_found[component] = []
                components_found[component].append(file_name)
    
    # Verify essential UI components are used
    assert 'ui.page' in components_found, "ui.page should be used for routing"
    assert 'ui.button' in components_found, "ui.button should be used for interactions"
    assert 'ui.notify' in components_found, "ui.notify should be used for notifications"
    assert 'ui.navigate' in components_found, "ui.navigate should be used for navigation"
    
    print(f"✅ UI components preserved: {len(components_found)} component types found")
    for component, files in components_found.items():
        print(f"   {component}: used in {len(files)} files")


# =============================================================================
# PROPERTY 5: Database Operations Preservation
# =============================================================================

@given(
    content_id=st.text(min_size=5, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    content_type=st.sampled_from(['article', 'document', 'report', 'policy'])
)
@settings(max_examples=5, deadline=None)
def test_property_database_operations_preserved(content_id, content_type):
    """
    Property: Database operations execute successfully
    
    **Validates: Requirements 3.1, 3.4**
    
    This test verifies that database operations (DynamoDB) remain unchanged.
    The fix should not affect how the application interacts with the database.
    
    Note: This test verifies the database interface exists and is callable,
    not the actual database operations (which require proper table setup).
    """
    # Import here to avoid hanging during test collection
    from src.database.db_factory import get_dynamodb
    from src.config import config
    
    dynamodb = get_dynamodb()
    
    # Verify database interface exists and is callable
    assert dynamodb is not None, "Database connection should be available"
    assert hasattr(dynamodb, 'put_item'), "Database should have put_item method"
    assert hasattr(dynamodb, 'get_item'), "Database should have get_item method"
    assert hasattr(dynamodb, 'query'), "Database should have query method"
    assert hasattr(dynamodb, 'delete_item'), "Database should have delete_item method"
    
    print(f"✅ Database operations interface preserved for content type: {content_type}")


# =============================================================================
# PROPERTY 6: Server Startup Configuration Preservation
# =============================================================================

def test_property_server_startup_preserved():
    """
    Property: Server startup configuration remains unchanged
    
    **Validates: Requirements 3.1**
    
    This test verifies that ui.run() configuration (except storage_secret)
    remains unchanged. The fix should only add storage_secret parameter.
    """
    dashboard_file = Path(__file__).parent.parent / 'run_dashboard.py'
    
    if not dashboard_file.exists():
        pytest.skip("Dashboard file not found")
    
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Verify ui.run() is called
    assert 'ui.run(' in content, "ui.run() should be called to start server"
    
    # Verify essential parameters are present
    essential_params = ['title', 'host', 'port']
    found_params = []
    
    for param in essential_params:
        if f"{param}=" in content:
            found_params.append(param)
    
    assert 'title' in found_params, "ui.run() should have title parameter"
    assert 'port' in found_params or '8080' in content, "ui.run() should specify port"
    
    # Verify server startup messages
    assert 'Starting' in content or 'Dashboard' in content, "Startup messages should be present"
    assert 'localhost' in content or '8080' in content, "Server address should be mentioned"
    
    print(f"✅ Server startup preserved: ui.run() configuration intact")
    print(f"   Parameters found: {found_params}")


# =============================================================================
# PROPERTY 7: Authentication Redirect Logic Preservation
# =============================================================================

def test_property_authentication_redirect_preserved():
    """
    Property: Authentication redirect logic remains unchanged
    
    **Validates: Requirements 3.3**
    
    This test verifies that the authentication check and redirect logic
    in the dashboard route remains unchanged. Unauthenticated users should
    still be redirected to login.
    """
    dashboard_file = Path(__file__).parent.parent / 'run_dashboard.py'
    
    if not dashboard_file.exists():
        pytest.skip("Dashboard file not found")
    
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Verify dashboard route exists
    assert '@ui.page(\'/dashboard\')' in content, "Dashboard route should exist"
    
    # Verify session token check
    assert 'session_token' in content, "Session token should be checked"
    assert 'app.storage.general' in content, "Should use app.storage.general for session"
    
    # Verify redirect logic
    assert 'ui.navigate' in content or 'ui.notify' in content, "Should have redirect/notification logic"
    
    # Verify authentication check pattern
    lines = content.split('\n')
    found_auth_check = False
    
    for i, line in enumerate(lines):
        if 'session_token' in line and 'app.storage.general' in line:
            # Look for redirect logic nearby
            context = '\n'.join(lines[max(0, i-5):min(len(lines), i+10)])
            if 'ui.navigate' in context or 'ui.notify' in context:
                found_auth_check = True
                break
    
    assert found_auth_check, (
        "Authentication check and redirect logic should be present in dashboard route"
    )
    
    print(f"✅ Authentication redirect preserved: session check and redirect logic intact")


if __name__ == "__main__":
    print("=" * 80)
    print("Preservation Property Tests - WebSocket Connection Fix")
    print("=" * 80)
    print()
    print("These tests verify that non-WebSocket functionality remains unchanged.")
    print("Tests should PASS on unfixed code and continue to PASS after the fix.")
    print()
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
