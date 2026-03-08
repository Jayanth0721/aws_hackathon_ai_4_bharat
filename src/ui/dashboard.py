
"""Ashoka GenAI Governance Dashboard - NiceGUI Implementation"""
from nicegui import ui, app
from datetime import datetime, timedelta
from typing import Optional
import json
import pytz

from src.services.content_ingestion import ContentIngestionService
from src.services.content_analyzer import ContentAnalyzer
from src.services.file_processor import file_processor
from src.services.content_transformer import content_transformer
from src.services.gemini_client import gemini_client
from src.services.auth_service import auth_service
from src.database.duckdb_schema import db_schema
from src.utils.logging import logger


class AshokaGovDashboard:
    """GenAI Governance Dashboard"""
    
    def __init__(self):
        self.ingestion_service = ContentIngestionService()
        self.analyzer = ContentAnalyzer()
        self.current_user = app.storage.general.get('user_id', 'demo_user')
        self.current_user_id = self.current_user  # Add user_id attribute for tracking
        self.current_user_role = 'creator'
        self.current_username = 'demo'
        self.current_email = 'demo@ashoka.ai'
        self.current_analysis = None
        self.uploaded_file_path = None
        
        # Processing flags to prevent auto-refresh interference during long operations
        self._youtube_processing = False
        self._audio_processing = False
        self._video_processing = False
        
        # Analysis history for Content Intelligence
        self.analysis_history = []
        self._metrics_cache = {}
        self._metrics_cache_ttl_seconds = 45
        
        # Session management - Load from storage or initialize
        # Load user's session timeout preference from storage (default 30 minutes)
        stored_session_timeout = app.storage.general.get('session_timeout', 30)
        self.session_duration = stored_session_timeout * 60  # Convert minutes to seconds
        
        # Try to load session start time from storage
        stored_session_start = app.storage.general.get('session_start_time')
        if stored_session_start:
            try:
                # Parse the stored timestamp
                self.session_start_time = datetime.fromisoformat(stored_session_start)
                logger.info(f"Loaded session start time from storage: {self.session_start_time}")
                logger.info(f"Session duration: {self.session_duration / 60} minutes")
            except Exception as e:
                logger.error(f"Error parsing stored session start time: {e}")
                self.session_start_time = datetime.now()
                app.storage.general['session_start_time'] = self.session_start_time.isoformat()
        else:
            # New session - store the start time
            self.session_start_time = datetime.now()
            app.storage.general['session_start_time'] = self.session_start_time.isoformat()
            logger.info(f"New session started at: {self.session_start_time}")
            logger.info(f"Session duration: {self.session_duration / 60} minutes")
        
        self.session_timer = None
        self.session_paused = False
        self.paused_tasks = []
        
        # Current operation tracking
        self.current_operation = None
        self.operation_paused = False
        
        # Use app.storage.general instead of app.storage.user (doesn't require secret)
        self.current_language = app.storage.general.get('language', 'English')
        
        # User preferences
        self.user_preferences = {
            'notifications': True,
            'auto_save': True,
            'theme': 'light',
            'language': 'English',
            'email_alerts': False,
            'session_timeout': 30,
            'timezone': 'IST'  # Default timezone
        }
        
        self.translations = {
            "English": {
                "title": "Ashoka",
                "subtitle": "GenAI Governance & Observability Platform",
                "overview": "Overview",
                "content_intelligence": "Content Intelligence",
                "transform": "Transform",
                "monitoring": "Monitoring",
                "alerts": "Alerts",
                "security": "Security",
                "profile": "Profile",
                "settings": "Settings",
                "logout": "Logout",
                "user_profile": "User Profile",
                "username": "Username",
                "email": "Email",
                "role": "Role",
                "member_since": "Member Since",
                "close": "Close",
                "language_settings": "Language Settings",
                "select_language": "Select Language",
                "apply": "Apply",
                # Overview Panel
                "platform_overview": "Platform Overview",
                "total_content": "Total Content",
                "this_week": "this week",
                "quality_score": "Quality Score",
                "excellent": "Excellent",
                "risk_alerts": "Risk Alerts",
                "resolved": "resolved",
                "ai_operations": "AI Operations",
                "success": "success",
                "recent_activity": "Recent Activity",
                "content_analyzed": "Content analyzed",
                "article_ai_ethics": "Article about AI ethics",
                "min_ago": "min ago",
                "risk_detected": "Risk detected",
                "policy_violation": "Potential policy violation",
                "content_transformed": "Content transformed",
                "linkedin_twitter": "LinkedIn + Twitter posts",
                "hour_ago": "hour ago",
                "quality_alert": "Quality alert",
                "readability_below": "Readability below threshold",
                "hours_ago": "hours ago",
                "system_health": "System Health",
                "ai_model_performance": "AI Model Performance",
                "content_processing_rate": "Content Processing Rate",
                "storage_utilization": "Storage Utilization",
                "api_healthy": "API: Healthy",
                "database_healthy": "Database: Healthy",
                "ai_healthy": "AI: Healthy",
                # Settings Dialog
                "settings_preferences": "Settings & Preferences",
                "language": "Language",
                "notifications": "Notifications",
                "enable_notifications": "Enable notifications",
                "email_alerts_critical": "Email alerts for critical issues",
                "content_management": "Content Management",
                "auto_save_drafts": "Auto-save content drafts",
                "session": "Session",
                "session_timeout_minutes": "Session timeout (minutes)",
                "paused_tasks": "Paused Tasks",
                "you_have_paused_tasks": "You have {count} paused tasks",
                "view_paused_tasks": "View Paused Tasks",
                "cancel": "Cancel",
                "save_settings": "Save Settings",
                "settings_saved": "Settings saved successfully"
            },
            "Hindi": {
                "title": "à¤…à¤¶à¥‹à¤•",
                "subtitle": "à¤œà¥‡à¤¨à¤à¤†à¤ˆ à¤—à¤µà¤°à¥à¤¨à¥‡à¤‚à¤¸ à¤”à¤° à¤‘à¤¬à¥à¤œà¤°à¥à¤µà¥‡à¤¬à¤¿à¤²à¤¿à¤Ÿà¥€ à¤ªà¥à¤²à¥‡à¤Ÿà¤«à¥‰à¤°à¥à¤®",
                "overview": "à¤…à¤µà¤²à¥‹à¤•à¤¨",
                "content_intelligence": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤¬à¥à¤¦à¥à¤§à¤¿à¤®à¤¤à¥à¤¤à¤¾",
                "transform": "à¤°à¥‚à¤ªà¤¾à¤‚à¤¤à¤°à¤£",
                "monitoring": "à¤¨à¤¿à¤—à¤°à¤¾à¤¨à¥€",
                "alerts": "à¤…à¤²à¤°à¥à¤Ÿ",
                "security": "à¤¸à¥à¤°à¤•à¥à¤·à¤¾",
                "profile": "à¤ªà¥à¤°à¥‹à¤«à¤¼à¤¾à¤‡à¤²",
                "settings": "à¤¸à¥‡à¤Ÿà¤¿à¤‚à¤—à¥à¤¸",
                "logout": "à¤²à¥‰à¤—à¤†à¤‰à¤Ÿ",
                "user_profile": "à¤‰à¤ªà¤¯à¥‹à¤—à¤•à¤°à¥à¤¤à¤¾ à¤ªà¥à¤°à¥‹à¤«à¤¼à¤¾à¤‡à¤²",
                "username": "à¤‰à¤ªà¤¯à¥‹à¤—à¤•à¤°à¥à¤¤à¤¾ à¤¨à¤¾à¤®",
                "email": "à¤ˆà¤®à¥‡à¤²",
                "role": "à¤­à¥‚à¤®à¤¿à¤•à¤¾",
                "member_since": "à¤¸à¤¦à¤¸à¥à¤¯ à¤¬à¤¨à¥‡",
                "close": "à¤¬à¤‚à¤¦ à¤•à¤°à¥‡à¤‚",
                "language_settings": "à¤­à¤¾à¤·à¤¾ à¤¸à¥‡à¤Ÿà¤¿à¤‚à¤—à¥à¤¸",
                "select_language": "à¤­à¤¾à¤·à¤¾ à¤šà¥à¤¨à¥‡à¤‚",
                "apply": "à¤²à¤¾à¤—à¥‚ à¤•à¤°à¥‡à¤‚",
                # Overview Panel
                "platform_overview": "à¤ªà¥à¤²à¥‡à¤Ÿà¤«à¤¼à¥‰à¤°à¥à¤® à¤…à¤µà¤²à¥‹à¤•à¤¨",
                "total_content": "à¤•à¥à¤² à¤¸à¤¾à¤®à¤—à¥à¤°à¥€",
                "this_week": "à¤‡à¤¸ à¤¸à¤ªà¥à¤¤à¤¾à¤¹",
                "quality_score": "à¤—à¥à¤£à¤µà¤¤à¥à¤¤à¤¾ à¤¸à¥à¤•à¥‹à¤°",
                "excellent": "à¤‰à¤¤à¥à¤•à¥ƒà¤·à¥à¤Ÿ",
                "risk_alerts": "à¤œà¥‹à¤–à¤¿à¤® à¤…à¤²à¤°à¥à¤Ÿ",
                "resolved": "à¤¹à¤² à¤•à¤¿à¤¯à¤¾ à¤—à¤¯à¤¾",
                "ai_operations": "à¤à¤†à¤ˆ à¤¸à¤‚à¤šà¤¾à¤²à¤¨",
                "success": "à¤¸à¤«à¤²à¤¤à¤¾",
                "recent_activity": "à¤¹à¤¾à¤² à¤•à¥€ à¤—à¤¤à¤¿à¤µà¤¿à¤§à¤¿",
                "content_analyzed": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤µà¤¿à¤¶à¥à¤²à¥‡à¤·à¤£",
                "article_ai_ethics": "à¤à¤†à¤ˆ à¤¨à¥ˆà¤¤à¤¿à¤•à¤¤à¤¾ à¤ªà¤° à¤²à¥‡à¤–",
                "min_ago": "à¤®à¤¿à¤¨à¤Ÿ à¤ªà¤¹à¤²à¥‡",
                "risk_detected": "à¤œà¥‹à¤–à¤¿à¤® à¤•à¤¾ à¤ªà¤¤à¤¾ à¤šà¤²à¤¾",
                "policy_violation": "à¤¸à¤‚à¤­à¤¾à¤µà¤¿à¤¤ à¤¨à¥€à¤¤à¤¿ à¤‰à¤²à¥à¤²à¤‚à¤˜à¤¨",
                "content_transformed": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤°à¥‚à¤ªà¤¾à¤‚à¤¤à¤°à¤¿à¤¤",
                "linkedin_twitter": "à¤²à¤¿à¤‚à¤•à¥à¤¡à¤‡à¤¨ + à¤Ÿà¥à¤µà¤¿à¤Ÿà¤° à¤ªà¥‹à¤¸à¥à¤Ÿ",
                "hour_ago": "à¤˜à¤‚à¤Ÿà¥‡ à¤ªà¤¹à¤²à¥‡",
                "quality_alert": "à¤—à¥à¤£à¤µà¤¤à¥à¤¤à¤¾ à¤…à¤²à¤°à¥à¤Ÿ",
                "readability_below": "à¤ªà¤ à¤¨à¥€à¤¯à¤¤à¤¾ à¤¸à¥€à¤®à¤¾ à¤¸à¥‡ à¤¨à¥€à¤šà¥‡",
                "hours_ago": "à¤˜à¤‚à¤Ÿà¥‡ à¤ªà¤¹à¤²à¥‡",
                "system_health": "à¤¸à¤¿à¤¸à¥à¤Ÿà¤® à¤¸à¥à¤µà¤¾à¤¸à¥à¤¥à¥à¤¯",
                "ai_model_performance": "à¤à¤†à¤ˆ à¤®à¥‰à¤¡à¤² à¤ªà¥à¤°à¤¦à¤°à¥à¤¶à¤¨",
                "content_processing_rate": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤ªà¥à¤°à¤¸à¤‚à¤¸à¥à¤•à¤°à¤£ à¤¦à¤°",
                "storage_utilization": "à¤­à¤‚à¤¡à¤¾à¤°à¤£ à¤‰à¤ªà¤¯à¥‹à¤—",
                "api_healthy": "à¤à¤ªà¥€à¤†à¤ˆ: à¤¸à¥à¤µà¤¸à¥à¤¥",
                "database_healthy": "à¤¡à¥‡à¤Ÿà¤¾à¤¬à¥‡à¤¸: à¤¸à¥à¤µà¤¸à¥à¤¥",
                "ai_healthy": "à¤à¤†à¤ˆ: à¤¸à¥à¤µà¤¸à¥à¤¥",
                # Settings Dialog
                "settings_preferences": "à¤¸à¥‡à¤Ÿà¤¿à¤‚à¤—à¥à¤¸ à¤”à¤° à¤ªà¥à¤°à¤¾à¤¥à¤®à¤¿à¤•à¤¤à¤¾à¤à¤‚",
                "language": "à¤­à¤¾à¤·à¤¾",
                "notifications": "à¤¸à¥‚à¤šà¤¨à¤¾à¤à¤‚",
                "enable_notifications": "à¤¸à¥‚à¤šà¤¨à¤¾à¤à¤‚ à¤¸à¤•à¥à¤·à¤® à¤•à¤°à¥‡à¤‚",
                "email_alerts_critical": "à¤®à¤¹à¤¤à¥à¤µà¤ªà¥‚à¤°à¥à¤£ à¤®à¥à¤¦à¥à¤¦à¥‹à¤‚ à¤•à¥‡ à¤²à¤¿à¤ à¤ˆà¤®à¥‡à¤² à¤…à¤²à¤°à¥à¤Ÿ",
                "content_management": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤ªà¥à¤°à¤¬à¤‚à¤§à¤¨",
                "auto_save_drafts": "à¤¸à¤¾à¤®à¤—à¥à¤°à¥€ à¤¡à¥à¤°à¤¾à¤«à¥à¤Ÿ à¤¸à¥à¤µà¤¤à¤ƒ à¤¸à¤¹à¥‡à¤œà¥‡à¤‚",
                "session": "à¤¸à¤¤à¥à¤°",
                "session_timeout_minutes": "à¤¸à¤¤à¥à¤° à¤¸à¤®à¤¯ à¤¸à¤®à¤¾à¤ªà¥à¤¤à¤¿ (à¤®à¤¿à¤¨à¤Ÿ)",
                "paused_tasks": "à¤°à¥‹à¤•à¥‡ à¤—à¤ à¤•à¤¾à¤°à¥à¤¯",
                "you_have_paused_tasks": "à¤†à¤ªà¤•à¥‡ à¤ªà¤¾à¤¸ {count} à¤°à¥‹à¤•à¥‡ à¤—à¤ à¤•à¤¾à¤°à¥à¤¯ à¤¹à¥ˆà¤‚",
                "view_paused_tasks": "à¤°à¥‹à¤•à¥‡ à¤—à¤ à¤•à¤¾à¤°à¥à¤¯ à¤¦à¥‡à¤–à¥‡à¤‚",
                "cancel": "à¤°à¤¦à¥à¤¦ à¤•à¤°à¥‡à¤‚",
                "save_settings": "à¤¸à¥‡à¤Ÿà¤¿à¤‚à¤—à¥à¤¸ à¤¸à¤¹à¥‡à¤œà¥‡à¤‚",
                "settings_saved": "à¤¸à¥‡à¤Ÿà¤¿à¤‚à¤—à¥à¤¸ à¤¸à¤«à¤²à¤¤à¤¾à¤ªà¥‚à¤°à¥à¤µà¤• à¤¸à¤¹à¥‡à¤œà¥€ à¤—à¤ˆà¤‚"
            },
            "Kannada": {
                "title": "à²…à²¶à³‹à²•",
                "subtitle": "à²œà³†à²¨à³â€Œà²Žà² à²†à²¡à²³à²¿à²¤ à²®à²¤à³à²¤à³ à²µà³€à²•à³à²·à²£à²¾ à²µà³‡à²¦à²¿à²•à³†",
                "overview": "à²…à²µà²²à³‹à²•à²¨",
                "content_intelligence": "à²µà²¿à²·à²¯ à²¬à³à²¦à³à²§à²¿à²µà²‚à²¤à²¿à²•à³†",
                "transform": "à²ªà²°à²¿à²µà²°à³à²¤à²¨à³†",
                "monitoring": "à²®à³‡à²²à³à²µà²¿à²šà²¾à²°à²£à³†",
                "alerts": "à²Žà²šà³à²šà²°à²¿à²•à³†à²—à²³à³",
                "security": "à²­à²¦à³à²°à²¤à³†",
                "profile": "à²ªà³à²°à³Šà²«à³ˆà²²à³",
                "settings": "à²¸à³†à²Ÿà³à²Ÿà²¿à²‚à²—à³â€Œà²—à²³à³",
                "logout": "à²²à²¾à²—à³à²”à²Ÿà³",
                "user_profile": "à²¬à²³à²•à³†à²¦à²¾à²° à²ªà³à²°à³Šà²«à³ˆà²²à³",
                "username": "à²¬à²³à²•à³†à²¦à²¾à²° à²¹à³†à²¸à²°à³",
                "email": "à²‡à²®à³‡à²²à³",
                "role": "à²ªà²¾à²¤à³à²°",
                "member_since": "à²¸à²¦à²¸à³à²¯à²°à²¾à²¦ à²¦à²¿à²¨à²¾à²‚à²•",
                "close": "à²®à³à²šà³à²šà²¿",
                "language_settings": "à²­à²¾à²·à²¾ à²¸à³†à²Ÿà³à²Ÿà²¿à²‚à²—à³â€Œà²—à²³à³",
                "select_language": "à²­à²¾à²·à³† à²†à²¯à³à²•à³†à²®à²¾à²¡à²¿",
                "apply": "à²…à²¨à³à²µà²¯à²¿à²¸à²¿",
                # Overview Panel
                "platform_overview": "à²µà³‡à²¦à²¿à²•à³† à²…à²µà²²à³‹à²•à²¨",
                "total_content": "à²’à²Ÿà³à²Ÿà³ à²µà²¿à²·à²¯",
                "this_week": "à²ˆ à²µà²¾à²°",
                "quality_score": "à²—à³à²£à²®à²Ÿà³à²Ÿ à²¸à³à²•à³‹à²°à³",
                "excellent": "à²…à²¤à³à²¯à³à²¤à³à²¤à²®",
                "risk_alerts": "à²…à²ªà²¾à²¯ à²Žà²šà³à²šà²°à²¿à²•à³†à²—à²³à³",
                "resolved": "à²ªà²°à²¿à²¹à²°à²¿à²¸à²²à²¾à²—à²¿à²¦à³†",
                "ai_operations": "à²Žà² à²•à²¾à²°à³à²¯à²¾à²šà²°à²£à³†à²—à²³à³",
                "success": "à²¯à²¶à²¸à³à²¸à³",
                "recent_activity": "à²‡à²¤à³à²¤à³€à²šà²¿à²¨ à²šà²Ÿà³à²µà²Ÿà²¿à²•à³†",
                "content_analyzed": "à²µà²¿à²·à²¯ à²µà²¿à²¶à³à²²à³‡à²·à²£à³†",
                "article_ai_ethics": "à²Žà² à²¨à³€à²¤à²¿à²¶à²¾à²¸à³à²¤à³à²°à²¦ à²²à³‡à²–à²¨",
                "min_ago": "à²¨à²¿à²®à²¿à²·à²—à²³ à²¹à²¿à²‚à²¦à³†",
                "risk_detected": "à²…à²ªà²¾à²¯ à²ªà²¤à³à²¤à³†à²¯à²¾à²—à²¿à²¦à³†",
                "policy_violation": "à²¸à²‚à²­à²¾à²µà³à²¯ à²¨à³€à²¤à²¿ à²‰à²²à³à²²à²‚à²˜à²¨à³†",
                "content_transformed": "à²µà²¿à²·à²¯ à²ªà²°à²¿à²µà²°à³à²¤à²¨à³†",
                "linkedin_twitter": "à²²à²¿à²‚à²•à³à²¡à³â€Œà²‡à²¨à³ + à²Ÿà³à²µà²¿à²Ÿà²°à³ à²ªà³‹à²¸à³à²Ÿà³â€Œà²—à²³à³",
                "hour_ago": "à²—à²‚à²Ÿà³† à²¹à²¿à²‚à²¦à³†",
                "quality_alert": "à²—à³à²£à²®à²Ÿà³à²Ÿ à²Žà²šà³à²šà²°à²¿à²•à³†",
                "readability_below": "à²“à²¦à³à²µà²¿à²•à³† à²®à²¿à²¤à²¿à²—à²¿à²‚à²¤ à²•à²¡à²¿à²®à³†",
                "hours_ago": "à²—à²‚à²Ÿà³†à²—à²³ à²¹à²¿à²‚à²¦à³†",
                "system_health": "à²µà³à²¯à²µà²¸à³à²¥à³† à²†à²°à³‹à²—à³à²¯",
                "ai_model_performance": "à²Žà² à²®à²¾à²¦à²°à²¿ à²•à²¾à²°à³à²¯à²•à³à²·à²®à²¤à³†",
                "content_processing_rate": "à²µà²¿à²·à²¯ à²ªà³à²°à²•à³à²°à²¿à²¯à³† à²¦à²°",
                "storage_utilization": "à²¸à²‚à²—à³à²°à²¹à²£à³† à²¬à²³à²•à³†",
                "api_healthy": "à²Žà²ªà²¿à²: à²†à²°à³‹à²—à³à²¯à²•à²°",
                "database_healthy": "à²¡à³‡à²Ÿà²¾à²¬à³‡à²¸à³: à²†à²°à³‹à²—à³à²¯à²•à²°",
                "ai_healthy": "à²Žà²: à²†à²°à³‹à²—à³à²¯à²•à²°",
                # Settings Dialog
                "settings_preferences": "à²¸à³†à²Ÿà³à²Ÿà²¿à²‚à²—à³â€Œà²—à²³à³ à²®à²¤à³à²¤à³ à²†à²¦à³à²¯à²¤à³†à²—à²³à³",
                "language": "à²­à²¾à²·à³†",
                "notifications": "à²…à²§à²¿à²¸à³‚à²šà²¨à³†à²—à²³à³",
                "enable_notifications": "à²…à²§à²¿à²¸à³‚à²šà²¨à³†à²—à²³à²¨à³à²¨à³ à²¸à²•à³à²°à²¿à²¯à²—à³Šà²³à²¿à²¸à²¿",
                "email_alerts_critical": "à²¨à²¿à²°à³à²£à²¾à²¯à²• à²¸à²®à²¸à³à²¯à³†à²—à²³à²¿à²—à³† à²‡à²®à³‡à²²à³ à²Žà²šà³à²šà²°à²¿à²•à³†à²—à²³à³",
                "content_management": "à²µà²¿à²·à²¯ à²¨à²¿à²°à³à²µà²¹à²£à³†",
                "auto_save_drafts": "à²µà²¿à²·à²¯ à²•à²°à²¡à³à²—à²³à²¨à³à²¨à³ à²¸à³à²µà²¯à²‚-à²‰à²³à²¿à²¸à²¿",
                "session": "à²…à²§à²¿à²µà³‡à²¶à²¨",
                "session_timeout_minutes": "à²…à²§à²¿à²µà³‡à²¶à²¨ à²…à²µà²§à²¿ à²®à³à²—à²¿à²¯à³à²µà²¿à²•à³† (à²¨à²¿à²®à²¿à²·à²—à²³à³)",
                "paused_tasks": "à²µà²¿à²°à²¾à²®à²—à³Šà²³à²¿à²¸à²¿à²¦ à²•à²¾à²°à³à²¯à²—à²³à³",
                "you_have_paused_tasks": "à²¨à³€à²µà³ {count} à²µà²¿à²°à²¾à²®à²—à³Šà²³à²¿à²¸à²¿à²¦ à²•à²¾à²°à³à²¯à²—à²³à²¨à³à²¨à³ à²¹à³Šà²‚à²¦à²¿à²¦à³à²¦à³€à²°à²¿",
                "view_paused_tasks": "à²µà²¿à²°à²¾à²®à²—à³Šà²³à²¿à²¸à²¿à²¦ à²•à²¾à²°à³à²¯à²—à²³à²¨à³à²¨à³ à²µà³€à²•à³à²·à²¿à²¸à²¿",
                "cancel": "à²°à²¦à³à²¦à³à²®à²¾à²¡à²¿",
                "save_settings": "à²¸à³†à²Ÿà³à²Ÿà²¿à²‚à²—à³â€Œà²—à²³à²¨à³à²¨à³ à²‰à²³à²¿à²¸à²¿",
                "settings_saved": "à²¸à³†à²Ÿà³à²Ÿà²¿à²‚à²—à³â€Œà²—à²³à²¨à³à²¨à³ à²¯à²¶à²¸à³à²µà²¿à²¯à²¾à²—à²¿ à²‰à²³à²¿à²¸à²²à²¾à²—à²¿à²¦à³†"
            },
            "Tamil": {
                "title": "à®…à®šà¯‹à®•à®¾",
                "subtitle": "à®œà¯†à®©à¯à®à® à®†à®³à¯à®®à¯ˆ à®®à®±à¯à®±à¯à®®à¯ à®•à®£à¯à®•à®¾à®£à®¿à®ªà¯à®ªà¯ à®¤à®³à®®à¯",
                "overview": "à®®à¯‡à®²à¯‹à®Ÿà¯à®Ÿà®®à¯",
                "content_intelligence": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®¨à¯à®£à¯à®£à®±à®¿à®µà¯",
                "transform": "à®®à®¾à®±à¯à®±à®®à¯",
                "monitoring": "à®•à®£à¯à®•à®¾à®£à®¿à®ªà¯à®ªà¯",
                "alerts": "à®Žà®šà¯à®šà®°à®¿à®•à¯à®•à¯ˆà®•à®³à¯",
                "security": "à®ªà®¾à®¤à¯à®•à®¾à®ªà¯à®ªà¯",
                "profile": "à®šà¯à®¯à®µà®¿à®µà®°à®®à¯",
                "settings": "à®…à®®à¯ˆà®ªà¯à®ªà¯à®•à®³à¯",
                "logout": "à®µà¯†à®³à®¿à®¯à¯‡à®±à¯",
                "user_profile": "à®ªà®¯à®©à®°à¯ à®šà¯à®¯à®µà®¿à®µà®°à®®à¯",
                "username": "à®ªà®¯à®©à®°à¯ à®ªà¯†à®¯à®°à¯",
                "email": "à®®à®¿à®©à¯à®©à®žà¯à®šà®²à¯",
                "role": "à®ªà®™à¯à®•à¯",
                "member_since": "à®‰à®±à¯à®ªà¯à®ªà®¿à®©à®°à®¾à®© à®¤à¯‡à®¤à®¿",
                "close": "à®®à¯‚à®Ÿà¯",
                "language_settings": "à®®à¯Šà®´à®¿ à®…à®®à¯ˆà®ªà¯à®ªà¯à®•à®³à¯",
                "select_language": "à®®à¯Šà®´à®¿à®¯à¯ˆà®¤à¯ à®¤à¯‡à®°à¯à®¨à¯à®¤à¯†à®Ÿà¯à®•à¯à®•à®µà¯à®®à¯",
                "apply": "à®ªà®¯à®©à¯à®ªà®Ÿà¯à®¤à¯à®¤à¯",
                # Overview Panel
                "platform_overview": "à®¤à®³ à®®à¯‡à®²à¯‹à®Ÿà¯à®Ÿà®®à¯",
                "total_content": "à®®à¯Šà®¤à¯à®¤ à®‰à®³à¯à®³à®Ÿà®•à¯à®•à®®à¯",
                "this_week": "à®‡à®¨à¯à®¤ à®µà®¾à®°à®®à¯",
                "quality_score": "à®¤à®° à®®à®¤à®¿à®ªà¯à®ªà¯†à®£à¯",
                "excellent": "à®šà®¿à®±à®¨à¯à®¤à®¤à¯",
                "risk_alerts": "à®…à®ªà®¾à®¯ à®Žà®šà¯à®šà®°à®¿à®•à¯à®•à¯ˆà®•à®³à¯",
                "resolved": "à®¤à¯€à®°à¯à®•à¯à®•à®ªà¯à®ªà®Ÿà¯à®Ÿà®¤à¯",
                "ai_operations": "à®à® à®šà¯†à®¯à®²à¯à®ªà®¾à®Ÿà¯à®•à®³à¯",
                "success": "à®µà¯†à®±à¯à®±à®¿",
                "recent_activity": "à®šà®®à¯€à®ªà®¤à¯à®¤à®¿à®¯ à®šà¯†à®¯à®²à¯à®ªà®¾à®Ÿà¯",
                "content_analyzed": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®ªà®•à¯à®ªà¯à®ªà®¾à®¯à¯à®µà¯",
                "article_ai_ethics": "à®à® à®¨à¯†à®±à®¿à®®à¯à®±à¯ˆà®•à®³à¯ à®ªà®±à¯à®±à®¿à®¯ à®•à®Ÿà¯à®Ÿà¯à®°à¯ˆ",
                "min_ago": "à®¨à®¿à®®à®¿à®Ÿà®™à¯à®•à®³à¯à®•à¯à®•à¯ à®®à¯à®©à¯",
                "risk_detected": "à®…à®ªà®¾à®¯à®®à¯ à®•à®£à¯à®Ÿà®±à®¿à®¯à®ªà¯à®ªà®Ÿà¯à®Ÿà®¤à¯",
                "policy_violation": "à®šà®¾à®¤à¯à®¤à®¿à®¯à®®à®¾à®© à®•à¯Šà®³à¯à®•à¯ˆ à®®à¯€à®±à®²à¯",
                "content_transformed": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®®à®¾à®±à¯à®±à®®à¯",
                "linkedin_twitter": "à®²à®¿à®™à¯à®•à¯à®Ÿà¯à®‡à®©à¯ + à®Ÿà¯à®µà®¿à®Ÿà¯à®Ÿà®°à¯ à®‡à®Ÿà¯à®•à¯ˆà®•à®³à¯",
                "hour_ago": "à®®à®£à®¿ à®¨à¯‡à®°à®¤à¯à®¤à®¿à®±à¯à®•à¯ à®®à¯à®©à¯",
                "quality_alert": "à®¤à®° à®Žà®šà¯à®šà®°à®¿à®•à¯à®•à¯ˆ",
                "readability_below": "à®µà®¾à®šà®¿à®ªà¯à®ªà¯à®¤à¯à®¤à®¿à®±à®©à¯ à®µà®°à®®à¯à®ªà¯à®•à¯à®•à¯à®•à¯ à®•à¯€à®´à¯‡",
                "hours_ago": "à®®à®£à®¿ à®¨à¯‡à®°à®™à¯à®•à®³à¯à®•à¯à®•à¯ à®®à¯à®©à¯",
                "system_health": "à®…à®®à¯ˆà®ªà¯à®ªà¯ à®†à®°à¯‹à®•à¯à®•à®¿à®¯à®®à¯",
                "ai_model_performance": "à®à® à®®à®¾à®¤à®¿à®°à®¿ à®šà¯†à®¯à®²à¯à®¤à®¿à®±à®©à¯",
                "content_processing_rate": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®šà¯†à®¯à®²à®¾à®•à¯à®• à®µà®¿à®•à®¿à®¤à®®à¯",
                "storage_utilization": "à®šà¯‡à®®à®¿à®ªà¯à®ªà®• à®ªà®¯à®©à¯à®ªà®¾à®Ÿà¯",
                "api_healthy": "à®à®ªà®¿à®: à®†à®°à¯‹à®•à¯à®•à®¿à®¯à®®à®¾à®©à®¤à¯",
                "database_healthy": "à®¤à®°à®µà¯à®¤à¯à®¤à®³à®®à¯: à®†à®°à¯‹à®•à¯à®•à®¿à®¯à®®à®¾à®©à®¤à¯",
                "ai_healthy": "à®à®: à®†à®°à¯‹à®•à¯à®•à®¿à®¯à®®à®¾à®©à®¤à¯",
                # Settings Dialog
                "settings_preferences": "à®…à®®à¯ˆà®ªà¯à®ªà¯à®•à®³à¯ à®®à®±à¯à®±à¯à®®à¯ à®µà®¿à®°à¯à®ªà¯à®ªà®¤à¯à®¤à¯‡à®°à¯à®µà¯à®•à®³à¯",
                "language": "à®®à¯Šà®´à®¿",
                "notifications": "à®…à®±à®¿à®µà®¿à®ªà¯à®ªà¯à®•à®³à¯",
                "enable_notifications": "à®…à®±à®¿à®µà®¿à®ªà¯à®ªà¯à®•à®³à¯ˆ à®‡à®¯à®•à¯à®•à¯",
                "email_alerts_critical": "à®®à¯à®•à¯à®•à®¿à®¯à®®à®¾à®© à®šà®¿à®•à¯à®•à®²à¯à®•à®³à¯à®•à¯à®•à¯ à®®à®¿à®©à¯à®©à®žà¯à®šà®²à¯ à®Žà®šà¯à®šà®°à®¿à®•à¯à®•à¯ˆà®•à®³à¯",
                "content_management": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®®à¯‡à®²à®¾à®£à¯à®®à¯ˆ",
                "auto_save_drafts": "à®‰à®³à¯à®³à®Ÿà®•à¯à®• à®µà®°à¯ˆà®µà¯à®•à®³à¯ˆ à®¤à®¾à®©à®¾à®• à®šà¯‡à®®à®¿",
                "session": "à®…à®®à®°à¯à®µà¯",
                "session_timeout_minutes": "à®…à®®à®°à¯à®µà¯ à®•à®¾à®²à®¾à®µà®¤à®¿ (à®¨à®¿à®®à®¿à®Ÿà®™à¯à®•à®³à¯)",
                "paused_tasks": "à®‡à®Ÿà¯ˆà®¨à®¿à®±à¯à®¤à¯à®¤à®ªà¯à®ªà®Ÿà¯à®Ÿ à®ªà®£à®¿à®•à®³à¯",
                "you_have_paused_tasks": "à®¨à¯€à®™à¯à®•à®³à¯ {count} à®‡à®Ÿà¯ˆà®¨à®¿à®±à¯à®¤à¯à®¤à®ªà¯à®ªà®Ÿà¯à®Ÿ à®ªà®£à®¿à®•à®³à¯ˆ à®•à¯Šà®£à¯à®Ÿà¯à®³à¯à®³à¯€à®°à¯à®•à®³à¯",
                "view_paused_tasks": "à®‡à®Ÿà¯ˆà®¨à®¿à®±à¯à®¤à¯à®¤à®ªà¯à®ªà®Ÿà¯à®Ÿ à®ªà®£à®¿à®•à®³à¯ˆà®•à¯ à®•à®¾à®£à¯à®•",
                "cancel": "à®°à®¤à¯à®¤à¯à®šà¯†à®¯à¯",
                "save_settings": "à®…à®®à¯ˆà®ªà¯à®ªà¯à®•à®³à¯ˆà®šà¯ à®šà¯‡à®®à®¿",
                "settings_saved": "à®…à®®à¯ˆà®ªà¯à®ªà¯à®•à®³à¯ à®µà¯†à®±à¯à®±à®¿à®•à®°à®®à®¾à®• à®šà¯‡à®®à®¿à®•à¯à®•à®ªà¯à®ªà®Ÿà¯à®Ÿà®©"
            }
        }
        
        # Initialize database connection (schema initialization is idempotent but can be slow)
        # Only connect here, schema will be initialized on first use if needed
        if not db_schema.conn:
            db_schema.connect()
        self._load_current_user_context()

    def _load_current_user_context(self):
        """Load current user details and role for role-based visibility."""
        try:
            # Get username from session storage
            username = app.storage.general.get('username', '')
            if not username:
                # Fallback to user_id if username not available
                username = app.storage.general.get('user_id', 'demo_user')
            
            # Check if we already loaded this user (avoid redundant DB calls)
            if hasattr(self, 'current_username') and self.current_username == username:
                logger.info(f"User context already loaded for {username}, skipping DB query")
                return
            
            # Load user from database
            from src.database.db_factory import get_dynamodb
            from src.config import config
            
            # get_item expects a dictionary with the key
            user_id = f"user_{username}"
            dynamodb = get_dynamodb()
            user_data = dynamodb.get_item(config.DYNAMODB_USERS_TABLE, {"user_id": user_id})
            if user_data:
                self.current_username = user_data.get('username', username)
                self.current_email = f"{self.current_username}@ashoka.ai"
                self.current_user_role = user_data.get('role', 'user')
                self.current_user = user_data.get('user_id', user_id)
                self.current_user_id = self.current_user  # Sync user_id for tracking
                logger.info(f"Loaded user context: {self.current_username}, role: {self.current_user_role}")
            else:
                # Default values if user not found
                self.current_username = username or 'demo'
                self.current_email = f"{self.current_username}@ashoka.ai"
                self.current_user_role = 'user'
                self.current_user_id = f"user_{self.current_username}"  # Set default user_id
                logger.warning(f"User {username} not found in database, using defaults")
        except Exception as e:
            logger.warning(f"Failed to load current user context: {e}")
            self.current_user_role = 'user'
            self.current_user_id = 'user_demo'  # Fallback user_id
    
    def t(self, key: str) -> str:
        """Get translation for current language"""
        return self.translations.get(self.current_language, self.translations["English"]).get(key, key)
    
    def create_dashboard(self):
        """Create the main dashboard UI"""
        
        # Reload user context to get current logged-in user details
        self._load_current_user_context()
        
        # Ensure current_user_id is synced with current_user
        if hasattr(self, 'current_user'):
            self.current_user_id = self.current_user
        
        # Custom CSS aligned with auth theme (cream + teal + blue)
        ui.add_head_html('''
            <style>
                :root {
                    --bg-primary: #f3efe8;
                    --bg-secondary: #fbf8f3;
                    --text-primary: #1f2937;
                    --text-secondary: #526173;
                    --accent-color: #0f766e;
                    --accent-soft: #0b4f6c;
                    --card-bg: #ffffff;
                    --line: rgba(31, 41, 55, 0.14);
                    --header-from: #0b4f6c;
                    --header-to: #0f766e;
                }
                
                .dark-mode {
                    --bg-primary: #0f172a;
                    --bg-secondary: #1e293b;
                    --text-primary: #e2e8f0;
                    --text-secondary: #b8c3d2;
                    --accent-color: #4dd0c8;
                    --accent-soft: #6ec5e9;
                    --card-bg: #172436;
                    --line: rgba(226, 232, 240, 0.22);
                    --header-from: #0b3c52;
                    --header-to: #14685f;
                }
                
                body {
                    font-family: "Sora", "Segoe UI", "Helvetica Neue", sans-serif;
                    background: radial-gradient(circle at top left, #f8f4ed 0%, var(--bg-primary) 45%, #ece6dd 100%) !important;
                    color: var(--text-primary) !important;
                    transition: background 0.3s ease, color 0.3s ease;
                    overflow-x: hidden !important;
                    max-width: 100vw !important;
                }

                .nicegui-content {
                    max-width: 100vw !important;
                    overflow-x: hidden !important;
                }

                .app-shell {
                    max-width: 1480px;
                    margin: 0 auto;
                    padding: 18px 24px 36px 24px;
                    overflow-x: hidden !important;
                }

                .dashboard-grid {
                    display: grid;
                    grid-template-columns: 250px minmax(0, 1fr);
                    gap: 16px;
                    max-width: 100%;
                    overflow-x: hidden;
                }

                .dashboard-sidebar {
                    background: rgba(255, 255, 255, 0.75);
                    border: 1px solid var(--line);
                    border-radius: 18px;
                    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.1);
                    backdrop-filter: blur(5px);
                    overflow-x: hidden;
                }

                .dashboard-main {
                    background: rgba(255, 255, 255, 0.66);
                    border: 1px solid var(--line);
                    border-radius: 18px;
                    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.1);
                    backdrop-filter: blur(5px);
                    overflow-x: hidden;
                    max-width: 100%;
                }

                .dark-mode .dashboard-sidebar,
                .dark-mode .dashboard-main {
                    background: rgba(23, 36, 54, 0.82);
                }
                
                .dashboard-card {
                    background: linear-gradient(135deg, var(--header-from) 0%, var(--header-to) 100%);
                    border-radius: 16px;
                    padding: 20px;
                    color: white;
                    box-shadow: 0 10px 24px rgba(27, 92, 98, 0.24);
                    transition: transform 0.18s ease, box-shadow 0.18s ease;
                }
                
                .dashboard-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 14px 30px rgba(27, 92, 98, 0.28);
                }
                
                .metric-card {
                    background: var(--card-bg) !important;
                    border-radius: 14px;
                    padding: 20px;
                    box-shadow: 0 8px 20px rgba(44, 77, 82, 0.12);
                    border: 1px solid var(--line);
                    border-left: 4px solid var(--accent-color);
                    color: var(--text-primary) !important;
                    transition: transform 0.18s ease, box-shadow 0.18s ease;
                }
                
                .metric-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 12px 24px rgba(44, 77, 82, 0.16);
                }
                
                .risk-high {
                    border-left-color: #ef4444 !important;
                }
                .risk-medium {
                    border-left-color: #f59e0b !important;
                }
                .risk-low {
                    border-left-color: #10b981 !important;
                }
                
                .content-card {
                    background: var(--bg-secondary);
                    border-radius: 12px;
                    padding: 16px;
                    margin: 8px 0;
                    border: 1px solid var(--line);
                }
                
                .q-card {
                    background: var(--card-bg) !important;
                    color: var(--text-primary) !important;
                    border-radius: 14px !important;
                    border: 1px solid var(--line) !important;
                    box-shadow: 0 8px 18px rgba(44, 77, 82, 0.12) !important;
                }
                
                .q-tab {
                    color: var(--text-secondary) !important;
                    font-weight: 600;
                }
                
                .q-tab--active {
                    color: var(--accent-color) !important;
                }

                .q-tabs:not(.side-tabs) {
                    border-bottom: 1px solid var(--line);
                }

                .side-tabs.q-tabs {
                    border-bottom: none !important;
                }

                .side-tabs .q-tab {
                    justify-content: flex-start !important;
                    min-height: 42px;
                    min-width: 100% !important;
                    border-radius: 10px;
                    margin-bottom: 18px;
                    padding: 8px 12px !important;
                }

                .side-tabs .q-tab--active {
                    background: rgba(15, 118, 110, 0.12);
                }
                
                .q-header {
                    background: linear-gradient(to right, var(--header-from), var(--header-to)) !important;
                    backdrop-filter: blur(6px);
                }

                .app-header {
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 20px rgba(13, 71, 76, 0.25);
                }
                
                .dark-mode .text-gray-600 {
                    color: #b5cfd1 !important;
                }
                
                .dark-mode .text-gray-500 {
                    color: #8fb1b4 !important;
                }
                
                .dark-mode .text-gray-700 {
                    color: #deecee !important;
                }

                .dark-mode .text-gray-800 {
                    color: #e2e8f0 !important;
                }

                .dark-mode .text-gray-400 {
                    color: #94a3b8 !important;
                }

                .dark-mode .text-gray-900 {
                    color: #f1f5f9 !important;
                }

                /* Feature card text styles */
                .feature-card-title {
                    color: var(--text-primary) !important;
                }

                .feature-card-subtitle {
                    color: var(--text-secondary) !important;
                }

                .feature-card-text {
                    color: var(--text-primary) !important;
                }

                .dark-mode .feature-card-title {
                    color: #e2e8f0 !important;
                }

                .dark-mode .feature-card-subtitle {
                    color: #cbd5e1 !important;
                }

                .dark-mode .feature-card-text {
                    color: #f1f5f9 !important;
                }
                
                .timer-shell {
                    background: linear-gradient(135deg, #4ea66a, #388e57) !important;
                    border-radius: 14px !important;
                    border: 1px solid rgba(255,255,255,0.25) !important;
                }

                .timer-text {
                    color: #ffffff !important;
                }

                .dark-mode .timer-text {
                    color: #ffffff !important;
                }
                
                /* Tab spacing */
                .q-tab {
                    padding: 0 24px !important;
                    min-width: 140px !important;
                    display: flex !important;
                    justify-content: center !important;
                }
                
                .q-tab__content {
                    display: flex !important;
                    flex-direction: row !important;
                    justify-content: center !important;
                    align-items: center !important;
                    gap: 2px !important;
                }
                
                .q-tab__icon {
                    margin: 0 !important;
                }
                
                .q-tab__label {
                    margin: 0 !important;
                }
                
                /* Fix overlapping content */
                .q-tab-panel {
                    padding: 18px 14px 20px 14px !important;
                    overflow-x: hidden !important;
                    max-width: 100% !important;
                }

                .q-tab-panels {
                    overflow-x: hidden !important;
                    max-width: 100% !important;
                }

                .q-page {
                    overflow-x: hidden !important;
                    max-width: 100% !important;
                }

                /* Prevent horizontal overflow on all containers */
                .q-card, .q-dialog__inner {
                    max-width: 100% !important;
                    overflow-x: hidden !important;
                }

                /* Fix for rows and columns */
                .row, .column {
                    max-width: 100% !important;
                    overflow-x: hidden !important;
                }
                
                /* Header logo hover effect */
                .app-header .cursor-pointer:hover {
                    opacity: 0.8;
                    transition: opacity 0.2s ease;
                }
                
                .content-input-area {
                    background: rgba(45, 138, 132, 0.06) !important;
                    border: 1px solid rgba(45, 138, 132, 0.25) !important;
                    border-radius: 12px !important;
                }
                
                .dark-mode .content-input-area {
                    background: rgba(45, 138, 132, 0.15) !important;
                    border: 1px solid rgba(112, 184, 178, 0.32) !important;
                }
                
                .table-header-blue {
                    background-color: #d7e8fb !important;
                    color: #24506f !important;
                    font-weight: 600 !important;
                }
                
                .dark-mode .table-header-blue {
                    background-color: #234c69 !important;
                    color: #d7ebff !important;
                }
                
                /* Glassmorphism styles for Recently Used Features cards */
                .glass-card {
                    background: rgba(255, 255, 255, 0.3) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    border: 1px solid rgba(255, 255, 255, 0.4) !important;
                    box-shadow: 0 8px 24px rgba(11, 79, 108, 0.12) !important;
                }
                
                .dark-mode .glass-card {
                    background: rgba(45, 138, 132, 0.2) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    border: 1px solid rgba(112, 184, 178, 0.3) !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                }

                @media (max-width: 1024px) {
                    .dashboard-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        ''')
        
        # Header
        with ui.header().classes('app-header'):
            with ui.row().classes('w-full items-center'):
                # Clickable logo and title to scroll to top
                with ui.row().classes('items-center cursor-pointer').on('click', lambda: ui.run_javascript('window.scrollTo({ top: 0, behavior: "smooth" })')):
                    ui.icon('shield_with_heart', size='lg').classes('text-white')
                    self.title_label = ui.label(self.t('title')).classes('text-2xl font-bold text-white ml-2')
                self.subtitle_label = ui.label(self.t('subtitle')).classes('text-sm text-cyan-50 ml-4')
                ui.space()
                
                # Session timer in header
                with ui.card().classes('timer-shell px-4 py-2 shadow-lg mr-3'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='sm').classes('text-white')
                        self.timer_label = ui.label('30:00').classes('timer-text font-mono text-lg font-bold')
        
        # Start session timer
        self._start_session_timer()
        
        # Start auto-refresh timers for real-time updates
        self._start_auto_refresh_timers()

        with ui.column().classes('app-shell w-full gap-4'):
            with ui.card().classes('w-full dashboard-card'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column().classes('gap-1'):
                        ui.label('Command Center').classes('text-2xl font-bold')
                        ui.label(f'Workspace for {self.current_username}').classes('text-sm').style('color: #a855f7; font-weight: 600;')  # Purple color
                    # Right side: Date-time display and role
                    with ui.row().classes('items-center gap-4'):
                        # Calendar/Date-Time display (moved from header)
                        with ui.card().classes('px-4 py-2 shadow-lg'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('calendar_today', size='sm')
                                # Get current date and time with timezone
                                timezone = self.user_preferences.get('timezone', 'IST')
                                if timezone == 'IST':
                                    tz = pytz.timezone('Asia/Kolkata')
                                else:
                                    tz = pytz.UTC
                                current_dt = datetime.now(tz)
                                date_str = current_dt.strftime('%d-%b-%Y')
                                time_str = current_dt.strftime('%I:%M %p')
                                self.datetime_label = ui.label(f'{date_str} {time_str} {timezone}').classes('font-mono text-sm font-bold').style('color: #000000;')
                        
                        # Role badge only (no username)
                        role_color = 'red' if self.current_user_role == 'admin' else 'blue' if self.current_user_role == 'creator' else 'green'
                        ui.badge(self.current_user_role.upper(), color=role_color).classes('text-sm').style('color: #000000;')

            with ui.element('div').classes('dashboard-grid w-full'):
                with ui.card().classes('dashboard-sidebar p-3 h-fit'):
                    # Navigation Panel heading
                    ui.label('Navigation Panel').classes('text-2xl font-bold mb-3').style('color: #000000')
                    
                    # Main content tabs as side navigation - all in one continuous list
                    with ui.tabs().props('vertical').classes('w-full side-tabs') as tabs:
                        self.overview_tab = ui.tab(self.t('overview'), icon='dashboard').on('click', lambda: self.main_tabs.set_value(self.overview_tab))

                        # Content Intelligence tab - accessible to ALL users (admin, creator, viewer)
                        self.content_tab = ui.tab(self.t('content_intelligence'), icon='psychology').on('click', lambda: self.main_tabs.set_value(self.content_tab))

                        # Monitoring tab - only for creator and admin roles
                        self.monitor_tab = None
                        if self.current_user_role in ['creator', 'admin']:
                            self.monitor_tab = ui.tab(self.t('monitoring'), icon='bar_chart').on('click', lambda: self.main_tabs.set_value(self.monitor_tab))
                        
                        self.alerts_tab = ui.tab(self.t('alerts'), icon='notifications').on('click', lambda: self.main_tabs.set_value(self.alerts_tab))
                        self.security_tab = None
                        if self.current_user_role == 'admin':
                            self.security_tab = ui.tab(self.t('security'), icon='security').on('click', lambda: self.main_tabs.set_value(self.security_tab))
                        
                        # Help tab - accessible to ALL users
                        self.help_tab = ui.tab('Help', icon='help').on('click', lambda: self.main_tabs.set_value(self.help_tab))
                        
                        # About tab - accessible to ALL users
                        self.about_tab = ui.tab('About', icon='info').on('click', lambda: self.main_tabs.set_value(self.about_tab))
                        
                        # Refresh button - refreshes monitoring and alerts, then goes to home
                        ui.tab('Refresh', icon='refresh').on('click', self._refresh_and_go_home)
                        
                        # Account options as tabs
                        self.profile_tab = ui.tab(self.t('profile'), icon='account_circle').on('click', lambda: self.main_tabs.set_value(self.profile_tab))
                        self.settings_tab = ui.tab(self.t('settings'), icon='settings').on('click', lambda: self.main_tabs.set_value(self.settings_tab))
                        ui.tab(self.t('logout'), icon='logout').on('click', self._handle_logout).classes('text-red-600')

                # Store tabs reference for navigation
                self.main_tabs = tabs

                with ui.card().classes('dashboard-main p-2 md:p-4'):
                    with ui.tab_panels(tabs, value=self.overview_tab).classes('w-full') as tab_panels:
                        # Store tab_panels reference for navigation
                        self.main_tab_panels = tab_panels

                        # Overview Panel
                        with ui.tab_panel(self.overview_tab):
                            self._create_overview_panel()

                        # Content Intelligence Panel - accessible to all users
                        with ui.tab_panel(self.content_tab):
                            self._create_content_intelligence_panel()

                        # Monitoring Panel - only for creator and admin
                        if self.monitor_tab:
                            with ui.tab_panel(self.monitor_tab):
                                with ui.column().classes('w-full'):
                                    self._create_monitoring_panel()

                        # Alerts Panel
                        with ui.tab_panel(self.alerts_tab):
                            self._create_alerts_panel()

                        # Security Panel (admin only)
                        if self.security_tab is not None:
                            with ui.tab_panel(self.security_tab):
                                self._create_security_panel()
                        
                        # Help Panel - accessible to all users
                        with ui.tab_panel(self.help_tab):
                            self._create_help_panel()
                        
                        # About Panel - accessible to all users
                        with ui.tab_panel(self.about_tab):
                            self._create_about_panel()
                        
                        # Profile Panel - accessible to all users
                        with ui.tab_panel(self.profile_tab):
                            self._create_profile_panel()
                        
                        # Settings Panel - accessible to all users
                        with ui.tab_panel(self.settings_tab):
                            self._create_settings_panel()
    
    def _handle_logout(self):
        """Handle user logout - clear session and redirect to login"""
        # Clear session storage
        app.storage.general.clear()
        
        # Notify user
        ui.notify('Logged out successfully', type='info')
        
        # Redirect to login page
        ui.navigate.to('/')
    
    def _refresh_and_go_home(self):
        """Refresh monitoring and alerts data, then navigate to home page"""
        # Refresh both monitoring and alerts
        self._refresh_monitoring_metrics(show_notification=False)
        self._refresh_alerts(show_notification=False)
        
        # Navigate to overview/home page
        self.main_tabs.set_value(self.overview_tab)
        
        # Show single notification
        ui.notify('Dashboard refreshed', type='positive')
    
    def _start_session_timer(self):
        """Start the session countdown timer"""
        def update_timer():
            # Update date-time display
            timezone = self.user_preferences.get('timezone', 'IST')
            if timezone == 'IST':
                tz = pytz.timezone('Asia/Kolkata')
            else:
                tz = pytz.UTC
            current_dt = datetime.now(tz)
            date_str = current_dt.strftime('%d-%b-%Y')
            time_str = current_dt.strftime('%I:%M %p')
            self.datetime_label.set_text(f'{date_str} {time_str} {timezone}')
            
            # Use timezone-naive datetime for consistency
            # Convert session_start_time to naive if it's aware
            start_time = self.session_start_time
            if hasattr(start_time, 'tzinfo') and start_time.tzinfo is not None:
                # Convert to local time if timezone-aware
                start_time = start_time.replace(tzinfo=None)
            
            current_time = datetime.now()
            elapsed = (current_time - start_time).total_seconds()
            remaining = self.session_duration - elapsed
            
            # Debug logging
            if elapsed < 0:
                logger.error(f"Negative elapsed time! start_time={start_time}, current_time={current_time}, elapsed={elapsed}")
                logger.error(f"session_duration={self.session_duration}, remaining={remaining}")
            
            if remaining <= 0:
                # Session expired
                self.timer_label.set_text('00:00')
                self.timer_label.classes('text-red-600', remove='text-gray-800 text-orange-600')
                ui.notify('Session expired. Please login again.', type='warning')
                ui.run_javascript('setTimeout(() => window.location.href = "/", 2000)')
                return
            
            # Check if operation is running and time is low
            if self.current_operation and remaining <= 10 and not self.operation_paused:
                self._pause_current_operation()
            
            # Update timer display
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            timer_text = f'{minutes:02d}:{seconds:02d}'
            self.timer_label.set_text(timer_text)
            
            # Change color when time is low (white text on green background)
            if remaining <= 60:
                self.timer_label.classes('text-red-100', remove='text-white text-orange-100')
            elif remaining <= 300:
                self.timer_label.classes('text-orange-100', remove='text-white text-red-100')
            else:
                self.timer_label.classes('text-white', remove='text-orange-100 text-red-100')
        
        # Use repeating timer (every 1 second)
        ui.timer(1.0, update_timer)
    
    def _start_auto_refresh_timers(self):
        """Start timers for auto-refreshing dashboard data"""
        # Note: These will only refresh if the respective panels have been created
        # Refresh intervals are configurable
        
        # Refresh monitoring metrics every 10 minutes (600 seconds)
        def refresh_monitoring():
            try:
                if self._is_processing_operation_running():
                    return
                if hasattr(self, 'quality_metrics_container'):
                    self._refresh_monitoring_metrics(show_notification=False)
            except Exception as e:
                logger.error(f"Auto-refresh monitoring error: {e}")
        
        ui.timer(600.0, refresh_monitoring)
        
        # Refresh alerts every 10 minutes (600 seconds)
        def refresh_alerts():
            try:
                if self._is_processing_operation_running():
                    return
                if hasattr(self, 'alerts_container'):
                    self._refresh_alerts(show_notification=False)
            except Exception as e:
                logger.error(f"Auto-refresh alerts error: {e}")
        
        ui.timer(600.0, refresh_alerts)
        
        # Refresh security logs every 10 minutes (600 seconds)
        def refresh_security():
            try:
                if self._is_processing_operation_running():
                    return
                if hasattr(self, 'security_metrics_container'):
                    self._refresh_security_logs(show_notification=False)
            except Exception as e:
                logger.error(f"Auto-refresh security error: {e}")
        
        ui.timer(600.0, refresh_security)
        
        logger.info("Auto-refresh timers started: Monitoring (10min), Alerts (10min), Security (10min)")

    def _is_processing_operation_running(self) -> bool:
        """Return True when any long-running media operation is active."""
        return bool(self._youtube_processing or self._audio_processing or self._video_processing)
    
    def _pause_current_operation(self):
        """Pause current content operation when timer is low"""
        if not self.operation_paused and self.current_operation:
            self.operation_paused = True
            
            # Save paused task
            paused_task = {
                'id': len(self.paused_tasks) + 1,
                'type': self.current_operation.get('type', 'Analysis'),
                'content_preview': self.current_operation.get('content', '')[:50] + '...',
                'paused_at': datetime.now(),
                'status': 'Paused',
                'progress': self.current_operation.get('progress', 0)
            }
            self.paused_tasks.append(paused_task)
            
            ui.notify('Operation paused due to low session time. Please extend session to continue.', type='warning')
            
            # Show resume dialog
            self._show_resume_dialog()
    
    def _show_resume_dialog(self):
        """Show dialog to resume paused operation"""
        with ui.dialog() as resume_dialog, ui.card().classes('w-96'):
            ui.label('Operation Paused').classes('text-xl font-bold mb-4')
            ui.label('Your session time is running low. Would you like to extend your session and resume?').classes('text-sm mb-4')
            
            with ui.row().classes('w-full justify-end gap-2'):
                ui.button('Cancel', on_click=resume_dialog.close).props('flat')
                ui.button(
                    'Extend & Resume',
                    on_click=lambda: self._extend_session(resume_dialog)
                ).props('color=primary')
        
        resume_dialog.open()
    
    def _extend_session(self, dialog):
        """Extend session by 30 minutes"""
        self.session_start_time = datetime.now()
        # Update storage with new session start time
        app.storage.general['session_start_time'] = self.session_start_time.isoformat()
        self.operation_paused = False
        dialog.close()
        ui.notify('Session extended by 30 minutes', type='positive')
        logger.info(f"Session extended at: {self.session_start_time}")
    
    def _get_profile_stats(self):
        """Get compact profile stats for the current user."""
        stats = {
            'analyzed': 0,
            'transformed': 0,
            'paused_tasks': len(self.paused_tasks),
            'risk_alerts': 0,
        }

        try:
            if not db_schema.conn:
                db_schema.connect()

            analyzed_row = db_schema.conn.execute("""
                SELECT COUNT(*)
                FROM ashoka_contentint
                WHERE user_id = ? AND analyzed_at IS NOT NULL
            """, [self.current_user]).fetchone()
            stats['analyzed'] = int(analyzed_row[0]) if analyzed_row else 0

            transformed_row = db_schema.conn.execute("""
                SELECT COUNT(*)
                FROM transform_history
                WHERE user_id = ?
            """, [self.current_user]).fetchone()
            stats['transformed'] = int(transformed_row[0]) if transformed_row else 0

            risk_row = db_schema.conn.execute("""
                SELECT COUNT(*)
                FROM ashoka_contentint
                WHERE user_id = ? AND sentiment = 'negative'
            """, [self.current_user]).fetchone()
            stats['risk_alerts'] = int(risk_row[0]) if risk_row else 0

        except Exception as e:
            logger.warning(f'Could not load profile stats: {e}')

        return stats
    
    def _show_profile_dialog(self):
        """Show user profile dialog with a cleaner and data-driven layout."""
        role_color = 'red' if self.current_user_role == 'admin' else 'blue' if self.current_user_role == 'creator' else 'green'
        stats = self._get_profile_stats()

        with ui.dialog() as profile_dialog, ui.card().classes('w-[720px] max-w-[95vw] p-0 overflow-hidden'):
            with ui.column().classes('w-full'):
                with ui.row().classes('w-full items-center justify-between px-6 py-5 bg-gradient-to-r from-teal-600 to-cyan-700'):
                    with ui.row().classes('items-center gap-3'):
                        ui.avatar(color='white', text_color='teal-700', icon='person').classes('shadow')
                        with ui.column().classes('gap-0'):
                            ui.label(self.t('user_profile')).classes('text-2xl font-bold text-white')
                            ui.label(self.current_email).classes('text-cyan-50 text-sm')
                    ui.badge(self.current_user_role.upper(), color=role_color).classes('text-sm font-semibold')

                with ui.column().classes('w-full p-6 gap-5'):
                    with ui.card().classes('w-full'):
                        with ui.row().classes('w-full items-center'):
                            with ui.column().classes('flex-1 gap-1'):
                                ui.label(self.t('username')).classes('text-xs uppercase tracking-wide text-gray-500')
                                ui.label(self.current_username).classes('text-lg font-semibold')
                            with ui.column().classes('flex-1 gap-1'):
                                ui.label(self.t('role')).classes('text-xs uppercase tracking-wide text-gray-500')
                                ui.label(self.current_user_role.title()).classes('text-lg font-semibold')
                            with ui.column().classes('flex-1 gap-1'):
                                ui.label(self.t('member_since')).classes('text-xs uppercase tracking-wide text-gray-500')
                                ui.label('February 2026').classes('text-lg font-semibold')

                    with ui.card().classes('w-full'):
                        ui.label('Session').classes('text-base font-semibold mb-3')
                        with ui.row().classes('w-full items-center justify-between'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('schedule').classes('text-teal-600')
                                ui.label('Started')
                            ui.label(self.session_start_time.strftime('%Y-%m-%d %I:%M %p')).classes('font-medium')

                    with ui.column().classes('w-full gap-2'):
                        ui.label('Activity').classes('text-base font-semibold')
                        with ui.row().classes('w-full gap-3'):
                            for icon, label, value, color in [
                                ('description', 'Content Analyzed', stats['analyzed'], 'blue'),
                                ('transform', 'Transformations', stats['transformed'], 'purple'),
                                ('pause_circle', 'Paused Tasks', stats['paused_tasks'], 'orange'),
                                ('warning', 'Risk Alerts', stats['risk_alerts'], 'red'),
                            ]:
                                with ui.card().classes('flex-1 text-center p-4'):
                                    ui.icon(icon).classes(f'text-{color}-600 mb-1')
                                    ui.label(label).classes('text-xs text-gray-600')
                                    ui.label(str(value)).classes(f'text-2xl font-bold text-{color}-700')

                with ui.row().classes('w-full justify-end px-6 py-4 bg-gray-50 border-t'):
                    ui.button(self.t('close'), on_click=profile_dialog.close).props('color=primary')

        profile_dialog.open()
    
    def _show_settings_dialog_old(self):
        """Show user profile dialog"""
        with ui.dialog() as profile_dialog, ui.card().classes('w-96'):
            with ui.row().classes('w-full items-center mb-4'):
                ui.icon('account_circle', size='xl').classes('text-amber-900')
                ui.label(self.t('user_profile')).classes('text-2xl font-bold ml-2')
            
            ui.separator()
            
            with ui.column().classes('w-full gap-4 mt-4'):
                # Username
                with ui.row().classes('w-full items-center'):
                    ui.icon('person').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('username')).classes('text-sm text-gray-600')
                        ui.label('demo').classes('text-lg font-semibold')
                
                # Email
                with ui.row().classes('w-full items-center'):
                    ui.icon('email').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('email')).classes('text-sm text-gray-600')
                        ui.label('demo@ashoka.ai').classes('text-lg font-semibold')
                
                # Role
                with ui.row().classes('w-full items-center'):
                    ui.icon('badge').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('role')).classes('text-sm text-gray-600')
                        ui.label('Content Creator').classes('text-lg font-semibold')
                
                # Member Since
                with ui.row().classes('w-full items-center'):
                    ui.icon('calendar_today').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('member_since')).classes('text-sm text-gray-600')
                        ui.label('February 2026').classes('text-lg font-semibold')
            
            ui.separator().classes('mt-4')
            
            with ui.row().classes('w-full justify-end mt-4'):
                ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
        profile_dialog.open()
    
    def _show_settings_dialog(self):
        """Show settings dialog matching profile dialog style"""
        with ui.dialog() as settings_dialog, ui.card().classes('w-[650px] max-w-[95vw] p-0 overflow-hidden'):
            with ui.column().classes('w-full'):
                # Header with gradient (matching profile dialog style)
                with ui.row().classes('w-full items-center justify-between px-6 py-5 bg-gradient-to-r from-teal-600 to-cyan-700'):
                    with ui.row().classes('items-center gap-3'):
                        ui.avatar(color='white', text_color='teal-700', icon='settings').classes('shadow')
                        with ui.column().classes('gap-0'):
                            ui.label(self.t('settings_preferences')).classes('text-2xl font-bold text-white')
                            ui.label('Customize your experience').classes('text-cyan-50 text-sm')

                with ui.column().classes('w-full p-6 gap-4 max-h-[500px] overflow-y-auto'):
                    # AI Engine Information Card
                    with ui.card().classes('w-full bg-gradient-to-r from-purple-50 to-blue-50'):
                        with ui.row().classes('items-center gap-2 mb-3'):
                            ui.icon('smart_toy', size='sm').classes('text-purple-600')
                            ui.label('AI Engine Status').classes('text-base font-semibold')
                        
                        # Import AI client to get status
                        from src.services.ai_engine import ai_client as multi_ai
                        
                        if multi_ai.is_available():
                            engines = multi_ai.get_available_engines()
                            rate_limits = multi_ai.get_rate_limits()
                            
                            with ui.column().classes('w-full gap-2'):
                                ui.label(f'✓ Active Engines: {", ".join(engines)}').classes('text-sm text-green-700 font-medium')
                                
                                # Display rate limits
                                ui.label('Rate Limits (Free Tier):').classes('text-xs font-semibold text-gray-700 mt-2')
                                for engine_info, limit in rate_limits.items():
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('circle', size='xs').classes('text-blue-500')
                                        ui.label(f'{engine_info}: {limit}').classes('text-xs text-gray-600')
                        else:
                            ui.label('⚠ No AI engines available').classes('text-sm text-orange-600 font-medium')
                            ui.label('Configure API keys in .env file').classes('text-xs text-gray-500')
                    
                    # Language & Timezone Card
                    with ui.card().classes('w-full'):
                        ui.label('Language & Region').classes('text-base font-semibold mb-3')
                        with ui.column().classes('w-full gap-3'):
                            language_select = ui.select(
                                ['English', 'Hindi', 'Kannada', 'Tamil'],
                                value=self.current_language,
                                label=self.t('select_language')
                            ).classes('w-full')
                            timezone_select = ui.select(
                                ['IST', 'UTC'],
                                value=self.user_preferences.get('timezone', 'IST'),
                                label='Timezone'
                            ).classes('w-full')

                    # Notifications Card
                    with ui.card().classes('w-full'):
                        ui.label(self.t('notifications')).classes('text-base font-semibold mb-3')
                        with ui.column().classes('w-full gap-2'):
                            notif_enabled = ui.checkbox(
                                self.t('enable_notifications'),
                                value=self.user_preferences.get('notifications', True)
                            )
                            email_alerts = ui.checkbox(
                                self.t('email_alerts_critical'),
                                value=self.user_preferences.get('email_alerts', False)
                            )

                    # Content & Session Card
                    with ui.card().classes('w-full'):
                        ui.label('Content & Session').classes('text-base font-semibold mb-3')
                        with ui.column().classes('w-full gap-3'):
                            auto_save = ui.checkbox(
                                self.t('auto_save_drafts'),
                                value=self.user_preferences.get('auto_save', True)
                            )
                            session_timeout = ui.select(
                                [15, 30, 60, 120],
                                value=self.user_preferences.get('session_timeout', 30),
                                label=self.t('session_timeout_minutes')
                            ).classes('w-full')

                    # Paused Tasks Card (if any)
                    if self.paused_tasks:
                        with ui.card().classes('w-full'):
                            ui.label(self.t('paused_tasks')).classes('text-base font-semibold mb-3')
                            paused_count_text = self.t('you_have_paused_tasks').replace('{count}', str(len(self.paused_tasks)))
                            ui.label(paused_count_text).classes('text-sm text-gray-600 mb-3')
                            ui.button(
                                self.t('view_paused_tasks'),
                                icon='pause_circle',
                                on_click=lambda: self._show_paused_tasks_dialog()
                            ).props('color=orange outlined').classes('w-full')

                # Footer with action buttons
                with ui.row().classes('w-full justify-end gap-3 px-6 py-4 bg-gray-50 border-t'):
                    ui.button(self.t('cancel'), on_click=settings_dialog.close).props('flat')
                    ui.button(
                        self.t('save_settings'),
                        icon='check_circle',
                        on_click=lambda: self._save_settings(
                            language_select.value,
                            notif_enabled.value,
                            email_alerts.value,
                            auto_save.value,
                            timezone_select.value,
                            session_timeout.value,
                            settings_dialog
                        )
                    ).props('color=primary')
        
        settings_dialog.open()
    
    def _save_settings(self, language, notifications, email_alerts, auto_save, timezone, session_timeout, dialog):
        """Save user settings"""
        # Update preferences
        self.user_preferences['notifications'] = notifications
        self.user_preferences['email_alerts'] = email_alerts
        self.user_preferences['auto_save'] = auto_save
        self.user_preferences['timezone'] = timezone
        self.user_preferences['session_timeout'] = session_timeout
        
        # Update session duration if changed
        if session_timeout != self.session_duration // 60:
            self.session_duration = session_timeout * 60
            self.session_start_time = datetime.now()
            # Update storage with new session timeout and start time
            app.storage.general['session_timeout'] = session_timeout
            app.storage.general['session_start_time'] = self.session_start_time.isoformat()
            logger.info(f"Session timeout changed to {session_timeout} minutes, timer reset")
        
        # Change language if different
        if language != self.current_language:
            self._change_language(language, dialog)
        else:
            ui.notify(self.t('settings_saved'), type='positive')
            dialog.close()
    
    def _show_paused_tasks_dialog(self):
        """Show paused tasks with date filters"""
        with ui.dialog() as tasks_dialog, ui.card().classes('w-[800px]'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Paused Content Tasks').classes('text-2xl font-bold')
                ui.button(icon='close', on_click=tasks_dialog.close).props('flat round')
            
            ui.separator()
            
            # Date filter
            with ui.row().classes('w-full items-center gap-2 my-4'):
                ui.label('Filter:').classes('font-medium')
                date_filter = ui.select(
                    ['Last Week', 'Last 15 Days', 'Last 30 Days', 'Last 3 Months', 'Last 6 Months', 'Last Year'],
                    value='Last 30 Days',
                    label='Time Period'
                ).classes('w-48')
                ui.button(
                    'Apply Filter',
                    icon='filter_list',
                    on_click=lambda: self._filter_paused_tasks(date_filter.value, tasks_container)
                ).props('flat')
            
            # Tasks table
            tasks_container = ui.column().classes('w-full')
            self._display_paused_tasks(tasks_container, 'Last 30 Days')
        
        tasks_dialog.open()
    
    def _filter_paused_tasks(self, filter_value, container):
        """Filter paused tasks by date range"""
        self._display_paused_tasks(container, filter_value)
        ui.notify(f'Filtered by: {filter_value}', type='info')
    
    def _display_paused_tasks(self, container, filter_value):
        """Display paused tasks table"""
        container.clear()
        
        # Calculate date range
        now = datetime.now()
        if filter_value == 'Last Week':
            cutoff = now - timedelta(days=7)
        elif filter_value == 'Last 15 Days':
            cutoff = now - timedelta(days=15)
        elif filter_value == 'Last 30 Days':
            cutoff = now - timedelta(days=30)
        elif filter_value == 'Last 3 Months':
            cutoff = now - timedelta(days=90)
        elif filter_value == 'Last 6 Months':
            cutoff = now - timedelta(days=180)
        else:  # Last Year
            cutoff = now - timedelta(days=365)
        
        # Filter tasks
        filtered_tasks = [t for t in self.paused_tasks if t['paused_at'] >= cutoff]
        
        with container:
            if not filtered_tasks:
                ui.label('No paused tasks in this time period').classes('text-gray-500 text-center py-8')
            else:
                # Table header - Lightish blue background
                with ui.row().classes('w-full table-header-blue p-3 font-semibold rounded-t'):
                    ui.label('ID').classes('w-16')
                    ui.label('Type').classes('w-32')
                    ui.label('Content Preview').classes('flex-1')
                    ui.label('Paused At').classes('w-40')
                    ui.label('Progress').classes('w-24')
                    ui.label('Actions').classes('w-32')
                
                # Table rows
                for task in filtered_tasks:
                    with ui.row().classes('w-full p-3 border-b items-center'):
                        ui.label(f"#{task['id']}").classes('w-16')
                        ui.badge(task['type'], color='blue').classes('w-32')
                        ui.label(task['content_preview']).classes('flex-1 text-sm')
                        ui.label(task['paused_at'].strftime('%Y-%m-%d %H:%M')).classes('w-40 text-sm')
                        ui.label(f"{task['progress']}%").classes('w-24')
                        ui.button(
                            'Resume',
                            icon='play_arrow',
                            on_click=lambda t=task: self._resume_task(t)
                        ).props('flat dense color=green')
    
    def _resume_task(self, task):
        """Resume a paused task"""
        # Remove from paused tasks
        self.paused_tasks = [t for t in self.paused_tasks if t['id'] != task['id']]
        
        # Reset operation state
        self.operation_paused = False
        self.current_operation = None
        
        ui.notify(f"Task #{task['id']} resumed", type='positive')
    
    def _change_language(self, language: str, dialog):
        """Change platform language"""
        self.current_language = language
        
        # Store language preference in general storage (doesn't require secret)
        app.storage.general['language'] = language
        
        ui.notify(f'Language changed to {language}. Refreshing...', type='positive')
        dialog.close()
        
        # Reload the page to apply translations
        ui.run_javascript('window.location.reload()')
    
    def _create_overview_panel(self):
        """Create overview dashboard panel with real metrics from database"""

        ui.label('Recently Used Features').classes('text-2xl font-bold mb-3')
        with ui.row().classes('w-full gap-6 mb-6 justify-start'):
            recent_features = self._get_recently_used_features()
            for feature in recent_features[:3]:
                def create_feature_card(feat):
                    with ui.card().classes('cursor-pointer hover:shadow-2xl transition-all glass-card').style('width: 280px; min-height: 220px; padding: 24px; margin: 8px;').on('click', lambda: self._navigate_to_feature(feat)):
                        with ui.column().classes('w-full gap-5 justify-between h-full'):
                            with ui.column().classes('items-center gap-3 text-center'):
                                ui.icon(feat['icon'], size='xl').classes(f'text-{feat["color"]}-600').style('font-size: 50px;')
                                ui.label(feat['name']).classes('text-xl font-bold feature-card-title')
                            with ui.column().classes('gap-2 mt-auto text-center'):
                                ui.label(f"Last used: {feat['last_used']}").classes('text-sm feature-card-subtitle')

                create_feature_card(feature)

        ui.separator().classes('my-5')

        with ui.card().classes('w-full glass-card').style('padding: 28px;'):
            ui.label('Ashoka Platform').classes('text-3xl font-bold mb-2')
            ui.label('GenAI Governance and Observability').classes('text-base text-gray-600 mb-5')

            with ui.row().classes('w-full gap-8 wrap'):
                with ui.column().classes('flex-1 min-w-[280px]'):
                    ui.label('Core Services').classes('text-xl font-bold mb-3 text-teal-700')
                    services = [
                        ('psychology', 'Content Intelligence', 'AI-powered analysis across text, media, and documents'),
                        ('transform', 'Content Transformation', 'Cross-platform adaptation with tone controls'),
                        ('analytics', 'Monitoring', 'Quality, risk, and operations visibility'),
                        ('notifications', 'Alerts', 'Realtime warnings and actionable notifications'),
                        ('security', 'Security', 'Role-aware access and audit visibility'),
                    ]
                    for icon, name, desc in services:
                        with ui.row().classes('items-start gap-3 mb-3'):
                            ui.icon(icon).classes('text-teal-600 mt-1')
                            with ui.column().classes('gap-0'):
                                ui.label(name).classes('font-bold text-gray-800')
                                ui.label(desc).classes('text-sm text-gray-600')

                with ui.column().classes('flex-1 min-w-[280px]'):
                    ui.label('How It Works').classes('text-xl font-bold mb-3 text-sky-700')
                    checkpoints = [
                        ('Upload or enter content', 'Text, image, video, or document'),
                        ('Analyze and transform', 'Generate insights and platform-ready outputs'),
                        ('Track performance', 'Review quality/risk trends and system health'),
                        ('Respond quickly', 'Act on alerts and security events'),
                    ]
                    for step, detail in checkpoints:
                        with ui.card().classes('mb-2 p-3'):
                            ui.label(step).classes('font-semibold text-gray-800')
                            ui.label(detail).classes('text-sm text-gray-600')

        ui.separator().classes('my-4')

        ui.label(self.t('platform_overview')).classes('text-3xl font-bold mb-4')

        # Fetch real metrics from database
        metrics = self._get_dashboard_metrics()

        # Paused Tasks Summary (if any)
        if self.paused_tasks:
            with ui.card().classes('w-full bg-orange-50 mb-4'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('pause_circle', size='lg').classes('text-orange-600')
                        with ui.column():
                            ui.label(f'{len(self.paused_tasks)} Paused Tasks').classes('text-lg font-semibold')
                            ui.label('Resume your work from where you left off').classes('text-sm text-gray-600')
                    ui.button(
                        'View Tasks',
                        icon='arrow_forward',
                        on_click=self._show_paused_tasks_dialog
                    ).props('flat color=orange')

        # Key Metrics Row - Real data from database
        with ui.row().classes('w-full gap-4 mb-6'):
            self._create_metric_card(
                self.t('total_content'),
                str(metrics['total_content']),
                'description',
                'text-blue-600',
                f"+{metrics['content_this_week']} {self.t('this_week')}"
            )
            self._create_metric_card(
                self.t('quality_score'),
                f"{metrics['avg_quality']:.1f}%",
                'verified',
                'text-green-600',
                self.t('excellent') if metrics['avg_quality'] >= 85 else 'Good'
            )
            self._create_metric_card(
                self.t('risk_alerts'),
                str(metrics['risk_alerts']),
                'warning',
                'text-orange-600',
                f"{metrics['resolved_risks']} {self.t('resolved')}"
            )
            self._create_metric_card(
                self.t('ai_operations'),
                str(metrics['ai_operations']),
                'smart_toy',
                'text-purple-600',
                f"{metrics['success_rate']:.1f}% {self.t('success')}"
            )

        # Charts Row
        with ui.row().classes('w-full gap-4 mb-6'):
            # Content Processing Trend Chart - Real data
            with ui.card().classes('flex-1'):
                ui.label('Content Processing Trend').classes('text-xl font-semibold mb-4')

                trend_data = metrics['content_trend']
                max_value = max(val for _, val in trend_data) if trend_data else 1

                with ui.column().classes('w-full gap-2'):
                    for label, value in trend_data:
                        with ui.row().classes('w-full items-center gap-3'):
                            ui.label(label).classes('w-16 text-xs font-medium')
                            bar_width = (value / max_value * 100) if max_value > 0 else 0
                            with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
                                with ui.element('div').classes('bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded').style(f'width: {bar_width}%'):
                                    pass
                            ui.label(str(value)).classes('w-12 text-xs font-bold text-purple-600')

            # Sentiment Distribution - Real data
            with ui.card().classes('flex-1'):
                ui.label('Sentiment Distribution').classes('text-xl font-semibold mb-4')

                sentiment_data = metrics['sentiment_distribution']

                with ui.column().classes('w-full gap-3'):
                    for label, percentage, color in sentiment_data:
                        with ui.column().classes('w-full gap-1'):
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label(label).classes('text-xs font-medium')
                                ui.label(f'{percentage}%').classes(f'text-xs font-bold text-{color}-600')
                            ui.linear_progress(percentage / 100).props(f'color={color}').classes('h-2')



    def _get_dashboard_metrics(self, force_refresh: bool = False):
        """Fetch real metrics from database"""
        now = datetime.now()
        cached_metrics = self._metrics_cache.get('dashboard_metrics')
        if (
            not force_refresh
            and cached_metrics
            and (now - cached_metrics['generated_at']).total_seconds() < self._metrics_cache_ttl_seconds
        ):
            return cached_metrics['data']

        if not db_schema.conn:
            db_schema.connect()
        
        try:
            aggregate = db_schema.conn.execute("""
                SELECT
                    COUNT(*) AS total_content,
                    COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE - INTERVAL '7 days') AS content_this_week,
                    AVG(sentiment_confidence * 100) FILTER (WHERE sentiment_confidence IS NOT NULL) AS avg_quality,
                    COUNT(*) FILTER (WHERE sentiment = 'negative') AS risk_alerts,
                    COUNT(*) FILTER (
                        WHERE sentiment = 'negative'
                        AND created_at < CURRENT_DATE - INTERVAL '7 days'
                    ) AS resolved_risks,
                    COUNT(*) FILTER (WHERE analyzed_at IS NOT NULL) AS ai_operations,
                    COUNT(*) FILTER (WHERE sentiment = 'positive') AS positive_count,
                    COUNT(*) FILTER (WHERE sentiment = 'neutral') AS neutral_count,
                    COUNT(*) FILTER (WHERE sentiment = 'negative') AS negative_count,
                    COALESCE(SUM(file_size_mb), 0) AS storage_mb
                FROM ashoka_contentint
            """).fetchone()

            (
                total_content,
                content_this_week,
                avg_quality_result,
                risk_alerts,
                resolved_risks,
                ai_operations,
                positive_count,
                neutral_count,
                negative_count,
                storage_mb,
            ) = aggregate
            avg_quality = avg_quality_result if avg_quality_result else 85.0
            
            # Success rate (content with analysis)
            success_rate = (ai_operations / total_content * 100) if total_content > 0 else 100.0
            
            # Content trend (last 5 weeks)
            trend_rows = db_schema.conn.execute("""
                SELECT
                    DATE_DIFF('week', DATE_TRUNC('week', created_at), DATE_TRUNC('week', CURRENT_DATE)) AS week_diff,
                    COUNT(*) AS week_count
                FROM ashoka_contentint
                WHERE created_at >= DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '4 weeks'
                GROUP BY week_diff
            """).fetchall()
            trend_lookup = {int(row[0]): int(row[1]) for row in trend_rows if row[0] is not None and 0 <= row[0] <= 4}
            trend_data = [(f'Week {i + 1}', trend_lookup.get(4 - i, 0)) for i in range(5)]
            
            total_sentiment = positive_count + neutral_count + negative_count
            if total_sentiment > 0:
                sentiment_distribution = [
                    ('Positive', int(positive_count / total_sentiment * 100), 'green'),
                    ('Neutral', int(neutral_count / total_sentiment * 100), 'blue'),
                    ('Negative', int(negative_count / total_sentiment * 100), 'red')
                ]
            else:
                sentiment_distribution = [
                    ('Positive', 33, 'green'),
                    ('Neutral', 34, 'blue'),
                    ('Negative', 33, 'red')
                ]
            
            # Recent activities (last 5)
            recent_activities = []
            recent_content = db_schema.conn.execute("""
                SELECT content_type, sentiment, created_at, content_text
                FROM ashoka_contentint
                ORDER BY created_at DESC
                LIMIT 5
            """).fetchall()
            
            for content_type, sentiment, created_at, content_text in recent_content:
                time_diff = datetime.now() - created_at
                if time_diff.total_seconds() < 3600:
                    time_str = f"{int(time_diff.total_seconds() / 60)} min ago"
                elif time_diff.total_seconds() < 86400:
                    time_str = f"{int(time_diff.total_seconds() / 3600)} hour ago"
                else:
                    time_str = f"{int(time_diff.days)} days ago"
                
                preview = content_text[:50] + '...' if content_text and len(content_text) > 50 else content_text or 'No content'
                
                if sentiment == 'negative':
                    icon, color = 'warning', 'text-red-500'
                    title = 'Risk detected'
                elif sentiment == 'positive':
                    icon, color = 'check_circle', 'text-green-500'
                    title = 'Content analyzed'
                else:
                    icon, color = 'info', 'text-blue-500'
                    title = 'Content processed'
                
                recent_activities.append({
                    'title': title,
                    'description': preview,
                    'time': time_str,
                    'icon': icon,
                    'color': color
                })
            
            # If no activities, show placeholder
            if not recent_activities:
                recent_activities = [{
                    'title': 'No recent activity',
                    'description': 'Start analyzing content to see activity',
                    'time': 'Now',
                    'icon': 'info',
                    'color': 'text-gray-500'
                }]
            
            # Processing rate (based on content with analysis)
            processing_rate = success_rate / 100
            
            # Storage utilization (estimate based on file sizes)
            storage_utilization = min(storage_mb / 1000, 0.95)  # Assume 1GB limit
            
            metrics = {
                'total_content': total_content,
                'content_this_week': content_this_week,
                'avg_quality': avg_quality,
                'risk_alerts': risk_alerts,
                'resolved_risks': resolved_risks,
                'ai_operations': ai_operations,
                'success_rate': success_rate,
                'content_trend': trend_data,
                'sentiment_distribution': sentiment_distribution,
                'recent_activities': recent_activities,
                'processing_rate': processing_rate,
                'storage_utilization': storage_utilization
            }
            self._metrics_cache['dashboard_metrics'] = {'generated_at': now, 'data': metrics}
            return metrics
            
        except Exception as e:
            logger.error(f"Error fetching dashboard metrics: {e}")
            # Return default values on error
            fallback_metrics = {
                'total_content': 0,
                'content_this_week': 0,
                'avg_quality': 85.0,
                'risk_alerts': 0,
                'resolved_risks': 0,
                'ai_operations': 0,
                'success_rate': 100.0,
                'content_trend': [(f'Week {i}', 0) for i in range(1, 6)],
                'sentiment_distribution': [
                    ('Positive', 33, 'green'),
                    ('Neutral', 34, 'blue'),
                    ('Negative', 33, 'red')
                ],
                'recent_activities': [{
                    'title': 'No recent activity',
                    'description': 'Start analyzing content to see activity',
                    'time': 'Now',
                    'icon': 'info',
                    'color': 'text-gray-500'
                }],
                'processing_rate': 0.78,
                'storage_utilization': 0.10
            }
            self._metrics_cache['dashboard_metrics'] = {'generated_at': now, 'data': fallback_metrics}
            return fallback_metrics
    
    def _get_recently_used_features(self):
        """Get top 3 recently used features for current user based on actual usage"""
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            features = []
            
            # Check Content Intelligence usage
            analysis_count = db_schema.conn.execute("""
                SELECT COUNT(*), MAX(analyzed_at) as last_used
                FROM ashoka_contentint
                WHERE user_id = ?
            """, [self.current_user]).fetchone()
            
            if analysis_count and analysis_count[0] > 0:
                features.append({
                    'name': 'Content Intelligence',
                    'icon': 'psychology',
                    'color': 'blue',
                    'usage_count': analysis_count[0],
                    'last_used': self._format_time_ago(analysis_count[1]),
                    'timestamp': analysis_count[1],
                    'tab': 'content_intelligence'
                })
            
            # Check Transform usage
            transform_count = db_schema.conn.execute("""
                SELECT COUNT(*), MAX(created_at) as last_used
                FROM transform_history
                WHERE user_id = ?
            """, [self.current_user]).fetchone()
            
            if transform_count and transform_count[0] > 0:
                features.append({
                    'name': 'Transformer',
                    'icon': 'transform',
                    'color': 'purple',
                    'usage_count': transform_count[0],
                    'last_used': self._format_time_ago(transform_count[1]),
                    'timestamp': transform_count[1],
                    'tab': 'content_intelligence',
                    'scroll_to': 'transformer'
                })
            
            # Sort by timestamp (most recent first)
            features.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min, reverse=True)
            
            # Add remaining services to fill up to 3 cards
            all_services = [
                {'name': 'Content Intelligence', 'icon': 'psychology', 'color': 'blue', 'tab': 'content_intelligence'},
                {'name': 'Transformer', 'icon': 'transform', 'color': 'purple', 'tab': 'content_intelligence', 'scroll_to': 'transformer'},
                {'name': 'Alerts', 'icon': 'notifications', 'color': 'orange', 'tab': 'alerts'},
            ]
            
            # Add Monitoring for admin/creator users only (not for regular users)
            if self.current_user_role in ['admin', 'creator']:
                all_services.insert(2, {'name': 'Monitoring', 'icon': 'bar_chart', 'color': 'green', 'tab': 'monitoring'})
            
            # Add Multi-Platform Content Transformer for admin/creator users only
            if self.current_user_role in ['admin', 'creator']:
                all_services.insert(2, {'name': 'Multi-Platform Content Transformer', 'icon': 'auto_awesome', 'color': 'indigo', 'tab': 'content_intelligence', 'scroll_to': 'transformer'})
            
            # Add Security for admin users
            if self.current_user_role == 'admin':
                all_services.append({'name': 'Security', 'icon': 'security', 'color': 'red', 'tab': 'security'})
            
            # Get names of already added features
            added_names = {f['name'] for f in features}
            
            # Add services not yet in the list
            for service in all_services:
                if service['name'] not in added_names and len(features) < 3:
                    features.append({
                        'name': service['name'],
                        'icon': service['icon'],
                        'color': service['color'],
                        'usage_count': 0,
                        'last_used': 'Not used yet',
                        'timestamp': None,
                        'tab': service['tab']
                    })
            
            return features[:3]
            
        except Exception as e:
            logger.error(f"Error getting recently used features: {e}")
            return [
                {'name': 'Content Intelligence', 'icon': 'psychology', 'color': 'blue', 'usage_count': 0, 'last_used': 'Never', 'tab': 'content_intelligence'},
                {'name': 'Monitoring', 'icon': 'bar_chart', 'color': 'green', 'usage_count': 0, 'last_used': 'Never', 'tab': 'monitoring'},
                {'name': 'Alerts', 'icon': 'notifications', 'color': 'orange', 'usage_count': 0, 'last_used': 'Never', 'tab': 'alerts'}
            ]
    
    def _navigate_to_feature(self, feature):
        """Navigate to the feature tab when card is clicked"""
        try:
            # Map tab identifiers to tab objects
            tab_mapping = {
                'content_intelligence': self.content_tab,
                'monitoring': self.monitor_tab,
                'alerts': self.alerts_tab,
                'security': self.security_tab if hasattr(self, 'security_tab') and self.security_tab else None,
            }
            
            # Get the tab identifier from the feature
            tab_id = feature.get('tab', '').lower()
            target_tab = tab_mapping.get(tab_id)
            
            if target_tab:
                # Switch to the target tab
                self.main_tab_panels.set_value(target_tab)
                
                # If there's a scroll_to target, scroll to that section
                if feature.get('scroll_to'):
                    scroll_target = feature['scroll_to']
                    # Use JavaScript to scroll to the element after a short delay to ensure tab is loaded
                    ui.run_javascript(f'''
                        setTimeout(() => {{
                            const element = document.getElementById('{scroll_target}-section');
                            if (element) {{
                                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                            }}
                        }}, 300);
                    ''')
                
                ui.notify(f"Opened {feature['name']}", type='positive', timeout=2000)
            else:
                logger.warning(f"Tab not found for feature: {feature['name']}, tab_id: {tab_id}")
                ui.notify(f"Tab not available: {feature['name']}", type='warning')
                
        except Exception as e:
            logger.error(f"Error navigating to feature: {e}")
            ui.notify(f"Could not open {feature['name']}", type='warning')
    
    def _create_content_intelligence_panel(self):
        """Create content intelligence panel"""
        ui.label('Content Intelligence & Analysis').classes('text-3xl font-bold mb-4')
        
        # Submit Content for Analysis Section
        with ui.card().classes('w-full'):
            ui.label('Submit Content for Analysis').classes('text-xl font-semibold mb-4')
            
            # Tab selector for input type with modern icons
            with ui.tabs().classes('w-full') as input_tabs:
                text_tab = ui.tab('TEXT', icon='article')
                image_tab = ui.tab('IMAGE', icon='photo')
                video_tab = ui.tab('VIDEO', icon='movie')
                document_tab = ui.tab('DOCUMENT', icon='description')
            
            with ui.tab_panels(input_tabs, value=text_tab).classes('w-full'):
                # Text input panel
                with ui.tab_panel(text_tab):
                    # AI Engine Usage Dashboard
                    with ui.card().classes('w-full bg-gradient-to-r from-purple-50 to-blue-50 mb-4'):
                        ui.label('🚀 AI Engine Usage & Selection').classes('text-lg font-bold text-gray-800 mb-3')
                        
                        # Get usage stats
                        try:
                            from src.services.api_usage_tracker import api_usage_tracker
                            usage_stats = api_usage_tracker.get_all_usage_today(self.current_user_id)
                            
                            # Engine usage cards
                            with ui.row().classes('w-full gap-3'):
                                # Engine 1: Gemini
                                with ui.card().classes('flex-1 bg-white'):
                                    with ui.column().classes('gap-2'):
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label('Engine 1: Gemini').classes('text-sm font-bold text-blue-600')
                                            self.gemini_badge = ui.badge(f"{usage_stats['gemini']['used']}/{usage_stats['gemini']['limit']}", color='blue').classes('text-xs')
                                        
                                        # Progress bar
                                        percentage = usage_stats['gemini']['percentage']
                                        color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                                        self.gemini_progress = ui.linear_progress(value=percentage/100, color=color).classes('w-full')
                                        
                                        with ui.row().classes('justify-between w-full'):
                                            ui.label(f"Used: {usage_stats['gemini']['used']}").classes('text-xs text-gray-600')
                                            self.gemini_remaining = ui.label(f"Left: {usage_stats['gemini']['remaining']}").classes('text-xs font-semibold text-gray-800')
                                
                                # Engine 2: Sarvam AI
                                with ui.card().classes('flex-1 bg-white'):
                                    with ui.column().classes('gap-2'):
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label('Engine 2: Sarvam AI').classes('text-sm font-bold text-green-600')
                                            self.sarvam_badge = ui.badge(f"{usage_stats['sarvam']['used']}/{usage_stats['sarvam']['limit']}", color='green').classes('text-xs')
                                        
                                        # Progress bar
                                        percentage = usage_stats['sarvam']['percentage']
                                        color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                                        self.sarvam_progress = ui.linear_progress(value=percentage/100, color=color).classes('w-full')
                                        
                                        with ui.row().classes('justify-between w-full'):
                                            ui.label(f"Used: {usage_stats['sarvam']['used']}").classes('text-xs text-gray-600')
                                            self.sarvam_remaining = ui.label(f"Left: {usage_stats['sarvam']['remaining']}").classes('text-xs font-semibold text-gray-800')
                                
                                # Engine 3: Gemini Backup
                                with ui.card().classes('flex-1 bg-white'):
                                    with ui.column().classes('gap-2'):
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label('Engine 3: Gemini').classes('text-sm font-bold text-purple-600')
                                            self.gemini3_badge = ui.badge(f"{usage_stats['gemini3']['used']}/{usage_stats['gemini3']['limit']}", color='purple').classes('text-xs')
                                        
                                        # Progress bar
                                        percentage = usage_stats['gemini3']['percentage']
                                        color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                                        self.gemini3_progress = ui.linear_progress(value=percentage/100, color=color).classes('w-full')
                                        
                                        with ui.row().classes('justify-between w-full'):
                                            ui.label(f"Used: {usage_stats['gemini3']['used']}").classes('text-xs text-gray-600')
                                            self.gemini3_remaining = ui.label(f"Left: {usage_stats['gemini3']['remaining']}").classes('text-xs font-semibold text-gray-800')
                            
                            # Engine selector
                            with ui.row().classes('items-center gap-3 mt-3'):
                                ui.label('Select Engine:').classes('text-sm font-semibold text-gray-700')
                                self.engine_selector = ui.select(
                                    options={
                                        'auto': '🤖 Auto (Recommended)',
                                        'gemini': f'⚡ Engine 1: Gemini ({usage_stats["gemini"]["remaining"]} left)',
                                        'sarvam': f'🌏 Engine 2: Sarvam AI ({usage_stats["sarvam"]["remaining"]} left)',
                                        'gemini3': f'🔄 Engine 3: Gemini Backup ({usage_stats["gemini3"]["remaining"]} left)'
                                    },
                                    value='auto'
                                ).classes('flex-1').props('dense')
                                
                                ui.button(
                                    icon='refresh',
                                    on_click=lambda: self._refresh_engine_usage()
                                ).props('flat dense').tooltip('Refresh usage stats')
                        
                        except Exception as e:
                            logger.error(f"Error loading engine usage: {e}")
                            ui.label('⚠️ Engine usage tracking unavailable').classes('text-sm text-orange-600')
                            self.engine_selector = ui.select(
                                options={'auto': '🤖 Auto (Recommended)'},
                                value='auto'
                            ).classes('w-full')
                            # Initialize empty references
                            self.gemini_badge = None
                            self.gemini_progress = None
                            self.gemini_remaining = None
                            self.sarvam_badge = None
                            self.sarvam_progress = None
                            self.sarvam_remaining = None
                            self.gemini3_badge = None
                            self.gemini3_progress = None
                            self.gemini3_remaining = None
                    
                    # AI Model Information Card
                    with ui.card().classes('w-full bg-blue-50 mb-4'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('info', size='sm').classes('text-blue-600 mt-1')
                            with ui.column().classes('flex-1 gap-1'):
                                ui.label('AI Analysis Information').classes('text-sm font-semibold text-blue-900')
                                ui.label('Powered by: Multi-Engine AI (Gemini + Sarvam AI + Gemini Backup)').classes('text-xs text-blue-700')
                                ui.label('Character Limit: 1,000 characters per analysis').classes('text-xs text-blue-700')
                                ui.label('Analysis includes: Sentiment, Keywords, Topics, Quality Score, Takeaways').classes('text-xs text-blue-700')
                    
                    # Text input with character counter
                    self.content_input = ui.textarea(
                        label='Enter your content',
                        placeholder='Paste your content here for AI-powered analysis...',
                        on_change=lambda e: self._update_char_counter(e.value)
                    ).classes('w-full').props('rows=10')
                    
                    # Character counter
                    self.char_counter = ui.label('0 / 1,000 characters').classes('text-xs text-gray-500 mt-1')
                    
                    with ui.row().classes('gap-2 mt-4'):
                        ui.button(
                            'Analyze Text',
                            icon='psychology',
                            on_click=lambda: self._analyze_content_with_validation(self.content_input.value)
                        ).props('color=primary')
                        ui.button('Clear', icon='clear', on_click=self._clear_text_analysis).props('flat')
                    
                    # Inline results container for text analysis
                    self.text_analysis_container = ui.column().classes('w-full mt-4')
                
                # Image upload panel
                with ui.tab_panel(image_tab):
                    ui.label('Upload an image to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                    
                    # Image preview container
                    self.image_preview_container = ui.column().classes('w-full mb-4')
                    
                    # Upload button
                    ui.upload(
                        label='Choose Image',
                        on_upload=self._handle_image_upload,
                        auto_upload=True
                    ).props('accept="image/*"').classes('w-full')
                    
                    ui.label('Supported formats: JPG, PNG, GIF, WEBP').classes('text-xs text-gray-500 mt-2')
                
                # Video upload panel
                with ui.tab_panel(video_tab):
                    ui.label('Upload a video to extract transcription and analyze content').classes('text-sm text-gray-600 mb-3')
                    
                    # Video preview container
                    self.video_preview_container = ui.column().classes('w-full mb-4')
                    
                    # Upload button
                    ui.upload(
                        label='Choose Video',
                        on_upload=self._handle_video_upload,
                        auto_upload=True
                    ).props('accept="video/*"').classes('w-full')
                    
                    ui.label('Supported formats: MP4, MOV, AVI, WEBM').classes('text-xs text-gray-500 mt-2')
                
                # Document upload panel
                with ui.tab_panel(document_tab):
                    ui.label('Upload a document to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                    
                    # Document preview container
                    self.document_preview_container = ui.column().classes('w-full mb-4')
                    
                    # Upload button
                    ui.upload(
                        label='Choose Document',
                        on_upload=self._handle_document_upload,
                        auto_upload=True
                    ).props('accept=".pdf,.docx,.txt,.md"').classes('w-full')
                    
                    ui.label('Supported formats: PDF, DOCX, TXT, MD').classes('text-xs text-gray-500 mt-2')
        
        # AI Content Generator Section
        with ui.card().classes('w-full mt-4'):
            ui.label('AI Content Generator').classes('text-2xl font-bold mb-4')
            ui.label('Generate text, notes, or images using AI prompts').classes('text-sm text-gray-600 mb-4')
            
            with ui.row().classes('w-full gap-4'):
                # Input Section
                with ui.card().classes('flex-1'):
                    ui.label('Enter Your Prompt').classes('text-lg font-semibold mb-3')
                    
                    # Generation type selector
                    with ui.row().classes('items-center gap-4 mb-3'):
                        ui.label('Generate:').classes('text-sm font-medium')
                        self.gen_type = ui.radio(['Text/Notes', 'Image', 'Video'], value='Text/Notes').props('inline')
                    
                    # Prompt input
                    self.generator_prompt = ui.textarea(
                        label='Describe what you want to generate',
                        placeholder='Example: Write a professional email about project updates...'
                    ).classes('w-full').props('rows=6')
                    
                    # Generate button
                    ui.button(
                        'Generate Content',
                        icon='auto_awesome',
                        on_click=self._generate_ai_content
                    ).props('color=primary').classes('w-full mt-3')
                
                # Output Section
                with ui.card().classes('flex-1'):
                    ui.label('Generated Content').classes('text-lg font-semibold mb-3')
                    
                    self.generator_output_container = ui.column().classes('w-full')
                    with self.generator_output_container:
                        ui.label('Generated content will appear here').classes('text-gray-500 text-center py-8')
        
        # Multi-Platform Content Transformer Section - with access control
        with ui.card().classes('w-full mt-4').props('id="transformer-section"'):
            ui.label('Multi-Platform Content Transformer').classes('text-2xl font-bold mb-4')
            
            # Check if user has access to Transform feature
            if self.current_user_role not in ['admin', 'creator']:
                # Show access denied message for viewers
                with ui.column().classes('w-full items-center justify-center py-12'):
                    ui.icon('lock', size='xl').classes('text-gray-400 mb-4')
                    ui.label('Access Restricted').classes('text-2xl font-bold text-gray-600 mb-2')
                    ui.label('You don\'t have the necessary permissions to access this feature.').classes('text-gray-500 mb-2')
                    ui.label('Transform feature is available for Admin and Creator roles only.').classes('text-sm text-gray-400')
            else:
                # Show full transform interface for admin and creator
                ui.label('Transform your content for different social media platforms').classes('text-sm text-gray-600 mb-4')
                
                with ui.row().classes('w-full gap-4'):
                    # Input & Configuration Section
                    with ui.card().classes('w-2/5'):
                        ui.label('Content & Settings').classes('text-xl font-semibold mb-4')
                        
                        # Content input
                        ui.label('Original Content').classes('text-sm font-medium mb-2')
                        self.transform_input = ui.textarea(
                            label='Enter content to transform',
                            placeholder='Paste your content here to transform it for multiple platforms...'
                        ).classes('w-full').props('rows=8')
                        
                        ui.separator().classes('my-4')
                        
                        # Platform selection
                        ui.label('Select Platforms').classes('text-sm font-medium mb-2')
                        self.platform_linkedin = ui.checkbox('LinkedIn', value=True)
                        self.platform_twitter = ui.checkbox('Twitter/X', value=True)
                        self.platform_instagram = ui.checkbox('Instagram', value=False)
                        self.platform_facebook = ui.checkbox('Facebook', value=False)
                        self.platform_threads = ui.checkbox('Threads', value=False)
                        
                        ui.separator().classes('my-4')
                        
                        # Tone selection
                        ui.label('Tone').classes('text-sm font-medium mb-2')
                        self.tone_selector = ui.radio(
                            ['Professional', 'Casual', 'Storytelling'],
                            value='Professional'
                        ).props('inline')
                        
                        ui.separator().classes('my-4')
                        
                        # Hashtag option
                        self.include_hashtags = ui.checkbox('Include Hashtags', value=True)
                        
                        # Transform button
                        ui.button(
                            'Transform Content',
                            icon='transform',
                            on_click=self._transform_content
                        ).props('color=primary').classes('w-full mt-4')
                    
                    # Output Preview Section
                    with ui.card().classes('flex-1'):
                        ui.label('Platform Outputs').classes('text-xl font-semibold mb-4')
                        
                        self.transform_results_container = ui.column().classes('w-full gap-2')
                        with self.transform_results_container:
                            ui.label('Configure settings and click "Transform Content" to see results').classes('text-gray-500 text-center py-8')
        
        # Results are displayed inline within each input type section
    
    def _create_monitoring_panel(self):
        """Create monitoring dashboard panel"""
        from src.services.monitoring_service import monitoring_service
        
        with ui.column().classes('w-full gap-4'):
            # Header without refresh button
            ui.label('Quality, Risk & Operations Monitoring').classes('text-3xl font-bold mb-2')
            
            # Performance Trend Chart - AWS EC2 Style Line Graph
            with ui.card().classes('w-full'):
                ui.label('Performance Trends (Last 24 Hours)').classes('text-xl font-semibold mb-4')
                
                # Create line graph using Plotly
                self.performance_chart_container = ui.column().classes('w-full')
                self._render_performance_line_graph()
            
            # Quality Metrics
            with ui.card().classes('w-full'):
                ui.label('Quality Metrics').classes('text-xl font-semibold mb-4')
                self.quality_metrics_container = ui.row().classes('w-full gap-4')
            
            # Risk Assessment
            with ui.card().classes('w-full'):
                ui.label('Risk & Safety Assessment').classes('text-xl font-semibold mb-4')
                self.risk_metrics_container = ui.row().classes('w-full gap-4')
            
            # Operations Metrics
            with ui.card().classes('w-full'):
                ui.label('AI Operations Performance').classes('text-xl font-semibold mb-4')
                self.operations_metrics_container = ui.row().classes('w-full gap-4')
            
            # System Health
            with ui.card().classes('w-full'):
                ui.label('System Health').classes('text-xl font-semibold mb-4')
                self.system_health_container = ui.column().classes('w-full gap-3')
        
        # Load initial metrics
        self._refresh_monitoring_metrics()
    
    def _render_performance_line_graph(self):
        """Render AWS EC2-style line graph for performance trends - USER SPECIFIC"""
        try:
            # Get performance data from database FOR CURRENT USER ONLY
            from datetime import datetime, timedelta
            
            if not db_schema.conn:
                db_schema.connect()
            
            # Get hourly success rates for last 24 hours - FILTERED BY USER
            hours_data = []
            success_rates = []
            
            for i in range(24, 0, -1):
                hour_start = datetime.now() - timedelta(hours=i)
                hour_end = hour_start + timedelta(hours=1)
                
                # Count successful operations in this hour FOR THIS USER
                result = db_schema.conn.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN quality_score >= 70 THEN 1 ELSE 0 END) as successful
                    FROM ashoka_contentint
                    WHERE user_id = ? AND analyzed_at >= ? AND analyzed_at < ?
                """, [self.current_user, hour_start, hour_end]).fetchone()
                
                total, successful = result if result else (0, 0)
                success_rate = (successful / total * 100) if total > 0 else 0  # Show 0 if no data
                
                hours_data.append(hour_start.strftime('%H:%M'))
                success_rates.append(success_rate)
            
            # If all zeros, show a message
            if all(rate == 0 for rate in success_rates):
                self.performance_chart_container.clear()
                with self.performance_chart_container:
                    with ui.card().classes('w-full text-center p-8 bg-blue-50'):
                        ui.icon('info', size='xl').classes('text-blue-600 mb-3')
                        ui.label('No activity in the last 24 hours').classes('text-lg font-semibold text-gray-700')
                        ui.label('Start analyzing content to see your performance trends').classes('text-sm text-gray-600')
                return
            
            # Create line graph HTML with inline SVG (AWS EC2 style)
            self.performance_chart_container.clear()
            with self.performance_chart_container:
                # User indicator
                with ui.row().classes('w-full items-center gap-2 mb-2'):
                    ui.icon('person', size='sm').classes('text-blue-600')
                    ui.label(f'Your Performance (User: {self.current_user.replace("user_", "")})').classes('text-sm font-medium text-gray-700')
                
                # Simple line graph using HTML/CSS
                with ui.element('div').classes('w-full h-64 relative bg-gray-50 rounded p-4'):
                    # Y-axis labels
                    with ui.element('div').classes('absolute left-0 top-0 bottom-0 w-12 flex flex-col justify-between text-xs text-gray-600'):
                        ui.label('100%').classes('text-right pr-2')
                        ui.label('75%').classes('text-right pr-2')
                        ui.label('50%').classes('text-right pr-2')
                        ui.label('25%').classes('text-right pr-2')
                        ui.label('0%').classes('text-right pr-2')
                    
                    # Graph area with SVG
                    svg_points = []
                    width = 800
                    height = 200
                    for i, rate in enumerate(success_rates):
                        x = (i / (len(success_rates) - 1)) * width
                        y = height - (rate / 100 * height)
                        svg_points.append(f"{x},{y}")
                    
                    polyline_points = " ".join(svg_points)
                    
                    ui.html(f'''
                        <svg width="100%" height="200" viewBox="0 0 {width} {height}" class="ml-12">
                            <!-- Grid lines -->
                            <line x1="0" y1="0" x2="{width}" y2="0" stroke="#e5e7eb" stroke-width="1"/>
                            <line x1="0" y1="50" x2="{width}" y2="50" stroke="#e5e7eb" stroke-width="1"/>
                            <line x1="0" y1="100" x2="{width}" y2="100" stroke="#e5e7eb" stroke-width="1"/>
                            <line x1="0" y1="150" x2="{width}" y2="150" stroke="#e5e7eb" stroke-width="1"/>
                            <line x1="0" y1="{height}" x2="{width}" y2="{height}" stroke="#e5e7eb" stroke-width="1"/>
                            
                            <!-- Area fill -->
                            <polygon points="0,{height} {polyline_points} {width},{height}" fill="rgba(59, 130, 246, 0.1)"/>
                            
                            <!-- Line -->
                            <polyline points="{polyline_points}" fill="none" stroke="#3b82f6" stroke-width="2"/>
                            
                            <!-- Data points -->
                            {"".join([f'<circle cx="{x}" cy="{y}" r="3" fill="#3b82f6"/>' for x, y in [p.split(',') for p in svg_points]])}
                        </svg>
                    ''')
                    
                    # X-axis labels (show every 4 hours)
                    with ui.row().classes('w-full justify-between text-xs text-gray-600 mt-2 ml-12'):
                        for i in range(0, 24, 4):
                            ui.label(hours_data[i])
                
                # Stats below graph - YOUR STATS
                with ui.row().classes('w-full justify-around mt-4 text-center'):
                    with ui.column():
                        ui.label('Current').classes('text-xs text-gray-600')
                        ui.label(f'{success_rates[-1]:.1f}%').classes('text-lg font-bold text-blue-600')
                    with ui.column():
                        ui.label('Average').classes('text-xs text-gray-600')
                        non_zero_rates = [r for r in success_rates if r > 0]
                        avg_rate = sum(non_zero_rates) / len(non_zero_rates) if non_zero_rates else 0
                        ui.label(f'{avg_rate:.1f}%').classes('text-lg font-bold text-green-600')
                    with ui.column():
                        ui.label('Peak').classes('text-xs text-gray-600')
                        ui.label(f'{max(success_rates):.1f}%').classes('text-lg font-bold text-purple-600')
                    with ui.column():
                        ui.label('Lowest').classes('text-xs text-gray-600')
                        ui.label(f'{min(success_rates):.1f}%').classes('text-lg font-bold text-orange-600')
        
        except Exception as e:
            logger.error(f"Error rendering performance line graph: {e}")
            self.performance_chart_container.clear()
            with self.performance_chart_container:
                ui.label(f'Error loading performance data: {str(e)}').classes('text-red-600')
    
    def _refresh_monitoring_metrics(self, show_notification: bool = True):
        """Refresh all monitoring metrics"""
        from src.services.monitoring_service import monitoring_service
        
        try:
            # Get metrics
            quality = monitoring_service.get_quality_metrics()
            risk = monitoring_service.get_risk_metrics()
            ops = monitoring_service.get_operations_metrics()
            health = monitoring_service.get_system_health()
            
            # Update Quality Metrics
            self.quality_metrics_container.clear()
            with self.quality_metrics_container:
                # Readability
                risk_class = 'risk-low' if quality.readability_score > 75 else 'risk-medium' if quality.readability_score > 60 else 'risk-high'
                color = 'green' if quality.readability_score > 75 else 'orange' if quality.readability_score > 60 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Readability Score').classes('text-sm text-gray-600')
                    ui.label(f'{quality.readability_score:.1f}').classes(f'text-3xl font-bold text-{color}-600')
                    change_icon = 'â†‘' if quality.readability_change > 0 else 'â†“'
                    ui.label(f'{change_icon} {abs(quality.readability_change):.1f} from baseline').classes(f'text-xs text-{color}-600')
                
                # Tone Consistency
                risk_class = 'risk-low' if quality.tone_consistency > 85 else 'risk-medium'
                color = 'green' if quality.tone_consistency > 85 else 'orange'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Tone Consistency').classes('text-sm text-gray-600')
                    ui.label(f'{quality.tone_consistency:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(quality.tone_status).classes(f'text-xs text-{color}-600')
                
                # Duplicate Detection
                risk_class = 'risk-low' if quality.duplicate_count == 0 else 'risk-medium' if quality.duplicate_count < 3 else 'risk-high'
                color = 'green' if quality.duplicate_count == 0 else 'orange' if quality.duplicate_count < 3 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Duplicate Detection').classes('text-sm text-gray-600')
                    ui.label(str(quality.duplicate_count)).classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(quality.duplicate_status).classes(f'text-xs text-{color}-600')
            
            # Update Risk Metrics
            self.risk_metrics_container.clear()
            with self.risk_metrics_container:
                # Toxicity
                risk_class = 'risk-low' if risk.toxicity_score < 0.2 else 'risk-medium' if risk.toxicity_score < 0.3 else 'risk-high'
                color = 'green' if risk.toxicity_score < 0.2 else 'orange' if risk.toxicity_score < 0.3 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Toxicity Score').classes('text-sm text-gray-600')
                    ui.label(f'{risk.toxicity_score:.2f}').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(risk.toxicity_level).classes(f'text-xs text-{color}-600')
                
                # Hate Speech
                risk_class = 'risk-low' if risk.hate_speech_count == 0 else 'risk-high'
                color = 'green' if risk.hate_speech_count == 0 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Hate Speech').classes('text-sm text-gray-600')
                    ui.label('None' if risk.hate_speech_count == 0 else str(risk.hate_speech_count)).classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(risk.hate_speech_status).classes(f'text-xs text-{color}-600')
                
                # Backlash Risk
                risk_class = 'risk-low' if risk.backlash_risk == 'Low' else 'risk-medium' if risk.backlash_risk == 'Medium' else 'risk-high'
                color = 'green' if risk.backlash_risk == 'Low' else 'orange' if risk.backlash_risk == 'Medium' else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Backlash Risk').classes('text-sm text-gray-600')
                    ui.label(risk.backlash_risk).classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(risk.backlash_status).classes(f'text-xs text-{color}-600')
            
            # Update Operations Metrics
            self.operations_metrics_container.clear()
            with self.operations_metrics_container:
                # Success Rate
                risk_class = 'risk-low' if ops.success_rate > 95 else 'risk-medium' if ops.success_rate > 90 else 'risk-high'
                color = 'green' if ops.success_rate > 95 else 'orange' if ops.success_rate > 90 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Success Rate').classes('text-sm text-gray-600')
                    ui.label(f'{ops.success_rate:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(f'{ops.total_operations:,} operations').classes('text-xs text-gray-600')
                
                # Latency
                risk_class = 'risk-low' if ops.avg_latency < 1.5 else 'risk-medium' if ops.avg_latency < 2.0 else 'risk-high'
                color = 'green' if ops.avg_latency < 1.5 else 'orange' if ops.avg_latency < 2.0 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Avg Latency').classes('text-sm text-gray-600')
                    ui.label(f'{ops.avg_latency:.1f}s').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(ops.latency_status).classes(f'text-xs text-{color}-600')
                
                # Quality Drift
                risk_class = 'risk-low' if ops.quality_drift > 0 else 'risk-medium'
                color = 'green' if ops.quality_drift > 0 else 'orange'
                drift_sign = '+' if ops.quality_drift > 0 else ''
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Quality Drift').classes('text-sm text-gray-600')
                    ui.label(f'{drift_sign}{ops.quality_drift:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(ops.drift_status).classes(f'text-xs text-{color}-600')
            
            # Update System Health
            self.system_health_container.clear()
            with self.system_health_container:
                ui.label('Component Status').classes('text-sm font-medium mb-2')
                with ui.row().classes('gap-2 mb-4'):
                    api_color = 'green' if health.api_status == 'Healthy' else 'orange'
                    ui.badge(f'API: {health.api_status}', color=api_color)
                    
                    db_color = 'green' if health.database_status == 'Healthy' else 'orange'
                    ui.badge(f'Database: {health.database_status}', color=db_color)
                    
                    ai_color = 'green' if health.ai_status == 'Healthy' else 'orange'
                    ui.badge(f'AI: {health.ai_status}', color=ai_color)
                
                ui.label('Resource Utilization').classes('text-sm font-medium mb-2')
                
                ui.label(f'AI Model Performance: {health.model_performance:.1%}').classes('text-sm text-gray-600 mb-1')
                ui.linear_progress(health.model_performance).classes('mb-3')
                
                ui.label(f'Content Processing Rate: {health.processing_rate:.1%}').classes('text-sm text-gray-600 mb-1')
                ui.linear_progress(health.processing_rate).classes('mb-3')
                
                ui.label(f'Storage Utilization: {health.storage_usage:.1%}').classes('text-sm text-gray-600 mb-1')
                ui.linear_progress(health.storage_usage).classes('mb-3')
            
            # Only show notification if not processing YouTube
            if show_notification and not self._is_processing_operation_running():
                ui.notify('Metrics refreshed', type='positive')
            
        except Exception as e:
            logger.error(f"Error refreshing metrics: {e}")
            ui.notify(f'Failed to refresh metrics: {str(e)}', type='negative')
    
    def _create_alerts_panel(self):
        """Create alerts panel with real data from Content Intelligence, Transformations, and Quality checks"""
        
        with ui.column().classes('w-full gap-4'):
            # Header without refresh button
            ui.label('Alerts & Notifications').classes('text-3xl font-bold mb-2')
            
            # System Health Section (moved from overview)
            with ui.card().classes('w-full bg-gradient-to-r from-teal-50 to-cyan-50'):
                ui.label('System Health').classes('text-xl font-semibold mb-4')
                self.alerts_system_health_container = ui.column().classes('w-full gap-3')
            
            # Summary Stats Row
            self.alert_stats_container = ui.row().classes('w-full gap-4 mb-4')
            
            # Filter buttons
            with ui.row().classes('gap-2 mb-4'):
                self.alert_filter = ui.select(
                    ['All', 'Critical', 'Warning', 'Info', 'Success'],
                    value='All',
                    label='Filter by type'
                ).classes('w-48')
                
                ui.button(
                    'Apply Filter',
                    icon='filter_list',
                    on_click=self._refresh_alerts
                ).props('flat')
            
            # Alert List
            self.alerts_container = ui.column().classes('w-full gap-2')
        
        # Load initial alerts
        self._refresh_alerts()
    
    def _refresh_alerts(self, show_notification: bool = True):
        """Refresh alerts list with real data from database"""
        from datetime import datetime, timedelta
        
        try:
            if not db_schema.conn:
                db_schema.connect()
            alerts = []
            quality_below_80_count = 0
            quality_below_60_count = 0
            successful_operations = 0
            
            # Get recent content analysis (last 24 hours)
            result = db_schema.conn.execute("""
                SELECT id, content_type, sentiment, sentiment_confidence, 
                       quality_score, created_at, summary
                FROM ashoka_contentint
                WHERE created_at >= ?
                ORDER BY created_at DESC
                LIMIT 20
            """, [datetime.now() - timedelta(hours=24)]).fetchall()
            
            for row in result:
                content_id, content_type, sentiment, confidence, quality, created_at, summary = row
                time_ago = self._format_time_ago(created_at)
                
                # Debug logging
                if quality is not None:
                    logger.info(f"Processing content: quality={quality:.1f}%, type={content_type}")
                else:
                    logger.debug(f"Content has no quality score: type={content_type}, id={content_id}")
                
                # Quality alerts - Critical (below 60%)
                if quality is not None and quality < 60:
                    quality_below_60_count += 1
                    quality_below_80_count += 1
                    logger.info(f"Critical quality detected: {quality:.1f}% - Counts: <60={quality_below_60_count}, <80={quality_below_80_count}")
                    alerts.append({
                        'title': f'Critical: Very Low Quality Content',
                        'description': f'{content_type.title()} content has quality score of {quality:.0f}%. Immediate review required.',
                        'type': 'critical',
                        'time_ago': time_ago,
                        'timestamp': created_at
                    })
                # Quality alerts - Warning (below 80%)
                elif quality is not None and quality < 80:
                    quality_below_80_count += 1
                    logger.info(f"Warning quality detected: {quality:.1f}% - Count <80={quality_below_80_count}")
                    logger.info(f"Warning quality detected: {quality}% - Count <80={quality_below_80_count}")
                    alerts.append({
                        'title': f'Warning: Low Quality Content',
                        'description': f'{content_type.title()} content has quality score of {quality:.0f}%. Review recommended.',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': created_at
                    })
                
                # Sentiment alerts
                if sentiment == 'negative' and confidence > 0.7:
                    alerts.append({
                        'title': f'Negative Sentiment Detected',
                        'description': f'{content_type.title()} content shows negative sentiment ({confidence*100:.0f}% confidence).',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': created_at
                    })
                
                # Success notifications - High quality content
                if quality and quality >= 85:
                    successful_operations += 1
                    alerts.append({
                        'title': f'Success: High Quality Content',
                        'description': f'{content_type.title()} content achieved {quality:.0f}% quality score.',
                        'type': 'success',
                        'time_ago': time_ago,
                        'timestamp': created_at
                    })
            
            # Get recent transformations (last 24 hours) - Count as successful operations
            result = db_schema.conn.execute("""
                SELECT id, platforms, tone, created_at
                FROM transform_history
                WHERE created_at >= ?
                ORDER BY created_at DESC
                LIMIT 10
            """, [datetime.now() - timedelta(hours=24)]).fetchall()
            
            for row in result:
                transform_id, platforms, tone, created_at = row
                time_ago = self._format_time_ago(created_at)
                successful_operations += 1
                
                import json
                platform_list = json.loads(platforms) if isinstance(platforms, str) else platforms
                platform_names = ', '.join(platform_list)
                
                alerts.append({
                    'title': f'Success: Content Transformed',
                    'description': f'Content transformed for {platform_names} with {tone} tone.',
                    'type': 'success',
                    'time_ago': time_ago,
                    'timestamp': created_at
                })
            
            # Get risk assessments (last 7 days)
            result = db_schema.conn.execute("""
                SELECT version_id, toxicity_score, policy_risk_level, 
                       backlash_risk_level, should_block, assessed_at
                FROM risk_assessments
                WHERE assessed_at >= ?
                ORDER BY assessed_at DESC
                LIMIT 5
            """, [datetime.now() - timedelta(days=7)]).fetchall()
            
            for row in result:
                version_id, toxicity, policy_risk, backlash_risk, should_block, assessed_at = row
                time_ago = self._format_time_ago(assessed_at)
                
                if should_block:
                    alerts.append({
                        'title': f'Critical: High Risk Content Blocked',
                        'description': f'Content flagged for review due to {policy_risk} policy risk and {backlash_risk} backlash risk.',
                        'type': 'critical',
                        'time_ago': time_ago,
                        'timestamp': assessed_at
                    })
                elif policy_risk == 'high' or backlash_risk == 'high':
                    alerts.append({
                        'title': f'Warning: Risk Alert',
                        'description': f'Content has {policy_risk} policy risk. Manual review recommended.',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': assessed_at
                    })
            
            # Sort alerts by timestamp (most recent first)
            alerts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Log quality score summary
            logger.info(f"Alert refresh complete: {len(alerts)} total alerts, Quality <80%: {quality_below_80_count}, Quality <60%: {quality_below_60_count}")
            
            # Filter if needed
            filter_type = self.alert_filter.value.lower()
            if filter_type != 'all':
                alerts = [a for a in alerts if a['type'] == filter_type]
            
            # Update stats with quality counts and successful operations
            self._update_alert_stats(alerts, quality_below_80_count, quality_below_60_count, successful_operations)
            
            # Display alerts
            self.alerts_container.clear()
            with self.alerts_container:
                if not alerts:
                    with ui.card().classes('w-full text-center p-8'):
                        ui.icon('notifications_none', size='xl').classes('text-gray-400')
                        ui.label('No alerts to display').classes('text-gray-500 mt-2')
                        ui.label('Alerts will appear here when content is analyzed or transformed').classes('text-sm text-gray-400 mt-1')
                else:
                    for alert in alerts[:20]:  # Limit to 20 most recent
                        self._create_alert_card(
                            alert['title'],
                            alert['description'],
                            alert['type'],
                            alert['time_ago']
                        )
            
            # Only show notification if not processing media
            if show_notification and not self._is_processing_operation_running():
                ui.notify('Alerts refreshed', type='positive')
            
            # Update System Health in alerts panel
            self._update_alerts_system_health()
            
        except Exception as e:
            logger.error(f"Error refreshing alerts: {e}")
            self.alerts_container.clear()
            with self.alerts_container:
                ui.label('No alerts available yet. Start analyzing or transforming content to see alerts here.').classes('text-gray-500 text-center py-8')
    
    def _update_alert_stats(self, alerts, quality_below_80=0, quality_below_60=0, successful_ops=0):
        """Update alert statistics summary with quality metrics and successful operations"""
        critical_count = sum(1 for a in alerts if a['type'] == 'critical')
        warning_count = sum(1 for a in alerts if a['type'] == 'warning')
        success_count = sum(1 for a in alerts if a['type'] == 'success')
        info_count = sum(1 for a in alerts if a['type'] == 'info')
        
        # Use quality_below_80 for warning count (more accurate than filtered alerts)
        # This ensures the count reflects actual quality issues, not just visible alerts
        # Ensure minimum of 1 warning is displayed
        warning_display_count = max(1, quality_below_80 if quality_below_80 > 0 else warning_count)
        
        self.alert_stats_container.clear()
        with self.alert_stats_container:
            with ui.card().classes('flex-1 metric-card risk-high' if critical_count > 0 else 'flex-1 metric-card'):
                ui.label('Critical').classes('text-sm text-gray-600')
                ui.label(str(critical_count)).classes('text-3xl font-bold text-red-600')
                ui.label(f'Quality <60%: {quality_below_60}').classes('text-xs text-gray-500')
                ui.label('Last 24 hours').classes('text-xs text-gray-500 mt-1')
            
            with ui.card().classes('flex-1 metric-card risk-medium' if warning_display_count > 0 else 'flex-1 metric-card'):
                ui.label('Warnings').classes('text-sm text-gray-600')
                ui.label(str(warning_display_count)).classes('text-3xl font-bold text-orange-600')
                ui.label(f'Quality <80%: {quality_below_80}').classes('text-xs text-gray-500')
                ui.label('Last 24 hours').classes('text-xs text-gray-500 mt-1')
            
            with ui.card().classes('flex-1 metric-card risk-low'):
                ui.label('Success').classes('text-sm text-gray-600')
                ui.label(str(successful_ops)).classes('text-3xl font-bold text-green-600')
                ui.label('Operations completed').classes('text-xs text-gray-500')
                ui.label('Last 24 hours').classes('text-xs text-gray-500 mt-1')
            
            with ui.card().classes('flex-1 metric-card'):
                ui.label('Total Alerts').classes('text-sm text-gray-600')
                ui.label(str(len(alerts))).classes('text-3xl font-bold text-blue-600')
                ui.label('All alert types').classes('text-xs text-gray-500')
                ui.label('Last 24 hours').classes('text-xs text-gray-500 mt-1')
    
    def _update_alerts_system_health(self):
        """Update system health section in alerts panel"""
        from src.services.monitoring_service import monitoring_service
        
        try:
            health = monitoring_service.get_system_health()
            
            self.alerts_system_health_container.clear()
            with self.alerts_system_health_container:
                ui.label('Component Status').classes('text-sm font-medium mb-2')
                with ui.row().classes('gap-2 mb-4'):
                    status_color = 'green' if health.api_status == 'Healthy' else 'orange' if health.api_status == 'Degraded' else 'red'
                    ui.badge(f'API: {health.api_status}', color=status_color)
                    
                    status_color = 'green' if health.database_status == 'Healthy' else 'orange' if health.database_status == 'Degraded' else 'red'
                    ui.badge(f'Database: {health.database_status}', color=status_color)
                    
                    status_color = 'green' if health.ai_status == 'Healthy' else 'orange' if health.ai_status == 'Degraded' else 'red'
                    ui.badge(f'AI: {health.ai_status}', color=status_color)
                
                # Performance metrics
                ui.label('Performance Metrics').classes('text-sm font-medium mb-2 mt-3')
                with ui.column().classes('gap-2 w-full'):
                    with ui.row().classes('items-center gap-2 w-full'):
                        ui.label('AI Model Performance').classes('text-xs text-gray-600 w-48')
                        ui.linear_progress(0.95).classes('flex-1').props('color=green')
                        ui.label('95%').classes('text-xs text-gray-600 w-12')
                    
                    with ui.row().classes('items-center gap-2 w-full'):
                        ui.label('Content Processing Rate').classes('text-xs text-gray-600 w-48')
                        ui.linear_progress(0.82).classes('flex-1').props('color=blue')
                        ui.label('82%').classes('text-xs text-gray-600 w-12')
                    
                    with ui.row().classes('items-center gap-2 w-full'):
                        ui.label('Storage Utilization').classes('text-xs text-gray-600 w-48')
                        ui.linear_progress(0.45).classes('flex-1').props('color=orange')
                        ui.label('45%').classes('text-xs text-gray-600 w-12')
        except Exception as e:
            logger.error(f"Error updating system health in alerts: {e}")
    
    def _format_time_ago(self, timestamp):
        """Format timestamp as 'X minutes/hours/days ago'"""
        from datetime import datetime
        
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        now = datetime.now()
        diff = now - timestamp
        
        if diff.total_seconds() < 60:
            return 'Just now'
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        else:
            days = int(diff.total_seconds() / 86400)
            return f'{days} day{"s" if days != 1 else ""} ago'
    
    def _format_timestamp_with_timezone(self, timestamp):
        """Format timestamp with timezone (IST or UTC based on user preference)"""
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        # Get user's timezone preference
        user_tz = self.user_preferences.get('timezone', 'IST')
        
        # Assume timestamp is in IST (India Standard Time)
        ist = pytz.timezone('Asia/Kolkata')
        utc = pytz.UTC
        
        # If timestamp is naive (no timezone info), assume it's IST
        if timestamp.tzinfo is None:
            timestamp = ist.localize(timestamp)
        
        # Convert to user's preferred timezone
        if user_tz == 'UTC':
            timestamp = timestamp.astimezone(utc)
            tz_suffix = ' UTC'
        else:  # IST
            timestamp = timestamp.astimezone(ist)
            tz_suffix = ' IST'
        
        # Format: YYYY-MM-DD HH:MM:SS TZ
        return timestamp.strftime('%Y-%m-%d %H:%M:%S') + tz_suffix
    
    def _calculate_quality_score(self, analysis, word_count: int) -> float:
        """Calculate quality score based on analysis metrics"""
        # Base score starts at 100
        score = 100.0
        
        # Deduct points for negative sentiment
        if analysis.sentiment.classification == 'negative':
            score -= 15
        elif analysis.sentiment.classification == 'neutral':
            score -= 5
        
        # Deduct points for low confidence
        if analysis.sentiment.confidence < 0.7:
            score -= 10
        
        # Deduct points for very short content
        if word_count < 20:
            score -= 20
        elif word_count < 50:
            score -= 10
        
        # Deduct points for lack of keywords
        if len(analysis.keywords) < 3:
            score -= 10
        
        # Deduct points for lack of topics
        if len(analysis.topics) < 2:
            score -= 5
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))
    
    def _create_security_panel(self):
        """Create security panel with login logs and security information"""
        from src.services.security_service import security_service
        
        with ui.column().classes('w-full gap-4'):
            # Header
            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label('Security & Access Logs').classes('text-3xl font-bold')
                ui.button(
                    'Refresh',
                    icon='refresh',
                    on_click=self._refresh_security_logs
                ).props('flat color=primary')
            
            # Recent Activity Section
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('history', size='md').classes('text-blue-600')
                    ui.label('Recent Activity').classes('text-xl font-semibold')
                
                # Get metrics to access recent activities
                metrics = self._get_dashboard_metrics()
                
                with ui.column().classes('w-full gap-2'):
                    for activity in metrics['recent_activities']:
                        self._create_activity_item(
                            activity['title'],
                            activity['description'],
                            activity['time'],
                            activity['icon'],
                            activity['color']
                        )
            
            # Security Metrics Row
            self.security_metrics_container = ui.row().classes('w-full gap-4 mb-4')
            
            # Login Activity Chart
            self.login_activity_chart_container = ui.card().classes('w-full')
            
            # Login Logs Table
            self.login_logs_container = ui.card().classes('w-full')
            
            # Security Timeline
            self.security_timeline_container = ui.card().classes('w-full')
            
            # Security Recommendations
            with ui.card().classes('w-full bg-blue-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('security', size='md').classes('text-blue-600')
                    ui.label('Security Recommendations').classes('text-xl font-semibold')
                
                recommendations = [
                    'Enable two-factor authentication for enhanced security',
                    'Review and update your security questions',
                    'Check connected devices and revoke unused sessions',
                    'Enable email notifications for login attempts'
                ]
                
                with ui.column().classes('gap-2'):
                    for i, rec in enumerate(recommendations, 1):
                        with ui.row().classes('items-start gap-2'):
                            ui.icon('check_circle').classes('text-blue-600 text-sm mt-1')
                            ui.label(rec).classes('text-sm text-gray-700')
            
            # Content Restrictions Section (Admin Only)
            with ui.card().classes('w-full bg-red-50 mt-4'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('block', size='md').classes('text-red-600')
                    ui.label('AI Content Generation Restrictions').classes('text-xl font-semibold')
                    ui.badge('Admin Only', color='red').classes('ml-2')
                
                ui.label('Define keywords or phrases that should block AI content generation').classes('text-sm text-gray-600 mb-3')
                
                # Add new restriction
                with ui.row().classes('w-full gap-2 mb-4'):
                    self.restriction_input = ui.input(
                        label='Restriction Keyword/Phrase',
                        placeholder='e.g., violence, hate speech, illegal activities'
                    ).classes('flex-1')
                    
                    self.restriction_desc_input = ui.input(
                        label='Description (optional)',
                        placeholder='Why this is restricted'
                    ).classes('flex-1')
                    
                    ui.button(
                        'Add Restriction',
                        icon='add_circle',
                        on_click=self._add_content_restriction
                    ).props('color=red')
                
                # Active restrictions list
                self.restrictions_container = ui.column().classes('w-full gap-2')
            
            # Query History Section (Combined Analysis + Transform History)
            with ui.card().classes('w-full mt-4 bg-purple-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('history', size='md').classes('text-purple-600')
                    ui.label('Query History').classes('text-xl font-semibold')
                    ui.badge('Admin Only', color='purple').classes('ml-2')
                
                ui.label('Complete history of all content analysis, generation, and transformation queries').classes('text-sm text-gray-600 mb-3')
                
                # Combined history table
                self.query_history_container = ui.column().classes('w-full')
                self._update_query_history()
        
        # Load initial data
        self._refresh_security_logs()
        self._load_content_restrictions()
    
    def _update_query_history(self):
        """Update combined query history (analysis + transform)"""
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            # Get analysis history
            analysis_results = db_schema.conn.execute("""
                SELECT 
                    id,
                    user_id,
                    content_type,
                    content_text,
                    summary,
                    sentiment,
                    created_at,
                    'analysis' as query_type
                FROM ashoka_contentint
                ORDER BY created_at DESC
                LIMIT 50
            """).fetchall()
            
            # Get transform history
            transform_results = db_schema.conn.execute("""
                SELECT 
                    id,
                    user_id,
                    original_content,
                    platforms,
                    tone,
                    created_at,
                    'transform' as query_type
                FROM transform_history
                ORDER BY created_at DESC
                LIMIT 50
            """).fetchall()
            
            # Combine and sort by timestamp
            all_queries = []
            
            for row in analysis_results:
                all_queries.append({
                    'id': row[0],
                    'user_id': row[1],
                    'type': 'Analysis',
                    'content_preview': (row[3] or row[4] or '')[:100],
                    'details': f"{row[2]} - {row[5] or 'N/A'}",
                    'timestamp': row[6],
                    'query_type': row[7]
                })
            
            for row in transform_results:
                platforms = json.loads(row[3]) if row[3] else []
                all_queries.append({
                    'id': row[0],
                    'user_id': row[1],
                    'type': 'Transform',
                    'content_preview': (row[2] or '')[:100],
                    'details': f"{', '.join(platforms)} - {row[4]}",
                    'timestamp': row[5],
                    'query_type': row[6]
                })
            
            # Sort by timestamp descending
            all_queries.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Display combined history
            self.query_history_container.clear()
            with self.query_history_container:
                if not all_queries:
                    ui.label('No query history yet').classes('text-gray-500 text-center py-8')
                else:
                    # Table header
                    with ui.row().classes('w-full table-header-blue p-3 font-semibold text-sm rounded-t'):
                        ui.label('Timestamp').classes('w-40')
                        ui.label('User').classes('w-24')
                        ui.label('Type').classes('w-24')
                        ui.label('Content Preview').classes('flex-1')
                        ui.label('Details').classes('w-48')
                    
                    # Table rows
                    for query in all_queries[:30]:  # Show last 30 queries
                        with ui.row().classes('w-full p-3 border-b items-center text-sm hover:bg-purple-100 cursor-pointer'):
                            timestamp = query['timestamp']
                            if isinstance(timestamp, str):
                                timestamp = datetime.fromisoformat(timestamp)
                            ui.label(self._format_timestamp_with_timezone(timestamp)).classes('w-40 text-gray-700')
                            ui.label(query['user_id'].replace('user_', '')).classes('w-24 font-medium')
                            
                            type_color = 'blue' if query['type'] == 'Analysis' else 'purple'
                            ui.badge(query['type'], color=type_color).classes('w-24')
                            
                            ui.label(query['content_preview'] + ('...' if len(query['content_preview']) >= 100 else '')).classes('flex-1 text-gray-600 truncate')
                            ui.label(query['details']).classes('w-48 text-gray-600 text-xs')
        
        except Exception as e:
            logger.error(f"Error updating query history: {e}")
            self.query_history_container.clear()
            with self.query_history_container:
                ui.label(f'Error loading query history: {str(e)}').classes('text-red-600')
    
    def _create_help_panel(self):
        """Create help and support panel accessible to all users"""
        with ui.column().classes('w-full gap-4'):
            # Header with solid blue background
            with ui.card().classes('w-full p-6').style('background-color: #2563eb;'):
                with ui.row().classes('items-center gap-3 mb-2'):
                    ui.icon('help_center', size='xl').style('color: #1f2937;')
                    ui.label('Help').classes('text-3xl font-bold').style('color: #1f2937;')
                ui.label('Get assistance with the Ashoka GenAI Governance Platform').classes('text-lg').style('color: #1f2937;')
            
            # Quick Help Section - Full width expansions
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('info', size='md').classes('text-blue-600')
                    ui.label('Quick Help').classes('text-xl font-semibold')
                
                with ui.column().classes('gap-3 w-full'):
                    with ui.expansion('Getting Started', icon='rocket_launch').classes('w-full'):
                        ui.label('Welcome to Ashoka! Here are the key features:').classes('font-semibold mb-2')
                        ui.html('''
                            <ul class="list-disc pl-5 space-y-1">
                                <li><strong>Content Intelligence:</strong> Analyze text, images, videos, and documents</li>
                                <li><strong>AI Content Generator:</strong> Generate text and images using Google Gemini AI</li>
                                <li><strong>Multi-Platform Transformer:</strong> Transform content for LinkedIn, Twitter, Instagram, Facebook, and more</li>
                                <li><strong>Monitoring:</strong> Track quality metrics, performance trends, and system health</li>
                                <li><strong>Alerts:</strong> Receive notifications for quality issues and risks</li>
                            </ul>
                        ''')
                    
                    with ui.expansion('Common Issues', icon='troubleshoot').classes('w-full'):
                        ui.html('''
                            <div class="space-y-3">
                                <div>
                                    <p class="font-semibold">Q: Analysis is not working</p>
                                    <p class="text-gray-600">A: Ensure you have a valid Gemini API key configured. Check the logs for any error messages.</p>
                                </div>
                                <div>
                                    <p class="font-semibold">Q: YouTube download failing</p>
                                    <p class="text-gray-600">A: YouTube may have detected automated access. Try again in a few minutes or use a different video.</p>
                                </div>
                                <div>
                                    <p class="font-semibold">Q: Copy to clipboard not working</p>
                                    <p class="text-gray-600">A: Clipboard access requires HTTPS or localhost. Ensure you're accessing the dashboard securely.</p>
                                </div>
                            </div>
                        ''')
                    
                    with ui.expansion('Feature Access by Role', icon='admin_panel_settings').classes('w-full'):
                        ui.html('''
                            <table class="w-full text-sm border-collapse">
                                <thead class="bg-gray-100">
                                    <tr>
                                        <th class="text-left py-3 px-4 font-semibold border-b-2 border-gray-300">Feature</th>
                                        <th class="text-center py-3 px-4 font-semibold border-b-2 border-gray-300">User</th>
                                        <th class="text-center py-3 px-4 font-semibold border-b-2 border-gray-300">Creator</th>
                                        <th class="text-center py-3 px-4 font-semibold border-b-2 border-gray-300">Admin</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="hover:bg-gray-50">
                                        <td class="py-3 px-4 border-b border-gray-200">Content Analysis</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                    </tr>
                                    <tr class="hover:bg-gray-50">
                                        <td class="py-3 px-4 border-b border-gray-200">Content Generation</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-gray-400">-</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                    </tr>
                                    <tr class="hover:bg-gray-50">
                                        <td class="py-3 px-4 border-b border-gray-200">Content Transformation</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-gray-400">-</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                    </tr>
                                    <tr class="hover:bg-gray-50">
                                        <td class="py-3 px-4 border-b border-gray-200">Monitoring & Alerts</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                        <td class="text-center py-3 px-4 border-b border-gray-200 text-green-600 font-bold">✓</td>
                                    </tr>
                                    <tr class="hover:bg-gray-50">
                                        <td class="py-3 px-4">Security Dashboard</td>
                                        <td class="text-center py-3 px-4 text-gray-400">-</td>
                                        <td class="text-center py-3 px-4 text-gray-400">-</td>
                                        <td class="text-center py-3 px-4 text-green-600 font-bold">✓</td>
                                    </tr>
                                </tbody>
                            </table>
                        ''')
            
            # Contact Support Section - Horizontal layout
            with ui.card().classes('w-full bg-teal-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('contact_support', size='md').classes('text-teal-600')
                    ui.label('Contact Support').classes('text-xl font-semibold')
                
                ui.label('Need personalized assistance? Reach out to our support team:').classes('text-gray-700 mb-4')
                
                # Horizontal layout for contact cards
                with ui.row().classes('w-full gap-4'):
                    # Contact 1
                    with ui.card().classes('flex-1 bg-white border-l-4 border-teal-500'):
                        with ui.row().classes('items-center gap-3'):
                            ui.icon('person', size='lg').classes('text-teal-600')
                            with ui.column().classes('gap-1'):
                                ui.label('Jayanth').classes('text-lg font-semibold')
                                ui.label('Support').classes('text-sm text-gray-600')
                        with ui.row().classes('items-center gap-2 mt-2'):
                            ui.icon('phone', size='sm').classes('text-gray-600')
                            ui.label('+91 8317465997').classes('text-base')
                            ui.button(
                                icon='content_copy',
                                on_click=lambda: self._copy_to_clipboard('+91 8317465997')
                            ).props('flat dense round').classes('ml-2')
                    
                    # Contact 2
                    with ui.card().classes('flex-1 bg-white border-l-4 border-cyan-500'):
                        with ui.row().classes('items-center gap-3'):
                            ui.icon('person', size='lg').classes('text-cyan-600')
                            with ui.column().classes('gap-1'):
                                ui.label('Loka Ram Kalyan').classes('text-lg font-semibold')
                                ui.label('Support').classes('text-sm text-gray-600')
                        with ui.row().classes('items-center gap-2 mt-2'):
                            ui.icon('phone', size='sm').classes('text-gray-600')
                            ui.label('+91 93928 79201').classes('text-base')
                            ui.button(
                                icon='content_copy',
                                on_click=lambda: self._copy_to_clipboard('+91 93928 79201')
                            ).props('flat dense round').classes('ml-2')
                
                ui.label('📧 Email: support@ashoka-platform.ai, guymovie89@gmail.com, alrk6125@gmail.com').classes('text-sm text-gray-600 mt-3')
                ui.label('⏰ Support Hours: Monday - Friday, 9:00 AM - 6:00 PM IST').classes('text-sm text-gray-600')
            
            # Documentation Section
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('menu_book', size='md').classes('text-purple-600')
                    ui.label('Documentation').classes('text-xl font-semibold')
                
                with ui.column().classes('gap-2'):
                    ui.label('📖 User Guide: Complete guide to using all features').classes('text-sm')
                    ui.label('🔧 API Documentation: Technical reference for developers').classes('text-sm')
                    ui.label('🎓 Video Tutorials: Step-by-step video guides').classes('text-sm')
                    ui.label('❓ FAQ: Frequently asked questions and answers').classes('text-sm')
            
            # System Information
            with ui.card().classes('w-full bg-gray-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('info', size='md').classes('text-gray-600')
                    ui.label('System Information').classes('text-xl font-semibold')
                
                with ui.column().classes('gap-1 text-sm'):
                    ui.label(f'Platform Version: 1.0.0').classes('text-gray-700')
                    ui.label(f'Your Role: {self.current_user_role.title()}').classes('text-gray-700')
                    ui.label(f'Logged in as: {self.current_username}').classes('text-gray-700')
    
    def _create_about_panel(self):
        """Create about panel with platform information"""
        with ui.column().classes('w-full gap-4'):
            # Header with solid blue background
            with ui.card().classes('w-full p-6').style('background-color: #2563eb;'):
                with ui.row().classes('items-center gap-3 mb-2'):
                    ui.icon('info', size='xl').style('color: #1f2937;')
                    ui.label('About Ashoka').classes('text-3xl font-bold').style('color: #1f2937;')
                ui.label('GenAI Governance & Observability Platform').classes('text-lg').style('color: #1f2937;')
            
            # Introduction Section
            with ui.card().classes('w-full'):
                ui.label('Ashoka is a comprehensive GenAI Governance and Observability Platform designed to empower everyone with responsible AI content management. By using this platform, you can track and analyze your content effortlessly, making it helpful for students, parents, working professionals, content creators, and journalists alike.').classes('text-base text-gray-700 leading-relaxed')
            
            # Built For Everyone Section
            with ui.card().classes('w-full bg-gradient-to-br from-blue-50 to-cyan-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('groups', size='md').classes('text-blue-600')
                    ui.label('Built For Everyone').classes('text-xl font-semibold')
                
                ui.label('Ashoka is designed to help diverse users accomplish their work in one consistent, all-in-one place:').classes('text-gray-700 mb-3')
                
                with ui.column().classes('gap-3'):
                    # Students
                    with ui.card().classes('w-full bg-white border-l-4 border-green-500'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('school', size='lg').classes('text-green-600 mt-1')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label('Students').classes('text-lg font-semibold text-green-700')
                                ui.label('Analyze study materials, generate notes, and create presentations with AI assistance').classes('text-sm text-gray-600')
                    
                    # Parents
                    with ui.card().classes('w-full bg-white border-l-4 border-purple-500'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('family_restroom', size='lg').classes('text-purple-600 mt-1')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label('Parents').classes('text-lg font-semibold text-purple-700')
                                ui.label('Monitor and understand content quality for educational purposes').classes('text-sm text-gray-600')
                    
                    # Working Professionals
                    with ui.card().classes('w-full bg-white border-l-4 border-blue-500'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('business_center', size='lg').classes('text-blue-600 mt-1')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label('Working Professionals').classes('text-lg font-semibold text-blue-700')
                                ui.label('Streamline reports, emails, and business communications with intelligent analysis').classes('text-sm text-gray-600')
                    
                    # Content Creators
                    with ui.card().classes('w-full bg-white border-l-4 border-orange-500'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('create', size='lg').classes('text-orange-600 mt-1')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label('Content Creators').classes('text-lg font-semibold text-orange-700')
                                ui.label('Easily generate content with customizable tones (professional, casual, storytelling) and transform it for multiple platforms').classes('text-sm text-gray-600')
                    
                    # Journalists
                    with ui.card().classes('w-full bg-white border-l-4 border-red-500'):
                        with ui.row().classes('items-start gap-3'):
                            ui.icon('article', size='lg').classes('text-red-600 mt-1')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label('Journalists').classes('text-lg font-semibold text-red-700')
                                ui.label('Verify content authenticity, analyze sources, fact-check information, and adapt articles for different media channels with AI-powered insights').classes('text-sm text-gray-600')
            
            # What We Do Section
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('auto_awesome', size='md').classes('text-teal-600')
                    ui.label('What We Do').classes('text-xl font-semibold')
                
                ui.label('Ashoka combines advanced AI capabilities with robust governance frameworks to deliver:').classes('text-gray-700 mb-3')
                
                ui.html('''
                    <ul class="list-disc pl-5 space-y-2 text-gray-700">
                        <li><strong>Intelligent Content Analysis:</strong> Leverage Google Gemini AI to analyze text, images, videos, and documents for sentiment, quality, and risk assessment</li>
                        <li><strong>AI Content Generation:</strong> Generate text-based content with tone customization (professional, casual, storytelling) to match your needs</li>
                        <li><strong>Multi-Platform Transformation:</strong> Seamlessly adapt your content for LinkedIn, Twitter, Instagram, Facebook, and other social platforms</li>
                        <li><strong>Real-Time Monitoring:</strong> Track quality metrics, performance trends, and system health with comprehensive dashboards</li>
                        <li><strong>Proactive Alerts:</strong> Stay informed with intelligent notifications for quality issues, risks, and policy violations</li>
                        <li><strong>All-in-One Workspace:</strong> Complete your work in a consistent, unified environment without switching between multiple tools</li>
                    </ul>
                ''')
            
            # Technology Stack Section
            with ui.card().classes('w-full bg-gray-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('code', size='md').classes('text-indigo-600')
                    ui.label('Our Technology Stack').classes('text-xl font-semibold')
                
                ui.label('Built on modern, scalable infrastructure:').classes('text-gray-700 mb-3')
                
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('psychology', size='sm').classes('text-purple-600')
                        ui.label('AI Engine: Google Gemini 2.5 Flash for advanced content understanding').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('cloud', size='sm').classes('text-blue-600')
                        ui.label('Cloud Infrastructure: AWS EC2 with S3, DynamoDB, and DuckDB for reliable data management').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('web', size='sm').classes('text-green-600')
                        ui.label('User Interface: NiceGUI framework for responsive, real-time interactions').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('security', size='sm').classes('text-red-600')
                        ui.label('Security: Industry-standard authentication and role-based access control').classes('text-sm text-gray-700')
            
            # Platform Highlights Section
            with ui.card().classes('w-full bg-gradient-to-br from-teal-50 to-blue-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('star', size='md').classes('text-yellow-600')
                    ui.label('Platform Highlights').classes('text-xl font-semibold')
                
                with ui.column().classes('gap-2'):
                    for highlight in [
                        'Multi-format content analysis (text, image, video, documents)',
                        'AI-powered content generation with tone selection',
                        'Multi-platform content transformation',
                        'Real-time quality and risk monitoring',
                        'Role-based access control (Admin, Creator, User)',
                        'Multi-language support (English, Hindi, Kannada, Tamil)',
                        'Comprehensive audit trails and reporting',
                        'Consistent, all-in-one workspace for all your content needs'
                    ]:
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('check_circle', size='sm').classes('text-green-600')
                            ui.label(highlight).classes('text-sm text-gray-700')
            
            # Contact Section
            with ui.card().classes('w-full bg-teal-50'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('contact_support', size='md').classes('text-teal-600')
                    ui.label('Get Started').classes('text-xl font-semibold')
                
                ui.label('Experience the power of responsible AI content governance. Whether you\'re analyzing your first piece of content or managing enterprise-scale operations, Ashoka provides the tools you need to succeed.').classes('text-gray-700 mb-4')
                
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('support_agent', size='sm').classes('text-teal-600')
                        ui.label('Support: +91 8317465997 (Jayanth), +91 93928 79201 (Loka Ram Kalyan)').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('email', size='sm').classes('text-teal-600')
                        ui.label('Email: support@ashoka-platform.ai, guymovie89@gmail.com, alrk6125@gmail.com').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='sm').classes('text-teal-600')
                        ui.label('Hours: Monday - Friday, 9:00 AM - 6:00 PM IST').classes('text-sm text-gray-700')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('public', size='sm').classes('text-teal-600')
                        ui.label('Web: ashoka-ai.hopto.org').classes('text-sm text-gray-700')
            
            # Footer
            with ui.card().classes('w-full bg-gray-100'):
                with ui.column().classes('items-center gap-1'):
                    ui.label('Platform Version: 1.0.0').classes('text-sm text-gray-600')
                    ui.label('Hosted on AWS Cloud Infrastructure').classes('text-xs text-gray-500')
    
    def _create_profile_panel(self):
        """Create profile panel as a full page (like help panel)"""
        role_color = 'red' if self.current_user_role == 'admin' else 'blue' if self.current_user_role == 'creator' else 'green'
        stats = self._get_profile_stats()
        
        with ui.column().classes('w-full gap-4'):
            # Header
            with ui.card().classes('w-full p-6').style('background: linear-gradient(to right, #14b8a6, #06b6d4);'):
                with ui.row().classes('items-center justify-between'):
                    with ui.row().classes('items-center gap-3'):
                        ui.avatar(color='white', text_color='teal-700', icon='person', size='xl').classes('shadow-lg')
                        with ui.column().classes('gap-1'):
                            ui.label(self.t('user_profile')).classes('text-3xl font-bold').style('color: #1f2937;')
                            ui.label(self.current_email).classes('text-lg').style('color: #1f2937; opacity: 0.9;')
                    ui.badge(self.current_user_role.upper(), color=role_color).classes('text-sm font-semibold px-4 py-2')
            
            # User Information Card
            with ui.card().classes('w-full'):
                ui.label('User Information').classes('text-xl font-semibold mb-4')
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-3'):
                        with ui.column().classes('gap-1'):
                            ui.label(self.t('username')).classes('text-xs uppercase tracking-wide text-gray-500')
                            ui.label(self.current_username).classes('text-lg font-semibold')
                        with ui.column().classes('gap-1'):
                            ui.label(self.t('email')).classes('text-xs uppercase tracking-wide text-gray-500')
                            ui.label(self.current_email).classes('text-lg font-semibold')
                    with ui.column().classes('flex-1 gap-3'):
                        with ui.column().classes('gap-1'):
                            ui.label(self.t('role')).classes('text-xs uppercase tracking-wide text-gray-500')
                            ui.label(self.current_user_role.title()).classes('text-lg font-semibold')
                        with ui.column().classes('gap-1'):
                            ui.label(self.t('member_since')).classes('text-xs uppercase tracking-wide text-gray-500')
                            ui.label('February 2026').classes('text-lg font-semibold')
            
            # Session Information Card
            with ui.card().classes('w-full'):
                ui.label('Session Information').classes('text-xl font-semibold mb-4')
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='md').classes('text-teal-600')
                        ui.label('Session Started').classes('text-base')
                    ui.label(self.session_start_time.strftime('%Y-%m-%d %I:%M %p')).classes('text-lg font-medium')
            
            # Activity Statistics Card
            with ui.card().classes('w-full'):
                ui.label('Activity Statistics').classes('text-xl font-semibold mb-4')
                with ui.row().classes('w-full gap-4'):
                    for icon, label, value, color in [
                        ('description', 'Content Analyzed', stats['analyzed'], 'blue'),
                        ('transform', 'Transformations', stats['transformed'], 'purple'),
                        ('pause_circle', 'Paused Tasks', stats['paused_tasks'], 'orange'),
                        ('warning', 'Risk Alerts', stats['risk_alerts'], 'red'),
                    ]:
                        with ui.card().classes('flex-1 text-center p-6 bg-gray-50'):
                            ui.icon(icon, size='lg').classes(f'text-{color}-600 mb-2')
                            ui.label(label).classes('text-sm text-gray-600 mb-1')
                            ui.label(str(value)).classes(f'text-3xl font-bold text-{color}-700')
    
    def _create_settings_panel(self):
        """Create settings panel as a full page (like help panel)"""
        with ui.column().classes('w-full gap-4'):
            # Header
            with ui.card().classes('w-full p-6').style('background: linear-gradient(to right, #14b8a6, #06b6d4);'):
                with ui.row().classes('items-center gap-3 mb-2'):
                    ui.icon('settings', size='xl').style('color: #1f2937;')
                    ui.label(self.t('settings_preferences')).classes('text-3xl font-bold').style('color: #1f2937;')
                ui.label('Customize your experience').classes('text-lg').style('color: #1f2937; opacity: 0.9;')
            
            # Language & Region Card
            with ui.card().classes('w-full'):
                ui.label('Language & Region').classes('text-xl font-semibold mb-4')
                with ui.column().classes('w-full gap-4'):
                    language_select = ui.select(
                        ['English', 'Hindi', 'Kannada', 'Tamil'],
                        value=self.current_language,
                        label=self.t('select_language')
                    ).classes('w-full')
                    timezone_select = ui.select(
                        ['IST', 'UTC'],
                        value=self.user_preferences.get('timezone', 'IST'),
                        label='Timezone'
                    ).classes('w-full')
            
            # Notifications Card
            with ui.card().classes('w-full'):
                ui.label(self.t('notifications')).classes('text-xl font-semibold mb-4')
                with ui.column().classes('w-full gap-3'):
                    notifications_switch = ui.switch(self.t('enable_notifications'), value=self.user_preferences.get('notifications', True))
                    email_alerts_switch = ui.switch(self.t('email_alerts_critical'), value=self.user_preferences.get('email_alerts', False))
            
            # Content Management Card
            with ui.card().classes('w-full'):
                ui.label(self.t('content_management')).classes('text-xl font-semibold mb-4')
                with ui.column().classes('w-full gap-3'):
                    auto_save_switch = ui.switch(self.t('auto_save_drafts'), value=self.user_preferences.get('auto_save', True))
            
            # Session Settings Card
            with ui.card().classes('w-full'):
                ui.label(self.t('session')).classes('text-xl font-semibold mb-4')
                with ui.column().classes('w-full gap-3'):
                    session_timeout_input = ui.number(
                        label=self.t('session_timeout_minutes'),
                        value=self.user_preferences.get('session_timeout', 30),
                        min=5,
                        max=120,
                        step=5
                    ).classes('w-full')
            
            # Paused Tasks Card (if any)
            if len(self.paused_tasks) > 0:
                with ui.card().classes('w-full bg-orange-50'):
                    ui.label(self.t('paused_tasks')).classes('text-xl font-semibold mb-4')
                    ui.label(self.t('you_have_paused_tasks').format(count=len(self.paused_tasks))).classes('text-base text-gray-700 mb-3')
                    ui.button(self.t('view_paused_tasks'), icon='visibility', on_click=self._show_paused_tasks_dialog).props('color=orange')
            
            # Save Button
            with ui.row().classes('w-full justify-end gap-2'):
                def save_settings():
                    # Update preferences
                    self.user_preferences['language'] = language_select.value
                    self.user_preferences['timezone'] = timezone_select.value
                    self.user_preferences['notifications'] = notifications_switch.value
                    self.user_preferences['email_alerts'] = email_alerts_switch.value
                    self.user_preferences['auto_save'] = auto_save_switch.value
                    self.user_preferences['session_timeout'] = int(session_timeout_input.value)
                    
                    # Save to storage
                    app.storage.general['language'] = language_select.value
                    app.storage.general['session_timeout'] = int(session_timeout_input.value)
                    
                    # Update current language
                    self.current_language = language_select.value
                    
                    # Update session duration if changed
                    new_timeout = int(session_timeout_input.value) * 60
                    if new_timeout != self.session_duration:
                        self.session_duration = new_timeout
                        app.storage.general['session_timeout'] = int(session_timeout_input.value)
                    
                    ui.notify(self.t('settings_saved'), type='positive')
                
                ui.button(self.t('save_settings'), icon='save', on_click=save_settings).props('color=primary')
    
    def _refresh_security_logs(self, show_notification: bool = True):
        """Refresh security logs with real data from DuckDB"""
        from src.services.security_service import security_service
        from datetime import datetime, timedelta
        
        try:
            # Get security metrics
            active_sessions = security_service.get_active_sessions_count()
            failed_logins = security_service.get_failed_login_count(24)
            security_score = security_service.get_security_score()
            
            # Update security metrics
            self.security_metrics_container.clear()
            with self.security_metrics_container:
                risk_class = 'risk-low' if active_sessions <= 2 else 'risk-medium'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Active Sessions').classes('text-sm text-gray-600')
                    ui.label(str(active_sessions)).classes('text-3xl font-bold text-green-600')
                    ui.label('Current user only').classes('text-xs text-gray-500')
                
                risk_class = 'risk-low' if failed_logins == 0 else 'risk-medium' if failed_logins < 5 else 'risk-high'
                color = 'green' if failed_logins == 0 else 'orange' if failed_logins < 5 else 'red'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Failed Login Attempts').classes('text-sm text-gray-600')
                    ui.label(str(failed_logins)).classes(f'text-3xl font-bold text-{color}-600')
                    ui.label('Last 24 hours').classes('text-xs text-gray-500')
                
                risk_class = 'risk-low' if security_score >= 90 else 'risk-medium' if security_score >= 70 else 'risk-high'
                color = 'green' if security_score >= 90 else 'orange' if security_score >= 70 else 'red'
                status = 'Excellent' if security_score >= 90 else 'Good' if security_score >= 70 else 'Needs Attention'
                with ui.card().classes(f'flex-1 metric-card {risk_class}'):
                    ui.label('Security Score').classes('text-sm text-gray-600')
                    ui.label(f'{security_score:.0f}%').classes(f'text-3xl font-bold text-{color}-600')
                    ui.label(status).classes('text-xs text-gray-500')
                
                with ui.card().classes('flex-1 metric-card risk-low'):
                    ui.label('Last Password Change').classes('text-sm text-gray-600')
                    ui.label('30d').classes('text-3xl font-bold text-blue-600')
                    ui.label('Recommended: 90 days').classes('text-xs text-gray-500')
            
            # Get login activity stats
            login_stats = security_service.get_login_activity_stats(7)
            
            # Update login activity chart
            self.login_activity_chart_container.clear()
            with self.login_activity_chart_container:
                ui.label('Login Activity (Last 7 Days)').classes('text-xl font-semibold mb-4')
                
                # Create day labels for last 7 days
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                today = datetime.now()
                
                # Build login data with actual counts
                login_data = []
                for i in range(7):
                    date = (today - timedelta(days=6-i)).date()
                    count = next((s['count'] for s in login_stats if s['date'] == date), 0)
                    day_name = days[(today.weekday() - 6 + i) % 7]
                    login_data.append((day_name, count))
                
                max_logins = max((count for _, count in login_data), default=1)
                
                with ui.column().classes('w-full gap-2'):
                    for day, count in login_data:
                        with ui.row().classes('w-full items-center gap-3'):
                            ui.label(day).classes('w-12 text-sm font-medium')
                            bar_width = (count / max_logins * 100) if max_logins > 0 else 0
                            with ui.element('div').classes('flex-1 bg-gray-200 rounded h-8 relative'):
                                with ui.element('div').classes('bg-blue-500 h-full rounded').style(f'width: {bar_width}%'):
                                    pass
                            ui.label(str(count)).classes('w-8 text-sm font-bold text-blue-600')
            
            # Get recent login logs
            login_logs = security_service.get_recent_login_logs(10)
            
            # Update login logs table
            self.login_logs_container.clear()
            with self.login_logs_container:
                ui.label('Recent Login Activity').classes('text-xl font-semibold mb-4')
                
                if not login_logs:
                    ui.label('No login activity recorded yet').classes('text-gray-500 text-center py-8')
                else:
                    # Table header - Lightish blue background
                    with ui.row().classes('w-full table-header-blue p-3 font-semibold text-sm rounded-t'):
                        ui.label('Timestamp').classes('w-40')
                        ui.label('User').classes('w-24')
                        ui.label('IP Address').classes('w-32')
                        ui.label('Location').classes('w-32')
                        ui.label('Device').classes('flex-1')
                        ui.label('Status').classes('w-24')
                    
                    # Table rows
                    for log in login_logs:
                        with ui.row().classes('w-full p-3 border-b items-center text-sm'):
                            timestamp = log['timestamp']
                            if isinstance(timestamp, str):
                                timestamp = datetime.fromisoformat(timestamp)
                            ui.label(self._format_timestamp_with_timezone(timestamp)).classes('w-48 text-gray-700')
                            ui.label(log['username']).classes('w-24 font-medium')
                            ui.label(log['ip_address']).classes('w-32 text-gray-600')
                            ui.label(log['location']).classes('w-32 text-gray-600')
                            ui.label(log['device_info']).classes('flex-1 text-gray-600')
                            
                            status_color = 'green' if log['status'] == 'Success' else 'red'
                            ui.badge(log['status'], color=status_color)
            
            # Get recent security events
            security_events = security_service.get_recent_security_events(5)
            
            # Update security timeline
            self.security_timeline_container.clear()
            with self.security_timeline_container:
                ui.label('Security Events Timeline').classes('text-xl font-semibold mb-4')
                
                if not security_events:
                    ui.label('No security events recorded yet').classes('text-gray-500 text-center py-8')
                else:
                    # Map event types to icons and colors
                    event_icons = {
                        'login': ('login', 'green'),
                        'password_verified': ('verified_user', 'blue'),
                        'session_extended': ('schedule', 'orange'),
                        'settings_updated': ('settings', 'purple'),
                        'new_device': ('devices', 'blue')
                    }
                    
                    with ui.column().classes('w-full gap-3'):
                        for event in security_events:
                            icon, color = event_icons.get(event['event_type'], ('info', 'gray'))
                            
                            # Calculate relative time
                            event_time = event['timestamp']
                            if isinstance(event_time, str):
                                event_time = datetime.fromisoformat(event_time)
                            time_diff = datetime.now() - event_time
                            
                            if time_diff.days > 0:
                                time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
                            elif time_diff.seconds >= 3600:
                                hours = time_diff.seconds // 3600
                                time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
                            else:
                                minutes = time_diff.seconds // 60
                                time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                            
                            with ui.row().classes('items-center gap-3 p-3 hover:bg-gray-50 rounded'):
                                ui.icon(icon).classes(f'text-{color}-500 text-2xl')
                                with ui.column().classes('flex-1'):
                                    ui.label(event['event_description']).classes('font-medium')
                                    ui.label(time_ago).classes('text-xs text-gray-500')
                                ui.icon('chevron_right').classes('text-gray-400')
            
            if show_notification:
                ui.notify('Security logs refreshed', type='positive')
            
        except Exception as e:
            logger.error(f"Error refreshing security logs: {e}")
            ui.notify(f'Failed to refresh security logs: {str(e)}', type='negative')
    
    def _add_content_restriction(self):
        """Add a new content restriction (Admin only)"""
        from datetime import datetime
        from src.utils.id_generator import generate_id
        
        restriction_text = self.restriction_input.value
        description = self.restriction_desc_input.value
        
        if not restriction_text or not restriction_text.strip():
            ui.notify('Please enter a restriction keyword or phrase', type='warning')
            return
        
        try:
            restriction_id = generate_id('restriction')
            username = app.storage.general.get('username', 'admin')
            
            db_schema.conn.execute("""
                INSERT INTO content_restrictions 
                (restriction_id, restriction_text, restriction_type, is_active, 
                 created_by, created_at, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                restriction_id,
                restriction_text.strip().lower(),
                'keyword',
                True,
                username,
                datetime.now(),
                description.strip() if description else None
            ])
            
            # Clear inputs
            self.restriction_input.value = ''
            self.restriction_desc_input.value = ''
            
            # Reload restrictions
            self._load_content_restrictions()
            
            ui.notify(f'Restriction added: {restriction_text}', type='positive')
            logger.info(f"Content restriction added by {username}: {restriction_text}")
            
        except Exception as e:
            logger.error(f"Error adding content restriction: {e}")
            ui.notify(f'Failed to add restriction: {str(e)}', type='negative')
    
    def _load_content_restrictions(self):
        """Load and display active content restrictions"""
        try:
            restrictions = db_schema.conn.execute("""
                SELECT restriction_id, restriction_text, description, 
                       created_by, created_at, is_active
                FROM content_restrictions
                ORDER BY created_at DESC
            """).fetchall()
            
            self.restrictions_container.clear()
            with self.restrictions_container:
                if not restrictions:
                    ui.label('No content restrictions defined yet').classes('text-gray-500 text-sm italic')
                else:
                    ui.label(f'Active Restrictions ({len(restrictions)})').classes('font-semibold text-sm mb-2')
                    
                    for restriction_id, text, desc, created_by, created_at, is_active in restrictions:
                        with ui.card().classes('w-full p-3 border-l-4 border-red-500'):
                            with ui.row().classes('w-full items-center justify-between'):
                                with ui.column().classes('flex-1'):
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('block').classes('text-red-600')
                                        ui.label(text).classes('font-semibold text-red-700')
                                        if is_active:
                                            ui.badge('Active', color='red')
                                        else:
                                            ui.badge('Inactive', color='gray')
                                    
                                    if desc:
                                        ui.label(desc).classes('text-sm text-gray-600 mt-1')
                                    
                                    ui.label(f'Added by {created_by} on {self._format_timestamp_with_timezone(created_at)}').classes('text-xs text-gray-400 mt-1')
                                
                                with ui.row().classes('gap-1'):
                                    ui.button(
                                        icon='delete',
                                        on_click=lambda rid=restriction_id: self._delete_content_restriction(rid)
                                    ).props('flat round dense color=red size=sm').tooltip('Delete restriction')
                                    
                                    toggle_icon = 'toggle_off' if is_active else 'toggle_on'
                                    ui.button(
                                        icon=toggle_icon,
                                        on_click=lambda rid=restriction_id, active=is_active: self._toggle_content_restriction(rid, active)
                                    ).props('flat round dense color=orange size=sm').tooltip('Toggle active/inactive')
        
        except Exception as e:
            logger.error(f"Error loading content restrictions: {e}")
            with self.restrictions_container:
                ui.label('Error loading restrictions').classes('text-red-500 text-sm')
    
    def _delete_content_restriction(self, restriction_id: str):
        """Delete a content restriction"""
        try:
            db_schema.conn.execute("""
                DELETE FROM content_restrictions WHERE restriction_id = ?
            """, [restriction_id])
            
            # Reload restrictions to update UI
            self._load_content_restrictions()
            
            # Log the deletion
            logger.info(f"Restriction deleted: {restriction_id}")
            
        except Exception as e:
            logger.error(f"Error deleting content restriction: {e}")
    
    def _toggle_content_restriction(self, restriction_id: str, current_active: bool):
        """Toggle restriction active/inactive status"""
        try:
            new_status = not current_active
            db_schema.conn.execute("""
                UPDATE content_restrictions 
                SET is_active = ?, updated_at = ?
                WHERE restriction_id = ?
            """, [new_status, datetime.now(), restriction_id])
            
            # Reload restrictions to update UI
            self._load_content_restrictions()
            
            # Log the change
            status_text = 'activated' if new_status else 'deactivated'
            logger.info(f"Restriction {status_text}: {restriction_id}")
            
        except Exception as e:
            logger.error(f"Error toggling content restriction: {e}")
    
    def _check_content_restrictions(self, content: str) -> tuple[bool, list]:
        """Check if content violates any active restrictions
        
        Returns:
            tuple: (is_blocked, list of violated restrictions)
        """
        try:
            restrictions = db_schema.conn.execute("""
                SELECT restriction_text, description
                FROM content_restrictions
                WHERE is_active = TRUE
            """).fetchall()
            
            content_lower = content.lower()
            violated = []
            
            for restriction_text, description in restrictions:
                # Split by comma to handle multiple keywords in one restriction
                keywords = [kw.strip() for kw in restriction_text.split(',')]
                
                # Check each keyword
                for keyword in keywords:
                    if keyword and keyword in content_lower:
                        violated.append({
                            'text': keyword,
                            'description': description or f'Part of restriction: {restriction_text}'
                        })
                        break  # Only add this restriction once even if multiple keywords match
            
            return len(violated) > 0, violated
            
        except Exception as e:
            logger.error(f"Error checking content restrictions: {e}")
            return False, []
    
    def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str):
        """Create a metric card"""
        with ui.card().classes('flex-1 metric-card'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label(title).classes('text-sm text-gray-600')
                    ui.label(value).classes(f'text-3xl font-bold {color}')
                    ui.label(subtitle).classes('text-xs text-gray-500')
                ui.icon(icon).classes(f'{color} text-4xl')
    
    def _create_activity_item(self, title: str, description: str, time: str, icon: str, color: str):
        """Create an activity item"""
        with ui.row().classes('items-center gap-3 p-2 hover:bg-gray-50 rounded'):
            ui.icon(icon).classes(f'{color} text-2xl')
            with ui.column().classes('flex-1'):
                ui.label(title).classes('font-medium')
                ui.label(description).classes('text-sm text-gray-600')
            ui.label(time).classes('text-xs text-gray-400')
    
    def _create_alert_card(self, title: str, message: str, severity: str, time: str):
        """Create an alert card"""
        color_map = {
            'critical': 'border-red-500 bg-red-50',
            'warning': 'border-orange-500 bg-orange-50',
            'info': 'border-blue-500 bg-blue-50',
            'success': 'border-green-500 bg-green-50'
        }
        icon_map = {
            'critical': 'error',
            'warning': 'warning',
            'info': 'info',
            'success': 'check_circle'
        }
        icon_color_map = {
            'critical': 'text-red-600',
            'warning': 'text-orange-600',
            'info': 'text-blue-600',
            'success': 'text-green-600'
        }
        
        with ui.card().classes(f'w-full border-l-4 {color_map.get(severity, "border-gray-500")}'):
            with ui.row().classes('items-start justify-between'):
                with ui.row().classes('items-start gap-3 flex-1'):
                    ui.icon(icon_map.get(severity, 'info')).classes(f'text-2xl {icon_color_map.get(severity, "text-gray-600")}')
                    with ui.column():
                        ui.label(title).classes('font-semibold')
                        ui.label(message).classes('text-sm text-gray-600')
                        ui.label(time).classes('text-xs text-gray-400 mt-1')
                with ui.row().classes('gap-2'):
                    ui.button(icon='visibility', on_click=lambda: ui.notify('View details coming soon')).props('flat dense')
                    ui.button(icon='check', on_click=lambda: ui.notify('Alert acknowledged')).props('flat dense')
    
    def _clear_text_analysis(self):
        """Clear text input and analysis results"""
        self.content_input.set_value('')
        self.text_analysis_container.clear()
        ui.notify('Text and analysis cleared', type='info')
    
    def _refresh_engine_usage(self):
        """Refresh engine usage statistics"""
        try:
            from src.services.api_usage_tracker import api_usage_tracker
            usage_stats = api_usage_tracker.get_all_usage_today(self.current_user_id)
            
            # Update Gemini (Engine 1)
            if hasattr(self, 'gemini_badge') and self.gemini_badge:
                self.gemini_badge.set_text(f"{usage_stats['gemini']['used']}/{usage_stats['gemini']['limit']}")
            if hasattr(self, 'gemini_progress') and self.gemini_progress:
                percentage = usage_stats['gemini']['percentage']
                color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                self.gemini_progress.set_value(percentage/100)
                self.gemini_progress.props(f'color={color}')
            if hasattr(self, 'gemini_remaining') and self.gemini_remaining:
                self.gemini_remaining.set_text(f"Left: {usage_stats['gemini']['remaining']}")
            
            # Update Sarvam AI (Engine 2)
            if hasattr(self, 'sarvam_badge') and self.sarvam_badge:
                self.sarvam_badge.set_text(f"{usage_stats['sarvam']['used']}/{usage_stats['sarvam']['limit']}")
            if hasattr(self, 'sarvam_progress') and self.sarvam_progress:
                percentage = usage_stats['sarvam']['percentage']
                color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                self.sarvam_progress.set_value(percentage/100)
                self.sarvam_progress.props(f'color={color}')
            if hasattr(self, 'sarvam_remaining') and self.sarvam_remaining:
                self.sarvam_remaining.set_text(f"Left: {usage_stats['sarvam']['remaining']}")
            
            # Update Gemini3 (Engine 3)
            if hasattr(self, 'gemini3_badge') and self.gemini3_badge:
                self.gemini3_badge.set_text(f"{usage_stats['gemini3']['used']}/{usage_stats['gemini3']['limit']}")
            if hasattr(self, 'gemini3_progress') and self.gemini3_progress:
                percentage = usage_stats['gemini3']['percentage']
                color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
                self.gemini3_progress.set_value(percentage/100)
                self.gemini3_progress.props(f'color={color}')
            if hasattr(self, 'gemini3_remaining') and self.gemini3_remaining:
                self.gemini3_remaining.set_text(f"Left: {usage_stats['gemini3']['remaining']}")
            
            # Update engine selector options
            if hasattr(self, 'engine_selector'):
                current_value = self.engine_selector.value
                self.engine_selector.options = {
                    'auto': '🤖 Auto (Recommended)',
                    'gemini': f'⚡ Engine 1: Gemini ({usage_stats["gemini"]["remaining"]} left)',
                    'sarvam': f'🌏 Engine 2: Sarvam AI ({usage_stats["sarvam"]["remaining"]} left)',
                    'gemini3': f'🔄 Engine 3: Gemini Backup ({usage_stats["gemini3"]["remaining"]} left)'
                }
                self.engine_selector.update()
            
            ui.notify('Engine usage refreshed', type='positive')
        except Exception as e:
            logger.error(f"Error refreshing engine usage: {e}")
            ui.notify('Could not refresh usage stats', type='warning')
    
    def _update_char_counter(self, text: str):
        """Update character counter display"""
        char_count = len(text) if text else 0
        max_chars = 1000
        
        # Update counter text
        self.char_counter.set_text(f'{char_count:,} / {max_chars:,} characters')
        
        # Change color based on usage
        if char_count > max_chars:
            self.char_counter.classes('text-xs text-red-600 font-semibold', remove='text-gray-500 text-orange-600')
        elif char_count > max_chars * 0.9:
            self.char_counter.classes('text-xs text-orange-600 font-semibold', remove='text-gray-500 text-red-600')
        else:
            self.char_counter.classes('text-xs text-gray-500', remove='text-orange-600 text-red-600 font-semibold')
    
    async def _analyze_content_with_validation(self, content: str):
        """Validate content before analysis"""
        if not content or not content.strip():
            ui.notify('Please enter content to analyze', type='warning')
            return
        
        # Check character limit
        char_count = len(content)
        max_chars = 1000
        
        if char_count > max_chars:
            ui.notify(f'Content exceeds maximum limit of {max_chars:,} characters. Please reduce content length.', type='negative')
            return
        
        # Proceed with analysis
        await self._analyze_content(content)
    
    async def _analyze_content(self, content: str):
        """Analyze content and display results (async to prevent UI blocking)"""
        if not content or not content.strip():
            ui.notify('Please enter content to analyze', type='warning')
            return
        
        # Get selected engine
        selected_engine = None
        if hasattr(self, 'engine_selector') and self.engine_selector.value != 'auto':
            selected_engine = self.engine_selector.value
        
        # Track operation
        self.current_operation = {
            'type': 'Analysis',
            'content': content,
            'progress': 0,
            'engine': selected_engine or 'auto'
        }
        
        try:
            # Show loading state with animation in the inline text container
            self.text_analysis_container.clear()
            with self.text_analysis_container:
                with ui.card().classes('w-full text-center p-8 bg-blue-50 border-2 border-blue-500'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('AI is analyzing your content...').classes('text-xl font-bold mt-4')
                    engine_text = f'Engine: {selected_engine.upper()}' if selected_engine else 'Multi-Engine AI (Auto)'
                    ui.label(f'Powered by: {engine_text}').classes('text-lg font-bold text-blue-700 mt-2')
                    progress_label = ui.label('Ingesting content...').classes('text-sm text-gray-600 mt-2')
            
            # Check if operation should be paused
            if self.operation_paused:
                ui.notify('Operation paused. Please extend session to continue.', type='warning')
                return
            
            # Ingest content (run in executor to not block UI)
            import asyncio
            import uuid
            loop = asyncio.get_event_loop()
            version = await loop.run_in_executor(
                None, 
                self.ingestion_service.ingest_text, 
                self.current_user, 
                content
            )
            self.current_operation['progress'] = 30
            progress_label.set_text('Running AI analysis...')
            
            # Analyze content with selected engine (run in executor to not block UI)
            analysis = await loop.run_in_executor(
                None,
                lambda: self.analyzer.analyze_content(
                    version.version_id,
                    content,
                    preferred_engine=selected_engine,
                    user_id=self.current_user_id
                )
            )
            self.current_analysis = analysis
            self.current_operation['progress'] = 100
            progress_label.set_text('Complete!')
            
            # Refresh engine usage stats
            if hasattr(self, 'engine_selector'):
                self._refresh_engine_usage()
            
            # Store in ashoka_contentint table
            content_id = str(uuid.uuid4())
            word_count = len(content.split())
            char_count = len(content)
            
            # Calculate quality score based on sentiment confidence and content metrics
            quality_score = self._calculate_quality_score(analysis, word_count)
            
            if not db_schema.conn:
                db_schema.connect()
            
            db_schema.conn.execute("""
                INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                content_id,
                self.current_user,
                'text',
                content,
                None,  # file_path
                None,  # file_name
                None,  # file_size_mb
                json.dumps({'source': 'text_input'}),
                analysis.summary,
                analysis.sentiment.classification,
                analysis.sentiment.confidence,
                json.dumps(analysis.keywords),
                json.dumps(analysis.topics),
                json.dumps(analysis.takeaways),
                word_count,
                char_count,
                quality_score,  # quality_score calculated
                datetime.now(),
                analysis.analyzed_at
            ])
            
            # Store in history
            if not hasattr(self, 'analysis_history'):
                self.analysis_history = []
            
            self.analysis_history.insert(0, {
                'timestamp': datetime.now(),
                'content': content[:100] + '...' if len(content) > 100 else content,
                'full_content': content,
                'analysis': analysis,
                'sentiment': analysis.sentiment.classification,
                'version_id': version.version_id,
                'content_id': content_id
            })
            
            # Keep only last 20 analyses
            if len(self.analysis_history) > 20:
                self.analysis_history = self.analysis_history[:20]
            
            # Update UI with results
            self._display_analysis_results(analysis, content)
            
            # Update history table if it exists
            if hasattr(self, 'history_table_container'):
                self._update_history_table()
            
            # Clear operation tracking
            self.current_operation = None
            
            ui.notify('Content analyzed successfully!', type='positive')
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            self.text_analysis_container.clear()
            with self.text_analysis_container:
                with ui.card().classes('w-full text-center p-8 bg-red-50'):
                    ui.icon('error', size='xl').classes('text-red-600')
                    ui.label('Analysis Failed').classes('text-xl font-semibold text-red-600 mt-2')
                    ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
            ui.notify(f'Analysis failed: {str(e)}', type='negative')
            self.current_operation = None

    
    async def _transform_content(self):
        """Transform content for multiple platforms (async to prevent UI blocking)"""
        content = self.transform_input.value
        
        if not content or not content.strip():
            ui.notify('Please enter content to transform', type='warning')
            return
        
        # Get selected platforms
        platforms = []
        if self.platform_linkedin.value:
            platforms.append('linkedin')
        if self.platform_twitter.value:
            platforms.append('twitter')
        if self.platform_instagram.value:
            platforms.append('instagram')
        if self.platform_facebook.value:
            platforms.append('facebook')
        if self.platform_threads.value:
            platforms.append('threads')
        
        if not platforms:
            ui.notify('Please select at least one platform', type='warning')
            return
        
        try:
            # Show loading state with animation
            self.transform_results_container.clear()
            with self.transform_results_container:
                with ui.card().classes('w-full text-center p-8'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('ðŸ”„ Transforming content for social media...').classes('text-xl font-semibold mt-4')
                    progress_label = ui.label(f'Generating content for {len(platforms)} platforms...').classes('text-sm text-gray-600 mt-2')
            
            # Get tone
            tone = self.tone_selector.value.lower()
            include_hashtags = self.include_hashtags.value
            
            # Transform content (run in executor to not block UI)
            import asyncio
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                content_transformer.transform_for_platforms,
                content,
                platforms,
                tone,
                include_hashtags,
                self.current_user_id
            )
            
            # Refresh engine usage stats after transformation
            if hasattr(self, 'engine_selector'):
                self._refresh_engine_usage()
            
            # Store in database
            import uuid
            transform_id = str(uuid.uuid4())
            
            if not db_schema.conn:
                db_schema.connect()
            
            # Store transformed content
            db_schema.conn.execute("""
                INSERT INTO transform_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                transform_id,
                self.current_user,
                content,
                json.dumps(platforms),
                tone,
                include_hashtags,
                json.dumps({k: v.content if v else None for k, v in results.items()}),
                datetime.now()
            ])
            
            # Display results
            self._display_transform_results(results)
            
            # Update history table if it exists
            if hasattr(self, 'transform_history_container'):
                self._update_transform_history()
            
            ui.notify(f'Content transformed for {len(platforms)} platforms!', type='positive')
            
        except Exception as e:
            logger.error(f"Transformation error: {e}")
            self.transform_results_container.clear()
            with self.transform_results_container:
                with ui.card().classes('w-full text-center p-8 bg-red-50'):
                    ui.icon('error', size='xl').classes('text-red-600')
                    ui.label('Transformation Failed').classes('text-xl font-semibold text-red-600 mt-2')
                    ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
            ui.notify(f'Transformation failed: {str(e)}', type='negative')
    
    def _display_transform_results(self, results: dict):
        """Display transformation results for all platforms"""
        self.transform_results_container.clear()
        
        with self.transform_results_container:
            for platform_key, platform_content in results.items():
                if platform_content is None:
                    continue
                
                # Platform-specific styling
                platform_colors = {
                    'LinkedIn': ('bg-blue-50', 'blue', 'work'),
                    'Twitter/X': ('bg-sky-50', 'sky', 'chat'),
                    'Instagram': ('bg-pink-50', 'pink', 'photo_camera'),
                    'Facebook': ('bg-indigo-50', 'indigo', 'thumb_up'),
                    'Threads': ('bg-purple-50', 'purple', 'forum')
                }
                
                bg_color, badge_color, icon = platform_colors.get(
                    platform_content.platform,
                    ('bg-gray-50', 'gray', 'share')
                )
                
                # Create expansion for each platform
                with ui.expansion(
                    platform_content.platform,
                    icon=icon
                ).classes('w-full mb-2'):
                    with ui.card().classes(f'{bg_color} w-full'):
                        # Metadata
                        with ui.row().classes('items-center gap-2 mb-3'):
                            ui.label(f"Tone: {platform_content.metadata.get('tone', 'N/A').title()}").classes('text-sm text-gray-600')
                            ui.label('â€¢').classes('text-gray-400')
                            ui.label(f"Format: {platform_content.metadata.get('format', 'N/A').title()}").classes('text-sm text-gray-600')
                            
                            # Tweet count for Twitter
                            if 'tweet_count' in platform_content.metadata:
                                ui.label('â€¢').classes('text-gray-400')
                                ui.label(f"{platform_content.metadata['tweet_count']} tweets").classes('text-sm text-gray-600')
                        
                        # Content
                        with ui.scroll_area().classes('h-64 w-full'):
                            ui.label(platform_content.content).classes('text-gray-700 whitespace-pre-wrap')
                        
                        # Stats
                        with ui.row().classes('mt-4 gap-2 flex-wrap'):
                            ui.badge(
                                f"{platform_content.character_count:,} characters",
                                color=badge_color
                            )
                            
                            limit_color = 'green' if platform_content.within_limit else 'red'
                            limit_text = 'Within limit' if platform_content.within_limit else 'Exceeds limit'
                            ui.badge(limit_text, color=limit_color)
                            
                            if platform_content.hashtags:
                                ui.badge(
                                    f"{len(platform_content.hashtags)} hashtags",
                                    color='purple'
                                )
                        
                        # Hashtags
                        if platform_content.hashtags:
                            ui.label('Hashtags:').classes('text-sm font-medium mt-3 mb-2')
                            with ui.row().classes('gap-2 flex-wrap'):
                                for hashtag in platform_content.hashtags:
                                    ui.badge(f'#{hashtag}', text_color='white').props(f'color={badge_color}').classes('text-xs')
                        
                        # Copy button
                        ui.button(
                            'Copy to Clipboard',
                            icon='content_copy',
                            on_click=lambda c=platform_content.content: self._copy_to_clipboard(c)
                        ).props('flat').classes('mt-3')
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard with proper escaping and error handling - works on EC2/HTTPS"""
        try:
            payload = json.dumps(text)
            # Use modern clipboard API with fallback for non-HTTPS environments
            ui.run_javascript(f'''
                (async () => {{
                    try {{
                        // Try modern clipboard API (requires HTTPS)
                        if (navigator.clipboard && window.isSecureContext) {{
                            await navigator.clipboard.writeText({payload});
                            console.log('Copied to clipboard using Clipboard API');
                        }} else {{
                            // Fallback for non-HTTPS: create temporary textarea
                            const textArea = document.createElement("textarea");
                            textArea.value = {payload};
                            textArea.style.position = "fixed";
                            textArea.style.left = "-999999px";
                            textArea.style.top = "-999999px";
                            document.body.appendChild(textArea);
                            textArea.focus();
                            textArea.select();
                            try {{
                                document.execCommand('copy');
                                console.log('Copied to clipboard using execCommand fallback');
                            }} catch (err) {{
                                console.error('Fallback copy failed:', err);
                                throw err;
                            }} finally {{
                                textArea.remove();
                            }}
                        }}
                    }} catch (err) {{
                        console.error('Clipboard copy failed:', err);
                        throw err;
                    }}
                }})();
            ''')
            ui.notify('Copied to clipboard!', type='positive')
        except Exception as e:
            logger.error(f"Clipboard operation failed: {e}")
            ui.notify('Failed to copy to clipboard', type='negative')
    
    def _show_coming_soon_dialog(self, feature_name: str):
        """Show coming soon dialog for features under development"""
        with ui.dialog() as dialog, ui.card().classes('p-6 text-center'):
            ui.icon('construction', size='xl').classes('text-amber-600 mb-3')
            ui.label('Coming Soon').classes('text-2xl font-bold mb-2')
            ui.label(f'{feature_name} feature is under development').classes('text-gray-600 mb-4')
            ui.label('This feature will be available in a future update').classes('text-sm text-gray-500 mb-4')
            ui.button('Got it', on_click=dialog.close).props('color=primary')
        dialog.open()

    def _render_upload_preview(self, container, label: str):
        """Render uploaded file preview with a close button."""
        container.clear()
        with container:
            with ui.card().classes('w-full bg-gray-50'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.label(label).classes('font-semibold')
                    ui.button(
                        icon='close',
                        on_click=container.clear
                    ).props('flat round dense color=negative').tooltip('Remove preview')

    async def _handle_audio_upload(self, e):
        """Handle audio file upload with loading indicator"""
        try:
            # NiceGUI UploadEventArguments.file object
            uploaded_file = e.file
            filename = uploaded_file.name
            # read() is async, must await it
            file_content = await uploaded_file.read()
            
            logger.info(f"Audio upload: filename={filename}, content_size={len(file_content)}")
            
            if not file_content:
                ui.notify('No file content received', type='warning')
                return
            
            # Set processing flag to prevent auto-refresh interference
            self._audio_processing = True
            
            # Clear previous content and show loading indicator
            self.audio_preview_container.clear()
            with self.audio_preview_container:
                with ui.card().classes('w-full bg-blue-50 border-2 border-blue-500'):
                    with ui.column().classes('items-center gap-4 p-8'):
                        ui.spinner(size='xl', color='primary')
                        ui.label('ðŸŽ™ï¸ Transcribing Audio with OpenAI Whisper...').classes('text-xl font-bold text-blue-700')
                        ui.label(f'Processing: {filename}').classes('text-sm text-gray-600')
                        ui.label('This may take 1-3 minutes depending on audio length').classes('text-sm text-gray-600')
                        ui.label('âš ï¸ Please stay on this page and do not switch tabs...').classes('text-sm font-bold text-orange-600 mt-2')
            
            # Force UI update to show loading indicator
            await ui.context.client.connected()
            
            ui.notify(f'ðŸŽ™ï¸ Processing with OpenAI Whisper (Local AI): {filename}', type='info', timeout=3000)
            
            # Process audio file using Whisper
            transcription, file_path, metadata = file_processor.process_audio(file_content, filename)
            
            # Clear loading and show transcription preview
            self.audio_preview_container.clear()
            with self.audio_preview_container:
                with ui.card().classes('w-full bg-green-50 border-2 border-green-500'):
                    ui.label('Transcription Complete').classes('font-bold text-xl text-green-700')
                    ui.label('ðŸŽ™ï¸ Processed by: OpenAI Whisper (Local AI - FREE)').classes('font-bold text-lg text-blue-700 mt-1')
                    ui.label(f"Language: {metadata.get('language', 'unknown')} | Processor: {metadata.get('processor', 'Whisper')}").classes('text-sm text-gray-600 mt-1')
                    with ui.expansion('View Transcription', icon='text_snippet').classes('w-full mt-2'):
                        ui.label(transcription[:500] + '...' if len(transcription) > 500 else transcription).classes('text-sm')
                    ui.button(
                        'Analyze with Gemini AI',
                        icon='psychology',
                        on_click=lambda t=transcription: self._analyze_content(t)
                    ).props('color=primary').classes('w-full mt-2')
            
            ui.notify(f'Audio transcribed by OpenAI Whisper (Local AI)!', type='positive', timeout=4000)
            
            # Clear processing flag
            self._audio_processing = False
            
        except Exception as e:
            logger.error(f"Error handling audio upload: {e}")
            self.audio_preview_container.clear()
            with self.audio_preview_container:
                with ui.card().classes('w-full bg-red-50'):
                    ui.label('Error Processing Audio').classes('font-bold text-xl text-red-700')
                    ui.label(str(e)).classes('text-red-600')
            ui.notify(f'Error processing audio: {str(e)}', type='negative')
            # Clear processing flag on error
            self._audio_processing = False

    async def _handle_image_upload(self, e):
        """Handle image file upload and analyze with Gemini Vision"""
        try:
            # NiceGUI UploadEventArguments.file object
            uploaded_file = e.file
            filename = uploaded_file.name
            # read() is async, must await it
            file_content = await uploaded_file.read()
            
            logger.info(f"Image upload: filename={filename}, content_size={len(file_content)}")
            
            if not file_content:
                ui.notify('No file content received', type='warning')
                return
            
            self._render_upload_preview(self.image_preview_container, f'ðŸ–¼ï¸ Image: {filename}')
            
            # Show loading state
            self.image_preview_container.clear()
            with self.image_preview_container:
                with ui.card().classes('w-full text-center p-8 bg-blue-50 border-2 border-blue-500'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('AI is analyzing your image...').classes('text-xl font-bold mt-4')
                    ui.label('Powered by: Google Gemini Vision (Cloud API)').classes('text-lg font-bold text-blue-700 mt-2')
            
            ui.notify(f'ðŸ–¼ï¸ Analyzing image with Gemini Vision...', type='info', timeout=3000)
            
            # Analyze image using Gemini Vision
            import asyncio
            loop = asyncio.get_event_loop()
            analysis = await loop.run_in_executor(
                None,
                gemini_client.analyze_image,
                file_content,
                "Analyze this image in detail and provide comprehensive insights",
                self.current_user_id  # user_id for tracking
            )
            
            # Refresh engine usage stats after image analysis
            if hasattr(self, 'engine_selector'):
                self._refresh_engine_usage()
            
            # Save image file
            import uuid
            from pathlib import Path
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / filename
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Store in database
            content_id = str(uuid.uuid4())
            
            if not db_schema.conn:
                db_schema.connect()
            
            # Create a text summary for storage
            description = analysis.get('description', 'Image analysis')
            objects = analysis.get('objects', [])
            scene = analysis.get('scene', 'unknown')
            
            summary_text = f"Image: {filename}\nScene: {scene}\nObjects: {', '.join(objects) if objects else 'N/A'}\nDescription: {description}"
            
            # Calculate quality score for image based on analysis completeness
            image_quality_score = 100.0
            if not objects or len(objects) < 2:
                image_quality_score -= 15
            if not description or len(description) < 20:
                image_quality_score -= 20
            if scene == 'unknown':
                image_quality_score -= 10
            
            db_schema.conn.execute("""
                INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                content_id,
                self.current_user,
                'image',
                summary_text,
                str(file_path),
                filename,
                round(len(file_content) / (1024 * 1024), 2),  # size in MB
                json.dumps(analysis),
                description,
                'neutral',  # sentiment for images
                0.0,  # confidence
                json.dumps(analysis.get('suggested_tags', [])),
                json.dumps([scene]),
                json.dumps(objects),
                0,  # word_count
                len(description),  # char_count
                image_quality_score,  # quality_score calculated
                datetime.now(),
                datetime.now()
            ])
            
            # Store in history
            if not hasattr(self, 'analysis_history'):
                self.analysis_history = []
            
            self.analysis_history.insert(0, {
                'timestamp': datetime.now(),
                'content': f"Image: {filename}",
                'full_content': summary_text,
                'analysis': analysis,
                'sentiment': 'neutral',
                'content_id': content_id,
                'file_path': str(file_path),
                'file_type': 'image'
            })
            
            # Keep only last 20 analyses
            if len(self.analysis_history) > 20:
                self.analysis_history = self.analysis_history[:20]
            
            # Display results
            self.image_preview_container.clear()
            with self.image_preview_container:
                # Processor Info Banner
                with ui.card().classes('w-full bg-gradient-to-r from-purple-500 to-pink-500'):
                    with ui.row().classes('items-center justify-center gap-3 p-4'):
                        ui.icon('image', size='lg').classes('text-white')
                        ui.label('Image Analysis Complete').classes('font-bold text-2xl text-white')
                    with ui.row().classes('items-center justify-center gap-2 pb-3'):
                        ui.label('Powered by: Google Gemini Vision (Cloud API)').classes('font-bold text-xl text-white')
                
                # Image Preview
                with ui.card().classes('w-full'):
                    ui.label('Image Preview').classes('font-semibold text-lg mb-2')
                    # Display image
                    import base64
                    image_base64 = base64.b64encode(file_content).decode('utf-8')
                    ui.image(f'data:image/jpeg;base64,{image_base64}').classes('w-full max-h-96 object-contain')
                
                # Description
                with ui.card().classes('w-full bg-blue-50'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('description', size='sm').classes('text-blue-600')
                        ui.label('Description').classes('font-semibold text-lg')
                    ui.label(description).classes('text-gray-700')
                
                # Scene & Objects
                with ui.card().classes('w-full'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('category', size='sm').classes('text-purple-600')
                        ui.label('Scene & Objects').classes('font-semibold text-lg')
                    ui.label(f"Scene: {scene}").classes('text-gray-700 mb-1')
                    if objects:
                        with ui.row().classes('gap-1 flex-wrap'):
                            for obj in objects[:10]:
                                ui.badge(obj, color='purple')
                
                # Colors & Mood
                if analysis.get('colors') or analysis.get('mood'):
                    with ui.card().classes('w-full'):
                        with ui.row().classes('items-center gap-2 mb-2'):
                            ui.icon('palette', size='sm').classes('text-pink-600')
                            ui.label('Colors & Mood').classes('font-semibold text-lg')
                        if analysis.get('colors'):
                            ui.label(f"Colors: {', '.join(analysis['colors'])}").classes('text-gray-700 mb-1')
                        if analysis.get('mood'):
                            ui.label(f"Mood: {analysis['mood']}").classes('text-gray-700')
                
                # Tags
                if analysis.get('suggested_tags'):
                    with ui.card().classes('w-full'):
                        with ui.row().classes('items-center gap-2 mb-2'):
                            ui.icon('label', size='sm').classes('text-green-600')
                            ui.label('Suggested Tags').classes('font-semibold text-lg')
                        with ui.row().classes('gap-1 flex-wrap'):
                            for tag in analysis['suggested_tags'][:15]:
                                ui.badge(tag, color='green')
            
            ui.notify(f'Image analyzed by Gemini Vision!', type='positive', timeout=4000)
            
        except Exception as e:
            logger.error(f"Error handling image upload: {e}")
            self.image_preview_container.clear()
            with self.image_preview_container:
                ui.label(f'Error analyzing image: {str(e)}').classes('text-red-600')
            ui.notify(f'Error processing image: {str(e)}', type='negative')

    async def _handle_video_upload(self, e):
        """Handle video file upload with loading indicator"""
        try:
            # NiceGUI UploadEventArguments.file object
            uploaded_file = e.file
            filename = uploaded_file.name
            # read() is async, must await it
            file_content = await uploaded_file.read()
            
            logger.info(f"Video upload: filename={filename}, content_size={len(file_content)}")
            
            if not file_content:
                ui.notify('No file content received', type='warning')
                return
            
            # Set processing flag to prevent auto-refresh interference
            self._video_processing = True
            
            # Clear previous content and show loading indicator
            self.video_preview_container.clear()
            with self.video_preview_container:
                with ui.card().classes('w-full bg-blue-50 border-2 border-blue-500'):
                    with ui.column().classes('items-center gap-4 p-8'):
                        ui.spinner(size='xl', color='primary')
                        ui.label('Processing Video with Whisper + MoviePy...').classes('text-xl font-bold text-blue-700')
                        ui.label(f'Processing: {filename}').classes('text-sm text-gray-600')
                        ui.label('Extracting audio â†’ Transcribing').classes('text-sm text-gray-600')
                        ui.label('This may take 2-5 minutes depending on video length').classes('text-sm text-gray-600')
                        ui.label('âš ï¸ Please stay on this page and do not switch tabs...').classes('text-sm font-bold text-orange-600 mt-2')
            
            # Force UI update to show loading indicator
            await ui.context.client.connected()
            
            ui.notify(f'Processing with OpenAI Whisper + MoviePy (Local AI): {filename}', type='info', timeout=3000)
            
            # Process video file using Whisper
            transcription, file_path, metadata = file_processor.process_video(file_content, filename)
            
            # Clear loading and show transcription preview
            self.video_preview_container.clear()
            with self.video_preview_container:
                with ui.card().classes('w-full bg-green-50 border-2 border-green-500'):
                    ui.label('Transcription Complete').classes('font-bold text-xl text-green-700')
                    ui.label('Processed by: OpenAI Whisper + MoviePy (Local AI - FREE)').classes('font-bold text-lg text-blue-700 mt-1')
                    ui.label(f"Duration: {metadata.get('duration', 'Unknown')} | Language: {metadata.get('language', 'unknown')} | Processor: {metadata.get('processor', 'Whisper')}").classes('text-sm text-gray-600 mt-1')
                    with ui.expansion('View Transcription', icon='text_snippet').classes('w-full mt-2'):
                        ui.label(transcription[:500] + '...' if len(transcription) > 500 else transcription).classes('text-sm')
                    ui.button(
                        'Analyze with Gemini AI',
                        icon='psychology',
                        on_click=lambda t=transcription: self._analyze_content(t)
                    ).props('color=primary').classes('w-full mt-2')
            
            ui.notify(f'Video transcribed by OpenAI Whisper + MoviePy (Local AI)!', type='positive', timeout=4000)
            
            # Clear processing flag
            self._video_processing = False
            
        except Exception as e:
            logger.error(f"Error handling video upload: {e}")
            self.video_preview_container.clear()
            with self.video_preview_container:
                with ui.card().classes('w-full bg-red-50'):
                    ui.label('Error Processing Video').classes('font-bold text-xl text-red-700')
                    ui.label(str(e)).classes('text-red-600')
            ui.notify(f'Error processing video: {str(e)}', type='negative')
            # Clear processing flag on error
            self._video_processing = False

    async def _handle_document_upload(self, e):
        """Handle document file upload"""
        try:
            # NiceGUI UploadEventArguments.file is a LargeFileUpload/SmallFileUpload object
            uploaded_file = e.file
            filename = uploaded_file.name
            # read() is async, must await it
            file_content = await uploaded_file.read()
            
            logger.info(f"Document upload: filename={filename}, content_size={len(file_content)}")
            
            if not file_content:
                ui.notify('No file content received', type='warning')
                return
            
            self._render_upload_preview(self.document_preview_container, f'ðŸ“„ Document: {filename}')
            
            # Determine processor based on file type
            file_ext = filename.lower().split('.')[-1]
            if file_ext == 'pdf':
                processor_name = 'pdfplumber'
            elif file_ext in ['docx', 'doc']:
                processor_name = 'python-docx'
            else:
                processor_name = 'Python'
            
            ui.notify(f'ðŸ“ Processing with {processor_name} (Local Library): {filename}', type='info', timeout=3000)
            
            # Process document file (PDF with pdfplumber, DOCX with python-docx, TXT direct)
            extracted_text, file_path, metadata = file_processor.process_document(file_content, filename)
            
            # Show extraction preview
            with self.document_preview_container:
                with ui.card().classes('w-full mt-2 bg-green-50 border-2 border-green-500'):
                    ui.label('Text Extraction Complete').classes('font-bold text-xl text-green-700')
                    processor_display = metadata.get("processor", "Unknown")
                    ui.label(f'ðŸ“ Processed by: {processor_display} (Local Library - FREE)').classes('font-bold text-lg text-blue-700 mt-1')
                    ui.label(f"Type: {metadata.get('file_type', 'unknown')} | Pages: {metadata.get('page_count', 'N/A')} | Chars: {metadata.get('char_count', 0):,}").classes('text-sm text-gray-600 mt-1')
                    with ui.expansion('View Extracted Text', icon='text_snippet').classes('w-full mt-2'):
                        ui.label(extracted_text[:500] + '...' if len(extracted_text) > 500 else extracted_text).classes('text-sm')
                    ui.button(
                        'Analyze with Gemini AI',
                        icon='psychology',
                        on_click=lambda t=extracted_text: self._analyze_content(t)
                    ).props('color=primary').classes('w-full mt-2')
            
            processor_name = metadata.get('processor', 'Unknown')
            ui.notify(f'Document processed by {processor_name} (Local Library)!', type='positive', timeout=4000)
            
        except Exception as e:
            logger.error(f"Error handling document upload: {e}")
            logger.exception("Full traceback:")
            ui.notify(f'Error processing document: {str(e)}', type='negative')
    
    def _clear_youtube_input(self):
        """Clear YouTube input and preview"""
        self.youtube_url_input.set_value('')
        self.youtube_metadata_container.clear()
    
    async def _handle_youtube_analysis(self, url: str, mode: str):
        """Handle YouTube video analysis"""
        try:
            from src.services.youtube_analyzer import youtube_analyzer
            
            if not url or not url.strip():
                ui.notify('Please enter a YouTube URL', type='warning')
                return
            
            # Set processing flag to prevent auto-refresh interference
            self._youtube_processing = True
            
            # Clear previous metadata
            self.youtube_metadata_container.clear()
            
            # Show persistent loading indicator in the YouTube tab panel itself
            with self.youtube_metadata_container:
                with ui.card().classes('w-full bg-blue-50 border-2 border-blue-500'):
                    with ui.column().classes('items-center gap-4 p-8'):
                        ui.spinner(size='xl', color='primary')
                        if mode == 'Quick Summary':
                            ui.label('ðŸ” Fetching video metadata...').classes('text-xl font-bold text-blue-700')
                            ui.label('This will take 2-5 seconds').classes('text-sm text-gray-600')
                        else:
                            ui.label('Processing YouTube video...').classes('text-xl font-bold text-blue-700')
                            ui.label('Downloading â†’ Transcribing â†’ Analyzing').classes('text-sm text-gray-600')
                            ui.label('This may take 2-5 minutes').classes('text-sm text-gray-600')
                        ui.label('âš ï¸ Please stay on this page and do not switch tabs...').classes('text-sm font-bold text-orange-600 mt-2')
            
            # Force UI update to show loading indicator
            await ui.context.client.connected()
            
            if mode == 'Quick Summary':
                # Quick summary mode - metadata only
                result = youtube_analyzer.get_quick_summary(url)
                
                if not result.get('success'):
                    error_msg = result.get('error', 'Unknown error')
                    ui.notify(f'âŒ {error_msg}', type='negative')
                    self.youtube_metadata_container.clear()
                    with self.youtube_metadata_container:
                        with ui.card().classes('w-full bg-red-50'):
                            ui.label('Error').classes('font-bold text-xl text-red-700')
                            ui.label(error_msg).classes('text-red-600')
                    self._youtube_processing = False
                    return
                
                # Display metadata preview in the YouTube tab
                self._display_youtube_metadata_inline(result)
                ui.notify('Video metadata retrieved!', type='positive')
            
            else:
                # Full analysis mode
                # Get current user ID
                user_id = self.current_user_id if hasattr(self, 'current_user_id') else 'demo_user'
                
                result = youtube_analyzer.analyze_youtube_video(url, user_id, audio_only=True)
                
                if not result.get('success'):
                    error_msg = result.get('error', 'Unknown error')
                    error_code = result.get('error_code', '')
                    stage = result.get('stage', '')
                    
                    ui.notify(f'âŒ {error_msg}', type='negative')
                    self.youtube_metadata_container.clear()
                    with self.youtube_metadata_container:
                        with ui.card().classes('w-full bg-red-50'):
                            ui.label('Analysis Failed').classes('font-bold text-xl text-red-700')
                            ui.label(error_msg).classes('text-red-600 mb-2')
                            if stage:
                                ui.label(f'Failed at stage: {stage}').classes('text-sm text-gray-600')
                            if error_code:
                                ui.label(f'Error code: {error_code}').classes('text-xs text-gray-500')
                    self._youtube_processing = False
                    return
                
                # Display full analysis results in the YouTube tab
                self._display_youtube_analysis_inline(result)
                
                processing_time = result.get('processing_time', 0)
                ui.notify(f'Analysis complete in {processing_time:.1f}s!', type='positive')
            
            # Clear processing flag
            self._youtube_processing = False
        
        except Exception as e:
            logger.error(f"Error in YouTube analysis: {e}")
            logger.exception("Full traceback:")
            ui.notify(f'Error: {str(e)}', type='negative')
            self.youtube_metadata_container.clear()
            with self.youtube_metadata_container:
                with ui.card().classes('w-full bg-red-50'):
                    ui.label('Unexpected Error').classes('font-bold text-xl text-red-700')
                    ui.label(str(e)).classes('text-red-600')
            # Clear processing flag on error
            self._youtube_processing = False
    
    def _display_youtube_metadata(self, metadata: dict):
        """Display YouTube video metadata preview"""
        self.youtube_metadata_container.clear()
        with self.youtube_metadata_container:
            with ui.card().classes('w-full bg-blue-50'):
                ui.label('Video Preview').classes('font-bold text-lg mb-2')
                
                # Thumbnail
                if metadata.get('thumbnail'):
                    ui.image(metadata['thumbnail']).classes('w-full rounded')
                
                # Video info
                with ui.column().classes('gap-1 mt-2'):
                    ui.label(metadata.get('title', 'Unknown')).classes('font-bold text-lg')
                    ui.label(f"ðŸ‘¤ {metadata.get('uploader', 'Unknown')}").classes('text-sm text-gray-600')
                    
                    duration = metadata.get('duration', 0)
                    duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
                    views = metadata.get('view_count', 0)
                    views_str = f"{views:,}" if views else "Unknown"
                    
                    ui.label(f"â±ï¸ Duration: {duration_str} | ðŸ‘ï¸ Views: {views_str}").classes('text-sm text-gray-600')
                    
                    if metadata.get('description'):
                        with ui.expansion('Description', icon='description').classes('w-full mt-2'):
                            ui.label(metadata['description'][:500] + '...' if len(metadata['description']) > 500 else metadata['description']).classes('text-sm')
    
    def _display_youtube_analysis(self, result: dict):
        """Display full YouTube analysis results - DEPRECATED, use _display_youtube_analysis_inline instead"""
        # This function is no longer used - YouTube results display inline in the YouTube tab
        pass
    
    def _display_youtube_metadata_inline(self, metadata: dict):
        """Display YouTube video metadata preview inline in YouTube tab"""
        self.youtube_metadata_container.clear()
        with self.youtube_metadata_container:
            with ui.card().classes('w-full bg-gradient-to-r from-red-500 to-pink-500'):
                with ui.row().classes('items-center justify-center gap-3 p-4'):
                    ui.icon('smart_display', size='lg').classes('text-white')
                    ui.label('Quick Summary').classes('font-bold text-2xl text-white')
            
            with ui.card().classes('w-full'):
                if metadata.get('thumbnail'):
                    ui.image(metadata['thumbnail']).classes('w-full rounded mb-3')
                
                ui.label(metadata.get('title', 'Unknown')).classes('font-bold text-xl mb-2')
                ui.label(f"Channel: {metadata.get('uploader', 'Unknown')}").classes('text-gray-700 mb-1')
                
                duration = metadata.get('duration', 0)
                duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
                views = metadata.get('view_count', 0)
                views_str = f"{views:,}" if views else "Unknown"
                
                ui.label(f"Duration: {duration_str} | Views: {views_str}").classes('text-gray-600 mb-2')
                
                if metadata.get('description'):
                    with ui.expansion('Full Description', icon='description').classes('w-full'):
                        ui.label(metadata['description']).classes('text-sm')
    
    def _display_youtube_analysis_inline(self, result: dict):
        """Display full YouTube analysis results inline in YouTube tab"""
        self.youtube_metadata_container.clear()
        with self.youtube_metadata_container:
            # Header
            with ui.card().classes('w-full bg-gradient-to-r from-red-500 to-pink-500'):
                with ui.row().classes('items-center justify-center gap-3 p-4'):
                    ui.icon('smart_display', size='lg').classes('text-white')
                    ui.label('YouTube Analysis Complete').classes('font-bold text-2xl text-white')
                with ui.row().classes('items-center justify-center gap-2 pb-3'):
                    ui.label('Powered by: Whisper AI + Google Gemini').classes('font-bold text-xl text-white')
            
            metadata = result.get('metadata', {})
            analysis = result.get('analysis', {})
            transcript = result.get('transcript', '')
            
            # Video metadata card
            with ui.card().classes('w-full bg-blue-50'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('info', size='sm').classes('text-blue-600')
                    ui.label('Video Information').classes('font-semibold text-lg')
                
                if metadata.get('thumbnail'):
                    ui.image(metadata['thumbnail']).classes('w-full rounded mb-2')
                
                ui.label(metadata.get('title', 'Unknown')).classes('font-bold text-lg mb-1')
                ui.label(f"Channel: {metadata.get('uploader', 'Unknown')}").classes('text-gray-700')
                
                duration = metadata.get('duration', 0)
                duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
                views = metadata.get('view_count', 0)
                views_str = f"{views:,}" if views else "Unknown"
                language = metadata.get('language', 'unknown')
                
                ui.label(f"Duration: {duration_str} | Views: {views_str} | Language: {language}").classes('text-sm text-gray-600')
            
            # Summary card
            if analysis.get('summary'):
                with ui.card().classes('w-full bg-green-50'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('summarize', size='sm').classes('text-green-600')
                        ui.label('Summary').classes('font-semibold text-lg')
                    ui.label(analysis['summary']).classes('text-gray-700')
            
            # Sentiment card
            if analysis.get('sentiment'):
                with ui.card().classes('w-full'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('sentiment_satisfied', size='sm').classes('text-purple-600')
                        ui.label('Sentiment').classes('font-semibold text-lg')
                    
                    sentiment = analysis['sentiment']
                    confidence = analysis.get('sentiment_confidence', 0)
                    
                    sentiment_color = {
                        'positive': 'green',
                        'neutral': 'gray',
                        'negative': 'red'
                    }.get(sentiment, 'gray')
                    
                    with ui.row().classes('items-center gap-3'):
                        ui.badge(sentiment.upper(), color=sentiment_color).classes('text-lg px-4 py-2')
                        ui.label(f'Confidence: {confidence:.1%}').classes('text-gray-600')
            
            # Keywords card
            if analysis.get('keywords'):
                with ui.card().classes('w-full'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('label', size='sm').classes('text-orange-600')
                        ui.label('Keywords').classes('font-semibold text-lg')
                    with ui.row().classes('gap-2 flex-wrap'):
                        for keyword in analysis['keywords'][:10]:
                            ui.badge(keyword, color='orange').classes('px-3 py-1')
            
            # Topics card
            if analysis.get('topics'):
                with ui.card().classes('w-full'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('topic', size='sm').classes('text-indigo-600')
                        ui.label('Topics').classes('font-semibold text-lg')
                    with ui.column().classes('gap-1'):
                        for topic in analysis['topics']:
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('arrow_right', size='xs')
                                ui.label(topic).classes('text-gray-700')
            
            # Key takeaways card
            if analysis.get('takeaways'):
                with ui.card().classes('w-full bg-yellow-50'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('lightbulb', size='sm').classes('text-yellow-600')
                        ui.label('Key Takeaways').classes('font-semibold text-lg')
                    with ui.column().classes('gap-2'):
                        for i, takeaway in enumerate(analysis['takeaways'], 1):
                            with ui.row().classes('items-start gap-2'):
                                ui.badge(str(i), color='yellow').classes('mt-1')
                                ui.label(takeaway).classes('text-gray-700 flex-1')
            
            # Transcript card
            if transcript:
                with ui.card().classes('w-full'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('article', size='sm').classes('text-gray-600')
                        ui.label('Full Transcript').classes('font-semibold text-lg')
                    
                    word_count = result.get('word_count', 0)
                    char_count = result.get('char_count', 0)
                    ui.label(f"Words: {word_count:,} | Characters: {char_count:,}").classes('text-sm text-gray-600 mb-2')
                    
                    with ui.expansion('View Full Transcript', icon='text_snippet').classes('w-full'):
                        ui.label(transcript).classes('text-sm whitespace-pre-wrap')
                    
                    # Copy button
                    ui.button(
                        'Copy Transcript',
                        icon='content_copy',
                        on_click=lambda: ui.run_javascript(f'navigator.clipboard.writeText({json.dumps(transcript)})')
                    ).props('flat').classes('mt-2')

    def _display_analysis_results(self, analysis, content: str):
        """Display comprehensive analysis results inline in text tab"""
        self.text_analysis_container.clear()
        with self.text_analysis_container:
            # Processor Info Banner - BLACK TEXT
            with ui.card().classes('w-full bg-gradient-to-r from-blue-500 to-purple-500'):
                with ui.row().classes('items-center justify-center gap-3 p-4'):
                    ui.icon('auto_awesome', size='lg').classes('text-black')
                    ui.label('Analysis Complete').classes('font-bold text-2xl text-black')
                with ui.row().classes('items-center justify-center gap-2 pb-3'):
                    ui.label('Powered by: Google Gemini (Cloud API)').classes('font-bold text-xl text-black')
            
            # Summary Card
            with ui.card().classes('w-full bg-blue-50'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('summarize', size='sm').classes('text-blue-600')
                    ui.label('Summary').classes('font-semibold text-lg')
                ui.label(analysis.summary).classes('text-gray-700')
            
            # Sentiment Card
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
                    ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                
                sentiment_color = {
                    'positive': 'green',
                    'neutral': 'gray',
                    'negative': 'red'
                }.get(analysis.sentiment.classification, 'gray')
                
                with ui.row().classes('items-center gap-3'):
                    ui.badge(
                        analysis.sentiment.classification.upper(),
                        color=sentiment_color
                    ).classes('text-lg px-4 py-2')
                    ui.label(f'Confidence: {analysis.sentiment.confidence:.1%}').classes('text-sm text-gray-600')
                
                # Sentiment scores
                if analysis.sentiment.scores:
                    ui.label('Detailed Scores:').classes('text-sm font-medium mt-3 mb-2')
                    for emotion, score in analysis.sentiment.scores.items():
                        with ui.row().classes('items-center gap-2 w-full'):
                            ui.label(emotion.capitalize()).classes('text-sm w-20')
                            ui.linear_progress(score).classes('flex-1')
                            ui.label(f'{score:.1%}').classes('text-sm text-gray-600 w-12')
            
            # Keywords Card
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('label', size='sm').classes('text-purple-600')
                    ui.label('Keywords').classes('font-semibold text-lg')
                with ui.row().classes('gap-2 flex-wrap'):
                    for keyword in analysis.keywords[:15]:
                        ui.badge(keyword, color='purple').classes('text-sm')
            
            # Topics Card
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('topic', size='sm').classes('text-orange-600')
                    ui.label('Topics').classes('font-semibold text-lg')
                with ui.row().classes('gap-2 flex-wrap'):
                    for topic in analysis.topics:
                        ui.badge(topic, color='orange').classes('px-3 py-1')
            
            # Takeaways Card
            if analysis.takeaways:
                with ui.card().classes('w-full bg-green-50'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.icon('lightbulb', size='sm').classes('text-green-600')
                        ui.label('Key Takeaways').classes('font-semibold text-lg')
                    with ui.column().classes('gap-2'):
                        for i, takeaway in enumerate(analysis.takeaways, 1):
                            with ui.row().classes('items-start gap-2'):
                                ui.label(f'{i}.').classes('font-bold text-green-600')
                                ui.label(takeaway).classes('text-gray-700')
            
            # Metrics Card
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    ui.icon('analytics', size='sm').classes('text-indigo-600')
                    ui.label('Content Metrics').classes('font-semibold text-lg')
                
                word_count = len(content.split())
                char_count = len(content)
                
                with ui.grid(columns=3).classes('gap-4 w-full'):
                    with ui.card().classes('text-center p-4'):
                        ui.label(str(word_count)).classes('text-2xl font-bold text-indigo-600')
                        ui.label('Words').classes('text-sm text-gray-600')
                    
                    with ui.card().classes('text-center p-4'):
                        ui.label(str(char_count)).classes('text-2xl font-bold text-indigo-600')
                        ui.label('Characters').classes('text-sm text-gray-600')
                    
                    with ui.card().classes('text-center p-4'):
                        ui.label(str(len(analysis.keywords))).classes('text-2xl font-bold text-indigo-600')
                        ui.label('Keywords').classes('text-sm text-gray-600')
    
    def _update_history_table(self):
        """Update the analysis history table from database"""
        if not hasattr(self, 'history_table_container'):
            return
        
        self.history_table_container.clear()
        
        # Load history from database
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            history_data = db_schema.conn.execute("""
                SELECT id, content_text, sentiment, created_at, analyzed_at,
                       summary, keywords, topics, takeaways, sentiment_confidence
                FROM ashoka_contentint
                WHERE analyzed_at IS NOT NULL
                ORDER BY analyzed_at DESC
                LIMIT 20
            """).fetchall()
            
            if not history_data:
                with self.history_table_container:
                    ui.label('No analysis history yet').classes('text-gray-500 text-center py-4')
                return
            
            with self.history_table_container:
                # Create table with clickable rows
                with ui.column().classes('w-full gap-2'):
                    for row in history_data:
                        content_id, content_text, sentiment, created_at, analyzed_at, summary, keywords_json, topics_json, takeaways_json, confidence = row
                        
                        sentiment_color = {
                            'positive': 'green',
                            'neutral': 'gray',
                            'negative': 'red'
                        }.get(sentiment, 'gray')
                        
                        sentiment_icon = {
                            'positive': 'sentiment_satisfied',
                            'neutral': 'sentiment_neutral',
                            'negative': 'sentiment_dissatisfied'
                        }.get(sentiment, 'sentiment_neutral')
                        
                        content_preview = content_text[:100] + '...' if content_text and len(content_text) > 100 else content_text or 'No content'
                        
                        with ui.card().classes('w-full hover:bg-gray-50'):
                            with ui.row().classes('items-center gap-4 w-full'):
                                # Timestamp
                                with ui.column().classes('w-40'):
                                    timestamp_str = self._format_timestamp_with_timezone(analyzed_at)
                                    date_part, time_part = timestamp_str.rsplit(' ', 2)[0], ' '.join(timestamp_str.rsplit(' ', 2)[1:])
                                    ui.label(date_part).classes('text-sm font-medium')
                                    ui.label(time_part).classes('text-xs text-gray-500')
                                
                                # Content preview
                                with ui.column().classes('flex-1'):
                                    ui.label(content_preview).classes('text-sm text-gray-700 truncate')
                                
                                # Sentiment badge
                                with ui.row().classes('items-center gap-2 w-32'):
                                    ui.icon(sentiment_icon, size='sm').classes(f'text-{sentiment_color}-600')
                                    ui.badge(sentiment.upper(), color=sentiment_color).classes('text-xs')
                                
                                # Action buttons
                                with ui.row().classes('gap-2'):
                                    # Preview button (eye icon) - opens dialog
                                    ui.button(icon='visibility', on_click=lambda cid=content_id: self._show_analysis_preview_dialog(cid)).props('flat dense round').classes('text-blue-600').tooltip('Preview in dialog')
                                    # Load button - loads into main view
                                    ui.button(icon='open_in_full', on_click=lambda cid=content_id: self._load_analysis_from_history(cid)).props('flat dense round').classes('text-green-600').tooltip('Load into main view')
        
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            with self.history_table_container:
                ui.label('Error loading history').classes('text-red-500 text-center py-4')
    
    def _load_analysis_from_history(self, content_id: str):
        """Load and display an analysis from database history"""
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            # Fetch the analysis from database
            row = db_schema.conn.execute("""
                SELECT content_text, summary, sentiment, sentiment_confidence,
                       keywords, topics, takeaways, analyzed_at
                FROM ashoka_contentint
                WHERE id = ?
            """, [content_id]).fetchone()
            
            if not row:
                ui.notify('Analysis not found', type='warning')
                return
            
            content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at = row
            
            # Parse JSON fields
            keywords = json.loads(keywords_json) if keywords_json else []
            topics = json.loads(topics_json) if topics_json else []
            takeaways = json.loads(takeaways_json) if takeaways_json else []
            
            # Reconstruct analysis object
            from src.models.content import ContentAnalysis, Sentiment
            
            analysis = ContentAnalysis(
                version_id=content_id,
                summary=summary,
                takeaways=takeaways,
                keywords=keywords,
                topics=topics,
                sentiment=Sentiment(
                    classification=sentiment,
                    confidence=confidence,
                    scores={
                        'positive': confidence if sentiment == 'positive' else 0.3,
                        'neutral': confidence if sentiment == 'neutral' else 0.3,
                        'negative': confidence if sentiment == 'negative' else 0.3
                    }
                ),
                analyzed_at=analyzed_at
            )
            
            # Display the analysis results
            self._display_analysis_results(analysis, content_text)
            
        except Exception as e:
            logger.error(f"Error loading analysis from history: {e}")
            ui.notify(f'Error loading analysis: {str(e)}', type='negative')
    
    def _show_analysis_preview_dialog(self, content_id: str):
        """Show analysis preview in a dialog window"""
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            # Fetch the analysis from database
            row = db_schema.conn.execute("""
                SELECT content_text, summary, sentiment, sentiment_confidence,
                       keywords, topics, takeaways, analyzed_at, word_count, char_count
                FROM ashoka_contentint
                WHERE id = ?
            """, [content_id]).fetchone()
            
            if not row:
                ui.notify('Analysis not found', type='warning')
                return
            
            content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at, word_count, char_count = row
            
            # Parse JSON fields
            keywords = json.loads(keywords_json) if keywords_json else []
            topics = json.loads(topics_json) if topics_json else []
            takeaways = json.loads(takeaways_json) if takeaways_json else []
            
            # Create dialog
            with ui.dialog() as preview_dialog, ui.card().classes('w-[900px] max-h-[80vh]'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Analysis Preview').classes('text-2xl font-bold')
                    ui.button(icon='close', on_click=preview_dialog.close).props('flat round dense')
                
                with ui.scroll_area().classes('w-full h-[60vh]'):
                    with ui.column().classes('w-full gap-4 p-4'):
                        # Metadata
                        with ui.card().classes('w-full bg-gray-50'):
                            with ui.row().classes('items-center gap-4'):
                                ui.icon('schedule', size='sm').classes('text-gray-600')
                                ui.label(f"Analyzed: {self._format_timestamp_with_timezone(analyzed_at)}").classes('text-sm')
                                ui.label(f"Words: {word_count or len(content_text.split())}").classes('text-sm ml-4')
                                ui.label(f"Characters: {char_count or len(content_text)}").classes('text-sm ml-4')
                        
                        # Original Content
                        with ui.card().classes('w-full'):
                            ui.label('Original Content').classes('text-lg font-semibold mb-2')
                            with ui.scroll_area().classes('h-32 w-full'):
                                ui.label(content_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
                        # Summary
                        with ui.card().classes('w-full bg-blue-50'):
                            with ui.row().classes('items-center gap-2 mb-2'):
                                ui.icon('summarize', size='sm').classes('text-blue-600')
                                ui.label('Summary').classes('font-semibold text-lg')
                            ui.label(summary).classes('text-gray-700')
                        
                        # Sentiment
                        with ui.card().classes('w-full'):
                            with ui.row().classes('items-center gap-2 mb-2'):
                                ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
                                ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                            
                            sentiment_color = {
                                'positive': 'green',
                                'neutral': 'gray',
                                'negative': 'red'
                            }.get(sentiment, 'gray')
                            
                            with ui.row().classes('items-center gap-3'):
                                ui.badge(sentiment.upper(), color=sentiment_color).classes('text-lg px-4 py-2')
                                ui.label(f'Confidence: {confidence:.1%}').classes('text-sm text-gray-600')
                        
                        # Keywords
                        if keywords:
                            with ui.card().classes('w-full'):
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    ui.icon('label', size='sm').classes('text-purple-600')
                                    ui.label('Keywords').classes('font-semibold text-lg')
                                with ui.row().classes('gap-2 flex-wrap'):
                                    for keyword in keywords[:15]:
                                        ui.badge(keyword, color='purple').classes('text-sm')
                        
                        # Topics
                        if topics:
                            with ui.card().classes('w-full'):
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    ui.icon('topic', size='sm').classes('text-orange-600')
                                    ui.label('Topics').classes('font-semibold text-lg')
                                with ui.row().classes('gap-2 flex-wrap'):
                                    for topic in topics:
                                        ui.badge(topic, color='orange').classes('px-3 py-1')
                        
                        # Takeaways
                        if takeaways:
                            with ui.card().classes('w-full bg-green-50'):
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    ui.icon('lightbulb', size='sm').classes('text-green-600')
                                    ui.label('Key Takeaways').classes('font-semibold text-lg')
                                with ui.column().classes('gap-2'):
                                    for i, takeaway in enumerate(takeaways, 1):
                                        with ui.row().classes('items-start gap-2'):
                                            ui.label(f'{i}.').classes('font-bold text-green-600')
                                            ui.label(takeaway).classes('text-gray-700')
            
            preview_dialog.open()
            
        except Exception as e:
            logger.error(f"Error showing preview dialog: {e}")
            ui.notify(f'Error showing preview: {str(e)}', type='negative')
    
    async def _generate_ai_content(self):
        """Generate content using AI based on user prompt"""
        prompt = self.generator_prompt.value
        gen_type = self.gen_type.value
        
        if not prompt or not prompt.strip():
            ui.notify('Please enter a prompt', type='warning')
            return
        
        # Check content restrictions
        is_blocked, violated_restrictions = self._check_content_restrictions(prompt)
        if is_blocked:
            violation_list = ', '.join([r['text'] for r in violated_restrictions])
            ui.notify(f'â›” Content generation blocked: Restricted keywords detected ({violation_list})', type='negative', timeout=5000)
            
            # Show detailed violation message
            self.generator_output_container.clear()
            with self.generator_output_container:
                with ui.card().classes('w-full p-6 bg-red-50 border-l-4 border-red-500'):
                    with ui.row().classes('items-center gap-3 mb-3'):
                        ui.icon('block', size='xl').classes('text-red-600')
                        ui.label('Content Generation Blocked').classes('text-2xl font-bold text-red-700')
                    
                    ui.label('Your prompt contains restricted keywords or phrases that are not allowed for AI content generation.').classes('text-gray-700 mb-3')
                    
                    ui.label('Violated Restrictions:').classes('font-semibold text-red-700 mb-2')
                    for restriction in violated_restrictions:
                        with ui.row().classes('items-start gap-2 mb-2'):
                            ui.icon('warning').classes('text-red-500 text-sm mt-1')
                            with ui.column():
                                ui.label(f'Keyword: "{restriction["text"]}"').classes('font-medium text-red-600')
                                if restriction['description']:
                                    ui.label(restriction['description']).classes('text-sm text-gray-600')
                    
                    ui.label('Please modify your prompt to remove these restricted terms and try again.').classes('text-sm text-gray-600 mt-3 italic')
            
            logger.warning(f"Content generation blocked due to restrictions: {violation_list}")
            return
        
        try:
            # Show loading
            self.generator_output_container.clear()
            with self.generator_output_container:
                with ui.card().classes('w-full text-center p-8'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('AI is generating content...').classes('text-xl font-semibold mt-4')
                    progress_label = ui.label('Processing your prompt...').classes('text-sm text-gray-600 mt-2')
            
            # Generate content
            import asyncio
            loop = asyncio.get_event_loop()
            
            if gen_type == 'Text/Notes':
                # Generate text content using Multi-Engine AI
                generation_prompt = f"Generate professional content based on this prompt:\n\n{prompt}\n\nProvide a well-structured, detailed response."
                
                from src.services.ai_engine import ai_client
                result = await loop.run_in_executor(
                    None,
                    ai_client.generate_content,
                    generation_prompt,
                    None,  # system_instruction
                    0.7,   # temperature
                    None,  # preferred_engine
                    self.current_user_id  # user_id for tracking
                )
                
                generated_text = result.get('text', 'No content generated')
                
                # Refresh engine usage stats after generation
                if hasattr(self, 'engine_selector'):
                    self._refresh_engine_usage()
                
                # Display generated text
                self.generator_output_container.clear()
                with self.generator_output_container:
                    with ui.card().classes('w-full'):
                        with ui.row().classes('items-center justify-between mb-3'):
                            ui.label('Generated Text').classes('text-lg font-semibold')
                            ui.button(
                                icon='content_copy',
                                on_click=lambda: self._copy_to_clipboard(generated_text)
                            ).props('flat dense round').tooltip('Copy to clipboard')
                        
                        with ui.scroll_area().classes('h-96 w-full'):
                            ui.label(generated_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
                        # Action buttons
                        with ui.row().classes('gap-2 mt-3'):
                            ui.button(
                                'Analyze This Content',
                                icon='psychology',
                                on_click=lambda: self._analyze_content(generated_text)
                            ).props('color=primary')
                            ui.button(
                                'Use in Transformer',
                                icon='transform',
                                on_click=lambda: self._use_in_transformer(generated_text)
                            ).props('flat')
                
                ui.notify('Content generated successfully!', type='positive')
            
            elif gen_type == 'Image':
                # Image generation using Son of Ashoka API
                progress_label.set_text('Generating image... This may take up to 60 seconds...')
                
                from src.services.image_generator import image_generator
                
                result = await loop.run_in_executor(
                    None,
                    image_generator.generate_image,
                    prompt
                )
                
                if result['success']:
                    # Display generated image
                    self.generator_output_container.clear()
                    with self.generator_output_container:
                        with ui.card().classes('w-full'):
                            with ui.row().classes('items-center justify-between mb-3'):
                                ui.label('Generated Image').classes('text-lg font-semibold')
                                with ui.row().classes('gap-2'):
                                    ui.button(
                                        icon='download',
                                        on_click=lambda: self._download_generated_image(result['image_bytes'], prompt)
                                    ).props('flat dense round').tooltip('Download image')
                                    ui.button(
                                        icon='refresh',
                                        on_click=lambda: self._generate_ai_content()
                                    ).props('flat dense round').tooltip('Regenerate')
                            
                            # Display prompt
                            with ui.card().classes('w-full bg-gray-50 mb-3'):
                                ui.label('Prompt:').classes('text-xs font-semibold text-gray-600 mb-1')
                                ui.label(prompt).classes('text-sm text-gray-700')
                            
                            # Display image
                            with ui.column().classes('w-full items-center'):
                                ui.image(f'data:image/png;base64,{result["image_data"]}').classes('max-w-full rounded-lg shadow-lg')
                            
                            # Action button
                            with ui.row().classes('gap-2 mt-3 justify-center'):
                                ui.button(
                                    'Download Image',
                                    icon='download',
                                    on_click=lambda: self._download_generated_image(result['image_bytes'], prompt)
                                ).props('color=primary')
                    
                    ui.notify('Image generated successfully!', type='positive')
                else:
                    # Show error
                    self.generator_output_container.clear()
                    with self.generator_output_container:
                        with ui.card().classes('w-full text-center p-8 bg-red-50'):
                            ui.icon('error', size='xl').classes('text-red-600')
                            ui.label('Image Generation Failed').classes('text-xl font-semibold text-red-600 mt-2')
                            ui.label(result.get('error', 'Unknown error')).classes('text-sm text-gray-700 mt-2')
                            
                            ui.button(
                                'Try Again',
                                icon='refresh',
                                on_click=lambda: self._generate_ai_content()
                            ).props('color=primary').classes('mt-4')
                    ui.notify(f'Image generation failed: {result.get("error")}', type='negative')
            
            elif gen_type == 'Video':
                # Video generation - Coming Soon
                self.generator_output_container.clear()
                with self.generator_output_container:
                    with ui.card().classes('w-full text-center p-8 bg-amber-50'):
                        ui.icon('construction', size='xl').classes('text-amber-600 mb-3')
                        ui.label('Video Generation Coming Soon').classes('text-xl font-semibold mb-2')
                        ui.label('AI video generation feature is under development').classes('text-gray-600 mb-2')
                        ui.label('This feature will be available in a future update').classes('text-sm text-gray-500')
                ui.notify('Video generation coming soon', type='info')
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            self.generator_output_container.clear()
            with self.generator_output_container:
                with ui.card().classes('w-full text-center p-8 bg-red-50'):
                    ui.icon('error', size='xl').classes('text-red-600')
                    ui.label('Generation Failed').classes('text-xl font-semibold text-red-600 mt-2')
                    ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
            ui.notify(f'Generation failed: {str(e)}', type='negative')
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard with proper escaping and error handling - works on EC2/HTTPS"""
        try:
            payload = json.dumps(text)
            # Use modern clipboard API with fallback for non-HTTPS environments
            ui.run_javascript(f'''
                (async () => {{
                    try {{
                        // Try modern clipboard API (requires HTTPS)
                        if (navigator.clipboard && window.isSecureContext) {{
                            await navigator.clipboard.writeText({payload});
                            console.log('Copied to clipboard using Clipboard API');
                        }} else {{
                            // Fallback for non-HTTPS: create temporary textarea
                            const textArea = document.createElement("textarea");
                            textArea.value = {payload};
                            textArea.style.position = "fixed";
                            textArea.style.left = "-999999px";
                            textArea.style.top = "-999999px";
                            document.body.appendChild(textArea);
                            textArea.focus();
                            textArea.select();
                            try {{
                                document.execCommand('copy');
                                console.log('Copied to clipboard using execCommand fallback');
                            }} catch (err) {{
                                console.error('Fallback copy failed:', err);
                                throw err;
                            }} finally {{
                                textArea.remove();
                            }}
                        }}
                    }} catch (err) {{
                        console.error('Clipboard copy failed:', err);
                        throw err;
                    }}
                }})();
            ''')
            ui.notify('Copied to clipboard!', type='positive')
        except Exception as e:
            logger.error(f"Clipboard operation failed: {e}")
            ui.notify('Failed to copy to clipboard', type='negative')
    
    def _download_generated_image(self, image_bytes: bytes, prompt: str):
        """Download generated image"""
        try:
            import base64
            from datetime import datetime
            
            # Create filename from prompt (sanitized)
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"generated_{safe_prompt}_{timestamp}.png"
            
            # Convert bytes to base64 for download
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Trigger download using JavaScript
            ui.run_javascript(f'''
                const link = document.createElement('a');
                link.href = 'data:image/png;base64,{image_base64}';
                link.download = '{filename}';
                link.click();
            ''')
            
            ui.notify(f'Downloading {filename}', type='positive')
            logger.info(f"Image download triggered: {filename}")
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            ui.notify('Failed to download image', type='negative')
    
    def _use_in_transformer(self, text: str):
        """Use generated text in the transformer"""
        if hasattr(self, 'transform_input'):
            self.transform_input.set_value(text)
            ui.notify('Text loaded into transformer', type='info')
        else:
            ui.notify('Transformer not available', type='warning')
    
    def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str = ''):
        """Create a metric card"""
        with ui.card().classes('flex-1 dashboard-card'):
            with ui.row().classes('items-center gap-3'):
                ui.icon(icon, size='lg').classes(color)
                with ui.column().classes('gap-1'):
                    ui.label(title).classes('text-sm opacity-90')
                    ui.label(value).classes('text-3xl font-bold')
                    if subtitle:
                        ui.label(subtitle).classes('text-xs opacity-75')
    
    def _create_activity_item(self, title: str, description: str, time: str, icon: str, icon_color: str):
        """Create an activity item"""
        with ui.row().classes('items-start gap-3 p-3 content-card'):
            ui.icon(icon, size='md').classes(icon_color)
            with ui.column().classes('flex-1 gap-1'):
                ui.label(title).classes('font-semibold')
                ui.label(description).classes('text-sm text-gray-600')
                ui.label(time).classes('text-xs text-gray-500')


def launch_dashboard():
    """Launch the Ashoka dashboard"""
    dashboard = AshokaGovDashboard()
    dashboard.create_dashboard()
    
    ui.run(
        title='Ashoka - GenAI Governance Platform',
        favicon='🛡️',
        dark=False,
        reload=False,
        host="0.0.0.0",
        port=8080
    )


if __name__ in {"__main__", "__mp_main__"}:
    launch_dashboard()


