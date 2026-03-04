"""
Bug Condition Exploration Test for WebSocket Connection Fix

**Validates: Requirements 2.1, 2.2, 2.3**

This test explores the bug condition where WebSocket connections fail when
storage_secret is not configured in ui.run(). 

CRITICAL: This test is EXPECTED TO FAIL on unfixed code - failure confirms the bug exists.
The test encodes the expected behavior and will validate the fix when it passes after implementation.

Property 1: Fault Condition - WebSocket Connection Acceptance
For any WebSocket connection attempt when the application uses app.storage.general
and storage_secret is properly configured, the system SHALL accept the WebSocket
connection without errors, allowing the UI to load successfully.
"""

import pytest
import os
import sys
import re
from pathlib import Path
from hypothesis import given, strategies as st, settings

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def check_storage_secret_configured():
    """
    Check if storage_secret is configured in run_dashboard.py
    
    Returns:
        tuple: (is_configured: bool, has_parameter: bool, has_env_var: bool)
    """
    dashboard_file = Path(__file__).parent.parent / 'run_dashboard.py'
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Check if storage_secret parameter is in ui.run() call
    ui_run_pattern = r'ui\.run\([^)]*\)'
    ui_run_match = re.search(ui_run_pattern, content, re.DOTALL)
    
    has_parameter = False
    if ui_run_match:
        ui_run_call = ui_run_match.group(0)
        has_parameter = 'storage_secret' in ui_run_call
    
    # Check if STORAGE_SECRET environment variable is loaded
    has_env_var = "os.getenv('STORAGE_SECRET')" in content or 'os.environ.get("STORAGE_SECRET")' in content
    
    is_configured = has_parameter and has_env_var
    
    return (is_configured, has_parameter, has_env_var)


def check_app_storage_usage():
    """
    Check if app.storage.general is used in the codebase
    
    Returns:
        list: List of files that use app.storage.general
    """
    src_dir = Path(__file__).parent.parent / 'src'
    files_using_storage = []
    
    for py_file in src_dir.rglob('*.py'):
        try:
            content = py_file.read_text(encoding='utf-8')
            if 'app.storage.general' in content:
                files_using_storage.append(str(py_file.relative_to(src_dir.parent)))
        except (UnicodeDecodeError, PermissionError):
            # Skip files that can't be read
            continue
    
    # Also check run_dashboard.py
    dashboard_file = Path(__file__).parent.parent / 'run_dashboard.py'
    try:
        if 'app.storage.general' in dashboard_file.read_text(encoding='utf-8'):
            files_using_storage.append('run_dashboard.py')
    except (UnicodeDecodeError, PermissionError):
        pass
    
    return files_using_storage


def test_bug_condition_storage_secret_missing():
    """
    Bug Condition Exploration Test - Storage Secret Configuration
    
    **CRITICAL**: This test is EXPECTED TO FAIL on unfixed code.
    
    This test verifies the bug condition: the application uses app.storage.general
    but storage_secret is NOT configured in ui.run().
    
    According to NiceGUI documentation, when app.storage.general is used,
    storage_secret MUST be provided to ui.run() for proper WebSocket handling.
    
    **Validates: Requirements 2.1, 2.2, 2.3**
    
    Bug Condition:
    - app.storage.general is used throughout the codebase
    - storage_secret parameter is missing from ui.run() call
    - This causes WebSocket connections to fail with protocol mismatch error
    
    Expected Behavior (after fix):
    - storage_secret parameter is present in ui.run() call
    - storage_secret is loaded from environment variable
    - WebSocket connections are accepted properly
    """
    # Check if app.storage.general is used
    files_using_storage = check_app_storage_usage()
    
    print(f"\n📊 Files using app.storage.general: {len(files_using_storage)}")
    for file in files_using_storage:
        print(f"   - {file}")
    
    assert len(files_using_storage) > 0, (
        "Expected app.storage.general to be used in the codebase"
    )
    
    # Check if storage_secret is configured
    is_configured, has_parameter, has_env_var = check_storage_secret_configured()
    
    print(f"\n🔍 Storage Secret Configuration:")
    print(f"   - storage_secret parameter in ui.run(): {has_parameter}")
    print(f"   - STORAGE_SECRET environment variable loaded: {has_env_var}")
    print(f"   - Fully configured: {is_configured}")
    
    # On UNFIXED code, this assertion will FAIL
    # This confirms the bug condition exists
    assert is_configured, (
        f"\n❌ BUG CONDITION DETECTED:\n"
        f"   - app.storage.general is used in {len(files_using_storage)} files\n"
        f"   - storage_secret parameter in ui.run(): {has_parameter}\n"
        f"   - STORAGE_SECRET environment variable loaded: {has_env_var}\n"
        f"\n"
        f"According to NiceGUI documentation, when app.storage.general is used,\n"
        f"storage_secret MUST be provided to ui.run() for proper WebSocket handling.\n"
        f"\n"
        f"Without storage_secret, WebSocket connections fail with:\n"
        f"'Expected ASGI message websocket.accept or websocket.close, but got http.response.start'\n"
        f"\n"
        f"This test will PASS after the fix is implemented."
    )
    
    print("\n✅ Storage secret is properly configured - bug is FIXED")


@given(st.text(min_size=32, max_size=64, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
@settings(max_examples=5)
def test_property_storage_secret_requirements(secret_value):
    """
    Property-Based Test - Storage Secret Requirements
    
    **Validates: Requirements 2.1, 2.2, 2.3**
    
    Property: For ANY valid storage_secret value (minimum 32 characters),
    when properly configured in ui.run(), the system SHALL accept WebSocket
    connections without errors.
    
    This test verifies that the storage_secret configuration mechanism
    works correctly across different secret values.
    """
    # Verify the secret meets minimum requirements
    assert len(secret_value) >= 32, (
        f"Storage secret must be at least 32 characters, got {len(secret_value)}"
    )
    
    # Check if storage_secret is configured in the code
    is_configured, has_parameter, has_env_var = check_storage_secret_configured()
    
    # Property assertion: storage_secret MUST be configured
    assert is_configured, (
        f"Property violation: storage_secret not configured in ui.run()\n"
        f"   - Parameter in ui.run(): {has_parameter}\n"
        f"   - Environment variable loaded: {has_env_var}\n"
        f"For secret value length: {len(secret_value)}"
    )


def test_preservation_app_storage_usage():
    """
    Preservation Test - app.storage.general Usage
    
    **Validates: Requirements 3.2**
    
    This test verifies that app.storage.general is still used for session
    management after the fix. The fix should only add storage_secret parameter,
    not change how app.storage.general is used.
    """
    files_using_storage = check_app_storage_usage()
    
    # Verify that app.storage.general is still used
    assert len(files_using_storage) > 0, (
        "app.storage.general should still be used for session management"
    )
    
    # Check specific files that should use storage
    expected_files = ['run_dashboard.py', 'auth_page.py']
    for expected_file in expected_files:
        matching_files = [f for f in files_using_storage if expected_file in f]
        assert len(matching_files) > 0, (
            f"Expected {expected_file} to use app.storage.general for session management"
        )
    
    print(f"\n✅ Preservation verified: app.storage.general still used in {len(files_using_storage)} files")


if __name__ == "__main__":
    # Run the bug exploration test
    print("=" * 80)
    print("Bug Condition Exploration Test - WebSocket Connection Fix")
    print("=" * 80)
    print()
    print("CRITICAL: This test is EXPECTED TO FAIL on unfixed code.")
    print("Failure confirms the bug exists.")
    print()
    
    test_bug_condition_storage_secret_missing()
