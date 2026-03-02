"""Launch script for Ashoka Dashboard with Authentication"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Create data directory if it doesn't exist
data_dir = Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import NiceGUI and pages
from nicegui import ui, app
from src.ui.auth_page import create_auth_page
from src.ui.dashboard import AshokaGovDashboard

# Session middleware to check authentication
@ui.page('/')
def index():
    """Landing page - shows authentication"""
    create_auth_page()

@ui.page('/dashboard')
def dashboard():
    """Main dashboard - requires authentication"""
    # Check if user is authenticated
    session_token = app.storage.general.get('session_token')
    
    if not session_token:
        # Not authenticated - redirect to login
        ui.notify('Please login to access the dashboard', type='warning')
        ui.navigate.to('/')
        return
    
    # User is authenticated - show dashboard
    dashboard_instance = AshokaGovDashboard()
    dashboard_instance.create_dashboard()

if __name__ == "__main__":
    print("🛡️  Starting Ashoka GenAI Governance Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8080")
    print("🔐 Authentication required - Login with OTP")
    print()
    
    # Create demo users if they don't exist
    from src.services.auth_service import auth_service
    
    # Delete existing users to recreate with proper roles
    from src.database.db_factory import get_dynamodb
    from src.config import config
    
    print("🔄 Setting up default users...")
    
    dynamodb = get_dynamodb()
    
    # Create admin user with admin role (only if doesn't exist)
    try:
        existing_admin = dynamodb.get_item(config.DYNAMODB_USERS_TABLE, {"user_id": "user_admin"})
        if not existing_admin:
            success, message = auth_service.signup("admin", "admin@ashoka.ai", "admin123", "admin")
            if success:
                print("✅ Admin user created: admin / admin123 (role: admin)")
        else:
            # Ensure admin has correct role
            if existing_admin.get('role') != 'admin':
                existing_admin['role'] = 'admin'
                dynamodb.put_item(config.DYNAMODB_USERS_TABLE, existing_admin)
            print("✅ Admin user exists: admin / admin123 (role: admin)")
    except Exception as e:
        print(f"⚠️  Admin user setup: {e}")
    
    # Create demo user with user role (only if doesn't exist)
    try:
        existing_demo = dynamodb.get_item(config.DYNAMODB_USERS_TABLE, {"user_id": "user_demo"})
        if not existing_demo:
            success, message = auth_service.signup("demo", "demo@ashoka.ai", "demo123", "user")
            if success:
                print("✅ Demo user created: demo / demo123 (role: user)")
        else:
            # Ensure demo has correct role
            if existing_demo.get('role') != 'user':
                existing_demo['role'] = 'user'
                dynamodb.put_item(config.DYNAMODB_USERS_TABLE, existing_demo)
            print("✅ Demo user exists: demo / demo123 (role: user)")
    except Exception as e:
        print(f"⚠️  Demo user setup: {e}")
    
    # Show count of all users
    try:
        all_users = dynamodb.query(config.DYNAMODB_USERS_TABLE)
        print(f"📊 Total users in database: {len(all_users)}")
    except Exception as e:
        print(f"⚠️  Could not count users: {e}")
    
    print()
    
    # Check AI configuration
    use_gemini = os.getenv('USE_GEMINI', 'true').lower() == 'true'
    
    if use_gemini:
        print("🤖 AI: Google Gemini (gemini-2.0-flash-exp)")
    else:
        print("⚠️  AI: Not configured - set USE_GEMINI=true and add GEMINI_API_KEY")
    
    print()
    print("Ready! Open http://localhost:8080 in your browser")
    print()
    
    ui.run(
        title='Ashoka - GenAI Governance Platform',
        favicon='🛡️',
        dark=False,
        reload=False,
        host='0.0.0.0',
        port=8080
    )
