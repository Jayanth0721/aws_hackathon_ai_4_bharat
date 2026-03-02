# # """Ashoka GenAI Governance Dashboard - NiceGUI Implementation"""
# # from nicegui import ui, app
# # from datetime import datetime, timedelta
# # from typing import Optional
# # import json

# # from src.services.content_ingestion import ContentIngestionService
# # from src.services.content_analyzer import ContentAnalyzer
# # from src.services.file_processor import file_processor
# # from src.services.content_transformer import content_transformer
# # from src.services.gemini_client import gemini_client
# # from src.database.duckdb_schema import db_schema
# # from src.utils.logging import logger


# # class AshokaGovDashboard:
# #     """GenAI Governance Dashboard"""
    
# #     def __init__(self):
# #         self.ingestion_service = ContentIngestionService()
# #         self.analyzer = ContentAnalyzer()
# #         self.current_user = "demo_user"
# #         self.current_analysis = None
# #         self.dark_mode = False
# #         self.uploaded_file_path = None
        
# #         # Analysis history for Content Intelligence
# #         self.analysis_history = []
        
# #         # Session management
# #         self.session_duration = 30 * 60  # 30 minutes in seconds
# #         self.session_start_time = datetime.now()
# #         self.session_timer = None
# #         self.session_paused = False
# #         self.paused_tasks = []
        
# #         # Current operation tracking
# #         self.current_operation = None
# #         self.operation_paused = False
        
# #         # Use app.storage.general instead of app.storage.user (doesn't require secret)
# #         self.current_language = app.storage.general.get('language', 'English')
        
# #         # User preferences
# #         self.user_preferences = {
# #             'notifications': True,
# #             'auto_save': True,
# #             'theme': 'light',
# #             'language': 'English',
# #             'email_alerts': False,
# #             'session_timeout': 30
# #         }
        
# #         self.translations = {
# #             "English": {
# #                 "title": "Ashoka",
# #                 "subtitle": "GenAI Governance & Observability Platform",
# #                 "overview": "Overview",
# #                 "content_intelligence": "Content Intelligence",
# #                 "transform": "Transform",
# #                 "monitoring": "Monitoring",
# #                 "alerts": "Alerts",
# #                 "profile": "Profile",
# #                 "settings": "Settings",
# #                 "logout": "Logout",
# #                 "user_profile": "User Profile",
# #                 "username": "Username",
# #                 "email": "Email",
# #                 "role": "Role",
# #                 "member_since": "Member Since",
# #                 "close": "Close",
# #                 "language_settings": "Language Settings",
# #                 "select_language": "Select Language",
# #                 "apply": "Apply",
# #                 # Overview Panel
# #                 "platform_overview": "Platform Overview",
# #                 "total_content": "Total Content",
# #                 "this_week": "this week",
# #                 "quality_score": "Quality Score",
# #                 "excellent": "Excellent",
# #                 "risk_alerts": "Risk Alerts",
# #                 "resolved": "resolved",
# #                 "ai_operations": "AI Operations",
# #                 "success": "success",
# #                 "recent_activity": "Recent Activity",
# #                 "content_analyzed": "Content analyzed",
# #                 "article_ai_ethics": "Article about AI ethics",
# #                 "min_ago": "min ago",
# #                 "risk_detected": "Risk detected",
# #                 "policy_violation": "Potential policy violation",
# #                 "content_transformed": "Content transformed",
# #                 "linkedin_twitter": "LinkedIn + Twitter posts",
# #                 "hour_ago": "hour ago",
# #                 "quality_alert": "Quality alert",
# #                 "readability_below": "Readability below threshold",
# #                 "hours_ago": "hours ago",
# #                 "system_health": "System Health",
# #                 "ai_model_performance": "AI Model Performance",
# #                 "content_processing_rate": "Content Processing Rate",
# #                 "storage_utilization": "Storage Utilization",
# #                 "api_healthy": "API: Healthy",
# #                 "database_healthy": "Database: Healthy",
# #                 "ai_healthy": "AI: Healthy"
# #             },
# #             "Hindi": {
# #                 "title": "अशोक",
# #                 "subtitle": "जेनएआई गवर्नेंस और ऑब्जर्वेबिलिटी प्लेटफॉर्म",
# #                 "overview": "अवलोकन",
# #                 "content_intelligence": "सामग्री बुद्धिमत्ता",
# #                 "transform": "रूपांतरण",
# #                 "monitoring": "निगरानी",
# #                 "alerts": "अलर्ट",
# #                 "profile": "प्रोफ़ाइल",
# #                 "settings": "सेटिंग्स",
# #                 "logout": "लॉगआउट",
# #                 "user_profile": "उपयोगकर्ता प्रोफ़ाइल",
# #                 "username": "उपयोगकर्ता नाम",
# #                 "email": "ईमेल",
# #                 "role": "भूमिका",
# #                 "member_since": "सदस्य बने",
# #                 "close": "बंद करें",
# #                 "language_settings": "भाषा सेटिंग्स",
# #                 "select_language": "भाषा चुनें",
# #                 "apply": "लागू करें",
# #                 # Overview Panel
# #                 "platform_overview": "प्लेटफ़ॉर्म अवलोकन",
# #                 "total_content": "कुल सामग्री",
# #                 "this_week": "इस सप्ताह",
# #                 "quality_score": "गुणवत्ता स्कोर",
# #                 "excellent": "उत्कृष्ट",
# #                 "risk_alerts": "जोखिम अलर्ट",
# #                 "resolved": "हल किया गया",
# #                 "ai_operations": "एआई संचालन",
# #                 "success": "सफलता",
# #                 "recent_activity": "हाल की गतिविधि",
# #                 "content_analyzed": "सामग्री विश्लेषण",
# #                 "article_ai_ethics": "एआई नैतिकता पर लेख",
# #                 "min_ago": "मिनट पहले",
# #                 "risk_detected": "जोखिम का पता चला",
# #                 "policy_violation": "संभावित नीति उल्लंघन",
# #                 "content_transformed": "सामग्री रूपांतरित",
# #                 "linkedin_twitter": "लिंक्डइन + ट्विटर पोस्ट",
# #                 "hour_ago": "घंटे पहले",
# #                 "quality_alert": "गुणवत्ता अलर्ट",
# #                 "readability_below": "पठनीयता सीमा से नीचे",
# #                 "hours_ago": "घंटे पहले",
# #                 "system_health": "सिस्टम स्वास्थ्य",
# #                 "ai_model_performance": "एआई मॉडल प्रदर्शन",
# #                 "content_processing_rate": "सामग्री प्रसंस्करण दर",
# #                 "storage_utilization": "भंडारण उपयोग",
# #                 "api_healthy": "एपीआई: स्वस्थ",
# #                 "database_healthy": "डेटाबेस: स्वस्थ",
# #                 "ai_healthy": "एआई: स्वस्थ"
# #             },
# #             "Kannada": {
# #                 "title": "ಅಶೋಕ",
# #                 "subtitle": "ಜೆನ್‌ಎಐ ಆಡಳಿತ ಮತ್ತು ವೀಕ್ಷಣಾ ವೇದಿಕೆ",
# #                 "overview": "ಅವಲೋಕನ",
# #                 "content_intelligence": "ವಿಷಯ ಬುದ್ಧಿವಂತಿಕೆ",
# #                 "transform": "ಪರಿವರ್ತನೆ",
# #                 "monitoring": "ಮೇಲ್ವಿಚಾರಣೆ",
# #                 "alerts": "ಎಚ್ಚರಿಕೆಗಳು",
# #                 "profile": "ಪ್ರೊಫೈಲ್",
# #                 "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
# #                 "logout": "ಲಾಗ್ಔಟ್",
# #                 "user_profile": "ಬಳಕೆದಾರ ಪ್ರೊಫೈಲ್",
# #                 "username": "ಬಳಕೆದಾರ ಹೆಸರು",
# #                 "email": "ಇಮೇಲ್",
# #                 "role": "ಪಾತ್ರ",
# #                 "member_since": "ಸದಸ್ಯರಾದ ದಿನಾಂಕ",
# #                 "close": "ಮುಚ್ಚಿ",
# #                 "language_settings": "ಭಾಷಾ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
# #                 "select_language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
# #                 "apply": "ಅನ್ವಯಿಸಿ",
# #                 # Overview Panel
# #                 "platform_overview": "ವೇದಿಕೆ ಅವಲೋಕನ",
# #                 "total_content": "ಒಟ್ಟು ವಿಷಯ",
# #                 "this_week": "ಈ ವಾರ",
# #                 "quality_score": "ಗುಣಮಟ್ಟ ಸ್ಕೋರ್",
# #                 "excellent": "ಅತ್ಯುತ್ತಮ",
# #                 "risk_alerts": "ಅಪಾಯ ಎಚ್ಚರಿಕೆಗಳು",
# #                 "resolved": "ಪರಿಹರಿಸಲಾಗಿದೆ",
# #                 "ai_operations": "ಎಐ ಕಾರ್ಯಾಚರಣೆಗಳು",
# #                 "success": "ಯಶಸ್ಸು",
# #                 "recent_activity": "ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ",
# #                 "content_analyzed": "ವಿಷಯ ವಿಶ್ಲೇಷಣೆ",
# #                 "article_ai_ethics": "ಎಐ ನೀತಿಶಾಸ್ತ್ರದ ಲೇಖನ",
# #                 "min_ago": "ನಿಮಿಷಗಳ ಹಿಂದೆ",
# #                 "risk_detected": "ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
# #                 "policy_violation": "ಸಂಭಾವ್ಯ ನೀತಿ ಉಲ್ಲಂಘನೆ",
# #                 "content_transformed": "ವಿಷಯ ಪರಿವರ್ತನೆ",
# #                 "linkedin_twitter": "ಲಿಂಕ್ಡ್‌ಇನ್ + ಟ್ವಿಟರ್ ಪೋಸ್ಟ್‌ಗಳು",
# #                 "hour_ago": "ಗಂಟೆ ಹಿಂದೆ",
# #                 "quality_alert": "ಗುಣಮಟ್ಟ ಎಚ್ಚರಿಕೆ",
# #                 "readability_below": "ಓದುವಿಕೆ ಮಿತಿಗಿಂತ ಕಡಿಮೆ",
# #                 "hours_ago": "ಗಂಟೆಗಳ ಹಿಂದೆ",
# #                 "system_health": "ವ್ಯವಸ್ಥೆ ಆರೋಗ್ಯ",
# #                 "ai_model_performance": "ಎಐ ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ",
# #                 "content_processing_rate": "ವಿಷಯ ಪ್ರಕ್ರಿಯೆ ದರ",
# #                 "storage_utilization": "ಸಂಗ್ರಹಣೆ ಬಳಕೆ",
# #                 "api_healthy": "ಎಪಿಐ: ಆರೋಗ್ಯಕರ",
# #                 "database_healthy": "ಡೇಟಾಬೇಸ್: ಆರೋಗ್ಯಕರ",
# #                 "ai_healthy": "ಎಐ: ಆರೋಗ್ಯಕರ"
# #             },
# #             "Tamil": {
# #                 "title": "அசோகா",
# #                 "subtitle": "ஜென்ஏஐ ஆளுமை மற்றும் கண்காணிப்பு தளம்",
# #                 "overview": "மேலோட்டம்",
# #                 "content_intelligence": "உள்ளடக்க நுண்ணறிவு",
# #                 "transform": "மாற்றம்",
# #                 "monitoring": "கண்காணிப்பு",
# #                 "alerts": "எச்சரிக்கைகள்",
# #                 "profile": "சுயவிவரம்",
# #                 "settings": "அமைப்புகள்",
# #                 "logout": "வெளியேறு",
# #                 "user_profile": "பயனர் சுயவிவரம்",
# #                 "username": "பயனர் பெயர்",
# #                 "email": "மின்னஞ்சல்",
# #                 "role": "பங்கு",
# #                 "member_since": "உறுப்பினரான தேதி",
# #                 "close": "மூடு",
# #                 "language_settings": "மொழி அமைப்புகள்",
# #                 "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
# #                 "apply": "பயன்படுத்து",
# #                 # Overview Panel
# #                 "platform_overview": "தள மேலோட்டம்",
# #                 "total_content": "மொத்த உள்ளடக்கம்",
# #                 "this_week": "இந்த வாரம்",
# #                 "quality_score": "தர மதிப்பெண்",
# #                 "excellent": "சிறந்தது",
# #                 "risk_alerts": "அபாய எச்சரிக்கைகள்",
# #                 "resolved": "தீர்க்கப்பட்டது",
# #                 "ai_operations": "ஏஐ செயல்பாடுகள்",
# #                 "success": "வெற்றி",
# #                 "recent_activity": "சமீபத்திய செயல்பாடு",
# #                 "content_analyzed": "உள்ளடக்க பகுப்பாய்வு",
# #                 "article_ai_ethics": "ஏஐ நெறிமுறைகள் பற்றிய கட்டுரை",
# #                 "min_ago": "நிமிடங்களுக்கு முன்",
# #                 "risk_detected": "அபாயம் கண்டறியப்பட்டது",
# #                 "policy_violation": "சாத்தியமான கொள்கை மீறல்",
# #                 "content_transformed": "உள்ளடக்க மாற்றம்",
# #                 "linkedin_twitter": "லிங்க்ட்இன் + ட்விட்டர் இடுகைகள்",
# #                 "hour_ago": "மணி நேரத்திற்கு முன்",
# #                 "quality_alert": "தர எச்சரிக்கை",
# #                 "readability_below": "வாசிப்புத்திறன் வரம்புக்குக் கீழே",
# #                 "hours_ago": "மணி நேரங்களுக்கு முன்",
# #                 "system_health": "அமைப்பு ஆரோக்கியம்",
# #                 "ai_model_performance": "ஏஐ மாதிரி செயல்திறன்",
# #                 "content_processing_rate": "உள்ளடக்க செயலாக்க விகிதம்",
# #                 "storage_utilization": "சேமிப்பக பயன்பாடு",
# #                 "api_healthy": "ஏபிஐ: ஆரோக்கியமானது",
# #                 "database_healthy": "தரவுத்தளம்: ஆரோக்கியமானது",
# #                 "ai_healthy": "ஏஐ: ஆரோக்கியமானது"
# #             }
# #         }
        
# #         # Initialize database
# #         db_schema.connect()
# #         db_schema.initialize_schema()
    
# #     def t(self, key: str) -> str:
# #         """Get translation for current language"""
# #         return self.translations.get(self.current_language, self.translations["English"]).get(key, key)
    
# #     def create_dashboard(self):
# #         """Create the main dashboard UI"""
        
# #         # Custom CSS for aesthetic design with skinish brown theme
# #         ui.add_head_html('''
# #             <style>
# #                 :root {
# #                     --bg-primary: #f5e6d3;
# #                     --bg-secondary: #e8d4b8;
# #                     --text-primary: #3e2723;
# #                     --text-secondary: #5d4037;
# #                     --accent-color: #8d6e63;
# #                     --card-bg: #fff8f0;
# #                     --header-from: #78350f;
# #                     --header-to: #92400e;
# #                 }
                
# #                 .dark-mode {
# #                     --bg-primary: #1a1a1a;
# #                     --bg-secondary: #2d2d2d;
# #                     --text-primary: #e5e5e5;
# #                     --text-secondary: #b3b3b3;
# #                     --accent-color: #9ca3af;
# #                     --card-bg: #262626;
# #                     --header-from: #374151;
# #                     --header-to: #4b5563;
# #                 }
                
# #                 body {
# #                     background-color: var(--bg-primary) !important;
# #                     color: var(--text-primary) !important;
# #                     transition: all 0.3s ease;
# #                 }
                
# #                 .dashboard-card {
# #                     background: linear-gradient(135deg, #8d6e63 0%, #6d4c41 100%);
# #                     border-radius: 12px;
# #                     padding: 20px;
# #                     color: white;
# #                     box-shadow: 0 4px 6px rgba(0,0,0,0.1);
# #                 }
                
# #                 .dark-mode .dashboard-card {
# #                     background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
# #                 }
                
# #                 .metric-card {
# #                     background: var(--card-bg) !important;
# #                     border-radius: 10px;
# #                     padding: 20px;
# #                     box-shadow: 0 2px 4px rgba(0,0,0,0.05);
# #                     border-left: 4px solid #8d6e63;
# #                     color: var(--text-primary) !important;
# #                 }
                
# #                 .dark-mode .metric-card {
# #                     border-left-color: #9ca3af;
# #                     box-shadow: 0 2px 4px rgba(0,0,0,0.3);
# #                 }
                
# #                 .risk-high {
# #                     border-left-color: #ef4444 !important;
# #                 }
# #                 .risk-medium {
# #                     border-left-color: #f59e0b !important;
# #                 }
# #                 .risk-low {
# #                     border-left-color: #10b981 !important;
# #                 }
                
# #                 .content-card {
# #                     background: var(--bg-secondary);
# #                     border-radius: 8px;
# #                     padding: 16px;
# #                     margin: 8px 0;
# #                 }
                
# #                 .q-card {
# #                     background: var(--card-bg) !important;
# #                     color: var(--text-primary) !important;
# #                 }
                
# #                 .q-tab {
# #                     color: var(--text-secondary) !important;
# #                 }
                
# #                 .q-tab--active {
# #                     color: var(--accent-color) !important;
# #                 }
                
# #                 .q-header {
# #                     background: linear-gradient(to right, var(--header-from), var(--header-to)) !important;
# #                 }
                
# #                 .dark-mode .text-gray-600 {
# #                     color: #9ca3af !important;
# #                 }
                
# #                 .dark-mode .text-gray-500 {
# #                     color: #6b7280 !important;
# #                 }
                
# #                 .dark-mode .text-gray-700 {
# #                     color: #d1d5db !important;
# #                 }
                
# #                 /* Timer visibility in dark mode - white text on green */
# #                 .dark-mode .timer-text {
# #                     color: #ffffff !important;
# #                 }
                
# #                 /* Tab spacing */
# #                 .q-tab {
# #                     padding: 0 24px !important;
# #                     min-width: 140px !important;
# #                     display: flex !important;
# #                     justify-content: center !important;
# #                 }
                
# #                 .q-tab__content {
# #                     display: flex !important;
# #                     flex-direction: row !important;
# #                     justify-content: center !important;
# #                     align-items: center !important;
# #                     gap: 2px !important;
# #                 }
                
# #                 .q-tab__icon {
# #                     margin: 0 !important;
# #                 }
                
# #                 .q-tab__label {
# #                     margin: 0 !important;
# #                 }
                
# #                 /* Fix overlapping content */
# #                 .q-tab-panel {
# #                     padding: 24px !important;
# #                 }
                
# #                 /* Content Intelligence Panel - Professional Dark Theme */
# #                 .content-input-area {
# #                     background: rgba(100, 100, 100, 0.1) !important;
# #                     border: 1px solid rgba(150, 150, 150, 0.2) !important;
# #                     border-radius: 8px !important;
# #                 }
                
# #                 .dark-mode .content-input-area {
# #                     background: rgba(50, 50, 50, 0.3) !important;
# #                     border: 1px solid rgba(100, 100, 100, 0.3) !important;
# #                 }
                
# #                 /* Lightish blue table headers */
# #                 .table-header-blue {
# #                     background-color: #bfdbfe !important;
# #                     color: #1e40af !important;
# #                     font-weight: 600 !important;
# #                 }
                
# #                 .dark-mode .table-header-blue {
# #                     background-color: #1e3a8a !important;
# #                     color: #93c5fd !important;
# #                 }
# #             </style>
# #         ''')
        
# #         # Header
# #         with ui.header().classes('bg-gradient-to-r from-amber-900 to-brown-800'):
# #             with ui.row().classes('w-full items-center'):
# #                 ui.icon('shield_with_heart', size='lg').classes('text-white')
# #                 self.title_label = ui.label(self.t('title')).classes('text-2xl font-bold text-white ml-2')
# #                 self.subtitle_label = ui.label(self.t('subtitle')).classes('text-sm text-amber-100 ml-4')
# #                 ui.space()
                
# #                 # Session timer - Green background
# #                 with ui.card().classes('bg-green-400 px-4 py-2 shadow-lg'):
# #                     with ui.row().classes('items-center gap-2'):
# #                         ui.icon('schedule', size='sm').classes('text-red')
# #                         self.timer_label = ui.label('30:00').classes('timer-text text-green font-mono text-lg font-bold')
                
# #                 # Dark mode toggle
# #                 self.theme_toggle = ui.button(
# #                     icon='dark_mode',
# #                     on_click=self._toggle_theme
# #                 ).props('flat round').classes('text-white ml-2')
                
# #                 with ui.button(icon='account_circle').props('flat round').classes('text-white'):
# #                     with ui.menu():
# #                         ui.menu_item(self.t('profile'), on_click=self._show_profile_dialog)
# #                         ui.menu_item(self.t('settings'), on_click=self._show_settings_dialog)
# #                         ui.separator()
# #                         ui.menu_item(self.t('logout'), on_click=self._handle_logout)
        
# #         # Start session timer
# #         self._start_session_timer()
        
# #         # Start auto-refresh timers for real-time updates
# #         self._start_auto_refresh_timers()
        
# #         # Check user role for Security tab visibility
# #         username = app.storage.general.get('username', '')
# #         is_admin = self._check_if_admin(username)
        
# #         # Main content with tabs
# #         with ui.tabs().classes('w-full justify-center') as tabs:
# #             self.overview_tab = ui.tab(self.t('overview'), icon='dashboard')
# #             self.content_tab = ui.tab(self.t('content_intelligence'), icon='psychology')
# #             self.transform_tab = ui.tab(self.t('transform'), icon='transform')
# #             self.monitor_tab = ui.tab(self.t('monitoring'), icon='bar_chart')
# #             self.alerts_tab = ui.tab(self.t('alerts'), icon='notifications')
            
# #             # Security tab - always create but control visibility
# #             self.security_tab = ui.tab('Security', icon='security')
# #             self.security_tab.set_visibility(is_admin)
        
# #         with ui.tab_panels(tabs, value=self.overview_tab).classes('w-full'):
# #             # Overview Panel
# #             with ui.tab_panel(self.overview_tab):
# #                 self._create_overview_panel()
            
# #             # Content Intelligence Panel
# #             with ui.tab_panel(self.content_tab):
# #                 self._create_content_intelligence_panel()
            
# #             # Transform Panel
# #             with ui.tab_panel(self.transform_tab):
# #                 self._create_transform_panel()
            
# #             # Monitoring Panel
# #             with ui.tab_panel(self.monitor_tab):
# #                 with ui.column().classes('w-full'):
# #                     self._create_monitoring_panel()
            
# #             # Alerts Panel
# #             with ui.tab_panel(self.alerts_tab):
# #                 self._create_alerts_panel()
            
# #             # Security Panel - always create but only visible for admin
# #             with ui.tab_panel(self.security_tab):
# #                 self._create_security_panel()
    
# #     def _check_if_admin(self, username: str) -> bool:
# #         """Check if user has admin role"""
# #         if not username:
# #             return False
        
# #         try:
# #             from src.database.mock_storage import mock_dynamodb
# #             from src.config import config
            
# #             user_data = mock_dynamodb.get_item(config.DYNAMODB_USERS_TABLE, f"user_{username}")
# #             if user_data:
# #                 role = user_data.get('role', 'creator')
# #                 return role == 'admin'
# #         except Exception as e:
# #             logger.error(f"Error checking admin role: {e}")
        
# #         return False
    
# #     def _toggle_theme(self):
# #         """Toggle between light and dark mode"""
# #         self.dark_mode = not self.dark_mode
        
# #         if self.dark_mode:
# #             ui.run_javascript('document.body.classList.add("dark-mode")')
# #             self.theme_toggle.props('icon=light_mode')
# #         else:
# #             ui.run_javascript('document.body.classList.remove("dark-mode")')
# #             self.theme_toggle.props('icon=dark_mode')
    
# #     def _handle_logout(self):
# #         """Handle user logout - clear session and redirect to login"""
# #         # Clear session storage
# #         app.storage.general.clear()
        
# #         # Notify user
# #         ui.notify('Logged out successfully', type='info')
        
# #         # Redirect to login page
# #         ui.navigate.to('/')
    
# #     def _start_session_timer(self):
# #         """Start the session countdown timer"""
# #         def update_timer():
# #             elapsed = (datetime.now() - self.session_start_time).total_seconds()
# #             remaining = self.session_duration - elapsed
            
# #             if remaining <= 0:
# #                 # Session expired
# #                 self.timer_label.set_text('00:00')
# #                 self.timer_label.classes('text-red-600', remove='text-gray-800 text-orange-600')
# #                 ui.notify('Session expired. Please login again.', type='warning')
# #                 ui.run_javascript('setTimeout(() => window.location.href = "/", 2000)')
# #                 return
            
# #             # Check if operation is running and time is low
# #             if self.current_operation and remaining <= 10 and not self.operation_paused:
# #                 self._pause_current_operation()
            
# #             # Update timer display
# #             minutes = int(remaining // 60)
# #             seconds = int(remaining % 60)
# #             timer_text = f'{minutes:02d}:{seconds:02d}'
# #             self.timer_label.set_text(timer_text)
            
# #             # Change color when time is low (white text on green background)
# #             if remaining <= 60:
# #                 self.timer_label.classes('text-red-100', remove='text-white text-orange-100')
# #             elif remaining <= 300:
# #                 self.timer_label.classes('text-orange-100', remove='text-white text-red-100')
# #             else:
# #                 self.timer_label.classes('text-white', remove='text-orange-100 text-red-100')
        
# #         # Use repeating timer (every 1 second)
# #         ui.timer(1.0, update_timer)
    
# #     def _start_auto_refresh_timers(self):
# #         """Start timers for auto-refreshing dashboard data"""
# #         # Note: These will only refresh if the respective panels have been created
# #         # Refresh intervals are configurable
        
# #         # Refresh monitoring metrics every 60 seconds
# #         def refresh_monitoring():
# #             try:
# #                 if hasattr(self, 'quality_metrics_container'):
# #                     self._refresh_monitoring_metrics()
# #             except Exception as e:
# #                 logger.error(f"Auto-refresh monitoring error: {e}")
        
# #         ui.timer(60.0, refresh_monitoring)
        
# #         # Refresh alerts every 90 seconds
# #         def refresh_alerts():
# #             try:
# #                 if hasattr(self, 'alerts_container'):
# #                     self._refresh_alerts()
# #             except Exception as e:
# #                 logger.error(f"Auto-refresh alerts error: {e}")
        
# #         ui.timer(90.0, refresh_alerts)
        
# #         # Refresh security logs every 120 seconds
# #         def refresh_security():
# #             try:
# #                 if hasattr(self, 'security_metrics_container'):
# #                     self._refresh_security_logs()
# #             except Exception as e:
# #                 logger.error(f"Auto-refresh security error: {e}")
        
# #         ui.timer(120.0, refresh_security)
        
# #         logger.info("Auto-refresh timers started: Monitoring (60s), Alerts (90s), Security (120s)")
    
# #     def _pause_current_operation(self):
# #         """Pause current content operation when timer is low"""
# #         if not self.operation_paused and self.current_operation:
# #             self.operation_paused = True
            
# #             # Save paused task
# #             paused_task = {
# #                 'id': len(self.paused_tasks) + 1,
# #                 'type': self.current_operation.get('type', 'Analysis'),
# #                 'content_preview': self.current_operation.get('content', '')[:50] + '...',
# #                 'paused_at': datetime.now(),
# #                 'status': 'Paused',
# #                 'progress': self.current_operation.get('progress', 0)
# #             }
# #             self.paused_tasks.append(paused_task)
            
# #             ui.notify('Operation paused due to low session time. Please extend session to continue.', type='warning')
            
# #             # Show resume dialog
# #             self._show_resume_dialog()
    
# #     def _show_resume_dialog(self):
# #         """Show dialog to resume paused operation"""
# #         with ui.dialog() as resume_dialog, ui.card().classes('w-96'):
# #             ui.label('Operation Paused').classes('text-xl font-bold mb-4')
# #             ui.label('Your session time is running low. Would you like to extend your session and resume?').classes('text-sm mb-4')
            
# #             with ui.row().classes('w-full justify-end gap-2'):
# #                 ui.button('Cancel', on_click=resume_dialog.close).props('flat')
# #                 ui.button(
# #                     'Extend & Resume',
# #                     on_click=lambda: self._extend_session(resume_dialog)
# #                 ).props('color=primary')
        
# #         resume_dialog.open()
    
# #     def _extend_session(self, dialog):
# #         """Extend session by 30 minutes"""
# #         self.session_start_time = datetime.now()
# #         self.operation_paused = False
# #         dialog.close()
# #         ui.notify('Session extended by 30 minutes', type='positive')
    
# #     def _toggle_theme_old(self):
        
# #         if self.dark_mode:
# #             ui.run_javascript('document.body.classList.add("dark-mode")')
# #             self.theme_toggle.props('icon=light_mode')
# #         else:
# #             ui.run_javascript('document.body.classList.remove("dark-mode")')
# #             self.theme_toggle.props('icon=dark_mode')
    
# #     def _show_profile_dialog(self):
# #         """Show user profile dialog with functional features"""
# #         # Get username from session
# #         username = app.storage.general.get('username', 'demo')
        
# #         with ui.dialog() as profile_dialog, ui.card().classes('w-[500px]'):
# #             with ui.row().classes('w-full items-center mb-4'):
# #                 ui.icon('account_circle', size='xl').classes('text-amber-900')
# #                 ui.label(self.t('user_profile')).classes('text-2xl font-bold ml-2')
            
# #             ui.separator()
            
# #             with ui.column().classes('w-full gap-4 mt-4'):
# #                 # Username
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('person').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('username')).classes('text-sm text-gray-600')
# #                         ui.label(username).classes('text-lg font-semibold')
                
# #                 # Email
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('email').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('email')).classes('text-sm text-gray-600')
# #                         ui.label(f'{username}@ashoka.ai').classes('text-lg font-semibold')
                
# #                 # Role
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('badge').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('role')).classes('text-sm text-gray-600')
# #                         ui.label('Content Creator').classes('text-lg font-semibold')
                
# #                 # Member Since
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('calendar_today').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('member_since')).classes('text-sm text-gray-600')
# #                         ui.label('February 2026').classes('text-lg font-semibold')
                
# #                 ui.separator().classes('my-3')
                
# #                 # Session Info
# #                 ui.label('Session Information').classes('text-md font-semibold mb-2')
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('access_time').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label('Session Started').classes('text-sm text-gray-600')
# #                         ui.label(self.session_start_time.strftime('%I:%M %p')).classes('text-md')
                
# #                 # Activity Stats
# #                 ui.separator().classes('my-3')
# #                 ui.label('Activity Statistics').classes('text-md font-semibold mb-2')
# #                 with ui.grid(columns=2).classes('w-full gap-3'):
# #                     with ui.card().classes('p-3 text-center'):
# #                         ui.label('Content Analyzed').classes('text-xs text-gray-600')
# #                         ui.label('24').classes('text-2xl font-bold text-blue-600')
# #                     with ui.card().classes('p-3 text-center'):
# #                         ui.label('Transformations').classes('text-xs text-gray-600')
# #                         ui.label('18').classes('text-2xl font-bold text-purple-600')
# #                     with ui.card().classes('p-3 text-center'):
# #                         ui.label('Paused Tasks').classes('text-xs text-gray-600')
# #                         ui.label(str(len(self.paused_tasks))).classes('text-2xl font-bold text-orange-600')
# #                     with ui.card().classes('p-3 text-center'):
# #                         ui.label('Alerts Viewed').classes('text-xs text-gray-600')
# #                         ui.label('12').classes('text-2xl font-bold text-green-600')
            
# #             ui.separator().classes('mt-4')
            
# #             with ui.row().classes('w-full justify-end mt-4'):
# #                 ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
# #         profile_dialog.open()
    
# #     def _show_settings_dialog_old(self):
# #         """Show user profile dialog"""
# #         with ui.dialog() as profile_dialog, ui.card().classes('w-96'):
# #             with ui.row().classes('w-full items-center mb-4'):
# #                 ui.icon('account_circle', size='xl').classes('text-amber-900')
# #                 ui.label(self.t('user_profile')).classes('text-2xl font-bold ml-2')
            
# #             ui.separator()
            
# #             with ui.column().classes('w-full gap-4 mt-4'):
# #                 # Username
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('person').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('username')).classes('text-sm text-gray-600')
# #                         ui.label('demo').classes('text-lg font-semibold')
                
# #                 # Email
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('email').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('email')).classes('text-sm text-gray-600')
# #                         ui.label('demo@ashoka.ai').classes('text-lg font-semibold')
                
# #                 # Role
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('badge').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('role')).classes('text-sm text-gray-600')
# #                         ui.label('Content Creator').classes('text-lg font-semibold')
                
# #                 # Member Since
# #                 with ui.row().classes('w-full items-center'):
# #                     ui.icon('calendar_today').classes('text-gray-600')
# #                     with ui.column().classes('ml-3'):
# #                         ui.label(self.t('member_since')).classes('text-sm text-gray-600')
# #                         ui.label('February 2026').classes('text-lg font-semibold')
            
# #             ui.separator().classes('mt-4')
            
# #             with ui.row().classes('w-full justify-end mt-4'):
# #                 ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
# #         profile_dialog.open()
    
# #     def _show_settings_dialog(self):
# #         """Show settings dialog with functional features"""
# #         with ui.dialog() as settings_dialog, ui.card().classes('w-[500px]'):
# #             with ui.row().classes('w-full items-center mb-4'):
# #                 ui.icon('settings', size='xl').classes('text-amber-900')
# #                 ui.label('Settings & Preferences').classes('text-2xl font-bold ml-2')
            
# #             ui.separator()
            
# #             with ui.column().classes('w-full gap-4 mt-4'):
# #                 # Language Settings
# #                 ui.label('Language').classes('text-lg font-semibold')
# #                 language_select = ui.select(
# #                     ['English', 'Hindi', 'Kannada', 'Tamil'],
# #                     value=self.current_language,
# #                     label='Select Language'
# #                 ).classes('w-full')
                
# #                 ui.separator().classes('my-3')
                
# #                 # Notification Settings
# #                 ui.label('Notifications').classes('text-lg font-semibold')
# #                 notif_enabled = ui.checkbox(
# #                     'Enable notifications',
# #                     value=self.user_preferences.get('notifications', True)
# #                 )
# #                 email_alerts = ui.checkbox(
# #                     'Email alerts for critical issues',
# #                     value=self.user_preferences.get('email_alerts', False)
# #                 )
                
# #                 ui.separator().classes('my-3')
                
# #                 # Auto-save Settings
# #                 ui.label('Content Management').classes('text-lg font-semibold')
# #                 auto_save = ui.checkbox(
# #                     'Auto-save content drafts',
# #                     value=self.user_preferences.get('auto_save', True)
# #                 )
                
# #                 ui.separator().classes('my-3')
                
# #                 # Session Settings
# #                 ui.label('Session').classes('text-lg font-semibold')
# #                 session_timeout = ui.select(
# #                     [15, 30, 60, 120],
# #                     value=self.user_preferences.get('session_timeout', 30),
# #                     label='Session timeout (minutes)'
# #                 ).classes('w-full')
                
# #                 ui.separator().classes('my-3')
                
# #                 # Paused Tasks
# #                 ui.label('Paused Tasks').classes('text-lg font-semibold')
# #                 ui.label(f'You have {len(self.paused_tasks)} paused tasks').classes('text-sm text-gray-600')
# #                 if self.paused_tasks:
# #                     ui.button(
# #                         'View Paused Tasks',
# #                         icon='pause_circle',
# #                         on_click=lambda: self._show_paused_tasks_dialog()
# #                     ).props('flat color=primary').classes('w-full')
            
# #             ui.separator().classes('mt-4')
            
# #             with ui.row().classes('w-full justify-end gap-2 mt-4'):
# #                 ui.button('Cancel', on_click=settings_dialog.close).props('flat')
# #                 ui.button(
# #                     'Save Settings',
# #                     on_click=lambda: self._save_settings(
# #                         language_select.value,
# #                         notif_enabled.value,
# #                         email_alerts.value,
# #                         auto_save.value,
# #                         session_timeout.value,
# #                         settings_dialog
# #                     )
# #                 ).props('color=primary')
        
# #         settings_dialog.open()
    
# #     def _save_settings(self, language, notifications, email_alerts, auto_save, session_timeout, dialog):
# #         """Save user settings"""
# #         # Update preferences
# #         self.user_preferences['notifications'] = notifications
# #         self.user_preferences['email_alerts'] = email_alerts
# #         self.user_preferences['auto_save'] = auto_save
# #         self.user_preferences['session_timeout'] = session_timeout
        
# #         # Update session duration if changed
# #         if session_timeout != self.session_duration // 60:
# #             self.session_duration = session_timeout * 60
# #             self.session_start_time = datetime.now()
        
# #         # Change language if different
# #         if language != self.current_language:
# #             self._change_language(language, dialog)
# #         else:
# #             ui.notify('Settings saved successfully', type='positive')
# #             dialog.close()
    
# #     def _show_paused_tasks_dialog(self):
# #         """Show paused tasks with date filters"""
# #         with ui.dialog() as tasks_dialog, ui.card().classes('w-[800px]'):
# #             with ui.row().classes('w-full items-center justify-between mb-4'):
# #                 ui.label('Paused Content Tasks').classes('text-2xl font-bold')
# #                 ui.button(icon='close', on_click=tasks_dialog.close).props('flat round')
            
# #             ui.separator()
            
# #             # Date filter
# #             with ui.row().classes('w-full items-center gap-2 my-4'):
# #                 ui.label('Filter:').classes('font-medium')
# #                 date_filter = ui.select(
# #                     ['Last Week', 'Last 15 Days', 'Last 30 Days', 'Last 3 Months', 'Last 6 Months', 'Last Year'],
# #                     value='Last 30 Days',
# #                     label='Time Period'
# #                 ).classes('w-48')
# #                 ui.button(
# #                     'Apply Filter',
# #                     icon='filter_list',
# #                     on_click=lambda: self._filter_paused_tasks(date_filter.value, tasks_container)
# #                 ).props('flat')
            
# #             # Tasks table
# #             tasks_container = ui.column().classes('w-full')
# #             self._display_paused_tasks(tasks_container, 'Last 30 Days')
        
# #         tasks_dialog.open()
    
# #     def _filter_paused_tasks(self, filter_value, container):
# #         """Filter paused tasks by date range"""
# #         self._display_paused_tasks(container, filter_value)
# #         ui.notify(f'Filtered by: {filter_value}', type='info')
    
# #     def _display_paused_tasks(self, container, filter_value):
# #         """Display paused tasks table"""
# #         container.clear()
        
# #         # Calculate date range
# #         now = datetime.now()
# #         if filter_value == 'Last Week':
# #             cutoff = now - timedelta(days=7)
# #         elif filter_value == 'Last 15 Days':
# #             cutoff = now - timedelta(days=15)
# #         elif filter_value == 'Last 30 Days':
# #             cutoff = now - timedelta(days=30)
# #         elif filter_value == 'Last 3 Months':
# #             cutoff = now - timedelta(days=90)
# #         elif filter_value == 'Last 6 Months':
# #             cutoff = now - timedelta(days=180)
# #         else:  # Last Year
# #             cutoff = now - timedelta(days=365)
        
# #         # Filter tasks
# #         filtered_tasks = [t for t in self.paused_tasks if t['paused_at'] >= cutoff]
        
# #         with container:
# #             if not filtered_tasks:
# #                 ui.label('No paused tasks in this time period').classes('text-gray-500 text-center py-8')
# #             else:
# #                 # Table header - Lightish blue background
# #                 with ui.row().classes('w-full table-header-blue p-3 font-semibold rounded-t'):
# #                     ui.label('ID').classes('w-16')
# #                     ui.label('Type').classes('w-32')
# #                     ui.label('Content Preview').classes('flex-1')
# #                     ui.label('Paused At').classes('w-40')
# #                     ui.label('Progress').classes('w-24')
# #                     ui.label('Actions').classes('w-32')
                
# #                 # Table rows
# #                 for task in filtered_tasks:
# #                     with ui.row().classes('w-full p-3 border-b items-center'):
# #                         ui.label(f"#{task['id']}").classes('w-16')
# #                         ui.badge(task['type'], color='blue').classes('w-32')
# #                         ui.label(task['content_preview']).classes('flex-1 text-sm')
# #                         ui.label(task['paused_at'].strftime('%Y-%m-%d %H:%M')).classes('w-40 text-sm')
# #                         ui.label(f"{task['progress']}%").classes('w-24')
# #                         ui.button(
# #                             'Resume',
# #                             icon='play_arrow',
# #                             on_click=lambda t=task: self._resume_task(t)
# #                         ).props('flat dense color=green')
    
# #     def _resume_task(self, task):
# #         """Resume a paused task"""
# #         # Remove from paused tasks
# #         self.paused_tasks = [t for t in self.paused_tasks if t['id'] != task['id']]
        
# #         # Reset operation state
# #         self.operation_paused = False
# #         self.current_operation = None
        
# #         ui.notify(f"Task #{task['id']} resumed", type='positive')
    
# #     def _change_language(self, language: str, dialog):
# #         """Change platform language"""
# #         self.current_language = language
        
# #         # Store language preference in general storage (doesn't require secret)
# #         app.storage.general['language'] = language
        
# #         ui.notify(f'Language changed to {language}. Refreshing...', type='positive')
# #         dialog.close()
        
# #         # Reload the page to apply translations
# #         ui.run_javascript('window.location.reload()')
    
# #     def _create_overview_panel(self):
# #         """Create overview dashboard panel with real metrics from database"""
# #         ui.label(self.t('platform_overview')).classes('text-3xl font-bold mb-4')
        
# #         # Fetch real metrics from database
# #         metrics = self._get_dashboard_metrics()
        
# #         # Paused Tasks Summary (if any)
# #         if self.paused_tasks:
# #             with ui.card().classes('w-full bg-orange-50 mb-4'):
# #                 with ui.row().classes('w-full items-center justify-between'):
# #                     with ui.row().classes('items-center gap-3'):
# #                         ui.icon('pause_circle', size='lg').classes('text-orange-600')
# #                         with ui.column():
# #                             ui.label(f'{len(self.paused_tasks)} Paused Tasks').classes('text-lg font-semibold')
# #                             ui.label('Resume your work from where you left off').classes('text-sm text-gray-600')
# #                     ui.button(
# #                         'View Tasks',
# #                         icon='arrow_forward',
# #                         on_click=self._show_paused_tasks_dialog
# #                     ).props('flat color=orange')
        
# #         # Key Metrics Row - Real data from database
# #         with ui.row().classes('w-full gap-4 mb-6'):
# #             self._create_metric_card(
# #                 self.t('total_content'), 
# #                 str(metrics['total_content']), 
# #                 'description', 
# #                 'text-blue-600', 
# #                 f"+{metrics['content_this_week']} {self.t('this_week')}"
# #             )
# #             self._create_metric_card(
# #                 self.t('quality_score'), 
# #                 f"{metrics['avg_quality']:.1f}%", 
# #                 'verified', 
# #                 'text-green-600', 
# #                 self.t('excellent') if metrics['avg_quality'] >= 85 else 'Good'
# #             )
# #             self._create_metric_card(
# #                 self.t('risk_alerts'), 
# #                 str(metrics['risk_alerts']), 
# #                 'warning', 
# #                 'text-orange-600', 
# #                 f"{metrics['resolved_risks']} {self.t('resolved')}"
# #             )
# #             self._create_metric_card(
# #                 self.t('ai_operations'), 
# #                 str(metrics['ai_operations']), 
# #                 'smart_toy', 
# #                 'text-purple-600', 
# #                 f"{metrics['success_rate']:.1f}% {self.t('success')}"
# #             )
        
# #         # Charts Row
# #         with ui.row().classes('w-full gap-4 mb-6'):
# #             # Content Processing Trend Chart - Real data
# #             with ui.card().classes('flex-1'):
# #                 ui.label('Content Processing Trend').classes('text-xl font-semibold mb-4')
                
# #                 trend_data = metrics['content_trend']
# #                 max_value = max(val for _, val in trend_data) if trend_data else 1
                
# #                 with ui.column().classes('w-full gap-2'):
# #                     for label, value in trend_data:
# #                         with ui.row().classes('w-full items-center gap-3'):
# #                             ui.label(label).classes('w-16 text-xs font-medium')
# #                             bar_width = (value / max_value * 100) if max_value > 0 else 0
# #                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
# #                                 with ui.element('div').classes('bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded').style(f'width: {bar_width}%'):
# #                                     pass
# #                             ui.label(str(value)).classes('w-12 text-xs font-bold text-purple-600')
            
# #             # Sentiment Distribution - Real data
# #             with ui.card().classes('flex-1'):
# #                 ui.label('Sentiment Distribution').classes('text-xl font-semibold mb-4')
                
# #                 sentiment_data = metrics['sentiment_distribution']
                
# #                 with ui.column().classes('w-full gap-3'):
# #                     for label, percentage, color in sentiment_data:
# #                         with ui.column().classes('w-full gap-1'):
# #                             with ui.row().classes('w-full items-center justify-between'):
# #                                 ui.label(label).classes('text-xs font-medium')
# #                                 ui.label(f'{percentage}%').classes(f'text-xs font-bold text-{color}-600')
# #                             ui.linear_progress(percentage / 100).props(f'color={color}').classes('h-2')
        
# #         with ui.row().classes('w-full gap-4'):
# #             # Recent Activity - Real data
# #             with ui.card().classes('flex-1'):
# #                 ui.label(self.t('recent_activity')).classes('text-xl font-semibold mb-4')
# #                 with ui.column().classes('gap-2'):
# #                     for activity in metrics['recent_activities']:
# #                         self._create_activity_item(
# #                             activity['title'],
# #                             activity['description'],
# #                             activity['time'],
# #                             activity['icon'],
# #                             activity['color']
# #                         )
            
# #             # System Health
# #             with ui.card().classes('flex-1'):
# #                 ui.label(self.t('system_health')).classes('text-xl font-semibold mb-4')
                
# #                 ui.label(self.t('ai_model_performance')).classes('text-sm text-gray-600 mb-2')
# #                 ui.linear_progress(0.95).classes('mb-4').props('color=green')
                
# #                 ui.label(self.t('content_processing_rate')).classes('text-sm text-gray-600 mb-2')
# #                 ui.linear_progress(metrics['processing_rate']).classes('mb-4').props('color=blue')
                
# #                 ui.label(self.t('storage_utilization')).classes('text-sm text-gray-600 mb-2')
# #                 ui.linear_progress(metrics['storage_utilization']).classes('mb-4').props('color=orange')
                
# #                 with ui.row().classes('gap-2 mt-4'):
# #                     ui.badge(self.t('api_healthy'), color='green')
# #                     ui.badge(self.t('database_healthy'), color='green')
# #                     ui.badge(self.t('ai_healthy'), color='green')
    
# #     def _get_dashboard_metrics(self):
# #         """Fetch real metrics from database"""
# #         if not db_schema.conn:
# #             db_schema.connect()
        
# #         try:
# #             # Total content count
# #             total_content = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint
# #             """).fetchone()[0]
            
# #             # Content this week
# #             content_this_week = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint
# #                 WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
# #             """).fetchone()[0]
            
# #             # Average quality (based on sentiment confidence)
# #             avg_quality_result = db_schema.conn.execute("""
# #                 SELECT AVG(sentiment_confidence * 100) FROM ashoka_contentint
# #                 WHERE sentiment_confidence IS NOT NULL
# #             """).fetchone()[0]
# #             avg_quality = avg_quality_result if avg_quality_result else 85.0
            
# #             # Risk alerts (negative sentiment content)
# #             risk_alerts = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint
# #                 WHERE sentiment = 'negative'
# #             """).fetchone()[0]
            
# #             # Resolved risks (assuming older negative content is resolved)
# #             resolved_risks = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint
# #                 WHERE sentiment = 'negative' 
# #                 AND created_at < CURRENT_DATE - INTERVAL '7 days'
# #             """).fetchone()[0]
            
# #             # AI operations (total analyses)
# #             ai_operations = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint
# #                 WHERE analyzed_at IS NOT NULL
# #             """).fetchone()[0]
            
# #             # Success rate (content with analysis)
# #             success_rate = (ai_operations / total_content * 100) if total_content > 0 else 100.0
            
# #             # Content trend (last 5 weeks)
# #             trend_data = []
# #             for i in range(4, -1, -1):
# #                 week_start = f"CURRENT_DATE - INTERVAL '{i*7 + 7} days'"
# #                 week_end = f"CURRENT_DATE - INTERVAL '{i*7} days'"
# #                 count = db_schema.conn.execute(f"""
# #                     SELECT COUNT(*) FROM ashoka_contentint
# #                     WHERE created_at >= {week_start} AND created_at < {week_end}
# #                 """).fetchone()[0]
# #                 trend_data.append((f'Week {5-i}', count))
            
# #             # Sentiment distribution
# #             positive_count = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'positive'
# #             """).fetchone()[0]
# #             neutral_count = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'neutral'
# #             """).fetchone()[0]
# #             negative_count = db_schema.conn.execute("""
# #                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'negative'
# #             """).fetchone()[0]
            
# #             total_sentiment = positive_count + neutral_count + negative_count
# #             if total_sentiment > 0:
# #                 sentiment_distribution = [
# #                     ('Positive', int(positive_count / total_sentiment * 100), 'green'),
# #                     ('Neutral', int(neutral_count / total_sentiment * 100), 'blue'),
# #                     ('Negative', int(negative_count / total_sentiment * 100), 'red')
# #                 ]
# #             else:
# #                 sentiment_distribution = [
# #                     ('Positive', 33, 'green'),
# #                     ('Neutral', 34, 'blue'),
# #                     ('Negative', 33, 'red')
# #                 ]
            
# #             # Recent activities (last 5)
# #             recent_activities = []
# #             recent_content = db_schema.conn.execute("""
# #                 SELECT content_type, sentiment, created_at, content_text
# #                 FROM ashoka_contentint
# #                 ORDER BY created_at DESC
# #                 LIMIT 5
# #             """).fetchall()
            
# #             for content_type, sentiment, created_at, content_text in recent_content:
# #                 time_diff = datetime.now() - created_at
# #                 if time_diff.total_seconds() < 3600:
# #                     time_str = f"{int(time_diff.total_seconds() / 60)} min ago"
# #                 elif time_diff.total_seconds() < 86400:
# #                     time_str = f"{int(time_diff.total_seconds() / 3600)} hour ago"
# #                 else:
# #                     time_str = f"{int(time_diff.days)} days ago"
                
# #                 preview = content_text[:50] + '...' if content_text and len(content_text) > 50 else content_text or 'No content'
                
# #                 if sentiment == 'negative':
# #                     icon, color = 'warning', 'text-red-500'
# #                     title = 'Risk detected'
# #                 elif sentiment == 'positive':
# #                     icon, color = 'check_circle', 'text-green-500'
# #                     title = 'Content analyzed'
# #                 else:
# #                     icon, color = 'info', 'text-blue-500'
# #                     title = 'Content processed'
                
# #                 recent_activities.append({
# #                     'title': title,
# #                     'description': preview,
# #                     'time': time_str,
# #                     'icon': icon,
# #                     'color': color
# #                 })
            
# #             # If no activities, show placeholder
# #             if not recent_activities:
# #                 recent_activities = [{
# #                     'title': 'No recent activity',
# #                     'description': 'Start analyzing content to see activity',
# #                     'time': 'Now',
# #                     'icon': 'info',
# #                     'color': 'text-gray-500'
# #                 }]
            
# #             # Processing rate (based on content with analysis)
# #             processing_rate = success_rate / 100
            
# #             # Storage utilization (estimate based on file sizes)
# #             storage_result = db_schema.conn.execute("""
# #                 SELECT SUM(file_size_mb) FROM ashoka_contentint
# #                 WHERE file_size_mb IS NOT NULL
# #             """).fetchone()[0]
# #             storage_mb = storage_result if storage_result else 0
# #             storage_utilization = min(storage_mb / 1000, 0.95)  # Assume 1GB limit
            
# #             return {
# #                 'total_content': total_content,
# #                 'content_this_week': content_this_week,
# #                 'avg_quality': avg_quality,
# #                 'risk_alerts': risk_alerts,
# #                 'resolved_risks': resolved_risks,
# #                 'ai_operations': ai_operations,
# #                 'success_rate': success_rate,
# #                 'content_trend': trend_data,
# #                 'sentiment_distribution': sentiment_distribution,
# #                 'recent_activities': recent_activities,
# #                 'processing_rate': processing_rate,
# #                 'storage_utilization': storage_utilization
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error fetching dashboard metrics: {e}")
# #             # Return default values on error
# #             return {
# #                 'total_content': 0,
# #                 'content_this_week': 0,
# #                 'avg_quality': 85.0,
# #                 'risk_alerts': 0,
# #                 'resolved_risks': 0,
# #                 'ai_operations': 0,
# #                 'success_rate': 100.0,
# #                 'content_trend': [(f'Week {i}', 0) for i in range(1, 6)],
# #                 'sentiment_distribution': [
# #                     ('Positive', 33, 'green'),
# #                     ('Neutral', 34, 'blue'),
# #                     ('Negative', 33, 'red')
# #                 ],
# #                 'recent_activities': [{
# #                     'title': 'No recent activity',
# #                     'description': 'Start analyzing content to see activity',
# #                     'time': 'Now',
# #                     'icon': 'info',
# #                     'color': 'text-gray-500'
# #                 }],
# #                 'processing_rate': 0.78,
# #                 'storage_utilization': 0.10
# #             }
    
# #     def _create_content_intelligence_panel(self):
# #         """Create content intelligence panel"""
# #         ui.label('Content Intelligence & Analysis').classes('text-3xl font-bold mb-4')
        
# #         with ui.row().classes('w-full gap-4'):
# #             # Input Section
# #             with ui.card().classes('flex-1'):
# #                 ui.label('Submit Content for Analysis').classes('text-xl font-semibold mb-4')
                
# #                 # Tab selector for input type with modern icons
# #                 with ui.tabs().classes('w-full') as input_tabs:
# #                     text_tab = ui.tab('TEXT', icon='article')
# #                     image_tab = ui.tab('IMAGE', icon='photo')
# #                     video_tab = ui.tab('VIDEO', icon='movie')
# #                     document_tab = ui.tab('DOCUMENT', icon='description')
                
# #                 with ui.tab_panels(input_tabs, value=text_tab).classes('w-full'):
# #                     # Text input panel
# #                     with ui.tab_panel(text_tab):
# #                         self.content_input = ui.textarea(
# #                             label='Enter your content',
# #                             placeholder='Paste your content here for AI-powered analysis...'
# #                         ).classes('w-full').props('rows=10')
                        
# #                         with ui.row().classes('gap-2 mt-4'):
# #                             ui.button(
# #                                 'Analyze Text',
# #                                 icon='psychology',
# #                                 on_click=lambda: self._analyze_content(self.content_input.value)
# #                             ).props('color=primary')
# #                             ui.button('Clear', icon='clear', on_click=lambda: self.content_input.set_value('')).props('flat')
                    
# #                     # Image upload panel
# #                     with ui.tab_panel(image_tab):
# #                         ui.label('Upload an image to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                        
# #                         # Image preview container
# #                         self.image_preview_container = ui.column().classes('w-full mb-4')
                        
# #                         # Upload button
# #                         ui.upload(
# #                             label='Choose Image',
# #                             on_upload=self._handle_image_upload,
# #                             auto_upload=True
# #                         ).props('accept="image/*"').classes('w-full')
                        
# #                         ui.label('Supported formats: JPG, PNG, GIF, WEBP').classes('text-xs text-gray-500 mt-2')
                    
# #                     # Video upload panel
# #                     with ui.tab_panel(video_tab):
# #                         ui.label('Upload a video to extract transcription and analyze content').classes('text-sm text-gray-600 mb-3')
                        
# #                         # Video preview container
# #                         self.video_preview_container = ui.column().classes('w-full mb-4')
                        
# #                         # Upload button
# #                         ui.upload(
# #                             label='Choose Video',
# #                             on_upload=self._handle_video_upload,
# #                             auto_upload=True
# #                         ).props('accept="video/*"').classes('w-full')
                        
# #                         ui.label('Supported formats: MP4, MOV, AVI, WEBM').classes('text-xs text-gray-500 mt-2')
                    
# #                     # Document upload panel
# #                     with ui.tab_panel(document_tab):
# #                         ui.label('Upload a document to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                        
# #                         # Document preview container
# #                         self.document_preview_container = ui.column().classes('w-full mb-4')
                        
# #                         # Upload button
# #                         ui.upload(
# #                             label='Choose Document',
# #                             on_upload=self._handle_document_upload,
# #                             auto_upload=True
# #                         ).props('accept=".pdf,.docx,.txt,.md"').classes('w-full')
                        
# #                         ui.label('Supported formats: PDF, DOCX, TXT, MD').classes('text-xs text-gray-500 mt-2')
            
# #             # Analysis Results
# #             with ui.card().classes('flex-1'):
# #                 ui.label('Analysis Results').classes('text-xl font-semibold mb-4')
                
# #                 self.analysis_container = ui.column().classes('w-full gap-3')
# #                 with self.analysis_container:
# #                     ui.label('Submit content to see analysis results').classes('text-gray-500 text-center py-8')
        
# #         # AI Content Generator Section (moved here - right after Submit Content)
# #         with ui.card().classes('w-full mt-4'):
# #             ui.label('AI Content Generator').classes('text-2xl font-bold mb-4')
# #             ui.label('Generate text, notes, or images using AI prompts').classes('text-sm text-gray-600 mb-4')
            
# #             with ui.row().classes('w-full gap-4'):
# #                 # Input Section
# #                 with ui.card().classes('flex-1'):
# #                     ui.label('Enter Your Prompt').classes('text-lg font-semibold mb-3')
                    
# #                     # Generation type selector
# #                     with ui.row().classes('items-center gap-4 mb-3'):
# #                         ui.label('Generate:').classes('text-sm font-medium')
# #                         self.gen_type = ui.radio(['Text/Notes', 'Image'], value='Text/Notes').props('inline')
                    
# #                     # Prompt input
# #                     self.generator_prompt = ui.textarea(
# #                         label='Describe what you want to generate',
# #                         placeholder='Example: Write a professional email about project updates...'
# #                     ).classes('w-full').props('rows=6')
                    
# #                     # Generate button
# #                     ui.button(
# #                         'Generate Content',
# #                         icon='auto_awesome',
# #                         on_click=self._generate_ai_content
# #                     ).props('color=primary').classes('w-full mt-3')
                
# #                 # Output Section
# #                 with ui.card().classes('flex-1'):
# #                     ui.label('Generated Content').classes('text-lg font-semibold mb-3')
                    
# #                     self.generator_output_container = ui.column().classes('w-full')
# #                     with self.generator_output_container:
# #                         ui.label('Generated content will appear here').classes('text-gray-500 text-center py-8')
        
# #         # Analysis & Generator History Section (renamed and combined - at the bottom)
# #         with ui.card().classes('w-full mt-4'):
# #             with ui.row().classes('items-center justify-between mb-4'):
# #                 ui.label('Analysis & Generator History').classes('text-xl font-semibold')
# #                 ui.label('History of analyzed and generated content - Click any row to preview').classes('text-sm text-gray-500')
            
# #             self.history_table_container = ui.column().classes('w-full')
# #             # Load initial history from database
# #             self._update_history_table()
    
# #     def _create_transform_panel(self):
# #         """Create content transformation panel"""
# #         ui.label('Multi-Platform Content Transformer').classes('text-3xl font-bold mb-4')
        
# #         with ui.row().classes('w-full gap-4'):
# #             # Input & Configuration Section
# #             with ui.card().classes('w-2/5'):
# #                 ui.label('Content & Settings').classes('text-xl font-semibold mb-4')
                
# #                 # Content input
# #                 ui.label('Original Content').classes('text-sm font-medium mb-2')
# #                 self.transform_input = ui.textarea(
# #                     label='Enter content to transform',
# #                     placeholder='Paste your content here to transform it for multiple platforms...'
# #                 ).classes('w-full').props('rows=8')
                
# #                 ui.separator().classes('my-4')
                
# #                 # Platform selection
# #                 ui.label('Select Platforms').classes('text-sm font-medium mb-2')
# #                 self.platform_linkedin = ui.checkbox('LinkedIn', value=True)
# #                 self.platform_twitter = ui.checkbox('Twitter/X', value=True)
# #                 self.platform_instagram = ui.checkbox('Instagram', value=False)
# #                 self.platform_facebook = ui.checkbox('Facebook', value=False)
# #                 self.platform_threads = ui.checkbox('Threads', value=False)
                
# #                 ui.separator().classes('my-4')
                
# #                 # Tone selection
# #                 ui.label('Tone').classes('text-sm font-medium mb-2')
# #                 self.tone_selector = ui.radio(
# #                     ['Professional', 'Casual', 'Storytelling'],
# #                     value='Professional'
# #                 ).props('inline')
                
# #                 ui.separator().classes('my-4')
                
# #                 # Hashtag option
# #                 self.include_hashtags = ui.checkbox('Include Hashtags', value=True)
                
# #                 # Transform button
# #                 ui.button(
# #                     'Transform Content',
# #                     icon='transform',
# #                     on_click=self._transform_content
# #                 ).props('color=primary').classes('w-full mt-4')
            
# #             # Output Preview Section
# #             with ui.card().classes('flex-1'):
# #                 ui.label('Platform Outputs').classes('text-xl font-semibold mb-4')
                
# #                 self.transform_results_container = ui.column().classes('w-full gap-2')
# #                 with self.transform_results_container:
# #                     ui.label('Configure settings and click "Transform Content" to see results').classes('text-gray-500 text-center py-8')
        
# #         # Transform History Section
# #         with ui.card().classes('w-full mt-4'):
# #             ui.label('Transform History').classes('text-xl font-semibold mb-4')
# #             ui.label('Click any row to load that transformation').classes('text-sm text-gray-600 mb-2')
            
# #             self.transform_history_container = ui.column().classes('w-full')
# #             self._update_transform_history()
    
# #     def _create_monitoring_panel(self):
# #         """Create monitoring dashboard panel"""
# #         from src.services.monitoring_service import monitoring_service
        
# #         with ui.column().classes('w-full gap-4'):
# #             # Header with refresh button
# #             with ui.row().classes('w-full items-center justify-between mb-2'):
# #                 ui.label('Quality, Risk & Operations Monitoring').classes('text-3xl font-bold')
# #                 ui.button(
# #                     'Refresh Metrics',
# #                     icon='refresh',
# #                     on_click=self._refresh_monitoring_metrics
# #                 ).props('flat color=primary')
            
# #             # Performance Trend Chart
# #             with ui.card().classes('w-full'):
# #                 ui.label('Performance Trends (Last 24 Hours)').classes('text-xl font-semibold mb-4')
                
# #                 # Mock hourly performance data
# #                 hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00']
# #                 success_rates = [98.5, 97.8, 99.2, 98.9, 99.5, 98.3, 99.1]
# #                 max_rate = 100
                
# #                 with ui.column().classes('w-full gap-2'):
# #                     for hour, rate in zip(hours, success_rates):
# #                         with ui.row().classes('w-full items-center gap-3'):
# #                             ui.label(hour).classes('w-12 text-xs font-medium')
# #                             bar_width = (rate / max_rate * 100)
# #                             color = 'green' if rate >= 98 else 'orange' if rate >= 95 else 'red'
# #                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
# #                                 with ui.element('div').classes(f'bg-{color}-500 h-full rounded').style(f'width: {bar_width}%'):
# #                                     pass
# #                             ui.label(f'{rate}%').classes(f'w-12 text-xs font-bold text-{color}-600')
            
# #             # Quality Metrics
# #             with ui.card().classes('w-full'):
# #                 ui.label('Quality Metrics').classes('text-xl font-semibold mb-4')
# #                 self.quality_metrics_container = ui.row().classes('w-full gap-4')
            
# #             # Risk Assessment
# #             with ui.card().classes('w-full'):
# #                 ui.label('Risk & Safety Assessment').classes('text-xl font-semibold mb-4')
# #                 self.risk_metrics_container = ui.row().classes('w-full gap-4')
            
# #             # Operations Metrics
# #             with ui.card().classes('w-full'):
# #                 ui.label('AI Operations Performance').classes('text-xl font-semibold mb-4')
# #                 self.operations_metrics_container = ui.row().classes('w-full gap-4')
            
# #             # System Health
# #             with ui.card().classes('w-full'):
# #                 ui.label('System Health').classes('text-xl font-semibold mb-4')
# #                 self.system_health_container = ui.column().classes('w-full gap-3')
        
# #         # Load initial metrics
# #         self._refresh_monitoring_metrics()
    
# #     def _refresh_monitoring_metrics(self):
# #         """Refresh all monitoring metrics"""
# #         from src.services.monitoring_service import monitoring_service
        
# #         try:
# #             # Get metrics
# #             quality = monitoring_service.get_quality_metrics()
# #             risk = monitoring_service.get_risk_metrics()
# #             ops = monitoring_service.get_operations_metrics()
# #             health = monitoring_service.get_system_health()
            
# #             # Update Quality Metrics
# #             self.quality_metrics_container.clear()
# #             with self.quality_metrics_container:
# #                 # Readability
# #                 risk_class = 'risk-low' if quality.readability_score > 75 else 'risk-medium' if quality.readability_score > 60 else 'risk-high'
# #                 color = 'green' if quality.readability_score > 75 else 'orange' if quality.readability_score > 60 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Readability Score').classes('text-sm text-gray-600')
# #                     ui.label(f'{quality.readability_score:.1f}').classes(f'text-3xl font-bold text-{color}-600')
# #                     change_icon = '↑' if quality.readability_change > 0 else '↓'
# #                     ui.label(f'{change_icon} {abs(quality.readability_change):.1f} from baseline').classes(f'text-xs text-{color}-600')
                
# #                 # Tone Consistency
# #                 risk_class = 'risk-low' if quality.tone_consistency > 85 else 'risk-medium'
# #                 color = 'green' if quality.tone_consistency > 85 else 'orange'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Tone Consistency').classes('text-sm text-gray-600')
# #                     ui.label(f'{quality.tone_consistency:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(quality.tone_status).classes(f'text-xs text-{color}-600')
                
# #                 # Duplicate Detection
# #                 risk_class = 'risk-low' if quality.duplicate_count == 0 else 'risk-medium' if quality.duplicate_count < 3 else 'risk-high'
# #                 color = 'green' if quality.duplicate_count == 0 else 'orange' if quality.duplicate_count < 3 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Duplicate Detection').classes('text-sm text-gray-600')
# #                     ui.label(str(quality.duplicate_count)).classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(quality.duplicate_status).classes(f'text-xs text-{color}-600')
            
# #             # Update Risk Metrics
# #             self.risk_metrics_container.clear()
# #             with self.risk_metrics_container:
# #                 # Toxicity
# #                 risk_class = 'risk-low' if risk.toxicity_score < 0.2 else 'risk-medium' if risk.toxicity_score < 0.3 else 'risk-high'
# #                 color = 'green' if risk.toxicity_score < 0.2 else 'orange' if risk.toxicity_score < 0.3 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Toxicity Score').classes('text-sm text-gray-600')
# #                     ui.label(f'{risk.toxicity_score:.2f}').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(risk.toxicity_level).classes(f'text-xs text-{color}-600')
                
# #                 # Hate Speech
# #                 risk_class = 'risk-low' if risk.hate_speech_count == 0 else 'risk-high'
# #                 color = 'green' if risk.hate_speech_count == 0 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Hate Speech').classes('text-sm text-gray-600')
# #                     ui.label('None' if risk.hate_speech_count == 0 else str(risk.hate_speech_count)).classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(risk.hate_speech_status).classes(f'text-xs text-{color}-600')
                
# #                 # Backlash Risk
# #                 risk_class = 'risk-low' if risk.backlash_risk == 'Low' else 'risk-medium' if risk.backlash_risk == 'Medium' else 'risk-high'
# #                 color = 'green' if risk.backlash_risk == 'Low' else 'orange' if risk.backlash_risk == 'Medium' else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Backlash Risk').classes('text-sm text-gray-600')
# #                     ui.label(risk.backlash_risk).classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(risk.backlash_status).classes(f'text-xs text-{color}-600')
            
# #             # Update Operations Metrics
# #             self.operations_metrics_container.clear()
# #             with self.operations_metrics_container:
# #                 # Success Rate
# #                 risk_class = 'risk-low' if ops.success_rate > 95 else 'risk-medium' if ops.success_rate > 90 else 'risk-high'
# #                 color = 'green' if ops.success_rate > 95 else 'orange' if ops.success_rate > 90 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Success Rate').classes('text-sm text-gray-600')
# #                     ui.label(f'{ops.success_rate:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(f'{ops.total_operations:,} operations').classes('text-xs text-gray-600')
                
# #                 # Latency
# #                 risk_class = 'risk-low' if ops.avg_latency < 1.5 else 'risk-medium' if ops.avg_latency < 2.0 else 'risk-high'
# #                 color = 'green' if ops.avg_latency < 1.5 else 'orange' if ops.avg_latency < 2.0 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Avg Latency').classes('text-sm text-gray-600')
# #                     ui.label(f'{ops.avg_latency:.1f}s').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(ops.latency_status).classes(f'text-xs text-{color}-600')
                
# #                 # Quality Drift
# #                 risk_class = 'risk-low' if ops.quality_drift > 0 else 'risk-medium'
# #                 color = 'green' if ops.quality_drift > 0 else 'orange'
# #                 drift_sign = '+' if ops.quality_drift > 0 else ''
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Quality Drift').classes('text-sm text-gray-600')
# #                     ui.label(f'{drift_sign}{ops.quality_drift:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(ops.drift_status).classes(f'text-xs text-{color}-600')
            
# #             # Update System Health
# #             self.system_health_container.clear()
# #             with self.system_health_container:
# #                 ui.label('Component Status').classes('text-sm font-medium mb-2')
# #                 with ui.row().classes('gap-2 mb-4'):
# #                     api_color = 'green' if health.api_status == 'Healthy' else 'orange'
# #                     ui.badge(f'API: {health.api_status}', color=api_color)
                    
# #                     db_color = 'green' if health.database_status == 'Healthy' else 'orange'
# #                     ui.badge(f'Database: {health.database_status}', color=db_color)
                    
# #                     ai_color = 'green' if health.ai_status == 'Healthy' else 'orange'
# #                     ui.badge(f'AI: {health.ai_status}', color=ai_color)
                
# #                 ui.label('Resource Utilization').classes('text-sm font-medium mb-2')
                
# #                 ui.label(f'AI Model Performance: {health.model_performance:.1%}').classes('text-sm text-gray-600 mb-1')
# #                 ui.linear_progress(health.model_performance).classes('mb-3')
                
# #                 ui.label(f'Content Processing Rate: {health.processing_rate:.1%}').classes('text-sm text-gray-600 mb-1')
# #                 ui.linear_progress(health.processing_rate).classes('mb-3')
                
# #                 ui.label(f'Storage Utilization: {health.storage_usage:.1%}').classes('text-sm text-gray-600 mb-1')
# #                 ui.linear_progress(health.storage_usage).classes('mb-3')
            
# #             ui.notify('Metrics refreshed', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Error refreshing metrics: {e}")
# #             ui.notify(f'Failed to refresh metrics: {str(e)}', type='negative')
    
# #     def _create_alerts_panel(self):
# #         """Create alerts panel"""
# #         from src.services.monitoring_service import monitoring_service
        
# #         with ui.column().classes('w-full gap-4'):
# #             # Header with refresh button
# #             with ui.row().classes('w-full items-center justify-between mb-2'):
# #                 ui.label('Alerts & Notifications').classes('text-3xl font-bold')
# #                 ui.button(
# #                     'Refresh Alerts',
# #                     icon='refresh',
# #                     on_click=self._refresh_alerts
# #                 ).props('flat color=primary')
            
# #             # Filter buttons
# #             with ui.row().classes('gap-2 mb-4'):
# #                 self.alert_filter = ui.select(
# #                     ['All', 'Critical', 'Warning', 'Info', 'Success'],
# #                     value='All',
# #                     label='Filter by type'
# #                 ).classes('w-48')
                
# #                 ui.button(
# #                     'Apply Filter',
# #                     icon='filter_list',
# #                     on_click=self._refresh_alerts
# #                 ).props('flat')
            
# #             # Alert List
# #             self.alerts_container = ui.column().classes('w-full gap-2')
        
# #         # Load initial alerts
# #         self._refresh_alerts()
    
# #     def _refresh_alerts(self):
# #         """Refresh alerts list"""
# #         from src.services.monitoring_service import monitoring_service
        
# #         try:
# #             # Get alerts
# #             alerts = monitoring_service.get_recent_alerts(limit=15)
            
# #             # Filter if needed
# #             filter_type = self.alert_filter.value.lower()
# #             if filter_type != 'all':
# #                 alerts = [a for a in alerts if a['type'] == filter_type]
            
# #             # Display alerts
# #             self.alerts_container.clear()
# #             with self.alerts_container:
# #                 if not alerts:
# #                     ui.label('No alerts to display').classes('text-gray-500 text-center py-8')
# #                 else:
# #                     for alert in alerts:
# #                         self._create_alert_card(
# #                             alert['title'],
# #                             alert['description'],
# #                             alert['type'],
# #                             alert['time_ago']
# #                         )
            
# #             ui.notify('Alerts refreshed', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Error refreshing alerts: {e}")
# #             ui.notify(f'Failed to refresh alerts: {str(e)}', type='negative')
    
# #     def _create_security_panel(self):
# #         """Create security panel with login logs and security information"""
# #         from src.services.security_service import security_service
        
# #         with ui.column().classes('w-full gap-4'):
# #             # Header
# #             with ui.row().classes('w-full items-center justify-between mb-2'):
# #                 ui.label('Security & Access Logs').classes('text-3xl font-bold')
# #                 ui.button(
# #                     'Refresh',
# #                     icon='refresh',
# #                     on_click=self._refresh_security_logs
# #                 ).props('flat color=primary')
            
# #             # Security Metrics Row
# #             self.security_metrics_container = ui.row().classes('w-full gap-4 mb-4')
            
# #             # Login Activity Chart
# #             self.login_activity_chart_container = ui.card().classes('w-full')
            
# #             # Login Logs Table
# #             self.login_logs_container = ui.card().classes('w-full')
            
# #             # Security Timeline
# #             self.security_timeline_container = ui.card().classes('w-full')
            
# #             # Security Recommendations
# #             with ui.card().classes('w-full bg-blue-50'):
# #                 with ui.row().classes('items-center gap-2 mb-3'):
# #                     ui.icon('security', size='md').classes('text-blue-600')
# #                     ui.label('Security Recommendations').classes('text-xl font-semibold')
                
# #                 recommendations = [
# #                     'Enable two-factor authentication for enhanced security',
# #                     'Review and update your security questions',
# #                     'Check connected devices and revoke unused sessions',
# #                     'Enable email notifications for login attempts'
# #                 ]
                
# #                 with ui.column().classes('gap-2'):
# #                     for i, rec in enumerate(recommendations, 1):
# #                         with ui.row().classes('items-start gap-2'):
# #                             ui.icon('check_circle').classes('text-blue-600 text-sm mt-1')
# #                             ui.label(rec).classes('text-sm text-gray-700')
        
# #         # Load initial data
# #         self._refresh_security_logs()
    
# #     def _refresh_security_logs(self):
# #         """Refresh security logs with real data from DuckDB"""
# #         from src.services.security_service import security_service
# #         from datetime import datetime, timedelta
        
# #         try:
# #             # Get security metrics
# #             active_sessions = security_service.get_active_sessions_count()
# #             failed_logins = security_service.get_failed_login_count(24)
# #             security_score = security_service.get_security_score()
            
# #             # Update security metrics
# #             self.security_metrics_container.clear()
# #             with self.security_metrics_container:
# #                 risk_class = 'risk-low' if active_sessions <= 2 else 'risk-medium'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Active Sessions').classes('text-sm text-gray-600')
# #                     ui.label(str(active_sessions)).classes('text-3xl font-bold text-green-600')
# #                     ui.label('Current user only').classes('text-xs text-gray-500')
                
# #                 risk_class = 'risk-low' if failed_logins == 0 else 'risk-medium' if failed_logins < 5 else 'risk-high'
# #                 color = 'green' if failed_logins == 0 else 'orange' if failed_logins < 5 else 'red'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Failed Login Attempts').classes('text-sm text-gray-600')
# #                     ui.label(str(failed_logins)).classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label('Last 24 hours').classes('text-xs text-gray-500')
                
# #                 risk_class = 'risk-low' if security_score >= 90 else 'risk-medium' if security_score >= 70 else 'risk-high'
# #                 color = 'green' if security_score >= 90 else 'orange' if security_score >= 70 else 'red'
# #                 status = 'Excellent' if security_score >= 90 else 'Good' if security_score >= 70 else 'Needs Attention'
# #                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
# #                     ui.label('Security Score').classes('text-sm text-gray-600')
# #                     ui.label(f'{security_score:.0f}%').classes(f'text-3xl font-bold text-{color}-600')
# #                     ui.label(status).classes('text-xs text-gray-500')
                
# #                 with ui.card().classes('flex-1 metric-card risk-low'):
# #                     ui.label('Last Password Change').classes('text-sm text-gray-600')
# #                     ui.label('30d').classes('text-3xl font-bold text-blue-600')
# #                     ui.label('Recommended: 90 days').classes('text-xs text-gray-500')
            
# #             # Get login activity stats
# #             login_stats = security_service.get_login_activity_stats(7)
            
# #             # Update login activity chart
# #             self.login_activity_chart_container.clear()
# #             with self.login_activity_chart_container:
# #                 ui.label('Login Activity (Last 7 Days)').classes('text-xl font-semibold mb-4')
                
# #                 # Create day labels for last 7 days
# #                 days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# #                 today = datetime.now()
                
# #                 # Build login data with actual counts
# #                 login_data = []
# #                 for i in range(7):
# #                     date = (today - timedelta(days=6-i)).date()
# #                     count = next((s['count'] for s in login_stats if s['date'] == date), 0)
# #                     day_name = days[(today.weekday() - 6 + i) % 7]
# #                     login_data.append((day_name, count))
                
# #                 max_logins = max((count for _, count in login_data), default=1)
                
# #                 with ui.column().classes('w-full gap-2'):
# #                     for day, count in login_data:
# #                         with ui.row().classes('w-full items-center gap-3'):
# #                             ui.label(day).classes('w-12 text-sm font-medium')
# #                             bar_width = (count / max_logins * 100) if max_logins > 0 else 0
# #                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-8 relative'):
# #                                 with ui.element('div').classes('bg-blue-500 h-full rounded').style(f'width: {bar_width}%'):
# #                                     pass
# #                             ui.label(str(count)).classes('w-8 text-sm font-bold text-blue-600')
            
# #             # Get recent login logs
# #             login_logs = security_service.get_recent_login_logs(10)
            
# #             # Update login logs table
# #             self.login_logs_container.clear()
# #             with self.login_logs_container:
# #                 ui.label('Recent Login Activity').classes('text-xl font-semibold mb-4')
                
# #                 if not login_logs:
# #                     ui.label('No login activity recorded yet').classes('text-gray-500 text-center py-8')
# #                 else:
# #                     # Table header - Lightish blue background
# #                     with ui.row().classes('w-full table-header-blue p-3 font-semibold text-sm rounded-t'):
# #                         ui.label('Timestamp').classes('w-40')
# #                         ui.label('User').classes('w-24')
# #                         ui.label('IP Address').classes('w-32')
# #                         ui.label('Location').classes('w-32')
# #                         ui.label('Device').classes('flex-1')
# #                         ui.label('Status').classes('w-24')
                    
# #                     # Table rows
# #                     for log in login_logs:
# #                         with ui.row().classes('w-full p-3 border-b items-center text-sm'):
# #                             timestamp = log['timestamp']
# #                             if isinstance(timestamp, str):
# #                                 timestamp = datetime.fromisoformat(timestamp)
# #                             ui.label(timestamp.strftime('%Y-%m-%d %H:%M:%S')).classes('w-40 text-gray-700')
# #                             ui.label(log['username']).classes('w-24 font-medium')
# #                             ui.label(log['ip_address']).classes('w-32 text-gray-600')
# #                             ui.label(log['location']).classes('w-32 text-gray-600')
# #                             ui.label(log['device_info']).classes('flex-1 text-gray-600')
                            
# #                             status_color = 'green' if log['status'] == 'Success' else 'red'
# #                             ui.badge(log['status'], color=status_color)
            
# #             # Get recent security events
# #             security_events = security_service.get_recent_security_events(5)
            
# #             # Update security timeline
# #             self.security_timeline_container.clear()
# #             with self.security_timeline_container:
# #                 ui.label('Security Events Timeline').classes('text-xl font-semibold mb-4')
                
# #                 if not security_events:
# #                     ui.label('No security events recorded yet').classes('text-gray-500 text-center py-8')
# #                 else:
# #                     # Map event types to icons and colors
# #                     event_icons = {
# #                         'login': ('login', 'green'),
# #                         'password_verified': ('verified_user', 'blue'),
# #                         'session_extended': ('schedule', 'orange'),
# #                         'settings_updated': ('settings', 'purple'),
# #                         'new_device': ('devices', 'blue')
# #                     }
                    
# #                     with ui.column().classes('w-full gap-3'):
# #                         for event in security_events:
# #                             icon, color = event_icons.get(event['event_type'], ('info', 'gray'))
                            
# #                             # Calculate relative time
# #                             event_time = event['timestamp']
# #                             if isinstance(event_time, str):
# #                                 event_time = datetime.fromisoformat(event_time)
# #                             time_diff = datetime.now() - event_time
                            
# #                             if time_diff.days > 0:
# #                                 time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
# #                             elif time_diff.seconds >= 3600:
# #                                 hours = time_diff.seconds // 3600
# #                                 time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
# #                             else:
# #                                 minutes = time_diff.seconds // 60
# #                                 time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                            
# #                             with ui.row().classes('items-center gap-3 p-3 hover:bg-gray-50 rounded'):
# #                                 ui.icon(icon).classes(f'text-{color}-500 text-2xl')
# #                                 with ui.column().classes('flex-1'):
# #                                     ui.label(event['event_description']).classes('font-medium')
# #                                     ui.label(time_ago).classes('text-xs text-gray-500')
# #                                 ui.icon('chevron_right').classes('text-gray-400')
            
# #             ui.notify('Security logs refreshed', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Error refreshing security logs: {e}")
# #             ui.notify(f'Failed to refresh security logs: {str(e)}', type='negative')
    
# #     def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str):
# #         """Create a metric card"""
# #         with ui.card().classes('flex-1 metric-card'):
# #             with ui.row().classes('items-center justify-between'):
# #                 with ui.column():
# #                     ui.label(title).classes('text-sm text-gray-600')
# #                     ui.label(value).classes(f'text-3xl font-bold {color}')
# #                     ui.label(subtitle).classes('text-xs text-gray-500')
# #                 ui.icon(icon).classes(f'{color} text-4xl')
    
# #     def _create_activity_item(self, title: str, description: str, time: str, icon: str, color: str):
# #         """Create an activity item"""
# #         with ui.row().classes('items-center gap-3 p-2 hover:bg-gray-50 rounded'):
# #             ui.icon(icon).classes(f'{color} text-2xl')
# #             with ui.column().classes('flex-1'):
# #                 ui.label(title).classes('font-medium')
# #                 ui.label(description).classes('text-sm text-gray-600')
# #             ui.label(time).classes('text-xs text-gray-400')
    
# #     def _create_alert_card(self, title: str, message: str, severity: str, time: str):
# #         """Create an alert card"""
# #         color_map = {
# #             'critical': 'border-red-500 bg-red-50',
# #             'warning': 'border-orange-500 bg-orange-50',
# #             'info': 'border-blue-500 bg-blue-50'
# #         }
# #         icon_map = {
# #             'critical': 'error',
# #             'warning': 'warning',
# #             'info': 'info'
# #         }
        
# #         with ui.card().classes(f'w-full border-l-4 {color_map.get(severity, "border-gray-500")}'):
# #             with ui.row().classes('items-start justify-between'):
# #                 with ui.row().classes('items-start gap-3 flex-1'):
# #                     ui.icon(icon_map.get(severity, 'info')).classes(f'text-2xl text-{severity}')
# #                     with ui.column():
# #                         ui.label(title).classes('font-semibold')
# #                         ui.label(message).classes('text-sm text-gray-600')
# #                         ui.label(time).classes('text-xs text-gray-400 mt-1')
# #                 with ui.row().classes('gap-2'):
# #                     ui.button(icon='visibility').props('flat dense')
# #                     ui.button(icon='check').props('flat dense')
    
# #     async def _analyze_content(self, content: str):
# #         """Analyze content and display results (async to prevent UI blocking)"""
# #         if not content or not content.strip():
# #             ui.notify('Please enter content to analyze', type='warning')
# #             return
        
# #         # Track operation
# #         self.current_operation = {
# #             'type': 'Analysis',
# #             'content': content,
# #             'progress': 0
# #         }
        
# #         try:
# #             # Show loading state with animation
# #             self.analysis_container.clear()
# #             with self.analysis_container:
# #                 with ui.card().classes('w-full text-center p-8'):
# #                     ui.spinner(size='xl', color='primary')
# #                     ui.label('🤖 AI is analyzing your content...').classes('text-xl font-semibold mt-4')
# #                     progress_label = ui.label('Ingesting content...').classes('text-sm text-gray-600 mt-2')
            
# #             # Check if operation should be paused
# #             if self.operation_paused:
# #                 ui.notify('Operation paused. Please extend session to continue.', type='warning')
# #                 return
            
# #             # Ingest content (run in executor to not block UI)
# #             import asyncio
# #             import uuid
# #             loop = asyncio.get_event_loop()
# #             version = await loop.run_in_executor(
# #                 None, 
# #                 self.ingestion_service.ingest_text, 
# #                 self.current_user, 
# #                 content
# #             )
# #             self.current_operation['progress'] = 30
# #             progress_label.set_text('Running AI analysis...')
            
# #             # Analyze content (run in executor to not block UI)
# #             analysis = await loop.run_in_executor(
# #                 None,
# #                 self.analyzer.analyze_content,
# #                 version.version_id,
# #                 content
# #             )
# #             self.current_analysis = analysis
# #             self.current_operation['progress'] = 100
# #             progress_label.set_text('Complete!')
            
# #             # Store in ashoka_contentint table
# #             content_id = str(uuid.uuid4())
# #             word_count = len(content.split())
# #             char_count = len(content)
            
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             db_schema.conn.execute("""
# #                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# #             """, [
# #                 content_id,
# #                 self.current_user,
# #                 'text',
# #                 content,
# #                 None,  # file_path
# #                 None,  # file_name
# #                 None,  # file_size_mb
# #                 json.dumps({'source': 'text_input'}),
# #                 analysis.summary,
# #                 analysis.sentiment.classification,
# #                 analysis.sentiment.confidence,
# #                 json.dumps(analysis.keywords),
# #                 json.dumps(analysis.topics),
# #                 json.dumps(analysis.takeaways),
# #                 word_count,
# #                 char_count,
# #                 None,  # quality_score (can be calculated later)
# #                 datetime.now(),
# #                 analysis.analyzed_at
# #             ])
            
# #             # Store in history
# #             if not hasattr(self, 'analysis_history'):
# #                 self.analysis_history = []
            
# #             self.analysis_history.insert(0, {
# #                 'timestamp': datetime.now(),
# #                 'content': content[:100] + '...' if len(content) > 100 else content,
# #                 'full_content': content,
# #                 'analysis': analysis,
# #                 'sentiment': analysis.sentiment.classification,
# #                 'version_id': version.version_id,
# #                 'content_id': content_id
# #             })
            
# #             # Keep only last 20 analyses
# #             if len(self.analysis_history) > 20:
# #                 self.analysis_history = self.analysis_history[:20]
            
# #             # Update UI with results
# #             self._display_analysis_results(analysis, content)
            
# #             # Update history table if it exists
# #             if hasattr(self, 'history_table_container'):
# #                 self._update_history_table()
            
# #             # Clear operation tracking
# #             self.current_operation = None
            
# #             ui.notify('✅ Content analyzed successfully!', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Analysis error: {e}")
# #             self.analysis_container.clear()
# #             with self.analysis_container:
# #                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
# #                     ui.icon('error', size='xl').classes('text-red-600')
# #                     ui.label('Analysis Failed').classes('text-xl font-semibold text-red-600 mt-2')
# #                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
# #             ui.notify(f'Analysis failed: {str(e)}', type='negative')
# #             self.current_operation = None

    
# #     async def _transform_content(self):
# #         """Transform content for multiple platforms (async to prevent UI blocking)"""
# #         content = self.transform_input.value
        
# #         if not content or not content.strip():
# #             ui.notify('Please enter content to transform', type='warning')
# #             return
        
# #         # Get selected platforms
# #         platforms = []
# #         if self.platform_linkedin.value:
# #             platforms.append('linkedin')
# #         if self.platform_twitter.value:
# #             platforms.append('twitter')
# #         if self.platform_instagram.value:
# #             platforms.append('instagram')
# #         if self.platform_facebook.value:
# #             platforms.append('facebook')
# #         if self.platform_threads.value:
# #             platforms.append('threads')
        
# #         if not platforms:
# #             ui.notify('Please select at least one platform', type='warning')
# #             return
        
# #         try:
# #             # Show loading state with animation
# #             self.transform_results_container.clear()
# #             with self.transform_results_container:
# #                 with ui.card().classes('w-full text-center p-8'):
# #                     ui.spinner(size='xl', color='primary')
# #                     ui.label('🔄 Transforming content for social media...').classes('text-xl font-semibold mt-4')
# #                     progress_label = ui.label(f'Generating content for {len(platforms)} platforms...').classes('text-sm text-gray-600 mt-2')
            
# #             # Get tone
# #             tone = self.tone_selector.value.lower()
# #             include_hashtags = self.include_hashtags.value
            
# #             # Transform content (run in executor to not block UI)
# #             import asyncio
# #             loop = asyncio.get_event_loop()
# #             results = await loop.run_in_executor(
# #                 None,
# #                 content_transformer.transform_for_platforms,
# #                 content,
# #                 platforms,
# #                 tone,
# #                 include_hashtags
# #             )
            
# #             # Store in database
# #             import uuid
# #             transform_id = str(uuid.uuid4())
            
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             # Store transformed content
# #             db_schema.conn.execute("""
# #                 INSERT INTO transform_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)
# #             """, [
# #                 transform_id,
# #                 self.current_user,
# #                 content,
# #                 json.dumps(platforms),
# #                 tone,
# #                 include_hashtags,
# #                 json.dumps({k: v.content if v else None for k, v in results.items()}),
# #                 datetime.now()
# #             ])
            
# #             # Display results
# #             self._display_transform_results(results)
            
# #             # Update history table if it exists
# #             if hasattr(self, 'transform_history_container'):
# #                 self._update_transform_history()
            
# #             ui.notify(f'✅ Content transformed for {len(platforms)} platforms!', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Transformation error: {e}")
# #             self.transform_results_container.clear()
# #             with self.transform_results_container:
# #                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
# #                     ui.icon('error', size='xl').classes('text-red-600')
# #                     ui.label('Transformation Failed').classes('text-xl font-semibold text-red-600 mt-2')
# #                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
# #             ui.notify(f'Transformation failed: {str(e)}', type='negative')
    
# #     def _display_transform_results(self, results: dict):
# #         """Display transformation results for all platforms"""
# #         self.transform_results_container.clear()
        
# #         with self.transform_results_container:
# #             for platform_key, platform_content in results.items():
# #                 if platform_content is None:
# #                     continue
                
# #                 # Platform-specific styling
# #                 platform_colors = {
# #                     'LinkedIn': ('bg-blue-50', 'blue', 'work'),
# #                     'Twitter/X': ('bg-sky-50', 'sky', 'chat'),
# #                     'Instagram': ('bg-pink-50', 'pink', 'photo_camera'),
# #                     'Facebook': ('bg-indigo-50', 'indigo', 'thumb_up'),
# #                     'Threads': ('bg-purple-50', 'purple', 'forum')
# #                 }
                
# #                 bg_color, badge_color, icon = platform_colors.get(
# #                     platform_content.platform,
# #                     ('bg-gray-50', 'gray', 'share')
# #                 )
                
# #                 # Create expansion for each platform
# #                 with ui.expansion(
# #                     platform_content.platform,
# #                     icon=icon
# #                 ).classes('w-full mb-2'):
# #                     with ui.card().classes(f'{bg_color} w-full'):
# #                         # Metadata
# #                         with ui.row().classes('items-center gap-2 mb-3'):
# #                             ui.label(f"Tone: {platform_content.metadata.get('tone', 'N/A').title()}").classes('text-sm text-gray-600')
# #                             ui.label('•').classes('text-gray-400')
# #                             ui.label(f"Format: {platform_content.metadata.get('format', 'N/A').title()}").classes('text-sm text-gray-600')
                            
# #                             # Tweet count for Twitter
# #                             if 'tweet_count' in platform_content.metadata:
# #                                 ui.label('•').classes('text-gray-400')
# #                                 ui.label(f"{platform_content.metadata['tweet_count']} tweets").classes('text-sm text-gray-600')
                        
# #                         # Content
# #                         with ui.scroll_area().classes('h-64 w-full'):
# #                             ui.label(platform_content.content).classes('text-gray-700 whitespace-pre-wrap')
                        
# #                         # Stats
# #                         with ui.row().classes('mt-4 gap-2 flex-wrap'):
# #                             ui.badge(
# #                                 f"{platform_content.character_count:,} characters",
# #                                 color=badge_color
# #                             )
                            
# #                             limit_color = 'green' if platform_content.within_limit else 'red'
# #                             limit_text = 'Within limit' if platform_content.within_limit else 'Exceeds limit'
# #                             ui.badge(limit_text, color=limit_color)
                            
# #                             if platform_content.hashtags:
# #                                 ui.badge(
# #                                     f"{len(platform_content.hashtags)} hashtags",
# #                                     color='purple'
# #                                 )
                        
# #                         # Hashtags
# #                         if platform_content.hashtags:
# #                             ui.label('Hashtags:').classes('text-sm font-medium mt-3 mb-2')
# #                             with ui.row().classes('gap-2 flex-wrap'):
# #                                 for hashtag in platform_content.hashtags:
# #                                     ui.chip(f'#{hashtag}', icon='tag').props(f'outline color={badge_color}').classes('text-xs')
                        
# #                         # Copy button
# #                         ui.button(
# #                             'Copy to Clipboard',
# #                             icon='content_copy',
# #                             on_click=lambda c=platform_content.content: self._copy_to_clipboard(c)
# #                         ).props('flat').classes('mt-3')
    
# #     def _copy_to_clipboard(self, text: str):
# #         """Copy text to clipboard"""
# #         ui.run_javascript(f'''
# #             navigator.clipboard.writeText(`{text.replace("`", "\\`")}`).then(() => {{
# #                 console.log('Copied to clipboard');
# #             }});
# #         ''')
# #         ui.notify('Copied to clipboard!', type='positive')
    
# #     def _update_transform_history(self):
# #         """Update transform history table"""
# #         try:
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             # Get last 20 transformations
# #             rows = db_schema.conn.execute("""
# #                 SELECT id, original_content, platforms, tone, created_at, transformed_results
# #                 FROM transform_history
# #                 WHERE user_id = ?
# #                 ORDER BY created_at DESC
# #                 LIMIT 20
# #             """, [self.current_user]).fetchall()
            
# #             self.transform_history_container.clear()
            
# #             if not rows:
# #                 with self.transform_history_container:
# #                     ui.label('No transform history yet').classes('text-gray-500 text-center py-4')
# #                 return
            
# #             with self.transform_history_container:
# #                 # Create table
# #                 columns = [
# #                     {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'left', 'sortable': True},
# #                     {'name': 'content', 'label': 'Original Content', 'field': 'content', 'align': 'left'},
# #                     {'name': 'platforms', 'label': 'Platforms', 'field': 'platforms', 'align': 'left'},
# #                     {'name': 'tone', 'label': 'Tone', 'field': 'tone', 'align': 'left'},
# #                     {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'}
# #                 ]
                
# #                 table_rows = []
# #                 for row in rows:
# #                     transform_id, content, platforms_json, tone, created_at, results_json = row
                    
# #                     # Parse platforms
# #                     platforms_list = json.loads(platforms_json) if platforms_json else []
# #                     platforms_str = ', '.join([p.title() for p in platforms_list])
                    
# #                     # Truncate content preview
# #                     content_preview = content[:80] + '...' if len(content) > 80 else content
                    
# #                     table_rows.append({
# #                         'id': transform_id,
# #                         'timestamp': created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(created_at, 'strftime') else str(created_at),
# #                         'content': content_preview,
# #                         'platforms': platforms_str,
# #                         'tone': tone.title(),
# #                         'actions': transform_id,
# #                         '_full_content': content,
# #                         '_platforms': platforms_list,
# #                         '_results': results_json
# #                     })
                
# #                 table = ui.table(
# #                     columns=columns,
# #                     rows=table_rows,
# #                     row_key='id'
# #                 ).classes('w-full')
                
# #                 # Add custom slot for actions column
# #                 table.add_slot('body-cell-actions', '''
# #                     <q-td :props="props">
# #                         <q-btn flat dense icon="visibility" color="primary" size="sm" @click="$parent.$emit('preview', props.row)" />
# #                         <q-btn flat dense icon="folder_open" color="secondary" size="sm" @click="$parent.$emit('load', props.row)" />
# #                     </q-td>
# #                 ''')
                
# #                 # Handle preview button click
# #                 table.on('preview', lambda e: self._show_transform_preview_dialog(e.args))
                
# #                 # Handle load button click
# #                 table.on('load', lambda e: self._load_transform_from_history(e.args))
                
# #         except Exception as e:
# #             logger.error(f"Error updating transform history: {e}")
# #             self.transform_history_container.clear()
# #             with self.transform_history_container:
# #                 ui.label(f'Error loading history: {str(e)}').classes('text-red-600')
    
# #     def _show_transform_preview_dialog(self, row_data):
# #         """Show transform preview in a dialog"""
# #         try:
# #             results_json = row_data.get('_results')
# #             if not results_json:
# #                 ui.notify('No results available', type='warning')
# #                 return
            
# #             results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
            
# #             with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
# #                 with ui.row().classes('w-full items-center justify-between mb-4'):
# #                     ui.label('Transform Preview').classes('text-2xl font-bold')
# #                     ui.button(icon='close', on_click=dialog.close).props('flat round')
                
# #                 ui.label(f"Original: {row_data.get('_full_content', '')[:200]}...").classes('text-sm text-gray-600 mb-4')
                
# #                 # Display each platform result
# #                 with ui.scroll_area().classes('h-96 w-full'):
# #                     for platform, content in results_dict.items():
# #                         if content:
# #                             with ui.card().classes('w-full mb-3 bg-gray-50'):
# #                                 ui.label(platform.title()).classes('text-lg font-semibold mb-2')
# #                                 ui.label(content).classes('text-gray-700 whitespace-pre-wrap')
                
# #                 ui.button('Close', on_click=dialog.close).props('color=primary').classes('mt-4')
            
# #             dialog.open()
            
# #         except Exception as e:
# #             logger.error(f"Error showing transform preview: {e}")
# #             ui.notify(f'Error: {str(e)}', type='negative')
    
# #     def _load_transform_from_history(self, row_data):
# #         """Load a past transformation into the main view"""
# #         try:
# #             # Load original content
# #             self.transform_input.value = row_data.get('_full_content', '')
            
# #             # Load platforms
# #             platforms = row_data.get('_platforms', [])
# #             self.platform_linkedin.value = 'linkedin' in platforms
# #             self.platform_twitter.value = 'twitter' in platforms
# #             self.platform_instagram.value = 'instagram' in platforms
# #             self.platform_facebook.value = 'facebook' in platforms
# #             self.platform_threads.value = 'threads' in platforms
            
# #             # Load tone
# #             tone = row_data.get('tone', 'Professional')
# #             self.tone_selector.value = tone.title()
            
# #             # Load and display results
# #             results_json = row_data.get('_results')
# #             if results_json:
# #                 results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
                
# #                 # Convert dict to PlatformContent objects
# #                 from src.services.content_transformer import PlatformContent
# #                 results = {}
# #                 for platform, content in results_dict.items():
# #                     if content:
# #                         results[platform] = PlatformContent(
# #                             platform=platform.title(),
# #                             content=content,
# #                             character_count=len(content),
# #                             within_limit=True,
# #                             hashtags=[],
# #                             metadata={'tone': tone, 'format': 'loaded'}
# #                         )
                
# #                 self._display_transform_results(results)
            
# #             ui.notify(f'Loaded transformation from {row_data.get("timestamp")}', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Error loading transform from history: {e}")
# #             ui.notify(f'Error: {str(e)}', type='negative')
    
# #     def _handle_image_upload(self, e):
# #         """Handle image file upload"""
# #         try:
# #             # Get uploaded file - handle both content types
# #             if hasattr(e.content, 'read'):
# #                 file_content = e.content.read()
# #             else:
# #                 file_content = e.content
# #             filename = e.name
            
# #             logger.info(f"Processing uploaded image: {filename}")
            
# #             # Show loading
# #             self.image_preview_container.clear()
# #             with self.image_preview_container:
# #                 ui.spinner(size='lg')
# #                 ui.label('Processing image...').classes('text-center mt-2')
            
# #             # Process image and extract text
# #             extracted_text, file_path = file_processor.process_image(file_content, filename)
# #             self.uploaded_file_path = file_path
            
# #             # Store in ashoka_contentint table
# #             import uuid
# #             content_id = str(uuid.uuid4())
# #             file_info = file_processor.get_file_info(file_path)
            
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             db_schema.conn.execute("""
# #                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# #             """, [
# #                 content_id,
# #                 self.current_user,
# #                 'image',
# #                 extracted_text,
# #                 file_path,
# #                 filename,
# #                 file_info.get('size_mb', 0),
# #                 json.dumps({'format': file_info.get('format', 'unknown')}),
# #                 None,  # summary (will be filled after analysis)
# #                 None,  # sentiment
# #                 None,  # sentiment_confidence
# #                 None,  # keywords
# #                 None,  # topics
# #                 None,  # takeaways
# #                 len(extracted_text.split()),
# #                 len(extracted_text),
# #                 None,  # quality_score
# #                 datetime.now(),
# #                 None  # analyzed_at (will be filled after analysis)
# #             ])
            
# #             # Show image preview
# #             self.image_preview_container.clear()
# #             with self.image_preview_container:
# #                 with ui.card().classes('w-full'):
# #                     ui.label('Uploaded Image:').classes('font-semibold mb-2')
# #                     # Display image
# #                     ui.image(file_path).classes('w-full max-h-64 object-contain')
                    
# #                     # File info
# #                     ui.label(f"File: {file_info.get('filename', 'Unknown')} ({file_info.get('size_mb', 0)} MB)").classes('text-sm text-gray-600 mt-2')
                
# #                 with ui.card().classes('w-full bg-blue-50'):
# #                     ui.label('Extracted Text:').classes('font-semibold mb-2')
# #                     ui.label(extracted_text).classes('text-sm text-gray-700')
                
# #                 ui.button(
# #                     'Analyze Extracted Text',
# #                     icon='psychology',
# #                     on_click=lambda: self._analyze_content(extracted_text)
# #                 ).props('color=primary').classes('w-full mt-2')
            
# #             ui.notify(f'Image uploaded: {filename}', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Image upload error: {e}")
# #             self.image_preview_container.clear()
# #             with self.image_preview_container:
# #                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
# #             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
# #     def _handle_video_upload(self, e):
# #         """Handle video file upload"""
# #         try:
# #             # Get uploaded file - handle both content types
# #             if hasattr(e.content, 'read'):
# #                 file_content = e.content.read()
# #             else:
# #                 file_content = e.content
# #             filename = e.name
            
# #             logger.info(f"Processing uploaded video: {filename}")
            
# #             # Show loading
# #             self.video_preview_container.clear()
# #             with self.video_preview_container:
# #                 ui.spinner(size='lg')
# #                 ui.label('Processing video...').classes('text-center mt-2')
            
# #             # Process video and extract transcription
# #             transcription, file_path, metadata = file_processor.process_video(file_content, filename)
# #             self.uploaded_file_path = file_path
            
# #             # Store in ashoka_contentint table
# #             import uuid
# #             content_id = str(uuid.uuid4())
# #             file_info = file_processor.get_file_info(file_path)
            
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             db_schema.conn.execute("""
# #                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# #             """, [
# #                 content_id,
# #                 self.current_user,
# #                 'video',
# #                 transcription,
# #                 file_path,
# #                 filename,
# #                 file_info.get('size_mb', 0),
# #                 json.dumps(metadata),
# #                 None,  # summary (will be filled after analysis)
# #                 None,  # sentiment
# #                 None,  # sentiment_confidence
# #                 None,  # keywords
# #                 None,  # topics
# #                 None,  # takeaways
# #                 len(transcription.split()),
# #                 len(transcription),
# #                 None,  # quality_score
# #                 datetime.now(),
# #                 None  # analyzed_at (will be filled after analysis)
# #             ])
            
# #             # Show video preview
# #             self.video_preview_container.clear()
# #             with self.video_preview_container:
# #                 with ui.card().classes('w-full'):
# #                     ui.label('Uploaded Video:').classes('font-semibold mb-2')
                    
# #                     # Display video player
# #                     ui.video(file_path).classes('w-full max-h-64')
                    
# #                     # File info
# #                     file_info = file_processor.get_file_info(file_path)
# #                     with ui.row().classes('gap-4 mt-2 text-sm text-gray-600'):
# #                         ui.label(f"📁 {file_info.get('filename', 'Unknown')}")
# #                         ui.label(f"💾 {file_info.get('size_mb', 0)} MB")
                
# #                 # Video metadata
# #                 with ui.card().classes('w-full bg-purple-50'):
# #                     ui.label('Video Information:').classes('font-semibold mb-2')
# #                     with ui.grid(columns=2).classes('gap-2 text-sm'):
# #                         ui.label('Duration:').classes('font-medium')
# #                         ui.label(metadata.get('duration', 'Unknown'))
# #                         ui.label('Resolution:').classes('font-medium')
# #                         ui.label(metadata.get('resolution', 'Unknown'))
# #                         ui.label('FPS:').classes('font-medium')
# #                         ui.label(str(metadata.get('fps', 'Unknown')))
# #                         ui.label('Codec:').classes('font-medium')
# #                         ui.label(metadata.get('codec', 'Unknown'))
                
# #                 # Transcription
# #                 with ui.card().classes('w-full bg-blue-50'):
# #                     ui.label('Video Transcription:').classes('font-semibold mb-2')
# #                     ui.label(transcription).classes('text-sm text-gray-700 whitespace-pre-wrap')
                
# #                 ui.button(
# #                     'Analyze Transcription',
# #                     icon='psychology',
# #                     on_click=lambda: self._analyze_content(transcription)
# #                 ).props('color=primary').classes('w-full mt-2')
            
# #             ui.notify(f'Video uploaded: {filename}', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Video upload error: {e}")
# #             self.video_preview_container.clear()
# #             with self.video_preview_container:
# #                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
# #             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
# #     def _handle_document_upload(self, e):
# #         """Handle document file upload"""
# #         try:
# #             # Get uploaded file - handle both content types
# #             if hasattr(e.content, 'read'):
# #                 file_content = e.content.read()
# #             else:
# #                 file_content = e.content
# #             filename = e.name
            
# #             logger.info(f"Processing uploaded document: {filename}")
            
# #             # Show loading
# #             self.document_preview_container.clear()
# #             with self.document_preview_container:
# #                 ui.spinner(size='lg')
# #                 ui.label('Processing document...').classes('text-center mt-2')
            
# #             # Process document and extract text
# #             extracted_text, file_path, metadata = file_processor.process_document(file_content, filename)
# #             self.uploaded_file_path = file_path
            
# #             # Store in ashoka_contentint table
# #             import uuid
# #             content_id = str(uuid.uuid4())
# #             file_info = file_processor.get_file_info(file_path)
            
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             db_schema.conn.execute("""
# #                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# #             """, [
# #                 content_id,
# #                 self.current_user,
# #                 'document',
# #                 extracted_text,
# #                 file_path,
# #                 filename,
# #                 file_info.get('size_mb', 0),
# #                 json.dumps(metadata),
# #                 None,  # summary (will be filled after analysis)
# #                 None,  # sentiment
# #                 None,  # sentiment_confidence
# #                 None,  # keywords
# #                 None,  # topics
# #                 None,  # takeaways
# #                 len(extracted_text.split()),
# #                 len(extracted_text),
# #                 None,  # quality_score
# #                 datetime.now(),
# #                 None  # analyzed_at (will be filled after analysis)
# #             ])
            
# #             # Show document preview
# #             self.document_preview_container.clear()
# #             with self.document_preview_container:
# #                 with ui.card().classes('w-full'):
# #                     ui.label('Uploaded Document:').classes('font-semibold mb-2')
                    
# #                     # File info
# #                     file_info = file_processor.get_file_info(file_path)
# #                     with ui.row().classes('gap-4 text-sm text-gray-600'):
# #                         ui.label(f"📄 {file_info.get('filename', 'Unknown')}")
# #                         ui.label(f"💾 {file_info.get('size_mb', 0)} MB")
                
# #                 # Document metadata
# #                 with ui.card().classes('w-full bg-indigo-50'):
# #                     ui.label('Document Information:').classes('font-semibold mb-2')
# #                     with ui.grid(columns=2).classes('gap-2 text-sm'):
# #                         ui.label('Format:').classes('font-medium')
# #                         ui.label(metadata.get('format', 'Unknown'))
# #                         ui.label('Pages:').classes('font-medium')
# #                         ui.label(str(metadata.get('pages', 'N/A')))
# #                         ui.label('Words:').classes('font-medium')
# #                         ui.label(f"{metadata.get('words', 0):,}")
# #                         ui.label('Size:').classes('font-medium')
# #                         ui.label(f"{metadata.get('size_kb', 0)} KB")
                
# #                 # Extracted text
# #                 with ui.card().classes('w-full bg-green-50'):
# #                     ui.label('Extracted Text:').classes('font-semibold mb-2')
# #                     with ui.scroll_area().classes('h-64 w-full'):
# #                         ui.label(extracted_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                
# #                 ui.button(
# #                     'Analyze Document',
# #                     icon='psychology',
# #                     on_click=lambda: self._analyze_content(extracted_text)
# #                 ).props('color=primary').classes('w-full mt-2')
            
# #             ui.notify(f'Document uploaded: {filename}', type='positive')
            
# #         except Exception as e:
# #             logger.error(f"Document upload error: {e}")
# #             self.document_preview_container.clear()
# #             with self.document_preview_container:
# #                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
# #             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
# #     def _display_analysis_results(self, analysis, content: str):
# #         """Display comprehensive analysis results"""
# #         self.analysis_container.clear()
# #         with self.analysis_container:
# #             # Summary Card
# #             with ui.card().classes('w-full bg-blue-50'):
# #                 with ui.row().classes('items-center gap-2 mb-2'):
# #                     ui.icon('summarize', size='sm').classes('text-blue-600')
# #                     ui.label('Summary').classes('font-semibold text-lg')
# #                 ui.label(analysis.summary).classes('text-gray-700')
            
# #             # Sentiment Card
# #             with ui.card().classes('w-full'):
# #                 with ui.row().classes('items-center gap-2 mb-2'):
# #                     ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
# #                     ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                
# #                 sentiment_color = {
# #                     'positive': 'green',
# #                     'neutral': 'gray',
# #                     'negative': 'red'
# #                 }.get(analysis.sentiment.classification, 'gray')
                
# #                 with ui.row().classes('items-center gap-3'):
# #                     ui.badge(
# #                         analysis.sentiment.classification.upper(),
# #                         color=sentiment_color
# #                     ).classes('text-lg px-4 py-2')
# #                     ui.label(f'Confidence: {analysis.sentiment.confidence:.1%}').classes('text-sm text-gray-600')
                
# #                 # Sentiment scores
# #                 if analysis.sentiment.scores:
# #                     ui.label('Detailed Scores:').classes('text-sm font-medium mt-3 mb-2')
# #                     for emotion, score in analysis.sentiment.scores.items():
# #                         with ui.row().classes('items-center gap-2 w-full'):
# #                             ui.label(emotion.capitalize()).classes('text-sm w-20')
# #                             ui.linear_progress(score).classes('flex-1')
# #                             ui.label(f'{score:.1%}').classes('text-sm text-gray-600 w-12')
            
# #             # Keywords Card
# #             with ui.card().classes('w-full'):
# #                 with ui.row().classes('items-center gap-2 mb-2'):
# #                     ui.icon('label', size='sm').classes('text-purple-600')
# #                     ui.label('Keywords').classes('font-semibold text-lg')
# #                 with ui.row().classes('gap-2 flex-wrap'):
# #                     for keyword in analysis.keywords[:15]:
# #                         ui.badge(keyword, color='purple').classes('text-sm')
            
# #             # Topics Card
# #             with ui.card().classes('w-full'):
# #                 with ui.row().classes('items-center gap-2 mb-2'):
# #                     ui.icon('topic', size='sm').classes('text-orange-600')
# #                     ui.label('Topics').classes('font-semibold text-lg')
# #                 with ui.row().classes('gap-2'):
# #                     for topic in analysis.topics:
# #                         ui.chip(topic, icon='topic').props('outline color=orange')
            
# #             # Takeaways Card
# #             if analysis.takeaways:
# #                 with ui.card().classes('w-full bg-green-50'):
# #                     with ui.row().classes('items-center gap-2 mb-2'):
# #                         ui.icon('lightbulb', size='sm').classes('text-green-600')
# #                         ui.label('Key Takeaways').classes('font-semibold text-lg')
# #                     with ui.column().classes('gap-2'):
# #                         for i, takeaway in enumerate(analysis.takeaways, 1):
# #                             with ui.row().classes('items-start gap-2'):
# #                                 ui.label(f'{i}.').classes('font-bold text-green-600')
# #                                 ui.label(takeaway).classes('text-gray-700')
            
# #             # Metrics Card
# #             with ui.card().classes('w-full'):
# #                 with ui.row().classes('items-center gap-2 mb-2'):
# #                     ui.icon('analytics', size='sm').classes('text-indigo-600')
# #                     ui.label('Content Metrics').classes('font-semibold text-lg')
                
# #                 word_count = len(content.split())
# #                 char_count = len(content)
                
# #                 with ui.grid(columns=3).classes('gap-4 w-full'):
# #                     with ui.card().classes('text-center p-4'):
# #                         ui.label(str(word_count)).classes('text-2xl font-bold text-indigo-600')
# #                         ui.label('Words').classes('text-sm text-gray-600')
                    
# #                     with ui.card().classes('text-center p-4'):
# #                         ui.label(str(char_count)).classes('text-2xl font-bold text-indigo-600')
# #                         ui.label('Characters').classes('text-sm text-gray-600')
                    
# #                     with ui.card().classes('text-center p-4'):
# #                         ui.label(str(len(analysis.keywords))).classes('text-2xl font-bold text-indigo-600')
# #                         ui.label('Keywords').classes('text-sm text-gray-600')
    
# #     def _update_history_table(self):
# #         """Update the analysis history table from database"""
# #         if not hasattr(self, 'history_table_container'):
# #             return
        
# #         self.history_table_container.clear()
        
# #         # Load history from database
# #         try:
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             history_data = db_schema.conn.execute("""
# #                 SELECT id, content_text, sentiment, created_at, analyzed_at,
# #                        summary, keywords, topics, takeaways, sentiment_confidence
# #                 FROM ashoka_contentint
# #                 WHERE analyzed_at IS NOT NULL
# #                 ORDER BY analyzed_at DESC
# #                 LIMIT 20
# #             """).fetchall()
            
# #             if not history_data:
# #                 with self.history_table_container:
# #                     ui.label('No analysis history yet').classes('text-gray-500 text-center py-4')
# #                 return
            
# #             with self.history_table_container:
# #                 # Create table with clickable rows
# #                 with ui.column().classes('w-full gap-2'):
# #                     for row in history_data:
# #                         content_id, content_text, sentiment, created_at, analyzed_at, summary, keywords_json, topics_json, takeaways_json, confidence = row
                        
# #                         sentiment_color = {
# #                             'positive': 'green',
# #                             'neutral': 'gray',
# #                             'negative': 'red'
# #                         }.get(sentiment, 'gray')
                        
# #                         sentiment_icon = {
# #                             'positive': 'sentiment_satisfied',
# #                             'neutral': 'sentiment_neutral',
# #                             'negative': 'sentiment_dissatisfied'
# #                         }.get(sentiment, 'sentiment_neutral')
                        
# #                         content_preview = content_text[:100] + '...' if content_text and len(content_text) > 100 else content_text or 'No content'
                        
# #                         with ui.card().classes('w-full hover:bg-gray-50'):
# #                             with ui.row().classes('items-center gap-4 w-full'):
# #                                 # Timestamp
# #                                 with ui.column().classes('w-32'):
# #                                     ui.label(analyzed_at.strftime('%Y-%m-%d')).classes('text-sm font-medium')
# #                                     ui.label(analyzed_at.strftime('%H:%M:%S')).classes('text-xs text-gray-500')
                                
# #                                 # Content preview
# #                                 with ui.column().classes('flex-1'):
# #                                     ui.label(content_preview).classes('text-sm text-gray-700 truncate')
                                
# #                                 # Sentiment badge
# #                                 with ui.row().classes('items-center gap-2 w-32'):
# #                                     ui.icon(sentiment_icon, size='sm').classes(f'text-{sentiment_color}-600')
# #                                     ui.badge(sentiment.upper(), color=sentiment_color).classes('text-xs')
                                
# #                                 # Action buttons
# #                                 with ui.row().classes('gap-2'):
# #                                     # Preview button (eye icon) - opens dialog
# #                                     ui.button(icon='visibility', on_click=lambda cid=content_id: self._show_analysis_preview_dialog(cid)).props('flat dense round').classes('text-blue-600').tooltip('Preview in dialog')
# #                                     # Load button - loads into main view
# #                                     ui.button(icon='open_in_full', on_click=lambda cid=content_id: self._load_analysis_from_history(cid)).props('flat dense round').classes('text-green-600').tooltip('Load into main view')
        
# #         except Exception as e:
# #             logger.error(f"Error loading history: {e}")
# #             with self.history_table_container:
# #                 ui.label('Error loading history').classes('text-red-500 text-center py-4')
    
# #     def _load_analysis_from_history(self, content_id: str):
# #         """Load and display an analysis from database history"""
# #         try:
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             # Fetch the analysis from database
# #             row = db_schema.conn.execute("""
# #                 SELECT content_text, summary, sentiment, sentiment_confidence,
# #                        keywords, topics, takeaways, analyzed_at
# #                 FROM ashoka_contentint
# #                 WHERE id = ?
# #             """, [content_id]).fetchone()
            
# #             if not row:
# #                 ui.notify('Analysis not found', type='warning')
# #                 return
            
# #             content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at = row
            
# #             # Parse JSON fields
# #             keywords = json.loads(keywords_json) if keywords_json else []
# #             topics = json.loads(topics_json) if topics_json else []
# #             takeaways = json.loads(takeaways_json) if takeaways_json else []
            
# #             # Reconstruct analysis object
# #             from src.models.content import ContentAnalysis, Sentiment
            
# #             analysis = ContentAnalysis(
# #                 version_id=content_id,
# #                 summary=summary,
# #                 takeaways=takeaways,
# #                 keywords=keywords,
# #                 topics=topics,
# #                 sentiment=Sentiment(
# #                     classification=sentiment,
# #                     confidence=confidence,
# #                     scores={
# #                         'positive': confidence if sentiment == 'positive' else 0.3,
# #                         'neutral': confidence if sentiment == 'neutral' else 0.3,
# #                         'negative': confidence if sentiment == 'negative' else 0.3
# #                     }
# #                 ),
# #                 analyzed_at=analyzed_at
# #             )
            
# #             # Display the analysis results
# #             self._display_analysis_results(analysis, content_text)
            
# #         except Exception as e:
# #             logger.error(f"Error loading analysis from history: {e}")
# #             ui.notify(f'Error loading analysis: {str(e)}', type='negative')
    
# #     def _show_analysis_preview_dialog(self, content_id: str):
# #         """Show analysis preview in a dialog window"""
# #         try:
# #             if not db_schema.conn:
# #                 db_schema.connect()
            
# #             # Fetch the analysis from database
# #             row = db_schema.conn.execute("""
# #                 SELECT content_text, summary, sentiment, sentiment_confidence,
# #                        keywords, topics, takeaways, analyzed_at, word_count, char_count
# #                 FROM ashoka_contentint
# #                 WHERE id = ?
# #             """, [content_id]).fetchone()
            
# #             if not row:
# #                 ui.notify('Analysis not found', type='warning')
# #                 return
            
# #             content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at, word_count, char_count = row
            
# #             # Parse JSON fields
# #             keywords = json.loads(keywords_json) if keywords_json else []
# #             topics = json.loads(topics_json) if topics_json else []
# #             takeaways = json.loads(takeaways_json) if takeaways_json else []
            
# #             # Create dialog
# #             with ui.dialog() as preview_dialog, ui.card().classes('w-[900px] max-h-[80vh]'):
# #                 with ui.row().classes('w-full items-center justify-between mb-4'):
# #                     ui.label('Analysis Preview').classes('text-2xl font-bold')
# #                     ui.button(icon='close', on_click=preview_dialog.close).props('flat round dense')
                
# #                 with ui.scroll_area().classes('w-full h-[60vh]'):
# #                     with ui.column().classes('w-full gap-4 p-4'):
# #                         # Metadata
# #                         with ui.card().classes('w-full bg-gray-50'):
# #                             with ui.row().classes('items-center gap-4'):
# #                                 ui.icon('schedule', size='sm').classes('text-gray-600')
# #                                 ui.label(f"Analyzed: {analyzed_at.strftime('%Y-%m-%d %H:%M:%S')}").classes('text-sm')
# #                                 ui.label(f"Words: {word_count or len(content_text.split())}").classes('text-sm ml-4')
# #                                 ui.label(f"Characters: {char_count or len(content_text)}").classes('text-sm ml-4')
                        
# #                         # Original Content
# #                         with ui.card().classes('w-full'):
# #                             ui.label('Original Content').classes('text-lg font-semibold mb-2')
# #                             with ui.scroll_area().classes('h-32 w-full'):
# #                                 ui.label(content_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
# #                         # Summary
# #                         with ui.card().classes('w-full bg-blue-50'):
# #                             with ui.row().classes('items-center gap-2 mb-2'):
# #                                 ui.icon('summarize', size='sm').classes('text-blue-600')
# #                                 ui.label('Summary').classes('font-semibold text-lg')
# #                             ui.label(summary).classes('text-gray-700')
                        
# #                         # Sentiment
# #                         with ui.card().classes('w-full'):
# #                             with ui.row().classes('items-center gap-2 mb-2'):
# #                                 ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
# #                                 ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                            
# #                             sentiment_color = {
# #                                 'positive': 'green',
# #                                 'neutral': 'gray',
# #                                 'negative': 'red'
# #                             }.get(sentiment, 'gray')
                            
# #                             with ui.row().classes('items-center gap-3'):
# #                                 ui.badge(sentiment.upper(), color=sentiment_color).classes('text-lg px-4 py-2')
# #                                 ui.label(f'Confidence: {confidence:.1%}').classes('text-sm text-gray-600')
                        
# #                         # Keywords
# #                         if keywords:
# #                             with ui.card().classes('w-full'):
# #                                 with ui.row().classes('items-center gap-2 mb-2'):
# #                                     ui.icon('label', size='sm').classes('text-purple-600')
# #                                     ui.label('Keywords').classes('font-semibold text-lg')
# #                                 with ui.row().classes('gap-2 flex-wrap'):
# #                                     for keyword in keywords[:15]:
# #                                         ui.badge(keyword, color='purple').classes('text-sm')
                        
# #                         # Topics
# #                         if topics:
# #                             with ui.card().classes('w-full'):
# #                                 with ui.row().classes('items-center gap-2 mb-2'):
# #                                     ui.icon('topic', size='sm').classes('text-orange-600')
# #                                     ui.label('Topics').classes('font-semibold text-lg')
# #                                 with ui.row().classes('gap-2'):
# #                                     for topic in topics:
# #                                         ui.chip(topic, icon='topic').props('outline color=orange')
                        
# #                         # Takeaways
# #                         if takeaways:
# #                             with ui.card().classes('w-full bg-green-50'):
# #                                 with ui.row().classes('items-center gap-2 mb-2'):
# #                                     ui.icon('lightbulb', size='sm').classes('text-green-600')
# #                                     ui.label('Key Takeaways').classes('font-semibold text-lg')
# #                                 with ui.column().classes('gap-2'):
# #                                     for i, takeaway in enumerate(takeaways, 1):
# #                                         with ui.row().classes('items-start gap-2'):
# #                                             ui.label(f'{i}.').classes('font-bold text-green-600')
# #                                             ui.label(takeaway).classes('text-gray-700')
            
# #             preview_dialog.open()
            
# #         except Exception as e:
# #             logger.error(f"Error showing preview dialog: {e}")
# #             ui.notify(f'Error showing preview: {str(e)}', type='negative')
    
# #     async def _generate_ai_content(self):
# #         """Generate content using AI based on user prompt"""
# #         prompt = self.generator_prompt.value
# #         gen_type = self.gen_type.value
        
# #         if not prompt or not prompt.strip():
# #             ui.notify('Please enter a prompt', type='warning')
# #             return
        
# #         try:
# #             # Show loading
# #             self.generator_output_container.clear()
# #             with self.generator_output_container:
# #                 with ui.card().classes('w-full text-center p-8'):
# #                     ui.spinner(size='xl', color='primary')
# #                     ui.label('🤖 AI is generating content...').classes('text-xl font-semibold mt-4')
# #                     progress_label = ui.label('Processing your prompt...').classes('text-sm text-gray-600 mt-2')
            
# #             # Generate content
# #             import asyncio
# #             loop = asyncio.get_event_loop()
            
# #             if gen_type == 'Text/Notes':
# #                 # Generate text content using Gemini
# #                 generation_prompt = f"Generate professional content based on this prompt:\n\n{prompt}\n\nProvide a well-structured, detailed response."
                
# #                 result = await loop.run_in_executor(
# #                     None,
# #                     gemini_client.generate_content,
# #                     generation_prompt
# #                 )
                
# #                 generated_text = result.get('text', 'No content generated')
                
# #                 # Display generated text
# #                 self.generator_output_container.clear()
# #                 with self.generator_output_container:
# #                     with ui.card().classes('w-full'):
# #                         with ui.row().classes('items-center justify-between mb-3'):
# #                             ui.label('Generated Text').classes('text-lg font-semibold')
# #                             ui.button(
# #                                 icon='content_copy',
# #                                 on_click=lambda: self._copy_to_clipboard(generated_text)
# #                             ).props('flat dense round').tooltip('Copy to clipboard')
                        
# #                         with ui.scroll_area().classes('h-96 w-full'):
# #                             ui.label(generated_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
# #                         # Action buttons
# #                         with ui.row().classes('gap-2 mt-3'):
# #                             ui.button(
# #                                 'Analyze This Content',
# #                                 icon='psychology',
# #                                 on_click=lambda: self._analyze_content(generated_text)
# #                             ).props('color=primary')
# #                             ui.button(
# #                                 'Use in Transformer',
# #                                 icon='transform',
# #                                 on_click=lambda: self._use_in_transformer(generated_text)
# #                             ).props('flat')
                
# #                 ui.notify('✅ Content generated successfully!', type='positive')
            
# #             elif gen_type == 'Image':
# #                 # Generate actual image using Hugging Face Inference Client
# #                 progress_label.set_text('Generating image with AI...')
                
# #                 from src.config import config
# #                 from pathlib import Path
# #                 import uuid
                
# #                 # Check if token is available
# #                 if not config.HUGGINGFACE_TOKEN:
# #                     raise Exception("HUGGINGFACE_TOKEN not found in .env file")
                
# #                 try:
# #                     from huggingface_hub import InferenceClient
# #                 except ImportError:
# #                     raise Exception("huggingface_hub not installed. Run: pip install huggingface_hub")
                
# #                 # Initialize Hugging Face Inference Client
# #                 client = InferenceClient(token=config.HUGGINGFACE_TOKEN)
                
# #                 # Generate image
# #                 def generate_image(prompt_text):
# #                     # Use text-to-image with the FLUX model
# #                     image = client.text_to_image(
# #                         prompt=prompt_text,
# #                         model=config.HUGGINGFACE_MODEL
# #                     )
# #                     return image
                
# #                 image = await loop.run_in_executor(None, generate_image, prompt)
                
# #                 # Save image to uploads folder
# #                 uploads_dir = Path("data/uploads")
# #                 uploads_dir.mkdir(parents=True, exist_ok=True)
                
# #                 image_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
# #                 image_path = uploads_dir / image_filename
                
# #                 # Save the PIL Image
# #                 image.save(str(image_path))
                
# #                 # Display generated image
# #                 self.generator_output_container.clear()
# #                 with self.generator_output_container:
# #                     with ui.card().classes('w-full'):
# #                         ui.label('Generated Image').classes('text-lg font-semibold mb-3')
                        
# #                         # Display the image
# #                         ui.image(str(image_path)).classes('w-full max-h-96 object-contain rounded')
                        
# #                         # Image info
# #                         with ui.row().classes('items-center gap-2 mt-3 text-sm text-gray-600'):
# #                             ui.icon('info', size='sm')
# #                             ui.label(f'Prompt: {prompt[:100]}{"..." if len(prompt) > 100 else ""}')
                        
# #                         # Action buttons
# #                         with ui.row().classes('gap-2 mt-3'):
# #                             ui.button(
# #                                 'Download Image',
# #                                 icon='download',
# #                                 on_click=lambda: ui.download(str(image_path), image_filename)
# #                             ).props('color=primary')
# #                             ui.button(
# #                                 'Generate Another',
# #                                 icon='refresh',
# #                                 on_click=lambda: self.generator_prompt.set_value('')
# #                             ).props('flat')
                
# #                 ui.notify('✅ Image generated successfully!', type='positive')
        
# #         except Exception as e:
# #             logger.error(f"Generation error: {e}")
# #             self.generator_output_container.clear()
# #             with self.generator_output_container:
# #                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
# #                     ui.icon('error', size='xl').classes('text-red-600')
# #                     ui.label('Generation Failed').classes('text-xl font-semibold text-red-600 mt-2')
# #                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
                    
# #                     if 'HUGGINGFACE_TOKEN' in str(e):
# #                         ui.label('Make sure HUGGINGFACE_TOKEN is set in your .env file').classes('text-xs text-gray-600 mt-2')
# #             ui.notify(f'Generation failed: {str(e)}', type='negative')
    
# #     def _copy_to_clipboard(self, text: str):
# #         """Copy text to clipboard"""
# #         ui.run_javascript(f'navigator.clipboard.writeText({json.dumps(text)})')
# #         ui.notify('Copied to clipboard!', type='positive')
    
# #     def _use_in_transformer(self, text: str):
# #         """Use generated text in the transformer"""
# #         if hasattr(self, 'transform_input'):
# #             self.transform_input.set_value(text)
# #             ui.notify('Text loaded into transformer', type='info')
# #         else:
# #             ui.notify('Transformer not available', type='warning')
    
# #     def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str = ''):
# #         """Create a metric card"""
# #         with ui.card().classes('flex-1 dashboard-card'):
# #             with ui.row().classes('items-center gap-3'):
# #                 ui.icon(icon, size='lg').classes(color)
# #                 with ui.column().classes('gap-1'):
# #                     ui.label(title).classes('text-sm opacity-90')
# #                     ui.label(value).classes('text-3xl font-bold')
# #                     if subtitle:
# #                         ui.label(subtitle).classes('text-xs opacity-75')
    
# #     def _create_activity_item(self, title: str, description: str, time: str, icon: str, icon_color: str):
# #         """Create an activity item"""
# #         with ui.row().classes('items-start gap-3 p-3 content-card'):
# #             ui.icon(icon, size='md').classes(icon_color)
# #             with ui.column().classes('flex-1 gap-1'):
# #                 ui.label(title).classes('font-semibold')
# #                 ui.label(description).classes('text-sm text-gray-600')
# #                 ui.label(time).classes('text-xs text-gray-500')


# # def launch_dashboard():
# #     """Launch the Ashoka dashboard"""
# #     dashboard = AshokaGovDashboard()
# #     dashboard.create_dashboard()
    
# #     ui.run(
# #         title='Ashoka - GenAI Governance Platform',
# #         favicon='🛡️',
# #         dark=False,
# #         reload=False,
# #         port=8080
# #     )


# # if __name__ in {"__main__", "__mp_main__"}:
# #     launch_dashboard()




# """Ashoka GenAI Governance Dashboard - NiceGUI Implementation"""
# from nicegui import ui, app
# from datetime import datetime, timedelta
# from typing import Optional
# import json

# from src.services.content_ingestion import ContentIngestionService
# from src.services.content_analyzer import ContentAnalyzer
# from src.services.file_processor import file_processor
# from src.services.content_transformer import content_transformer
# from src.services.gemini_client import gemini_client
# from src.database.duckdb_schema import db_schema
# from src.utils.logging import logger


# class AshokaGovDashboard:
#     """GenAI Governance Dashboard"""
    
#     def __init__(self):
#         self.ingestion_service = ContentIngestionService()
#         self.analyzer = ContentAnalyzer()
#         self.current_user = "demo_user"
#         self.current_analysis = None
#         self.dark_mode = False
#         self.uploaded_file_path = None
        
#         # Analysis history for Content Intelligence
#         self.analysis_history = []
        
#         # Session management
#         self.session_duration = 30 * 60  # 30 minutes in seconds
#         self.session_start_time = datetime.now()
#         self.session_timer = None
#         self.session_paused = False
#         self.paused_tasks = []
        
#         # Current operation tracking
#         self.current_operation = None
#         self.operation_paused = False
        
#         # Use app.storage.general instead of app.storage.user (doesn't require secret)
#         self.current_language = app.storage.general.get('language', 'English')
        
#         # User preferences
#         self.user_preferences = {
#             'notifications': True,
#             'auto_save': True,
#             'theme': 'light',
#             'language': 'English',
#             'email_alerts': False,
#             'session_timeout': 30
#         }
        
#         self.translations = {
#             "English": {
#                 "title": "Ashoka",
#                 "subtitle": "GenAI Governance & Observability Platform",
#                 "overview": "Overview",
#                 "content_intelligence": "Content Intelligence",
#                 "transform": "Transform",
#                 "monitoring": "Monitoring",
#                 "alerts": "Alerts",
#                 "profile": "Profile",
#                 "settings": "Settings",
#                 "logout": "Logout",
#                 "user_profile": "User Profile",
#                 "username": "Username",
#                 "email": "Email",
#                 "role": "Role",
#                 "member_since": "Member Since",
#                 "close": "Close",
#                 "language_settings": "Language Settings",
#                 "select_language": "Select Language",
#                 "apply": "Apply",
#                 # Overview Panel
#                 "platform_overview": "Platform Overview",
#                 "total_content": "Total Content",
#                 "this_week": "this week",
#                 "quality_score": "Quality Score",
#                 "excellent": "Excellent",
#                 "risk_alerts": "Risk Alerts",
#                 "resolved": "resolved",
#                 "ai_operations": "AI Operations",
#                 "success": "success",
#                 "recent_activity": "Recent Activity",
#                 "content_analyzed": "Content analyzed",
#                 "article_ai_ethics": "Article about AI ethics",
#                 "min_ago": "min ago",
#                 "risk_detected": "Risk detected",
#                 "policy_violation": "Potential policy violation",
#                 "content_transformed": "Content transformed",
#                 "linkedin_twitter": "LinkedIn + Twitter posts",
#                 "hour_ago": "hour ago",
#                 "quality_alert": "Quality alert",
#                 "readability_below": "Readability below threshold",
#                 "hours_ago": "hours ago",
#                 "system_health": "System Health",
#                 "ai_model_performance": "AI Model Performance",
#                 "content_processing_rate": "Content Processing Rate",
#                 "storage_utilization": "Storage Utilization",
#                 "api_healthy": "API: Healthy",
#                 "database_healthy": "Database: Healthy",
#                 "ai_healthy": "AI: Healthy"
#             },
#             "Hindi": {
#                 "title": "अशोक",
#                 "subtitle": "जेनएआई गवर्नेंस और ऑब्जर्वेबिलिटी प्लेटफॉर्म",
#                 "overview": "अवलोकन",
#                 "content_intelligence": "सामग्री बुद्धिमत्ता",
#                 "transform": "रूपांतरण",
#                 "monitoring": "निगरानी",
#                 "alerts": "अलर्ट",
#                 "profile": "प्रोफ़ाइल",
#                 "settings": "सेटिंग्स",
#                 "logout": "लॉगआउट",
#                 "user_profile": "उपयोगकर्ता प्रोफ़ाइल",
#                 "username": "उपयोगकर्ता नाम",
#                 "email": "ईमेल",
#                 "role": "भूमिका",
#                 "member_since": "सदस्य बने",
#                 "close": "बंद करें",
#                 "language_settings": "भाषा सेटिंग्स",
#                 "select_language": "भाषा चुनें",
#                 "apply": "लागू करें",
#                 # Overview Panel
#                 "platform_overview": "प्लेटफ़ॉर्म अवलोकन",
#                 "total_content": "कुल सामग्री",
#                 "this_week": "इस सप्ताह",
#                 "quality_score": "गुणवत्ता स्कोर",
#                 "excellent": "उत्कृष्ट",
#                 "risk_alerts": "जोखिम अलर्ट",
#                 "resolved": "हल किया गया",
#                 "ai_operations": "एआई संचालन",
#                 "success": "सफलता",
#                 "recent_activity": "हाल की गतिविधि",
#                 "content_analyzed": "सामग्री विश्लेषण",
#                 "article_ai_ethics": "एआई नैतिकता पर लेख",
#                 "min_ago": "मिनट पहले",
#                 "risk_detected": "जोखिम का पता चला",
#                 "policy_violation": "संभावित नीति उल्लंघन",
#                 "content_transformed": "सामग्री रूपांतरित",
#                 "linkedin_twitter": "लिंक्डइन + ट्विटर पोस्ट",
#                 "hour_ago": "घंटे पहले",
#                 "quality_alert": "गुणवत्ता अलर्ट",
#                 "readability_below": "पठनीयता सीमा से नीचे",
#                 "hours_ago": "घंटे पहले",
#                 "system_health": "सिस्टम स्वास्थ्य",
#                 "ai_model_performance": "एआई मॉडल प्रदर्शन",
#                 "content_processing_rate": "सामग्री प्रसंस्करण दर",
#                 "storage_utilization": "भंडारण उपयोग",
#                 "api_healthy": "एपीआई: स्वस्थ",
#                 "database_healthy": "डेटाबेस: स्वस्थ",
#                 "ai_healthy": "एआई: स्वस्थ"
#             },
#             "Kannada": {
#                 "title": "ಅಶೋಕ",
#                 "subtitle": "ಜೆನ್‌ಎಐ ಆಡಳಿತ ಮತ್ತು ವೀಕ್ಷಣಾ ವೇದಿಕೆ",
#                 "overview": "ಅವಲೋಕನ",
#                 "content_intelligence": "ವಿಷಯ ಬುದ್ಧಿವಂತಿಕೆ",
#                 "transform": "ಪರಿವರ್ತನೆ",
#                 "monitoring": "ಮೇಲ್ವಿಚಾರಣೆ",
#                 "alerts": "ಎಚ್ಚರಿಕೆಗಳು",
#                 "profile": "ಪ್ರೊಫೈಲ್",
#                 "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
#                 "logout": "ಲಾಗ್ಔಟ್",
#                 "user_profile": "ಬಳಕೆದಾರ ಪ್ರೊಫೈಲ್",
#                 "username": "ಬಳಕೆದಾರ ಹೆಸರು",
#                 "email": "ಇಮೇಲ್",
#                 "role": "ಪಾತ್ರ",
#                 "member_since": "ಸದಸ್ಯರಾದ ದಿನಾಂಕ",
#                 "close": "ಮುಚ್ಚಿ",
#                 "language_settings": "ಭಾಷಾ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
#                 "select_language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
#                 "apply": "ಅನ್ವಯಿಸಿ",
#                 # Overview Panel
#                 "platform_overview": "ವೇದಿಕೆ ಅವಲೋಕನ",
#                 "total_content": "ಒಟ್ಟು ವಿಷಯ",
#                 "this_week": "ಈ ವಾರ",
#                 "quality_score": "ಗುಣಮಟ್ಟ ಸ್ಕೋರ್",
#                 "excellent": "ಅತ್ಯುತ್ತಮ",
#                 "risk_alerts": "ಅಪಾಯ ಎಚ್ಚರಿಕೆಗಳು",
#                 "resolved": "ಪರಿಹರಿಸಲಾಗಿದೆ",
#                 "ai_operations": "ಎಐ ಕಾರ್ಯಾಚರಣೆಗಳು",
#                 "success": "ಯಶಸ್ಸು",
#                 "recent_activity": "ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ",
#                 "content_analyzed": "ವಿಷಯ ವಿಶ್ಲೇಷಣೆ",
#                 "article_ai_ethics": "ಎಐ ನೀತಿಶಾಸ್ತ್ರದ ಲೇಖನ",
#                 "min_ago": "ನಿಮಿಷಗಳ ಹಿಂದೆ",
#                 "risk_detected": "ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
#                 "policy_violation": "ಸಂಭಾವ್ಯ ನೀತಿ ಉಲ್ಲಂಘನೆ",
#                 "content_transformed": "ವಿಷಯ ಪರಿವರ್ತನೆ",
#                 "linkedin_twitter": "ಲಿಂಕ್ಡ್‌ಇನ್ + ಟ್ವಿಟರ್ ಪೋಸ್ಟ್‌ಗಳು",
#                 "hour_ago": "ಗಂಟೆ ಹಿಂದೆ",
#                 "quality_alert": "ಗುಣಮಟ್ಟ ಎಚ್ಚರಿಕೆ",
#                 "readability_below": "ಓದುವಿಕೆ ಮಿತಿಗಿಂತ ಕಡಿಮೆ",
#                 "hours_ago": "ಗಂಟೆಗಳ ಹಿಂದೆ",
#                 "system_health": "ವ್ಯವಸ್ಥೆ ಆರೋಗ್ಯ",
#                 "ai_model_performance": "ಎಐ ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ",
#                 "content_processing_rate": "ವಿಷಯ ಪ್ರಕ್ರಿಯೆ ದರ",
#                 "storage_utilization": "ಸಂಗ್ರಹಣೆ ಬಳಕೆ",
#                 "api_healthy": "ಎಪಿಐ: ಆರೋಗ್ಯಕರ",
#                 "database_healthy": "ಡೇಟಾಬೇಸ್: ಆರೋಗ್ಯಕರ",
#                 "ai_healthy": "ಎಐ: ಆರೋಗ್ಯಕರ"
#             },
#             "Tamil": {
#                 "title": "அசோகா",
#                 "subtitle": "ஜென்ஏஐ ஆளுமை மற்றும் கண்காணிப்பு தளம்",
#                 "overview": "மேலோட்டம்",
#                 "content_intelligence": "உள்ளடக்க நுண்ணறிவு",
#                 "transform": "மாற்றம்",
#                 "monitoring": "கண்காணிப்பு",
#                 "alerts": "எச்சரிக்கைகள்",
#                 "profile": "சுயவிவரம்",
#                 "settings": "அமைப்புகள்",
#                 "logout": "வெளியேறு",
#                 "user_profile": "பயனர் சுயவிவரம்",
#                 "username": "பயனர் பெயர்",
#                 "email": "மின்னஞ்சல்",
#                 "role": "பங்கு",
#                 "member_since": "உறுப்பினரான தேதி",
#                 "close": "மூடு",
#                 "language_settings": "மொழி அமைப்புகள்",
#                 "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
#                 "apply": "பயன்படுத்து",
#                 # Overview Panel
#                 "platform_overview": "தள மேலோட்டம்",
#                 "total_content": "மொத்த உள்ளடக்கம்",
#                 "this_week": "இந்த வாரம்",
#                 "quality_score": "தர மதிப்பெண்",
#                 "excellent": "சிறந்தது",
#                 "risk_alerts": "அபாய எச்சரிக்கைகள்",
#                 "resolved": "தீர்க்கப்பட்டது",
#                 "ai_operations": "ஏஐ செயல்பாடுகள்",
#                 "success": "வெற்றி",
#                 "recent_activity": "சமீபத்திய செயல்பாடு",
#                 "content_analyzed": "உள்ளடக்க பகுப்பாய்வு",
#                 "article_ai_ethics": "ஏஐ நெறிமுறைகள் பற்றிய கட்டுரை",
#                 "min_ago": "நிமிடங்களுக்கு முன்",
#                 "risk_detected": "அபாயம் கண்டறியப்பட்டது",
#                 "policy_violation": "சாத்தியமான கொள்கை மீறல்",
#                 "content_transformed": "உள்ளடக்க மாற்றம்",
#                 "linkedin_twitter": "லிங்க்ட்இன் + ட்விட்டர் இடுகைகள்",
#                 "hour_ago": "மணி நேரத்திற்கு முன்",
#                 "quality_alert": "தர எச்சரிக்கை",
#                 "readability_below": "வாசிப்புத்திறன் வரம்புக்குக் கீழே",
#                 "hours_ago": "மணி நேரங்களுக்கு முன்",
#                 "system_health": "அமைப்பு ஆரோக்கியம்",
#                 "ai_model_performance": "ஏஐ மாதிரி செயல்திறன்",
#                 "content_processing_rate": "உள்ளடக்க செயலாக்க விகிதம்",
#                 "storage_utilization": "சேமிப்பக பயன்பாடு",
#                 "api_healthy": "ஏபிஐ: ஆரோக்கியமானது",
#                 "database_healthy": "தரவுத்தளம்: ஆரோக்கியமானது",
#                 "ai_healthy": "ஏஐ: ஆரோக்கியமானது"
#             }
#         }
        
#         # Initialize database
#         db_schema.connect()
#         db_schema.initialize_schema()
    
#     def t(self, key: str) -> str:
#         """Get translation for current language"""
#         return self.translations.get(self.current_language, self.translations["English"]).get(key, key)
    
#     def create_dashboard(self):
#         """Create the main dashboard UI"""
        
#         # Custom CSS aligned with auth theme (cream + teal + blue)
#         ui.add_head_html('''
#             <style>
#                 :root {
#                     --bg-primary: #ded5c4;
#                     --bg-secondary: #efeeeb;
#                     --text-primary: #102d32;
#                     --text-secondary: #4e6b71;
#                     --accent-color: #2d8a84;
#                     --accent-soft: #5b93c9;
#                     --card-bg: #f8f6f2;
#                     --line: rgba(16, 45, 50, 0.16);
#                     --header-from: #2d8a84;
#                     --header-to: #176a66;
#                 }
                
#                 .dark-mode {
#                     --bg-primary: #102124;
#                     --bg-secondary: #173037;
#                     --text-primary: #e7f3f4;
#                     --text-secondary: #b5cfd1;
#                     --accent-color: #70b8b2;
#                     --accent-soft: #7caede;
#                     --card-bg: #1c3438;
#                     --line: rgba(231, 243, 244, 0.18);
#                     --header-from: #1f7d78;
#                     --header-to: #145f5b;
#                 }
                
#                 body {
#                     background: linear-gradient(150deg, var(--bg-primary), #d9d0c0) !important;
#                     color: var(--text-primary) !important;
#                     transition: background 0.3s ease, color 0.3s ease;
#                 }
                
#                 .dashboard-card {
#                     background: linear-gradient(135deg, var(--header-from) 0%, var(--header-to) 100%);
#                     border-radius: 16px;
#                     padding: 20px;
#                     color: white;
#                     box-shadow: 0 10px 24px rgba(27, 92, 98, 0.24);
#                     transition: transform 0.18s ease, box-shadow 0.18s ease;
#                 }
                
#                 .dashboard-card:hover {
#                     transform: translateY(-2px);
#                     box-shadow: 0 14px 30px rgba(27, 92, 98, 0.28);
#                 }
                
#                 .metric-card {
#                     background: var(--card-bg) !important;
#                     border-radius: 14px;
#                     padding: 20px;
#                     box-shadow: 0 8px 20px rgba(44, 77, 82, 0.12);
#                     border: 1px solid var(--line);
#                     border-left: 4px solid var(--accent-color);
#                     color: var(--text-primary) !important;
#                     transition: transform 0.18s ease, box-shadow 0.18s ease;
#                 }
                
#                 .metric-card:hover {
#                     transform: translateY(-2px);
#                     box-shadow: 0 12px 24px rgba(44, 77, 82, 0.16);
#                 }
                
#                 .risk-high {
#                     border-left-color: #ef4444 !important;
#                 }
#                 .risk-medium {
#                     border-left-color: #f59e0b !important;
#                 }
#                 .risk-low {
#                     border-left-color: #10b981 !important;
#                 }
                
#                 .content-card {
#                     background: var(--bg-secondary);
#                     border-radius: 12px;
#                     padding: 16px;
#                     margin: 8px 0;
#                     border: 1px solid var(--line);
#                 }
                
#                 .q-card {
#                     background: var(--card-bg) !important;
#                     color: var(--text-primary) !important;
#                     border-radius: 14px !important;
#                     border: 1px solid var(--line) !important;
#                     box-shadow: 0 8px 18px rgba(44, 77, 82, 0.12) !important;
#                 }
                
#                 .q-tab {
#                     color: var(--text-secondary) !important;
#                     font-weight: 600;
#                 }
                
#                 .q-tab--active {
#                     color: var(--accent-color) !important;
#                 }
                
#                 .q-header {
#                     background: linear-gradient(to right, var(--header-from), var(--header-to)) !important;
#                     backdrop-filter: blur(6px);
#                 }

#                 .app-header {
#                     border-bottom: 1px solid rgba(255, 255, 255, 0.2);
#                     box-shadow: 0 8px 20px rgba(13, 71, 76, 0.25);
#                 }
                
#                 .dark-mode .text-gray-600 {
#                     color: #b5cfd1 !important;
#                 }
                
#                 .dark-mode .text-gray-500 {
#                     color: #8fb1b4 !important;
#                 }
                
#                 .dark-mode .text-gray-700 {
#                     color: #deecee !important;
#                 }
                
#                 .timer-shell {
#                     background: linear-gradient(135deg, #4ea66a, #388e57) !important;
#                     border-radius: 14px !important;
#                     border: 1px solid rgba(255,255,255,0.25) !important;
#                 }

#                 .timer-text {
#                     color: #ffffff !important;
#                 }

#                 .dark-mode .timer-text {
#                     color: #ffffff !important;
#                 }
                
#                 /* Tab spacing */
#                 .q-tab {
#                     padding: 0 24px !important;
#                     min-width: 140px !important;
#                     display: flex !important;
#                     justify-content: center !important;
#                 }
                
#                 .q-tab__content {
#                     display: flex !important;
#                     flex-direction: row !important;
#                     justify-content: center !important;
#                     align-items: center !important;
#                     gap: 2px !important;
#                 }
                
#                 .q-tab__icon {
#                     margin: 0 !important;
#                 }
                
#                 .q-tab__label {
#                     margin: 0 !important;
#                 }
                
#                 /* Fix overlapping content */
#                 .q-tab-panel {
#                     padding: 24px !important;
#                 }
                
#                 .content-input-area {
#                     background: rgba(45, 138, 132, 0.06) !important;
#                     border: 1px solid rgba(45, 138, 132, 0.25) !important;
#                     border-radius: 12px !important;
#                 }
                
#                 .dark-mode .content-input-area {
#                     background: rgba(45, 138, 132, 0.15) !important;
#                     border: 1px solid rgba(112, 184, 178, 0.32) !important;
#                 }
                
#                 .table-header-blue {
#                     background-color: #d7e8fb !important;
#                     color: #24506f !important;
#                     font-weight: 600 !important;
#                 }
                
#                 .dark-mode .table-header-blue {
#                     background-color: #234c69 !important;
#                     color: #d7ebff !important;
#                 }
#             </style>
#         ''')
        
#         # Header
#         with ui.header().classes('app-header'):
#             with ui.row().classes('w-full items-center'):
#                 ui.icon('shield_with_heart', size='lg').classes('text-white')
#                 self.title_label = ui.label(self.t('title')).classes('text-2xl font-bold text-white ml-2')
#                 self.subtitle_label = ui.label(self.t('subtitle')).classes('text-sm text-cyan-50 ml-4')
#                 ui.space()
                
#                 # Session timer
#                 with ui.card().classes('timer-shell px-4 py-2 shadow-lg'):
#                     with ui.row().classes('items-center gap-2'):
#                         ui.icon('schedule', size='sm').classes('text-white')
#                         self.timer_label = ui.label('30:00').classes('timer-text font-mono text-lg font-bold')
                
#                 # Dark mode toggle
#                 self.theme_toggle = ui.button(
#                     icon='dark_mode',
#                     on_click=self._toggle_theme
#                 ).props('flat round').classes('text-white ml-2')
                
#                 with ui.button(icon='account_circle').props('flat round').classes('text-white'):
#                     with ui.menu():
#                         ui.menu_item(self.t('profile'), on_click=self._show_profile_dialog)
#                         ui.menu_item(self.t('settings'), on_click=self._show_settings_dialog)
#                         ui.separator()
#                         ui.menu_item(self.t('logout'), on_click=self._handle_logout)
        
#         # Start session timer
#         self._start_session_timer()
        
#         # Start auto-refresh timers for real-time updates
#         self._start_auto_refresh_timers()
        
#         # Check user role for Security tab visibility
#         username = app.storage.general.get('username', '')
#         is_admin = self._check_if_admin(username)
        
#         # Main content with tabs
#         with ui.tabs().classes('w-full justify-center') as tabs:
#             self.overview_tab = ui.tab(self.t('overview'), icon='dashboard')
#             self.content_tab = ui.tab(self.t('content_intelligence'), icon='psychology')
#             self.transform_tab = ui.tab(self.t('transform'), icon='transform')
#             self.monitor_tab = ui.tab(self.t('monitoring'), icon='bar_chart')
#             self.alerts_tab = ui.tab(self.t('alerts'), icon='notifications')
            
#             # Security tab - always create but control visibility
#             self.security_tab = ui.tab('Security', icon='security')
#             self.security_tab.set_visibility(is_admin)
        
#         with ui.tab_panels(tabs, value=self.overview_tab).classes('w-full'):
#             # Overview Panel
#             with ui.tab_panel(self.overview_tab):
#                 self._create_overview_panel()
            
#             # Content Intelligence Panel
#             with ui.tab_panel(self.content_tab):
#                 self._create_content_intelligence_panel()
            
#             # Transform Panel
#             with ui.tab_panel(self.transform_tab):
#                 self._create_transform_panel()
            
#             # Monitoring Panel
#             with ui.tab_panel(self.monitor_tab):
#                 with ui.column().classes('w-full'):
#                     self._create_monitoring_panel()
            
#             # Alerts Panel
#             with ui.tab_panel(self.alerts_tab):
#                 self._create_alerts_panel()
            
#             # Security Panel
#             with ui.tab_panel(self.security_tab):
#                 self._create_security_panel()
    
#     def _toggle_theme(self):
#         """Toggle between light and dark mode"""
#         self.dark_mode = not self.dark_mode
        
#         if self.dark_mode:
#             ui.run_javascript('document.body.classList.add("dark-mode")')
#             self.theme_toggle.props('icon=light_mode')
#         else:
#             ui.run_javascript('document.body.classList.remove("dark-mode")')
#             self.theme_toggle.props('icon=dark_mode')
    
#     def _handle_logout(self):
#         """Handle user logout - clear session and redirect to login"""
#         # Clear session storage
#         app.storage.general.clear()
        
#         # Notify user
#         ui.notify('Logged out successfully', type='info')
        
#         # Redirect to login page
#         ui.navigate.to('/')
    
#     def _check_if_admin(self, username: str) -> bool:
#         """Check if user has admin role"""
#         if not username:
#             return False
        
#         try:
#             from src.database.mock_storage import mock_dynamodb
#             from src.config import config
            
#             user_data = mock_dynamodb.get_item(config.DYNAMODB_USERS_TABLE, f"user_{username}")
#             if user_data:
#                 role = user_data.get('role', 'creator')
#                 logger.info(f"User {username} has role: {role}")
#                 return role == 'admin'
#         except Exception as e:
#             logger.error(f"Error checking admin role: {e}")
        
#         return False
    
#     def _start_session_timer(self):
#         """Start the session countdown timer"""
#         def update_timer():
#             elapsed = (datetime.now() - self.session_start_time).total_seconds()
#             remaining = self.session_duration - elapsed
            
#             if remaining <= 0:
#                 # Session expired
#                 self.timer_label.set_text('00:00')
#                 self.timer_label.classes('text-red-600', remove='text-gray-800 text-orange-600')
#                 ui.notify('Session expired. Please login again.', type='warning')
#                 ui.run_javascript('setTimeout(() => window.location.href = "/", 2000)')
#                 return
            
#             # Check if operation is running and time is low
#             if self.current_operation and remaining <= 10 and not self.operation_paused:
#                 self._pause_current_operation()
            
#             # Update timer display
#             minutes = int(remaining // 60)
#             seconds = int(remaining % 60)
#             timer_text = f'{minutes:02d}:{seconds:02d}'
#             self.timer_label.set_text(timer_text)
            
#             # Change color when time is low (white text on green background)
#             if remaining <= 60:
#                 self.timer_label.classes('text-red-100', remove='text-white text-orange-100')
#             elif remaining <= 300:
#                 self.timer_label.classes('text-orange-100', remove='text-white text-red-100')
#             else:
#                 self.timer_label.classes('text-white', remove='text-orange-100 text-red-100')
        
#         # Use repeating timer (every 1 second)
#         ui.timer(1.0, update_timer)
    
#     def _start_auto_refresh_timers(self):
#         """Start timers for auto-refreshing dashboard data"""
#         # Note: These will only refresh if the respective panels have been created
#         # Refresh intervals are configurable
        
#         # Refresh monitoring metrics every 60 seconds
#         def refresh_monitoring():
#             try:
#                 if hasattr(self, 'quality_metrics_container'):
#                     self._refresh_monitoring_metrics()
#             except Exception as e:
#                 logger.error(f"Auto-refresh monitoring error: {e}")
        
#         ui.timer(60.0, refresh_monitoring)
        
#         # Refresh alerts every 90 seconds
#         def refresh_alerts():
#             try:
#                 if hasattr(self, 'alerts_container'):
#                     self._refresh_alerts()
#             except Exception as e:
#                 logger.error(f"Auto-refresh alerts error: {e}")
        
#         ui.timer(90.0, refresh_alerts)
        
#         # Refresh security logs every 120 seconds
#         def refresh_security():
#             try:
#                 if hasattr(self, 'security_metrics_container'):
#                     self._refresh_security_logs()
#             except Exception as e:
#                 logger.error(f"Auto-refresh security error: {e}")
        
#         ui.timer(120.0, refresh_security)
        
#         logger.info("Auto-refresh timers started: Monitoring (60s), Alerts (90s), Security (120s)")
    
#     def _pause_current_operation(self):
#         """Pause current content operation when timer is low"""
#         if not self.operation_paused and self.current_operation:
#             self.operation_paused = True
            
#             # Save paused task
#             paused_task = {
#                 'id': len(self.paused_tasks) + 1,
#                 'type': self.current_operation.get('type', 'Analysis'),
#                 'content_preview': self.current_operation.get('content', '')[:50] + '...',
#                 'paused_at': datetime.now(),
#                 'status': 'Paused',
#                 'progress': self.current_operation.get('progress', 0)
#             }
#             self.paused_tasks.append(paused_task)
            
#             ui.notify('Operation paused due to low session time. Please extend session to continue.', type='warning')
            
#             # Show resume dialog
#             self._show_resume_dialog()
    
#     def _show_resume_dialog(self):
#         """Show dialog to resume paused operation"""
#         with ui.dialog() as resume_dialog, ui.card().classes('w-96'):
#             ui.label('Operation Paused').classes('text-xl font-bold mb-4')
#             ui.label('Your session time is running low. Would you like to extend your session and resume?').classes('text-sm mb-4')
            
#             with ui.row().classes('w-full justify-end gap-2'):
#                 ui.button('Cancel', on_click=resume_dialog.close).props('flat')
#                 ui.button(
#                     'Extend & Resume',
#                     on_click=lambda: self._extend_session(resume_dialog)
#                 ).props('color=primary')
        
#         resume_dialog.open()
    
#     def _extend_session(self, dialog):
#         """Extend session by 30 minutes"""
#         self.session_start_time = datetime.now()
#         self.operation_paused = False
#         dialog.close()
#         ui.notify('Session extended by 30 minutes', type='positive')
    
#     def _toggle_theme_old(self):
        
#         if self.dark_mode:
#             ui.run_javascript('document.body.classList.add("dark-mode")')
#             self.theme_toggle.props('icon=light_mode')
#         else:
#             ui.run_javascript('document.body.classList.remove("dark-mode")')
#             self.theme_toggle.props('icon=dark_mode')
    
#     def _show_profile_dialog(self):
#         """Show user profile dialog with functional features"""
#         # Get username from session
#         username = app.storage.general.get('username', 'demo')
        
#         with ui.dialog() as profile_dialog, ui.card().classes('w-[500px]'):
#             with ui.row().classes('w-full items-center mb-4'):
#                 ui.icon('account_circle', size='xl').classes('text-amber-900')
#                 ui.label(self.t('user_profile')).classes('text-2xl font-bold ml-2')
            
#             ui.separator()
            
#             with ui.column().classes('w-full gap-4 mt-4'):
#                 # Username
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('person').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('username')).classes('text-sm text-gray-600')
#                         ui.label(username).classes('text-lg font-semibold')
                
#                 # Email
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('email').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('email')).classes('text-sm text-gray-600')
#                         ui.label(f'{username}@ashoka.ai').classes('text-lg font-semibold')
                
#                 # Role
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('badge').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('role')).classes('text-sm text-gray-600')
#                         ui.label('Content Creator').classes('text-lg font-semibold')
                
#                 # Member Since
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('calendar_today').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('member_since')).classes('text-sm text-gray-600')
#                         ui.label('February 2026').classes('text-lg font-semibold')
                
#                 ui.separator().classes('my-3')
                
#                 # Session Info
#                 ui.label('Session Information').classes('text-md font-semibold mb-2')
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('access_time').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label('Session Started').classes('text-sm text-gray-600')
#                         ui.label(self.session_start_time.strftime('%I:%M %p')).classes('text-md')
                
#                 # Activity Stats
#                 ui.separator().classes('my-3')
#                 ui.label('Activity Statistics').classes('text-md font-semibold mb-2')
#                 with ui.grid(columns=2).classes('w-full gap-3'):
#                     with ui.card().classes('p-3 text-center'):
#                         ui.label('Content Analyzed').classes('text-xs text-gray-600')
#                         ui.label('24').classes('text-2xl font-bold text-blue-600')
#                     with ui.card().classes('p-3 text-center'):
#                         ui.label('Transformations').classes('text-xs text-gray-600')
#                         ui.label('18').classes('text-2xl font-bold text-purple-600')
#                     with ui.card().classes('p-3 text-center'):
#                         ui.label('Paused Tasks').classes('text-xs text-gray-600')
#                         ui.label(str(len(self.paused_tasks))).classes('text-2xl font-bold text-orange-600')
#                     with ui.card().classes('p-3 text-center'):
#                         ui.label('Alerts Viewed').classes('text-xs text-gray-600')
#                         ui.label('12').classes('text-2xl font-bold text-green-600')
            
#             ui.separator().classes('mt-4')
            
#             with ui.row().classes('w-full justify-end mt-4'):
#                 ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
#         profile_dialog.open()
    
#     def _show_settings_dialog_old(self):
#         """Show user profile dialog"""
#         with ui.dialog() as profile_dialog, ui.card().classes('w-96'):
#             with ui.row().classes('w-full items-center mb-4'):
#                 ui.icon('account_circle', size='xl').classes('text-amber-900')
#                 ui.label(self.t('user_profile')).classes('text-2xl font-bold ml-2')
            
#             ui.separator()
            
#             with ui.column().classes('w-full gap-4 mt-4'):
#                 # Username
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('person').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('username')).classes('text-sm text-gray-600')
#                         ui.label('demo').classes('text-lg font-semibold')
                
#                 # Email
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('email').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('email')).classes('text-sm text-gray-600')
#                         ui.label('demo@ashoka.ai').classes('text-lg font-semibold')
                
#                 # Role
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('badge').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('role')).classes('text-sm text-gray-600')
#                         ui.label('Content Creator').classes('text-lg font-semibold')
                
#                 # Member Since
#                 with ui.row().classes('w-full items-center'):
#                     ui.icon('calendar_today').classes('text-gray-600')
#                     with ui.column().classes('ml-3'):
#                         ui.label(self.t('member_since')).classes('text-sm text-gray-600')
#                         ui.label('February 2026').classes('text-lg font-semibold')
            
#             ui.separator().classes('mt-4')
            
#             with ui.row().classes('w-full justify-end mt-4'):
#                 ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
#         profile_dialog.open()
    
#     def _show_settings_dialog(self):
#         """Show settings dialog with functional features"""
#         with ui.dialog() as settings_dialog, ui.card().classes('w-[500px]'):
#             with ui.row().classes('w-full items-center mb-4'):
#                 ui.icon('settings', size='xl').classes('text-amber-900')
#                 ui.label('Settings & Preferences').classes('text-2xl font-bold ml-2')
            
#             ui.separator()
            
#             with ui.column().classes('w-full gap-4 mt-4'):
#                 # Language Settings
#                 ui.label('Language').classes('text-lg font-semibold')
#                 language_select = ui.select(
#                     ['English', 'Hindi', 'Kannada', 'Tamil'],
#                     value=self.current_language,
#                     label='Select Language'
#                 ).classes('w-full')
                
#                 ui.separator().classes('my-3')
                
#                 # Notification Settings
#                 ui.label('Notifications').classes('text-lg font-semibold')
#                 notif_enabled = ui.checkbox(
#                     'Enable notifications',
#                     value=self.user_preferences.get('notifications', True)
#                 )
#                 email_alerts = ui.checkbox(
#                     'Email alerts for critical issues',
#                     value=self.user_preferences.get('email_alerts', False)
#                 )
                
#                 ui.separator().classes('my-3')
                
#                 # Auto-save Settings
#                 ui.label('Content Management').classes('text-lg font-semibold')
#                 auto_save = ui.checkbox(
#                     'Auto-save content drafts',
#                     value=self.user_preferences.get('auto_save', True)
#                 )
                
#                 ui.separator().classes('my-3')
                
#                 # Session Settings
#                 ui.label('Session').classes('text-lg font-semibold')
#                 session_timeout = ui.select(
#                     [15, 30, 60, 120],
#                     value=self.user_preferences.get('session_timeout', 30),
#                     label='Session timeout (minutes)'
#                 ).classes('w-full')
                
#                 ui.separator().classes('my-3')
                
#                 # Paused Tasks
#                 ui.label('Paused Tasks').classes('text-lg font-semibold')
#                 ui.label(f'You have {len(self.paused_tasks)} paused tasks').classes('text-sm text-gray-600')
#                 if self.paused_tasks:
#                     ui.button(
#                         'View Paused Tasks',
#                         icon='pause_circle',
#                         on_click=lambda: self._show_paused_tasks_dialog()
#                     ).props('flat color=primary').classes('w-full')
            
#             ui.separator().classes('mt-4')
            
#             with ui.row().classes('w-full justify-end gap-2 mt-4'):
#                 ui.button('Cancel', on_click=settings_dialog.close).props('flat')
#                 ui.button(
#                     'Save Settings',
#                     on_click=lambda: self._save_settings(
#                         language_select.value,
#                         notif_enabled.value,
#                         email_alerts.value,
#                         auto_save.value,
#                         session_timeout.value,
#                         settings_dialog
#                     )
#                 ).props('color=primary')
        
#         settings_dialog.open()
    
#     def _save_settings(self, language, notifications, email_alerts, auto_save, session_timeout, dialog):
#         """Save user settings"""
#         # Update preferences
#         self.user_preferences['notifications'] = notifications
#         self.user_preferences['email_alerts'] = email_alerts
#         self.user_preferences['auto_save'] = auto_save
#         self.user_preferences['session_timeout'] = session_timeout
        
#         # Update session duration if changed
#         if session_timeout != self.session_duration // 60:
#             self.session_duration = session_timeout * 60
#             self.session_start_time = datetime.now()
        
#         # Change language if different
#         if language != self.current_language:
#             self._change_language(language, dialog)
#         else:
#             ui.notify('Settings saved successfully', type='positive')
#             dialog.close()
    
#     def _show_paused_tasks_dialog(self):
#         """Show paused tasks with date filters"""
#         with ui.dialog() as tasks_dialog, ui.card().classes('w-[800px]'):
#             with ui.row().classes('w-full items-center justify-between mb-4'):
#                 ui.label('Paused Content Tasks').classes('text-2xl font-bold')
#                 ui.button(icon='close', on_click=tasks_dialog.close).props('flat round')
            
#             ui.separator()
            
#             # Date filter
#             with ui.row().classes('w-full items-center gap-2 my-4'):
#                 ui.label('Filter:').classes('font-medium')
#                 date_filter = ui.select(
#                     ['Last Week', 'Last 15 Days', 'Last 30 Days', 'Last 3 Months', 'Last 6 Months', 'Last Year'],
#                     value='Last 30 Days',
#                     label='Time Period'
#                 ).classes('w-48')
#                 ui.button(
#                     'Apply Filter',
#                     icon='filter_list',
#                     on_click=lambda: self._filter_paused_tasks(date_filter.value, tasks_container)
#                 ).props('flat')
            
#             # Tasks table
#             tasks_container = ui.column().classes('w-full')
#             self._display_paused_tasks(tasks_container, 'Last 30 Days')
        
#         tasks_dialog.open()
    
#     def _filter_paused_tasks(self, filter_value, container):
#         """Filter paused tasks by date range"""
#         self._display_paused_tasks(container, filter_value)
#         ui.notify(f'Filtered by: {filter_value}', type='info')
    
#     def _display_paused_tasks(self, container, filter_value):
#         """Display paused tasks table"""
#         container.clear()
        
#         # Calculate date range
#         now = datetime.now()
#         if filter_value == 'Last Week':
#             cutoff = now - timedelta(days=7)
#         elif filter_value == 'Last 15 Days':
#             cutoff = now - timedelta(days=15)
#         elif filter_value == 'Last 30 Days':
#             cutoff = now - timedelta(days=30)
#         elif filter_value == 'Last 3 Months':
#             cutoff = now - timedelta(days=90)
#         elif filter_value == 'Last 6 Months':
#             cutoff = now - timedelta(days=180)
#         else:  # Last Year
#             cutoff = now - timedelta(days=365)
        
#         # Filter tasks
#         filtered_tasks = [t for t in self.paused_tasks if t['paused_at'] >= cutoff]
        
#         with container:
#             if not filtered_tasks:
#                 ui.label('No paused tasks in this time period').classes('text-gray-500 text-center py-8')
#             else:
#                 # Table header - Lightish blue background
#                 with ui.row().classes('w-full table-header-blue p-3 font-semibold rounded-t'):
#                     ui.label('ID').classes('w-16')
#                     ui.label('Type').classes('w-32')
#                     ui.label('Content Preview').classes('flex-1')
#                     ui.label('Paused At').classes('w-40')
#                     ui.label('Progress').classes('w-24')
#                     ui.label('Actions').classes('w-32')
                
#                 # Table rows
#                 for task in filtered_tasks:
#                     with ui.row().classes('w-full p-3 border-b items-center'):
#                         ui.label(f"#{task['id']}").classes('w-16')
#                         ui.badge(task['type'], color='blue').classes('w-32')
#                         ui.label(task['content_preview']).classes('flex-1 text-sm')
#                         ui.label(task['paused_at'].strftime('%Y-%m-%d %H:%M')).classes('w-40 text-sm')
#                         ui.label(f"{task['progress']}%").classes('w-24')
#                         ui.button(
#                             'Resume',
#                             icon='play_arrow',
#                             on_click=lambda t=task: self._resume_task(t)
#                         ).props('flat dense color=green')
    
#     def _resume_task(self, task):
#         """Resume a paused task"""
#         # Remove from paused tasks
#         self.paused_tasks = [t for t in self.paused_tasks if t['id'] != task['id']]
        
#         # Reset operation state
#         self.operation_paused = False
#         self.current_operation = None
        
#         ui.notify(f"Task #{task['id']} resumed", type='positive')
    
#     def _change_language(self, language: str, dialog):
#         """Change platform language"""
#         self.current_language = language
        
#         # Store language preference in general storage (doesn't require secret)
#         app.storage.general['language'] = language
        
#         ui.notify(f'Language changed to {language}. Refreshing...', type='positive')
#         dialog.close()
        
#         # Reload the page to apply translations
#         ui.run_javascript('window.location.reload()')
    
#     def _create_overview_panel(self):
#         """Create overview dashboard panel with real metrics from database"""
#         ui.label(self.t('platform_overview')).classes('text-3xl font-bold mb-4')
        
#         # Fetch real metrics from database
#         metrics = self._get_dashboard_metrics()
        
#         # Paused Tasks Summary (if any)
#         if self.paused_tasks:
#             with ui.card().classes('w-full bg-orange-50 mb-4'):
#                 with ui.row().classes('w-full items-center justify-between'):
#                     with ui.row().classes('items-center gap-3'):
#                         ui.icon('pause_circle', size='lg').classes('text-orange-600')
#                         with ui.column():
#                             ui.label(f'{len(self.paused_tasks)} Paused Tasks').classes('text-lg font-semibold')
#                             ui.label('Resume your work from where you left off').classes('text-sm text-gray-600')
#                     ui.button(
#                         'View Tasks',
#                         icon='arrow_forward',
#                         on_click=self._show_paused_tasks_dialog
#                     ).props('flat color=orange')
        
#         # Key Metrics Row - Real data from database
#         with ui.row().classes('w-full gap-4 mb-6'):
#             self._create_metric_card(
#                 self.t('total_content'), 
#                 str(metrics['total_content']), 
#                 'description', 
#                 'text-blue-600', 
#                 f"+{metrics['content_this_week']} {self.t('this_week')}"
#             )
#             self._create_metric_card(
#                 self.t('quality_score'), 
#                 f"{metrics['avg_quality']:.1f}%", 
#                 'verified', 
#                 'text-green-600', 
#                 self.t('excellent') if metrics['avg_quality'] >= 85 else 'Good'
#             )
#             self._create_metric_card(
#                 self.t('risk_alerts'), 
#                 str(metrics['risk_alerts']), 
#                 'warning', 
#                 'text-orange-600', 
#                 f"{metrics['resolved_risks']} {self.t('resolved')}"
#             )
#             self._create_metric_card(
#                 self.t('ai_operations'), 
#                 str(metrics['ai_operations']), 
#                 'smart_toy', 
#                 'text-purple-600', 
#                 f"{metrics['success_rate']:.1f}% {self.t('success')}"
#             )
        
#         # Charts Row
#         with ui.row().classes('w-full gap-4 mb-6'):
#             # Content Processing Trend Chart - Real data
#             with ui.card().classes('flex-1'):
#                 ui.label('Content Processing Trend').classes('text-xl font-semibold mb-4')
                
#                 trend_data = metrics['content_trend']
#                 max_value = max(val for _, val in trend_data) if trend_data else 1
                
#                 with ui.column().classes('w-full gap-2'):
#                     for label, value in trend_data:
#                         with ui.row().classes('w-full items-center gap-3'):
#                             ui.label(label).classes('w-16 text-xs font-medium')
#                             bar_width = (value / max_value * 100) if max_value > 0 else 0
#                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
#                                 with ui.element('div').classes('bg-gradient-to-r from-purple-500 to-blue-500 h-full rounded').style(f'width: {bar_width}%'):
#                                     pass
#                             ui.label(str(value)).classes('w-12 text-xs font-bold text-purple-600')
            
#             # Sentiment Distribution - Real data
#             with ui.card().classes('flex-1'):
#                 ui.label('Sentiment Distribution').classes('text-xl font-semibold mb-4')
                
#                 sentiment_data = metrics['sentiment_distribution']
                
#                 with ui.column().classes('w-full gap-3'):
#                     for label, percentage, color in sentiment_data:
#                         with ui.column().classes('w-full gap-1'):
#                             with ui.row().classes('w-full items-center justify-between'):
#                                 ui.label(label).classes('text-xs font-medium')
#                                 ui.label(f'{percentage}%').classes(f'text-xs font-bold text-{color}-600')
#                             ui.linear_progress(percentage / 100).props(f'color={color}').classes('h-2')
        
#         with ui.row().classes('w-full gap-4'):
#             # Recent Activity - Real data
#             with ui.card().classes('flex-1'):
#                 ui.label(self.t('recent_activity')).classes('text-xl font-semibold mb-4')
#                 with ui.column().classes('gap-2'):
#                     for activity in metrics['recent_activities']:
#                         self._create_activity_item(
#                             activity['title'],
#                             activity['description'],
#                             activity['time'],
#                             activity['icon'],
#                             activity['color']
#                         )
            
#             # System Health
#             with ui.card().classes('flex-1'):
#                 ui.label(self.t('system_health')).classes('text-xl font-semibold mb-4')
                
#                 ui.label(self.t('ai_model_performance')).classes('text-sm text-gray-600 mb-2')
#                 ui.linear_progress(0.95).classes('mb-4').props('color=green')
                
#                 ui.label(self.t('content_processing_rate')).classes('text-sm text-gray-600 mb-2')
#                 ui.linear_progress(metrics['processing_rate']).classes('mb-4').props('color=blue')
                
#                 ui.label(self.t('storage_utilization')).classes('text-sm text-gray-600 mb-2')
#                 ui.linear_progress(metrics['storage_utilization']).classes('mb-4').props('color=orange')
                
#                 with ui.row().classes('gap-2 mt-4'):
#                     ui.badge(self.t('api_healthy'), color='green')
#                     ui.badge(self.t('database_healthy'), color='green')
#                     ui.badge(self.t('ai_healthy'), color='green')
    
#     def _get_dashboard_metrics(self):
#         """Fetch real metrics from database"""
#         if not db_schema.conn:
#             db_schema.connect()
        
#         try:
#             # Total content count
#             total_content = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint
#             """).fetchone()[0]
            
#             # Content this week
#             content_this_week = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint
#                 WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
#             """).fetchone()[0]
            
#             # Average quality (based on sentiment confidence)
#             avg_quality_result = db_schema.conn.execute("""
#                 SELECT AVG(sentiment_confidence * 100) FROM ashoka_contentint
#                 WHERE sentiment_confidence IS NOT NULL
#             """).fetchone()[0]
#             avg_quality = avg_quality_result if avg_quality_result else 85.0
            
#             # Risk alerts (negative sentiment content)
#             risk_alerts = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint
#                 WHERE sentiment = 'negative'
#             """).fetchone()[0]
            
#             # Resolved risks (assuming older negative content is resolved)
#             resolved_risks = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint
#                 WHERE sentiment = 'negative' 
#                 AND created_at < CURRENT_DATE - INTERVAL '7 days'
#             """).fetchone()[0]
            
#             # AI operations (total analyses)
#             ai_operations = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint
#                 WHERE analyzed_at IS NOT NULL
#             """).fetchone()[0]
            
#             # Success rate (content with analysis)
#             success_rate = (ai_operations / total_content * 100) if total_content > 0 else 100.0
            
#             # Content trend (last 5 weeks)
#             trend_data = []
#             for i in range(4, -1, -1):
#                 week_start = f"CURRENT_DATE - INTERVAL '{i*7 + 7} days'"
#                 week_end = f"CURRENT_DATE - INTERVAL '{i*7} days'"
#                 count = db_schema.conn.execute(f"""
#                     SELECT COUNT(*) FROM ashoka_contentint
#                     WHERE created_at >= {week_start} AND created_at < {week_end}
#                 """).fetchone()[0]
#                 trend_data.append((f'Week {5-i}', count))
            
#             # Sentiment distribution
#             positive_count = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'positive'
#             """).fetchone()[0]
#             neutral_count = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'neutral'
#             """).fetchone()[0]
#             negative_count = db_schema.conn.execute("""
#                 SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'negative'
#             """).fetchone()[0]
            
#             total_sentiment = positive_count + neutral_count + negative_count
#             if total_sentiment > 0:
#                 sentiment_distribution = [
#                     ('Positive', int(positive_count / total_sentiment * 100), 'green'),
#                     ('Neutral', int(neutral_count / total_sentiment * 100), 'blue'),
#                     ('Negative', int(negative_count / total_sentiment * 100), 'red')
#                 ]
#             else:
#                 sentiment_distribution = [
#                     ('Positive', 33, 'green'),
#                     ('Neutral', 34, 'blue'),
#                     ('Negative', 33, 'red')
#                 ]
            
#             # Recent activities (last 5)
#             recent_activities = []
#             recent_content = db_schema.conn.execute("""
#                 SELECT content_type, sentiment, created_at, content_text
#                 FROM ashoka_contentint
#                 ORDER BY created_at DESC
#                 LIMIT 5
#             """).fetchall()
            
#             for content_type, sentiment, created_at, content_text in recent_content:
#                 time_diff = datetime.now() - created_at
#                 if time_diff.total_seconds() < 3600:
#                     time_str = f"{int(time_diff.total_seconds() / 60)} min ago"
#                 elif time_diff.total_seconds() < 86400:
#                     time_str = f"{int(time_diff.total_seconds() / 3600)} hour ago"
#                 else:
#                     time_str = f"{int(time_diff.days)} days ago"
                
#                 preview = content_text[:50] + '...' if content_text and len(content_text) > 50 else content_text or 'No content'
                
#                 if sentiment == 'negative':
#                     icon, color = 'warning', 'text-red-500'
#                     title = 'Risk detected'
#                 elif sentiment == 'positive':
#                     icon, color = 'check_circle', 'text-green-500'
#                     title = 'Content analyzed'
#                 else:
#                     icon, color = 'info', 'text-blue-500'
#                     title = 'Content processed'
                
#                 recent_activities.append({
#                     'title': title,
#                     'description': preview,
#                     'time': time_str,
#                     'icon': icon,
#                     'color': color
#                 })
            
#             # If no activities, show placeholder
#             if not recent_activities:
#                 recent_activities = [{
#                     'title': 'No recent activity',
#                     'description': 'Start analyzing content to see activity',
#                     'time': 'Now',
#                     'icon': 'info',
#                     'color': 'text-gray-500'
#                 }]
            
#             # Processing rate (based on content with analysis)
#             processing_rate = success_rate / 100
            
#             # Storage utilization (estimate based on file sizes)
#             storage_result = db_schema.conn.execute("""
#                 SELECT SUM(file_size_mb) FROM ashoka_contentint
#                 WHERE file_size_mb IS NOT NULL
#             """).fetchone()[0]
#             storage_mb = storage_result if storage_result else 0
#             storage_utilization = min(storage_mb / 1000, 0.95)  # Assume 1GB limit
            
#             return {
#                 'total_content': total_content,
#                 'content_this_week': content_this_week,
#                 'avg_quality': avg_quality,
#                 'risk_alerts': risk_alerts,
#                 'resolved_risks': resolved_risks,
#                 'ai_operations': ai_operations,
#                 'success_rate': success_rate,
#                 'content_trend': trend_data,
#                 'sentiment_distribution': sentiment_distribution,
#                 'recent_activities': recent_activities,
#                 'processing_rate': processing_rate,
#                 'storage_utilization': storage_utilization
#             }
            
#         except Exception as e:
#             logger.error(f"Error fetching dashboard metrics: {e}")
#             # Return default values on error
#             return {
#                 'total_content': 0,
#                 'content_this_week': 0,
#                 'avg_quality': 85.0,
#                 'risk_alerts': 0,
#                 'resolved_risks': 0,
#                 'ai_operations': 0,
#                 'success_rate': 100.0,
#                 'content_trend': [(f'Week {i}', 0) for i in range(1, 6)],
#                 'sentiment_distribution': [
#                     ('Positive', 33, 'green'),
#                     ('Neutral', 34, 'blue'),
#                     ('Negative', 33, 'red')
#                 ],
#                 'recent_activities': [{
#                     'title': 'No recent activity',
#                     'description': 'Start analyzing content to see activity',
#                     'time': 'Now',
#                     'icon': 'info',
#                     'color': 'text-gray-500'
#                 }],
#                 'processing_rate': 0.78,
#                 'storage_utilization': 0.10
#             }
    
#     def _create_content_intelligence_panel(self):
#         """Create content intelligence panel"""
#         ui.label('Content Intelligence & Analysis').classes('text-3xl font-bold mb-4')
        
#         with ui.row().classes('w-full gap-4'):
#             # Input Section
#             with ui.card().classes('flex-1'):
#                 ui.label('Submit Content for Analysis').classes('text-xl font-semibold mb-4')
                
#                 # Tab selector for input type with modern icons
#                 with ui.tabs().classes('w-full') as input_tabs:
#                     text_tab = ui.tab('TEXT', icon='article')
#                     image_tab = ui.tab('IMAGE', icon='photo')
#                     video_tab = ui.tab('VIDEO', icon='movie')
#                     document_tab = ui.tab('DOCUMENT', icon='description')
                
#                 with ui.tab_panels(input_tabs, value=text_tab).classes('w-full'):
#                     # Text input panel
#                     with ui.tab_panel(text_tab):
#                         self.content_input = ui.textarea(
#                             label='Enter your content',
#                             placeholder='Paste your content here for AI-powered analysis...'
#                         ).classes('w-full').props('rows=10')
                        
#                         with ui.row().classes('gap-2 mt-4'):
#                             ui.button(
#                                 'Analyze Text',
#                                 icon='psychology',
#                                 on_click=lambda: self._analyze_content(self.content_input.value)
#                             ).props('color=primary')
#                             ui.button('Clear', icon='clear', on_click=lambda: self.content_input.set_value('')).props('flat')
                    
#                     # Image upload panel
#                     with ui.tab_panel(image_tab):
#                         ui.label('Upload an image to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                        
#                         # Image preview container
#                         self.image_preview_container = ui.column().classes('w-full mb-4')
                        
#                         # Upload button
#                         ui.upload(
#                             label='Choose Image',
#                             on_upload=self._handle_image_upload,
#                             auto_upload=True
#                         ).props('accept="image/*"').classes('w-full')
                        
#                         ui.label('Supported formats: JPG, PNG, GIF, WEBP').classes('text-xs text-gray-500 mt-2')
                    
#                     # Video upload panel
#                     with ui.tab_panel(video_tab):
#                         ui.label('Upload a video to extract transcription and analyze content').classes('text-sm text-gray-600 mb-3')
                        
#                         # Video preview container
#                         self.video_preview_container = ui.column().classes('w-full mb-4')
                        
#                         # Upload button
#                         ui.upload(
#                             label='Choose Video',
#                             on_upload=self._handle_video_upload,
#                             auto_upload=True
#                         ).props('accept="video/*"').classes('w-full')
                        
#                         ui.label('Supported formats: MP4, MOV, AVI, WEBM').classes('text-xs text-gray-500 mt-2')
                    
#                     # Document upload panel
#                     with ui.tab_panel(document_tab):
#                         ui.label('Upload a document to extract and analyze text').classes('text-sm text-gray-600 mb-3')
                        
#                         # Document preview container
#                         self.document_preview_container = ui.column().classes('w-full mb-4')
                        
#                         # Upload button
#                         ui.upload(
#                             label='Choose Document',
#                             on_upload=self._handle_document_upload,
#                             auto_upload=True
#                         ).props('accept=".pdf,.docx,.txt,.md"').classes('w-full')
                        
#                         ui.label('Supported formats: PDF, DOCX, TXT, MD').classes('text-xs text-gray-500 mt-2')
            
#             # Analysis Results
#             with ui.card().classes('flex-1'):
#                 ui.label('Analysis Results').classes('text-xl font-semibold mb-4')
                
#                 self.analysis_container = ui.column().classes('w-full gap-3')
#                 with self.analysis_container:
#                     ui.label('Submit content to see analysis results').classes('text-gray-500 text-center py-8')
        
#         # AI Content Generator Section (moved here - right after Submit Content)
#         with ui.card().classes('w-full mt-4'):
#             ui.label('AI Content Generator').classes('text-2xl font-bold mb-4')
#             ui.label('Generate text, notes, or images using AI prompts').classes('text-sm text-gray-600 mb-4')
            
#             with ui.row().classes('w-full gap-4'):
#                 # Input Section
#                 with ui.card().classes('flex-1'):
#                     ui.label('Enter Your Prompt').classes('text-lg font-semibold mb-3')
                    
#                     # Generation type selector
#                     with ui.row().classes('items-center gap-4 mb-3'):
#                         ui.label('Generate:').classes('text-sm font-medium')
#                         self.gen_type = ui.radio(['Text/Notes', 'Image'], value='Text/Notes').props('inline')
                    
#                     # Prompt input
#                     self.generator_prompt = ui.textarea(
#                         label='Describe what you want to generate',
#                         placeholder='Example: Write a professional email about project updates...'
#                     ).classes('w-full').props('rows=6')
                    
#                     # Generate button
#                     ui.button(
#                         'Generate Content',
#                         icon='auto_awesome',
#                         on_click=self._generate_ai_content
#                     ).props('color=primary').classes('w-full mt-3')
                
#                 # Output Section
#                 with ui.card().classes('flex-1'):
#                     ui.label('Generated Content').classes('text-lg font-semibold mb-3')
                    
#                     self.generator_output_container = ui.column().classes('w-full')
#                     with self.generator_output_container:
#                         ui.label('Generated content will appear here').classes('text-gray-500 text-center py-8')
        
#         # Analysis & Generator History Section (renamed and combined - at the bottom)
#         with ui.card().classes('w-full mt-4'):
#             with ui.row().classes('items-center justify-between mb-4'):
#                 ui.label('Analysis & Generator History').classes('text-xl font-semibold')
#                 ui.label('History of analyzed and generated content - Click any row to preview').classes('text-sm text-gray-500')
            
#             self.history_table_container = ui.column().classes('w-full')
#             # Load initial history from database
#             self._update_history_table()
    
#     def _create_transform_panel(self):
#         """Create content transformation panel"""
#         ui.label('Multi-Platform Content Transformer').classes('text-3xl font-bold mb-4')
        
#         with ui.row().classes('w-full gap-4'):
#             # Input & Configuration Section
#             with ui.card().classes('w-2/5'):
#                 ui.label('Content & Settings').classes('text-xl font-semibold mb-4')
                
#                 # Content input
#                 ui.label('Original Content').classes('text-sm font-medium mb-2')
#                 self.transform_input = ui.textarea(
#                     label='Enter content to transform',
#                     placeholder='Paste your content here to transform it for multiple platforms...'
#                 ).classes('w-full').props('rows=8')
                
#                 ui.separator().classes('my-4')
                
#                 # Platform selection
#                 ui.label('Select Platforms').classes('text-sm font-medium mb-2')
#                 self.platform_linkedin = ui.checkbox('LinkedIn', value=True)
#                 self.platform_twitter = ui.checkbox('Twitter/X', value=True)
#                 self.platform_instagram = ui.checkbox('Instagram', value=False)
#                 self.platform_facebook = ui.checkbox('Facebook', value=False)
#                 self.platform_threads = ui.checkbox('Threads', value=False)
                
#                 ui.separator().classes('my-4')
                
#                 # Tone selection
#                 ui.label('Tone').classes('text-sm font-medium mb-2')
#                 self.tone_selector = ui.radio(
#                     ['Professional', 'Casual', 'Storytelling'],
#                     value='Professional'
#                 ).props('inline')
                
#                 ui.separator().classes('my-4')
                
#                 # Hashtag option
#                 self.include_hashtags = ui.checkbox('Include Hashtags', value=True)
                
#                 # Transform button
#                 ui.button(
#                     'Transform Content',
#                     icon='transform',
#                     on_click=self._transform_content
#                 ).props('color=primary').classes('w-full mt-4')
            
#             # Output Preview Section
#             with ui.card().classes('flex-1'):
#                 ui.label('Platform Outputs').classes('text-xl font-semibold mb-4')
                
#                 self.transform_results_container = ui.column().classes('w-full gap-2')
#                 with self.transform_results_container:
#                     ui.label('Configure settings and click "Transform Content" to see results').classes('text-gray-500 text-center py-8')
        
#         # Transform History Section
#         with ui.card().classes('w-full mt-4'):
#             ui.label('Transform History').classes('text-xl font-semibold mb-4')
#             ui.label('Click any row to load that transformation').classes('text-sm text-gray-600 mb-2')
            
#             self.transform_history_container = ui.column().classes('w-full')
#             self._update_transform_history()
    
#     def _create_monitoring_panel(self):
#         """Create monitoring dashboard panel"""
#         from src.services.monitoring_service import monitoring_service
        
#         with ui.column().classes('w-full gap-4'):
#             # Header with refresh button
#             with ui.row().classes('w-full items-center justify-between mb-2'):
#                 ui.label('Quality, Risk & Operations Monitoring').classes('text-3xl font-bold')
#                 ui.button(
#                     'Refresh Metrics',
#                     icon='refresh',
#                     on_click=self._refresh_monitoring_metrics
#                 ).props('flat color=primary')
            
#             # Performance Trend Chart
#             with ui.card().classes('w-full'):
#                 ui.label('Performance Trends (Last 24 Hours)').classes('text-xl font-semibold mb-4')
                
#                 # Mock hourly performance data
#                 hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00']
#                 success_rates = [98.5, 97.8, 99.2, 98.9, 99.5, 98.3, 99.1]
#                 max_rate = 100
                
#                 with ui.column().classes('w-full gap-2'):
#                     for hour, rate in zip(hours, success_rates):
#                         with ui.row().classes('w-full items-center gap-3'):
#                             ui.label(hour).classes('w-12 text-xs font-medium')
#                             bar_width = (rate / max_rate * 100)
#                             color = 'green' if rate >= 98 else 'orange' if rate >= 95 else 'red'
#                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
#                                 with ui.element('div').classes(f'bg-{color}-500 h-full rounded').style(f'width: {bar_width}%'):
#                                     pass
#                             ui.label(f'{rate}%').classes(f'w-12 text-xs font-bold text-{color}-600')
            
#             # Quality Metrics
#             with ui.card().classes('w-full'):
#                 ui.label('Quality Metrics').classes('text-xl font-semibold mb-4')
#                 self.quality_metrics_container = ui.row().classes('w-full gap-4')
            
#             # Risk Assessment
#             with ui.card().classes('w-full'):
#                 ui.label('Risk & Safety Assessment').classes('text-xl font-semibold mb-4')
#                 self.risk_metrics_container = ui.row().classes('w-full gap-4')
            
#             # Operations Metrics
#             with ui.card().classes('w-full'):
#                 ui.label('AI Operations Performance').classes('text-xl font-semibold mb-4')
#                 self.operations_metrics_container = ui.row().classes('w-full gap-4')
            
#             # System Health
#             with ui.card().classes('w-full'):
#                 ui.label('System Health').classes('text-xl font-semibold mb-4')
#                 self.system_health_container = ui.column().classes('w-full gap-3')
        
#         # Load initial metrics
#         self._refresh_monitoring_metrics()
    
#     def _refresh_monitoring_metrics(self):
#         """Refresh all monitoring metrics"""
#         from src.services.monitoring_service import monitoring_service
        
#         try:
#             # Get metrics
#             quality = monitoring_service.get_quality_metrics()
#             risk = monitoring_service.get_risk_metrics()
#             ops = monitoring_service.get_operations_metrics()
#             health = monitoring_service.get_system_health()
            
#             # Update Quality Metrics
#             self.quality_metrics_container.clear()
#             with self.quality_metrics_container:
#                 # Readability
#                 risk_class = 'risk-low' if quality.readability_score > 75 else 'risk-medium' if quality.readability_score > 60 else 'risk-high'
#                 color = 'green' if quality.readability_score > 75 else 'orange' if quality.readability_score > 60 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Readability Score').classes('text-sm text-gray-600')
#                     ui.label(f'{quality.readability_score:.1f}').classes(f'text-3xl font-bold text-{color}-600')
#                     change_icon = '↑' if quality.readability_change > 0 else '↓'
#                     ui.label(f'{change_icon} {abs(quality.readability_change):.1f} from baseline').classes(f'text-xs text-{color}-600')
                
#                 # Tone Consistency
#                 risk_class = 'risk-low' if quality.tone_consistency > 85 else 'risk-medium'
#                 color = 'green' if quality.tone_consistency > 85 else 'orange'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Tone Consistency').classes('text-sm text-gray-600')
#                     ui.label(f'{quality.tone_consistency:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(quality.tone_status).classes(f'text-xs text-{color}-600')
                
#                 # Duplicate Detection
#                 risk_class = 'risk-low' if quality.duplicate_count == 0 else 'risk-medium' if quality.duplicate_count < 3 else 'risk-high'
#                 color = 'green' if quality.duplicate_count == 0 else 'orange' if quality.duplicate_count < 3 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Duplicate Detection').classes('text-sm text-gray-600')
#                     ui.label(str(quality.duplicate_count)).classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(quality.duplicate_status).classes(f'text-xs text-{color}-600')
            
#             # Update Risk Metrics
#             self.risk_metrics_container.clear()
#             with self.risk_metrics_container:
#                 # Toxicity
#                 risk_class = 'risk-low' if risk.toxicity_score < 0.2 else 'risk-medium' if risk.toxicity_score < 0.3 else 'risk-high'
#                 color = 'green' if risk.toxicity_score < 0.2 else 'orange' if risk.toxicity_score < 0.3 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Toxicity Score').classes('text-sm text-gray-600')
#                     ui.label(f'{risk.toxicity_score:.2f}').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(risk.toxicity_level).classes(f'text-xs text-{color}-600')
                
#                 # Hate Speech
#                 risk_class = 'risk-low' if risk.hate_speech_count == 0 else 'risk-high'
#                 color = 'green' if risk.hate_speech_count == 0 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Hate Speech').classes('text-sm text-gray-600')
#                     ui.label('None' if risk.hate_speech_count == 0 else str(risk.hate_speech_count)).classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(risk.hate_speech_status).classes(f'text-xs text-{color}-600')
                
#                 # Backlash Risk
#                 risk_class = 'risk-low' if risk.backlash_risk == 'Low' else 'risk-medium' if risk.backlash_risk == 'Medium' else 'risk-high'
#                 color = 'green' if risk.backlash_risk == 'Low' else 'orange' if risk.backlash_risk == 'Medium' else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Backlash Risk').classes('text-sm text-gray-600')
#                     ui.label(risk.backlash_risk).classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(risk.backlash_status).classes(f'text-xs text-{color}-600')
            
#             # Update Operations Metrics
#             self.operations_metrics_container.clear()
#             with self.operations_metrics_container:
#                 # Success Rate
#                 risk_class = 'risk-low' if ops.success_rate > 95 else 'risk-medium' if ops.success_rate > 90 else 'risk-high'
#                 color = 'green' if ops.success_rate > 95 else 'orange' if ops.success_rate > 90 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Success Rate').classes('text-sm text-gray-600')
#                     ui.label(f'{ops.success_rate:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(f'{ops.total_operations:,} operations').classes('text-xs text-gray-600')
                
#                 # Latency
#                 risk_class = 'risk-low' if ops.avg_latency < 1.5 else 'risk-medium' if ops.avg_latency < 2.0 else 'risk-high'
#                 color = 'green' if ops.avg_latency < 1.5 else 'orange' if ops.avg_latency < 2.0 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Avg Latency').classes('text-sm text-gray-600')
#                     ui.label(f'{ops.avg_latency:.1f}s').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(ops.latency_status).classes(f'text-xs text-{color}-600')
                
#                 # Quality Drift
#                 risk_class = 'risk-low' if ops.quality_drift > 0 else 'risk-medium'
#                 color = 'green' if ops.quality_drift > 0 else 'orange'
#                 drift_sign = '+' if ops.quality_drift > 0 else ''
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Quality Drift').classes('text-sm text-gray-600')
#                     ui.label(f'{drift_sign}{ops.quality_drift:.1f}%').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(ops.drift_status).classes(f'text-xs text-{color}-600')
            
#             # Update System Health
#             self.system_health_container.clear()
#             with self.system_health_container:
#                 ui.label('Component Status').classes('text-sm font-medium mb-2')
#                 with ui.row().classes('gap-2 mb-4'):
#                     api_color = 'green' if health.api_status == 'Healthy' else 'orange'
#                     ui.badge(f'API: {health.api_status}', color=api_color)
                    
#                     db_color = 'green' if health.database_status == 'Healthy' else 'orange'
#                     ui.badge(f'Database: {health.database_status}', color=db_color)
                    
#                     ai_color = 'green' if health.ai_status == 'Healthy' else 'orange'
#                     ui.badge(f'AI: {health.ai_status}', color=ai_color)
                
#                 ui.label('Resource Utilization').classes('text-sm font-medium mb-2')
                
#                 ui.label(f'AI Model Performance: {health.model_performance:.1%}').classes('text-sm text-gray-600 mb-1')
#                 ui.linear_progress(health.model_performance).classes('mb-3')
                
#                 ui.label(f'Content Processing Rate: {health.processing_rate:.1%}').classes('text-sm text-gray-600 mb-1')
#                 ui.linear_progress(health.processing_rate).classes('mb-3')
                
#                 ui.label(f'Storage Utilization: {health.storage_usage:.1%}').classes('text-sm text-gray-600 mb-1')
#                 ui.linear_progress(health.storage_usage).classes('mb-3')
            
#             ui.notify('Metrics refreshed', type='positive')
            
#         except Exception as e:
#             logger.error(f"Error refreshing metrics: {e}")
#             ui.notify(f'Failed to refresh metrics: {str(e)}', type='negative')
    
#     def _create_alerts_panel(self):
#         """Create alerts panel"""
#         from src.services.monitoring_service import monitoring_service
        
#         with ui.column().classes('w-full gap-4'):
#             # Header with refresh button
#             with ui.row().classes('w-full items-center justify-between mb-2'):
#                 ui.label('Alerts & Notifications').classes('text-3xl font-bold')
#                 ui.button(
#                     'Refresh Alerts',
#                     icon='refresh',
#                     on_click=self._refresh_alerts
#                 ).props('flat color=primary')
            
#             # Filter buttons
#             with ui.row().classes('gap-2 mb-4'):
#                 self.alert_filter = ui.select(
#                     ['All', 'Critical', 'Warning', 'Info', 'Success'],
#                     value='All',
#                     label='Filter by type'
#                 ).classes('w-48')
                
#                 ui.button(
#                     'Apply Filter',
#                     icon='filter_list',
#                     on_click=self._refresh_alerts
#                 ).props('flat')
            
#             # Alert List
#             self.alerts_container = ui.column().classes('w-full gap-2')
        
#         # Load initial alerts
#         self._refresh_alerts()
    
#     def _refresh_alerts(self):
#         """Refresh alerts list"""
#         from src.services.monitoring_service import monitoring_service
        
#         try:
#             # Get alerts
#             alerts = monitoring_service.get_recent_alerts(limit=15)
            
#             # Filter if needed
#             filter_type = self.alert_filter.value.lower()
#             if filter_type != 'all':
#                 alerts = [a for a in alerts if a['type'] == filter_type]
            
#             # Display alerts
#             self.alerts_container.clear()
#             with self.alerts_container:
#                 if not alerts:
#                     ui.label('No alerts to display').classes('text-gray-500 text-center py-8')
#                 else:
#                     for alert in alerts:
#                         self._create_alert_card(
#                             alert['title'],
#                             alert['description'],
#                             alert['type'],
#                             alert['time_ago']
#                         )
            
#             ui.notify('Alerts refreshed', type='positive')
            
#         except Exception as e:
#             logger.error(f"Error refreshing alerts: {e}")
#             ui.notify(f'Failed to refresh alerts: {str(e)}', type='negative')
    
#     def _create_security_panel(self):
#         """Create security panel with login logs and security information"""
#         from src.services.security_service import security_service
        
#         with ui.column().classes('w-full gap-4'):
#             # Header
#             with ui.row().classes('w-full items-center justify-between mb-2'):
#                 ui.label('Security & Access Logs').classes('text-3xl font-bold')
#                 ui.button(
#                     'Refresh',
#                     icon='refresh',
#                     on_click=self._refresh_security_logs
#                 ).props('flat color=primary')
            
#             # Security Metrics Row
#             self.security_metrics_container = ui.row().classes('w-full gap-4 mb-4')
            
#             # Login Activity Chart
#             self.login_activity_chart_container = ui.card().classes('w-full')
            
#             # Login Logs Table
#             self.login_logs_container = ui.card().classes('w-full')
            
#             # Security Timeline
#             self.security_timeline_container = ui.card().classes('w-full')
            
#             # Security Recommendations
#             with ui.card().classes('w-full bg-blue-50'):
#                 with ui.row().classes('items-center gap-2 mb-3'):
#                     ui.icon('security', size='md').classes('text-blue-600')
#                     ui.label('Security Recommendations').classes('text-xl font-semibold')
                
#                 recommendations = [
#                     'Enable two-factor authentication for enhanced security',
#                     'Review and update your security questions',
#                     'Check connected devices and revoke unused sessions',
#                     'Enable email notifications for login attempts'
#                 ]
                
#                 with ui.column().classes('gap-2'):
#                     for i, rec in enumerate(recommendations, 1):
#                         with ui.row().classes('items-start gap-2'):
#                             ui.icon('check_circle').classes('text-blue-600 text-sm mt-1')
#                             ui.label(rec).classes('text-sm text-gray-700')
        
#         # Load initial data
#         self._refresh_security_logs()
    
#     def _refresh_security_logs(self):
#         """Refresh security logs with real data from DuckDB"""
#         from src.services.security_service import security_service
#         from datetime import datetime, timedelta
        
#         try:
#             # Get security metrics
#             active_sessions = security_service.get_active_sessions_count()
#             failed_logins = security_service.get_failed_login_count(24)
#             security_score = security_service.get_security_score()
            
#             # Update security metrics
#             self.security_metrics_container.clear()
#             with self.security_metrics_container:
#                 risk_class = 'risk-low' if active_sessions <= 2 else 'risk-medium'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Active Sessions').classes('text-sm text-gray-600')
#                     ui.label(str(active_sessions)).classes('text-3xl font-bold text-green-600')
#                     ui.label('Current user only').classes('text-xs text-gray-500')
                
#                 risk_class = 'risk-low' if failed_logins == 0 else 'risk-medium' if failed_logins < 5 else 'risk-high'
#                 color = 'green' if failed_logins == 0 else 'orange' if failed_logins < 5 else 'red'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Failed Login Attempts').classes('text-sm text-gray-600')
#                     ui.label(str(failed_logins)).classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label('Last 24 hours').classes('text-xs text-gray-500')
                
#                 risk_class = 'risk-low' if security_score >= 90 else 'risk-medium' if security_score >= 70 else 'risk-high'
#                 color = 'green' if security_score >= 90 else 'orange' if security_score >= 70 else 'red'
#                 status = 'Excellent' if security_score >= 90 else 'Good' if security_score >= 70 else 'Needs Attention'
#                 with ui.card().classes(f'flex-1 metric-card {risk_class}'):
#                     ui.label('Security Score').classes('text-sm text-gray-600')
#                     ui.label(f'{security_score:.0f}%').classes(f'text-3xl font-bold text-{color}-600')
#                     ui.label(status).classes('text-xs text-gray-500')
                
#                 with ui.card().classes('flex-1 metric-card risk-low'):
#                     ui.label('Last Password Change').classes('text-sm text-gray-600')
#                     ui.label('30d').classes('text-3xl font-bold text-blue-600')
#                     ui.label('Recommended: 90 days').classes('text-xs text-gray-500')
            
#             # Get login activity stats
#             login_stats = security_service.get_login_activity_stats(7)
            
#             # Update login activity chart
#             self.login_activity_chart_container.clear()
#             with self.login_activity_chart_container:
#                 ui.label('Login Activity (Last 7 Days)').classes('text-xl font-semibold mb-4')
                
#                 # Create day labels for last 7 days
#                 days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#                 today = datetime.now()
                
#                 # Build login data with actual counts
#                 login_data = []
#                 for i in range(7):
#                     date = (today - timedelta(days=6-i)).date()
#                     count = next((s['count'] for s in login_stats if s['date'] == date), 0)
#                     day_name = days[(today.weekday() - 6 + i) % 7]
#                     login_data.append((day_name, count))
                
#                 max_logins = max((count for _, count in login_data), default=1)
                
#                 with ui.column().classes('w-full gap-2'):
#                     for day, count in login_data:
#                         with ui.row().classes('w-full items-center gap-3'):
#                             ui.label(day).classes('w-12 text-sm font-medium')
#                             bar_width = (count / max_logins * 100) if max_logins > 0 else 0
#                             with ui.element('div').classes('flex-1 bg-gray-200 rounded h-8 relative'):
#                                 with ui.element('div').classes('bg-blue-500 h-full rounded').style(f'width: {bar_width}%'):
#                                     pass
#                             ui.label(str(count)).classes('w-8 text-sm font-bold text-blue-600')
            
#             # Get recent login logs
#             login_logs = security_service.get_recent_login_logs(10)
            
#             # Update login logs table
#             self.login_logs_container.clear()
#             with self.login_logs_container:
#                 ui.label('Recent Login Activity').classes('text-xl font-semibold mb-4')
                
#                 if not login_logs:
#                     ui.label('No login activity recorded yet').classes('text-gray-500 text-center py-8')
#                 else:
#                     # Table header - Lightish blue background
#                     with ui.row().classes('w-full table-header-blue p-3 font-semibold text-sm rounded-t'):
#                         ui.label('Timestamp').classes('w-40')
#                         ui.label('User').classes('w-24')
#                         ui.label('IP Address').classes('w-32')
#                         ui.label('Location').classes('w-32')
#                         ui.label('Device').classes('flex-1')
#                         ui.label('Status').classes('w-24')
                    
#                     # Table rows
#                     for log in login_logs:
#                         with ui.row().classes('w-full p-3 border-b items-center text-sm'):
#                             timestamp = log['timestamp']
#                             if isinstance(timestamp, str):
#                                 timestamp = datetime.fromisoformat(timestamp)
#                             ui.label(timestamp.strftime('%Y-%m-%d %H:%M:%S')).classes('w-40 text-gray-700')
#                             ui.label(log['username']).classes('w-24 font-medium')
#                             ui.label(log['ip_address']).classes('w-32 text-gray-600')
#                             ui.label(log['location']).classes('w-32 text-gray-600')
#                             ui.label(log['device_info']).classes('flex-1 text-gray-600')
                            
#                             status_color = 'green' if log['status'] == 'Success' else 'red'
#                             ui.badge(log['status'], color=status_color)
            
#             # Get recent security events
#             security_events = security_service.get_recent_security_events(5)
            
#             # Update security timeline
#             self.security_timeline_container.clear()
#             with self.security_timeline_container:
#                 ui.label('Security Events Timeline').classes('text-xl font-semibold mb-4')
                
#                 if not security_events:
#                     ui.label('No security events recorded yet').classes('text-gray-500 text-center py-8')
#                 else:
#                     # Map event types to icons and colors
#                     event_icons = {
#                         'login': ('login', 'green'),
#                         'password_verified': ('verified_user', 'blue'),
#                         'session_extended': ('schedule', 'orange'),
#                         'settings_updated': ('settings', 'purple'),
#                         'new_device': ('devices', 'blue')
#                     }
                    
#                     with ui.column().classes('w-full gap-3'):
#                         for event in security_events:
#                             icon, color = event_icons.get(event['event_type'], ('info', 'gray'))
                            
#                             # Calculate relative time
#                             event_time = event['timestamp']
#                             if isinstance(event_time, str):
#                                 event_time = datetime.fromisoformat(event_time)
#                             time_diff = datetime.now() - event_time
                            
#                             if time_diff.days > 0:
#                                 time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
#                             elif time_diff.seconds >= 3600:
#                                 hours = time_diff.seconds // 3600
#                                 time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
#                             else:
#                                 minutes = time_diff.seconds // 60
#                                 time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                            
#                             with ui.row().classes('items-center gap-3 p-3 hover:bg-gray-50 rounded'):
#                                 ui.icon(icon).classes(f'text-{color}-500 text-2xl')
#                                 with ui.column().classes('flex-1'):
#                                     ui.label(event['event_description']).classes('font-medium')
#                                     ui.label(time_ago).classes('text-xs text-gray-500')
#                                 ui.icon('chevron_right').classes('text-gray-400')
            
#             ui.notify('Security logs refreshed', type='positive')
            
#         except Exception as e:
#             logger.error(f"Error refreshing security logs: {e}")
#             ui.notify(f'Failed to refresh security logs: {str(e)}', type='negative')
    
#     def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str):
#         """Create a metric card"""
#         with ui.card().classes('flex-1 metric-card'):
#             with ui.row().classes('items-center justify-between'):
#                 with ui.column():
#                     ui.label(title).classes('text-sm text-gray-600')
#                     ui.label(value).classes(f'text-3xl font-bold {color}')
#                     ui.label(subtitle).classes('text-xs text-gray-500')
#                 ui.icon(icon).classes(f'{color} text-4xl')
    
#     def _create_activity_item(self, title: str, description: str, time: str, icon: str, color: str):
#         """Create an activity item"""
#         with ui.row().classes('items-center gap-3 p-2 hover:bg-gray-50 rounded'):
#             ui.icon(icon).classes(f'{color} text-2xl')
#             with ui.column().classes('flex-1'):
#                 ui.label(title).classes('font-medium')
#                 ui.label(description).classes('text-sm text-gray-600')
#             ui.label(time).classes('text-xs text-gray-400')
    
#     def _create_alert_card(self, title: str, message: str, severity: str, time: str):
#         """Create an alert card"""
#         color_map = {
#             'critical': 'border-red-500 bg-red-50',
#             'warning': 'border-orange-500 bg-orange-50',
#             'info': 'border-blue-500 bg-blue-50'
#         }
#         icon_map = {
#             'critical': 'error',
#             'warning': 'warning',
#             'info': 'info'
#         }
        
#         with ui.card().classes(f'w-full border-l-4 {color_map.get(severity, "border-gray-500")}'):
#             with ui.row().classes('items-start justify-between'):
#                 with ui.row().classes('items-start gap-3 flex-1'):
#                     ui.icon(icon_map.get(severity, 'info')).classes(f'text-2xl text-{severity}')
#                     with ui.column():
#                         ui.label(title).classes('font-semibold')
#                         ui.label(message).classes('text-sm text-gray-600')
#                         ui.label(time).classes('text-xs text-gray-400 mt-1')
#                 with ui.row().classes('gap-2'):
#                     ui.button(icon='visibility').props('flat dense')
#                     ui.button(icon='check').props('flat dense')
    
#     async def _analyze_content(self, content: str):
#         """Analyze content and display results (async to prevent UI blocking)"""
#         if not content or not content.strip():
#             ui.notify('Please enter content to analyze', type='warning')
#             return
        
#         # Track operation
#         self.current_operation = {
#             'type': 'Analysis',
#             'content': content,
#             'progress': 0
#         }
        
#         try:
#             # Show loading state with animation
#             self.analysis_container.clear()
#             with self.analysis_container:
#                 with ui.card().classes('w-full text-center p-8'):
#                     ui.spinner(size='xl', color='primary')
#                     ui.label('🤖 AI is analyzing your content...').classes('text-xl font-semibold mt-4')
#                     progress_label = ui.label('Ingesting content...').classes('text-sm text-gray-600 mt-2')
            
#             # Check if operation should be paused
#             if self.operation_paused:
#                 ui.notify('Operation paused. Please extend session to continue.', type='warning')
#                 return
            
#             # Ingest content (run in executor to not block UI)
#             import asyncio
#             import uuid
#             loop = asyncio.get_event_loop()
#             version = await loop.run_in_executor(
#                 None, 
#                 self.ingestion_service.ingest_text, 
#                 self.current_user, 
#                 content
#             )
#             self.current_operation['progress'] = 30
#             progress_label.set_text('Running AI analysis...')
            
#             # Analyze content (run in executor to not block UI)
#             analysis = await loop.run_in_executor(
#                 None,
#                 self.analyzer.analyze_content,
#                 version.version_id,
#                 content
#             )
#             self.current_analysis = analysis
#             self.current_operation['progress'] = 100
#             progress_label.set_text('Complete!')
            
#             # Store in ashoka_contentint table
#             content_id = str(uuid.uuid4())
#             word_count = len(content.split())
#             char_count = len(content)
            
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             db_schema.conn.execute("""
#                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, [
#                 content_id,
#                 self.current_user,
#                 'text',
#                 content,
#                 None,  # file_path
#                 None,  # file_name
#                 None,  # file_size_mb
#                 json.dumps({'source': 'text_input'}),
#                 analysis.summary,
#                 analysis.sentiment.classification,
#                 analysis.sentiment.confidence,
#                 json.dumps(analysis.keywords),
#                 json.dumps(analysis.topics),
#                 json.dumps(analysis.takeaways),
#                 word_count,
#                 char_count,
#                 None,  # quality_score (can be calculated later)
#                 datetime.now(),
#                 analysis.analyzed_at
#             ])
            
#             # Store in history
#             if not hasattr(self, 'analysis_history'):
#                 self.analysis_history = []
            
#             self.analysis_history.insert(0, {
#                 'timestamp': datetime.now(),
#                 'content': content[:100] + '...' if len(content) > 100 else content,
#                 'full_content': content,
#                 'analysis': analysis,
#                 'sentiment': analysis.sentiment.classification,
#                 'version_id': version.version_id,
#                 'content_id': content_id
#             })
            
#             # Keep only last 20 analyses
#             if len(self.analysis_history) > 20:
#                 self.analysis_history = self.analysis_history[:20]
            
#             # Update UI with results
#             self._display_analysis_results(analysis, content)
            
#             # Update history table if it exists
#             if hasattr(self, 'history_table_container'):
#                 self._update_history_table()
            
#             # Clear operation tracking
#             self.current_operation = None
            
#             ui.notify('✅ Content analyzed successfully!', type='positive')
            
#         except Exception as e:
#             logger.error(f"Analysis error: {e}")
#             self.analysis_container.clear()
#             with self.analysis_container:
#                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
#                     ui.icon('error', size='xl').classes('text-red-600')
#                     ui.label('Analysis Failed').classes('text-xl font-semibold text-red-600 mt-2')
#                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
#             ui.notify(f'Analysis failed: {str(e)}', type='negative')
#             self.current_operation = None

    
#     async def _transform_content(self):
#         """Transform content for multiple platforms (async to prevent UI blocking)"""
#         content = self.transform_input.value
        
#         if not content or not content.strip():
#             ui.notify('Please enter content to transform', type='warning')
#             return
        
#         # Get selected platforms
#         platforms = []
#         if self.platform_linkedin.value:
#             platforms.append('linkedin')
#         if self.platform_twitter.value:
#             platforms.append('twitter')
#         if self.platform_instagram.value:
#             platforms.append('instagram')
#         if self.platform_facebook.value:
#             platforms.append('facebook')
#         if self.platform_threads.value:
#             platforms.append('threads')
        
#         if not platforms:
#             ui.notify('Please select at least one platform', type='warning')
#             return
        
#         try:
#             # Show loading state with animation
#             self.transform_results_container.clear()
#             with self.transform_results_container:
#                 with ui.card().classes('w-full text-center p-8'):
#                     ui.spinner(size='xl', color='primary')
#                     ui.label('🔄 Transforming content for social media...').classes('text-xl font-semibold mt-4')
#                     progress_label = ui.label(f'Generating content for {len(platforms)} platforms...').classes('text-sm text-gray-600 mt-2')
            
#             # Get tone
#             tone = self.tone_selector.value.lower()
#             include_hashtags = self.include_hashtags.value
            
#             # Transform content (run in executor to not block UI)
#             import asyncio
#             loop = asyncio.get_event_loop()
#             results = await loop.run_in_executor(
#                 None,
#                 content_transformer.transform_for_platforms,
#                 content,
#                 platforms,
#                 tone,
#                 include_hashtags
#             )
            
#             # Store in database
#             import uuid
#             transform_id = str(uuid.uuid4())
            
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             # Store transformed content
#             db_schema.conn.execute("""
#                 INSERT INTO transform_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """, [
#                 transform_id,
#                 self.current_user,
#                 content,
#                 json.dumps(platforms),
#                 tone,
#                 include_hashtags,
#                 json.dumps({k: v.content if v else None for k, v in results.items()}),
#                 datetime.now()
#             ])
            
#             # Display results
#             self._display_transform_results(results)
            
#             # Update history table if it exists
#             if hasattr(self, 'transform_history_container'):
#                 self._update_transform_history()
            
#             ui.notify(f'✅ Content transformed for {len(platforms)} platforms!', type='positive')
            
#         except Exception as e:
#             logger.error(f"Transformation error: {e}")
#             self.transform_results_container.clear()
#             with self.transform_results_container:
#                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
#                     ui.icon('error', size='xl').classes('text-red-600')
#                     ui.label('Transformation Failed').classes('text-xl font-semibold text-red-600 mt-2')
#                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
#             ui.notify(f'Transformation failed: {str(e)}', type='negative')
    
#     def _display_transform_results(self, results: dict):
#         """Display transformation results for all platforms"""
#         self.transform_results_container.clear()
        
#         with self.transform_results_container:
#             for platform_key, platform_content in results.items():
#                 if platform_content is None:
#                     continue
                
#                 # Platform-specific styling
#                 platform_colors = {
#                     'LinkedIn': ('bg-blue-50', 'blue', 'work'),
#                     'Twitter/X': ('bg-sky-50', 'sky', 'chat'),
#                     'Instagram': ('bg-pink-50', 'pink', 'photo_camera'),
#                     'Facebook': ('bg-indigo-50', 'indigo', 'thumb_up'),
#                     'Threads': ('bg-purple-50', 'purple', 'forum')
#                 }
                
#                 bg_color, badge_color, icon = platform_colors.get(
#                     platform_content.platform,
#                     ('bg-gray-50', 'gray', 'share')
#                 )
                
#                 # Create expansion for each platform
#                 with ui.expansion(
#                     platform_content.platform,
#                     icon=icon
#                 ).classes('w-full mb-2'):
#                     with ui.card().classes(f'{bg_color} w-full'):
#                         # Metadata
#                         with ui.row().classes('items-center gap-2 mb-3'):
#                             ui.label(f"Tone: {platform_content.metadata.get('tone', 'N/A').title()}").classes('text-sm text-gray-600')
#                             ui.label('•').classes('text-gray-400')
#                             ui.label(f"Format: {platform_content.metadata.get('format', 'N/A').title()}").classes('text-sm text-gray-600')
                            
#                             # Tweet count for Twitter
#                             if 'tweet_count' in platform_content.metadata:
#                                 ui.label('•').classes('text-gray-400')
#                                 ui.label(f"{platform_content.metadata['tweet_count']} tweets").classes('text-sm text-gray-600')
                        
#                         # Content
#                         with ui.scroll_area().classes('h-64 w-full'):
#                             ui.label(platform_content.content).classes('text-gray-700 whitespace-pre-wrap')
                        
#                         # Stats
#                         with ui.row().classes('mt-4 gap-2 flex-wrap'):
#                             ui.badge(
#                                 f"{platform_content.character_count:,} characters",
#                                 color=badge_color
#                             )
                            
#                             limit_color = 'green' if platform_content.within_limit else 'red'
#                             limit_text = 'Within limit' if platform_content.within_limit else 'Exceeds limit'
#                             ui.badge(limit_text, color=limit_color)
                            
#                             if platform_content.hashtags:
#                                 ui.badge(
#                                     f"{len(platform_content.hashtags)} hashtags",
#                                     color='purple'
#                                 )
                        
#                         # Hashtags
#                         if platform_content.hashtags:
#                             ui.label('Hashtags:').classes('text-sm font-medium mt-3 mb-2')
#                             with ui.row().classes('gap-2 flex-wrap'):
#                                 for hashtag in platform_content.hashtags:
#                                     ui.chip(f'#{hashtag}', icon='tag').props(f'outline color={badge_color}').classes('text-xs')
                        
#                         # Copy button
#                         ui.button(
#                             'Copy to Clipboard',
#                             icon='content_copy',
#                             on_click=lambda c=platform_content.content: self._copy_to_clipboard(c)
#                         ).props('flat').classes('mt-3')
    
#     def _copy_to_clipboard(self, text: str):
#         """Copy text to clipboard"""
#         payload = json.dumps(text)
#         ui.run_javascript(
#             f"navigator.clipboard.writeText({payload}).then(() => {{ console.log('Copied to clipboard'); }});"
#         )
#         ui.notify('Copied to clipboard!', type='positive')
    
#     def _update_transform_history(self):
#         """Update transform history table"""
#         try:
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             # Get last 20 transformations
#             rows = db_schema.conn.execute("""
#                 SELECT id, original_content, platforms, tone, created_at, transformed_results
#                 FROM transform_history
#                 WHERE user_id = ?
#                 ORDER BY created_at DESC
#                 LIMIT 20
#             """, [self.current_user]).fetchall()
            
#             self.transform_history_container.clear()
            
#             if not rows:
#                 with self.transform_history_container:
#                     ui.label('No transform history yet').classes('text-gray-500 text-center py-4')
#                 return
            
#             with self.transform_history_container:
#                 # Create table
#                 columns = [
#                     {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'left', 'sortable': True},
#                     {'name': 'content', 'label': 'Original Content', 'field': 'content', 'align': 'left'},
#                     {'name': 'platforms', 'label': 'Platforms', 'field': 'platforms', 'align': 'left'},
#                     {'name': 'tone', 'label': 'Tone', 'field': 'tone', 'align': 'left'},
#                     {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'}
#                 ]
                
#                 table_rows = []
#                 for row in rows:
#                     transform_id, content, platforms_json, tone, created_at, results_json = row
                    
#                     # Parse platforms
#                     platforms_list = json.loads(platforms_json) if platforms_json else []
#                     platforms_str = ', '.join([p.title() for p in platforms_list])
                    
#                     # Truncate content preview
#                     content_preview = content[:80] + '...' if len(content) > 80 else content
                    
#                     table_rows.append({
#                         'id': transform_id,
#                         'timestamp': created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(created_at, 'strftime') else str(created_at),
#                         'content': content_preview,
#                         'platforms': platforms_str,
#                         'tone': tone.title(),
#                         'actions': transform_id,
#                         '_full_content': content,
#                         '_platforms': platforms_list,
#                         '_results': results_json
#                     })
                
#                 table = ui.table(
#                     columns=columns,
#                     rows=table_rows,
#                     row_key='id'
#                 ).classes('w-full')
                
#                 # Add custom slot for actions column
#                 table.add_slot('body-cell-actions', '''
#                     <q-td :props="props">
#                         <q-btn flat dense icon="visibility" color="primary" size="sm" @click="$parent.$emit('preview', props.row)" />
#                         <q-btn flat dense icon="folder_open" color="secondary" size="sm" @click="$parent.$emit('load', props.row)" />
#                     </q-td>
#                 ''')
                
#                 # Handle preview button click
#                 table.on('preview', lambda e: self._show_transform_preview_dialog(e.args))
                
#                 # Handle load button click
#                 table.on('load', lambda e: self._load_transform_from_history(e.args))
                
#         except Exception as e:
#             logger.error(f"Error updating transform history: {e}")
#             self.transform_history_container.clear()
#             with self.transform_history_container:
#                 ui.label(f'Error loading history: {str(e)}').classes('text-red-600')
    
#     def _show_transform_preview_dialog(self, row_data):
#         """Show transform preview in a dialog"""
#         try:
#             results_json = row_data.get('_results')
#             if not results_json:
#                 ui.notify('No results available', type='warning')
#                 return
            
#             results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
            
#             with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
#                 with ui.row().classes('w-full items-center justify-between mb-4'):
#                     ui.label('Transform Preview').classes('text-2xl font-bold')
#                     ui.button(icon='close', on_click=dialog.close).props('flat round')
                
#                 ui.label(f"Original: {row_data.get('_full_content', '')[:200]}...").classes('text-sm text-gray-600 mb-4')
                
#                 # Display each platform result
#                 with ui.scroll_area().classes('h-96 w-full'):
#                     for platform, content in results_dict.items():
#                         if content:
#                             with ui.card().classes('w-full mb-3 bg-gray-50'):
#                                 ui.label(platform.title()).classes('text-lg font-semibold mb-2')
#                                 ui.label(content).classes('text-gray-700 whitespace-pre-wrap')
                
#                 ui.button('Close', on_click=dialog.close).props('color=primary').classes('mt-4')
            
#             dialog.open()
            
#         except Exception as e:
#             logger.error(f"Error showing transform preview: {e}")
#             ui.notify(f'Error: {str(e)}', type='negative')
    
#     def _load_transform_from_history(self, row_data):
#         """Load a past transformation into the main view"""
#         try:
#             # Load original content
#             self.transform_input.value = row_data.get('_full_content', '')
            
#             # Load platforms
#             platforms = row_data.get('_platforms', [])
#             self.platform_linkedin.value = 'linkedin' in platforms
#             self.platform_twitter.value = 'twitter' in platforms
#             self.platform_instagram.value = 'instagram' in platforms
#             self.platform_facebook.value = 'facebook' in platforms
#             self.platform_threads.value = 'threads' in platforms
            
#             # Load tone
#             tone = row_data.get('tone', 'Professional')
#             self.tone_selector.value = tone.title()
            
#             # Load and display results
#             results_json = row_data.get('_results')
#             if results_json:
#                 results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
                
#                 # Convert dict to PlatformContent objects
#                 from src.services.content_transformer import PlatformContent
#                 results = {}
#                 for platform, content in results_dict.items():
#                     if content:
#                         results[platform] = PlatformContent(
#                             platform=platform.title(),
#                             content=content,
#                             character_count=len(content),
#                             within_limit=True,
#                             hashtags=[],
#                             metadata={'tone': tone, 'format': 'loaded'}
#                         )
                
#                 self._display_transform_results(results)
            
#             ui.notify(f'Loaded transformation from {row_data.get("timestamp")}', type='positive')
            
#         except Exception as e:
#             logger.error(f"Error loading transform from history: {e}")
#             ui.notify(f'Error: {str(e)}', type='negative')
    
#     def _handle_image_upload(self, e):
#         """Handle image file upload"""
#         try:
#             # Get uploaded file - handle both content types
#             if hasattr(e.content, 'read'):
#                 file_content = e.content.read()
#             else:
#                 file_content = e.content
#             filename = e.name
            
#             logger.info(f"Processing uploaded image: {filename}")
            
#             # Show loading
#             self.image_preview_container.clear()
#             with self.image_preview_container:
#                 ui.spinner(size='lg')
#                 ui.label('Processing image...').classes('text-center mt-2')
            
#             # Process image and extract text
#             extracted_text, file_path = file_processor.process_image(file_content, filename)
#             self.uploaded_file_path = file_path
            
#             # Store in ashoka_contentint table
#             import uuid
#             content_id = str(uuid.uuid4())
#             file_info = file_processor.get_file_info(file_path)
            
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             db_schema.conn.execute("""
#                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, [
#                 content_id,
#                 self.current_user,
#                 'image',
#                 extracted_text,
#                 file_path,
#                 filename,
#                 file_info.get('size_mb', 0),
#                 json.dumps({'format': file_info.get('format', 'unknown')}),
#                 None,  # summary (will be filled after analysis)
#                 None,  # sentiment
#                 None,  # sentiment_confidence
#                 None,  # keywords
#                 None,  # topics
#                 None,  # takeaways
#                 len(extracted_text.split()),
#                 len(extracted_text),
#                 None,  # quality_score
#                 datetime.now(),
#                 None  # analyzed_at (will be filled after analysis)
#             ])
            
#             # Show image preview
#             self.image_preview_container.clear()
#             with self.image_preview_container:
#                 with ui.card().classes('w-full'):
#                     ui.label('Uploaded Image:').classes('font-semibold mb-2')
#                     # Display image
#                     ui.image(file_path).classes('w-full max-h-64 object-contain')
                    
#                     # File info
#                     ui.label(f"File: {file_info.get('filename', 'Unknown')} ({file_info.get('size_mb', 0)} MB)").classes('text-sm text-gray-600 mt-2')
                
#                 with ui.card().classes('w-full bg-blue-50'):
#                     ui.label('Extracted Text:').classes('font-semibold mb-2')
#                     ui.label(extracted_text).classes('text-sm text-gray-700')
                
#                 ui.button(
#                     'Analyze Extracted Text',
#                     icon='psychology',
#                     on_click=lambda: self._analyze_content(extracted_text)
#                 ).props('color=primary').classes('w-full mt-2')
            
#             ui.notify(f'Image uploaded: {filename}', type='positive')
            
#         except Exception as e:
#             logger.error(f"Image upload error: {e}")
#             self.image_preview_container.clear()
#             with self.image_preview_container:
#                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
#             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
#     def _handle_video_upload(self, e):
#         """Handle video file upload"""
#         try:
#             # Get uploaded file - handle both content types
#             if hasattr(e.content, 'read'):
#                 file_content = e.content.read()
#             else:
#                 file_content = e.content
#             filename = e.name
            
#             logger.info(f"Processing uploaded video: {filename}")
            
#             # Show loading
#             self.video_preview_container.clear()
#             with self.video_preview_container:
#                 ui.spinner(size='lg')
#                 ui.label('Processing video...').classes('text-center mt-2')
            
#             # Process video and extract transcription
#             transcription, file_path, metadata = file_processor.process_video(file_content, filename)
#             self.uploaded_file_path = file_path
            
#             # Store in ashoka_contentint table
#             import uuid
#             content_id = str(uuid.uuid4())
#             file_info = file_processor.get_file_info(file_path)
            
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             db_schema.conn.execute("""
#                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, [
#                 content_id,
#                 self.current_user,
#                 'video',
#                 transcription,
#                 file_path,
#                 filename,
#                 file_info.get('size_mb', 0),
#                 json.dumps(metadata),
#                 None,  # summary (will be filled after analysis)
#                 None,  # sentiment
#                 None,  # sentiment_confidence
#                 None,  # keywords
#                 None,  # topics
#                 None,  # takeaways
#                 len(transcription.split()),
#                 len(transcription),
#                 None,  # quality_score
#                 datetime.now(),
#                 None  # analyzed_at (will be filled after analysis)
#             ])
            
#             # Show video preview
#             self.video_preview_container.clear()
#             with self.video_preview_container:
#                 with ui.card().classes('w-full'):
#                     ui.label('Uploaded Video:').classes('font-semibold mb-2')
                    
#                     # Display video player
#                     ui.video(file_path).classes('w-full max-h-64')
                    
#                     # File info
#                     file_info = file_processor.get_file_info(file_path)
#                     with ui.row().classes('gap-4 mt-2 text-sm text-gray-600'):
#                         ui.label(f"📁 {file_info.get('filename', 'Unknown')}")
#                         ui.label(f"💾 {file_info.get('size_mb', 0)} MB")
                
#                 # Video metadata
#                 with ui.card().classes('w-full bg-purple-50'):
#                     ui.label('Video Information:').classes('font-semibold mb-2')
#                     with ui.grid(columns=2).classes('gap-2 text-sm'):
#                         ui.label('Duration:').classes('font-medium')
#                         ui.label(metadata.get('duration', 'Unknown'))
#                         ui.label('Resolution:').classes('font-medium')
#                         ui.label(metadata.get('resolution', 'Unknown'))
#                         ui.label('FPS:').classes('font-medium')
#                         ui.label(str(metadata.get('fps', 'Unknown')))
#                         ui.label('Codec:').classes('font-medium')
#                         ui.label(metadata.get('codec', 'Unknown'))
                
#                 # Transcription
#                 with ui.card().classes('w-full bg-blue-50'):
#                     ui.label('Video Transcription:').classes('font-semibold mb-2')
#                     ui.label(transcription).classes('text-sm text-gray-700 whitespace-pre-wrap')
                
#                 ui.button(
#                     'Analyze Transcription',
#                     icon='psychology',
#                     on_click=lambda: self._analyze_content(transcription)
#                 ).props('color=primary').classes('w-full mt-2')
            
#             ui.notify(f'Video uploaded: {filename}', type='positive')
            
#         except Exception as e:
#             logger.error(f"Video upload error: {e}")
#             self.video_preview_container.clear()
#             with self.video_preview_container:
#                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
#             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
#     def _handle_document_upload(self, e):
#         """Handle document file upload"""
#         try:
#             # Get uploaded file - handle both content types
#             if hasattr(e.content, 'read'):
#                 file_content = e.content.read()
#             else:
#                 file_content = e.content
#             filename = e.name
            
#             logger.info(f"Processing uploaded document: {filename}")
            
#             # Show loading
#             self.document_preview_container.clear()
#             with self.document_preview_container:
#                 ui.spinner(size='lg')
#                 ui.label('Processing document...').classes('text-center mt-2')
            
#             # Process document and extract text
#             extracted_text, file_path, metadata = file_processor.process_document(file_content, filename)
#             self.uploaded_file_path = file_path
            
#             # Store in ashoka_contentint table
#             import uuid
#             content_id = str(uuid.uuid4())
#             file_info = file_processor.get_file_info(file_path)
            
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             db_schema.conn.execute("""
#                 INSERT INTO ashoka_contentint VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, [
#                 content_id,
#                 self.current_user,
#                 'document',
#                 extracted_text,
#                 file_path,
#                 filename,
#                 file_info.get('size_mb', 0),
#                 json.dumps(metadata),
#                 None,  # summary (will be filled after analysis)
#                 None,  # sentiment
#                 None,  # sentiment_confidence
#                 None,  # keywords
#                 None,  # topics
#                 None,  # takeaways
#                 len(extracted_text.split()),
#                 len(extracted_text),
#                 None,  # quality_score
#                 datetime.now(),
#                 None  # analyzed_at (will be filled after analysis)
#             ])
            
#             # Show document preview
#             self.document_preview_container.clear()
#             with self.document_preview_container:
#                 with ui.card().classes('w-full'):
#                     ui.label('Uploaded Document:').classes('font-semibold mb-2')
                    
#                     # File info
#                     file_info = file_processor.get_file_info(file_path)
#                     with ui.row().classes('gap-4 text-sm text-gray-600'):
#                         ui.label(f"📄 {file_info.get('filename', 'Unknown')}")
#                         ui.label(f"💾 {file_info.get('size_mb', 0)} MB")
                
#                 # Document metadata
#                 with ui.card().classes('w-full bg-indigo-50'):
#                     ui.label('Document Information:').classes('font-semibold mb-2')
#                     with ui.grid(columns=2).classes('gap-2 text-sm'):
#                         ui.label('Format:').classes('font-medium')
#                         ui.label(metadata.get('format', 'Unknown'))
#                         ui.label('Pages:').classes('font-medium')
#                         ui.label(str(metadata.get('pages', 'N/A')))
#                         ui.label('Words:').classes('font-medium')
#                         ui.label(f"{metadata.get('words', 0):,}")
#                         ui.label('Size:').classes('font-medium')
#                         ui.label(f"{metadata.get('size_kb', 0)} KB")
                
#                 # Extracted text
#                 with ui.card().classes('w-full bg-green-50'):
#                     ui.label('Extracted Text:').classes('font-semibold mb-2')
#                     with ui.scroll_area().classes('h-64 w-full'):
#                         ui.label(extracted_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                
#                 ui.button(
#                     'Analyze Document',
#                     icon='psychology',
#                     on_click=lambda: self._analyze_content(extracted_text)
#                 ).props('color=primary').classes('w-full mt-2')
            
#             ui.notify(f'Document uploaded: {filename}', type='positive')
            
#         except Exception as e:
#             logger.error(f"Document upload error: {e}")
#             self.document_preview_container.clear()
#             with self.document_preview_container:
#                 ui.label(f'Upload failed: {str(e)}').classes('text-red-600')
#             ui.notify(f'Upload failed: {str(e)}', type='negative')
    
#     def _display_analysis_results(self, analysis, content: str):
#         """Display comprehensive analysis results"""
#         self.analysis_container.clear()
#         with self.analysis_container:
#             # Summary Card
#             with ui.card().classes('w-full bg-blue-50'):
#                 with ui.row().classes('items-center gap-2 mb-2'):
#                     ui.icon('summarize', size='sm').classes('text-blue-600')
#                     ui.label('Summary').classes('font-semibold text-lg')
#                 ui.label(analysis.summary).classes('text-gray-700')
            
#             # Sentiment Card
#             with ui.card().classes('w-full'):
#                 with ui.row().classes('items-center gap-2 mb-2'):
#                     ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
#                     ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                
#                 sentiment_color = {
#                     'positive': 'green',
#                     'neutral': 'gray',
#                     'negative': 'red'
#                 }.get(analysis.sentiment.classification, 'gray')
                
#                 with ui.row().classes('items-center gap-3'):
#                     ui.badge(
#                         analysis.sentiment.classification.upper(),
#                         color=sentiment_color
#                     ).classes('text-lg px-4 py-2')
#                     ui.label(f'Confidence: {analysis.sentiment.confidence:.1%}').classes('text-sm text-gray-600')
                
#                 # Sentiment scores
#                 if analysis.sentiment.scores:
#                     ui.label('Detailed Scores:').classes('text-sm font-medium mt-3 mb-2')
#                     for emotion, score in analysis.sentiment.scores.items():
#                         with ui.row().classes('items-center gap-2 w-full'):
#                             ui.label(emotion.capitalize()).classes('text-sm w-20')
#                             ui.linear_progress(score).classes('flex-1')
#                             ui.label(f'{score:.1%}').classes('text-sm text-gray-600 w-12')
            
#             # Keywords Card
#             with ui.card().classes('w-full'):
#                 with ui.row().classes('items-center gap-2 mb-2'):
#                     ui.icon('label', size='sm').classes('text-purple-600')
#                     ui.label('Keywords').classes('font-semibold text-lg')
#                 with ui.row().classes('gap-2 flex-wrap'):
#                     for keyword in analysis.keywords[:15]:
#                         ui.badge(keyword, color='purple').classes('text-sm')
            
#             # Topics Card
#             with ui.card().classes('w-full'):
#                 with ui.row().classes('items-center gap-2 mb-2'):
#                     ui.icon('topic', size='sm').classes('text-orange-600')
#                     ui.label('Topics').classes('font-semibold text-lg')
#                 with ui.row().classes('gap-2'):
#                     for topic in analysis.topics:
#                         ui.chip(topic, icon='topic').props('outline color=orange')
            
#             # Takeaways Card
#             if analysis.takeaways:
#                 with ui.card().classes('w-full bg-green-50'):
#                     with ui.row().classes('items-center gap-2 mb-2'):
#                         ui.icon('lightbulb', size='sm').classes('text-green-600')
#                         ui.label('Key Takeaways').classes('font-semibold text-lg')
#                     with ui.column().classes('gap-2'):
#                         for i, takeaway in enumerate(analysis.takeaways, 1):
#                             with ui.row().classes('items-start gap-2'):
#                                 ui.label(f'{i}.').classes('font-bold text-green-600')
#                                 ui.label(takeaway).classes('text-gray-700')
            
#             # Metrics Card
#             with ui.card().classes('w-full'):
#                 with ui.row().classes('items-center gap-2 mb-2'):
#                     ui.icon('analytics', size='sm').classes('text-indigo-600')
#                     ui.label('Content Metrics').classes('font-semibold text-lg')
                
#                 word_count = len(content.split())
#                 char_count = len(content)
                
#                 with ui.grid(columns=3).classes('gap-4 w-full'):
#                     with ui.card().classes('text-center p-4'):
#                         ui.label(str(word_count)).classes('text-2xl font-bold text-indigo-600')
#                         ui.label('Words').classes('text-sm text-gray-600')
                    
#                     with ui.card().classes('text-center p-4'):
#                         ui.label(str(char_count)).classes('text-2xl font-bold text-indigo-600')
#                         ui.label('Characters').classes('text-sm text-gray-600')
                    
#                     with ui.card().classes('text-center p-4'):
#                         ui.label(str(len(analysis.keywords))).classes('text-2xl font-bold text-indigo-600')
#                         ui.label('Keywords').classes('text-sm text-gray-600')
    
#     def _update_history_table(self):
#         """Update the analysis history table from database"""
#         if not hasattr(self, 'history_table_container'):
#             return
        
#         self.history_table_container.clear()
        
#         # Load history from database
#         try:
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             history_data = db_schema.conn.execute("""
#                 SELECT id, content_text, sentiment, created_at, analyzed_at,
#                        summary, keywords, topics, takeaways, sentiment_confidence
#                 FROM ashoka_contentint
#                 WHERE analyzed_at IS NOT NULL
#                 ORDER BY analyzed_at DESC
#                 LIMIT 20
#             """).fetchall()
            
#             if not history_data:
#                 with self.history_table_container:
#                     ui.label('No analysis history yet').classes('text-gray-500 text-center py-4')
#                 return
            
#             with self.history_table_container:
#                 # Create table with clickable rows
#                 with ui.column().classes('w-full gap-2'):
#                     for row in history_data:
#                         content_id, content_text, sentiment, created_at, analyzed_at, summary, keywords_json, topics_json, takeaways_json, confidence = row
                        
#                         sentiment_color = {
#                             'positive': 'green',
#                             'neutral': 'gray',
#                             'negative': 'red'
#                         }.get(sentiment, 'gray')
                        
#                         sentiment_icon = {
#                             'positive': 'sentiment_satisfied',
#                             'neutral': 'sentiment_neutral',
#                             'negative': 'sentiment_dissatisfied'
#                         }.get(sentiment, 'sentiment_neutral')
                        
#                         content_preview = content_text[:100] + '...' if content_text and len(content_text) > 100 else content_text or 'No content'
                        
#                         with ui.card().classes('w-full hover:bg-gray-50'):
#                             with ui.row().classes('items-center gap-4 w-full'):
#                                 # Timestamp
#                                 with ui.column().classes('w-32'):
#                                     ui.label(analyzed_at.strftime('%Y-%m-%d')).classes('text-sm font-medium')
#                                     ui.label(analyzed_at.strftime('%H:%M:%S')).classes('text-xs text-gray-500')
                                
#                                 # Content preview
#                                 with ui.column().classes('flex-1'):
#                                     ui.label(content_preview).classes('text-sm text-gray-700 truncate')
                                
#                                 # Sentiment badge
#                                 with ui.row().classes('items-center gap-2 w-32'):
#                                     ui.icon(sentiment_icon, size='sm').classes(f'text-{sentiment_color}-600')
#                                     ui.badge(sentiment.upper(), color=sentiment_color).classes('text-xs')
                                
#                                 # Action buttons
#                                 with ui.row().classes('gap-2'):
#                                     # Preview button (eye icon) - opens dialog
#                                     ui.button(icon='visibility', on_click=lambda cid=content_id: self._show_analysis_preview_dialog(cid)).props('flat dense round').classes('text-blue-600').tooltip('Preview in dialog')
#                                     # Load button - loads into main view
#                                     ui.button(icon='open_in_full', on_click=lambda cid=content_id: self._load_analysis_from_history(cid)).props('flat dense round').classes('text-green-600').tooltip('Load into main view')
        
#         except Exception as e:
#             logger.error(f"Error loading history: {e}")
#             with self.history_table_container:
#                 ui.label('Error loading history').classes('text-red-500 text-center py-4')
    
#     def _load_analysis_from_history(self, content_id: str):
#         """Load and display an analysis from database history"""
#         try:
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             # Fetch the analysis from database
#             row = db_schema.conn.execute("""
#                 SELECT content_text, summary, sentiment, sentiment_confidence,
#                        keywords, topics, takeaways, analyzed_at
#                 FROM ashoka_contentint
#                 WHERE id = ?
#             """, [content_id]).fetchone()
            
#             if not row:
#                 ui.notify('Analysis not found', type='warning')
#                 return
            
#             content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at = row
            
#             # Parse JSON fields
#             keywords = json.loads(keywords_json) if keywords_json else []
#             topics = json.loads(topics_json) if topics_json else []
#             takeaways = json.loads(takeaways_json) if takeaways_json else []
            
#             # Reconstruct analysis object
#             from src.models.content import ContentAnalysis, Sentiment
            
#             analysis = ContentAnalysis(
#                 version_id=content_id,
#                 summary=summary,
#                 takeaways=takeaways,
#                 keywords=keywords,
#                 topics=topics,
#                 sentiment=Sentiment(
#                     classification=sentiment,
#                     confidence=confidence,
#                     scores={
#                         'positive': confidence if sentiment == 'positive' else 0.3,
#                         'neutral': confidence if sentiment == 'neutral' else 0.3,
#                         'negative': confidence if sentiment == 'negative' else 0.3
#                     }
#                 ),
#                 analyzed_at=analyzed_at
#             )
            
#             # Display the analysis results
#             self._display_analysis_results(analysis, content_text)
            
#         except Exception as e:
#             logger.error(f"Error loading analysis from history: {e}")
#             ui.notify(f'Error loading analysis: {str(e)}', type='negative')
    
#     def _show_analysis_preview_dialog(self, content_id: str):
#         """Show analysis preview in a dialog window"""
#         try:
#             if not db_schema.conn:
#                 db_schema.connect()
            
#             # Fetch the analysis from database
#             row = db_schema.conn.execute("""
#                 SELECT content_text, summary, sentiment, sentiment_confidence,
#                        keywords, topics, takeaways, analyzed_at, word_count, char_count
#                 FROM ashoka_contentint
#                 WHERE id = ?
#             """, [content_id]).fetchone()
            
#             if not row:
#                 ui.notify('Analysis not found', type='warning')
#                 return
            
#             content_text, summary, sentiment, confidence, keywords_json, topics_json, takeaways_json, analyzed_at, word_count, char_count = row
            
#             # Parse JSON fields
#             keywords = json.loads(keywords_json) if keywords_json else []
#             topics = json.loads(topics_json) if topics_json else []
#             takeaways = json.loads(takeaways_json) if takeaways_json else []
            
#             # Create dialog
#             with ui.dialog() as preview_dialog, ui.card().classes('w-[900px] max-h-[80vh]'):
#                 with ui.row().classes('w-full items-center justify-between mb-4'):
#                     ui.label('Analysis Preview').classes('text-2xl font-bold')
#                     ui.button(icon='close', on_click=preview_dialog.close).props('flat round dense')
                
#                 with ui.scroll_area().classes('w-full h-[60vh]'):
#                     with ui.column().classes('w-full gap-4 p-4'):
#                         # Metadata
#                         with ui.card().classes('w-full bg-gray-50'):
#                             with ui.row().classes('items-center gap-4'):
#                                 ui.icon('schedule', size='sm').classes('text-gray-600')
#                                 ui.label(f"Analyzed: {analyzed_at.strftime('%Y-%m-%d %H:%M:%S')}").classes('text-sm')
#                                 ui.label(f"Words: {word_count or len(content_text.split())}").classes('text-sm ml-4')
#                                 ui.label(f"Characters: {char_count or len(content_text)}").classes('text-sm ml-4')
                        
#                         # Original Content
#                         with ui.card().classes('w-full'):
#                             ui.label('Original Content').classes('text-lg font-semibold mb-2')
#                             with ui.scroll_area().classes('h-32 w-full'):
#                                 ui.label(content_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
#                         # Summary
#                         with ui.card().classes('w-full bg-blue-50'):
#                             with ui.row().classes('items-center gap-2 mb-2'):
#                                 ui.icon('summarize', size='sm').classes('text-blue-600')
#                                 ui.label('Summary').classes('font-semibold text-lg')
#                             ui.label(summary).classes('text-gray-700')
                        
#                         # Sentiment
#                         with ui.card().classes('w-full'):
#                             with ui.row().classes('items-center gap-2 mb-2'):
#                                 ui.icon('sentiment_satisfied', size='sm').classes('text-green-600')
#                                 ui.label('Sentiment Analysis').classes('font-semibold text-lg')
                            
#                             sentiment_color = {
#                                 'positive': 'green',
#                                 'neutral': 'gray',
#                                 'negative': 'red'
#                             }.get(sentiment, 'gray')
                            
#                             with ui.row().classes('items-center gap-3'):
#                                 ui.badge(sentiment.upper(), color=sentiment_color).classes('text-lg px-4 py-2')
#                                 ui.label(f'Confidence: {confidence:.1%}').classes('text-sm text-gray-600')
                        
#                         # Keywords
#                         if keywords:
#                             with ui.card().classes('w-full'):
#                                 with ui.row().classes('items-center gap-2 mb-2'):
#                                     ui.icon('label', size='sm').classes('text-purple-600')
#                                     ui.label('Keywords').classes('font-semibold text-lg')
#                                 with ui.row().classes('gap-2 flex-wrap'):
#                                     for keyword in keywords[:15]:
#                                         ui.badge(keyword, color='purple').classes('text-sm')
                        
#                         # Topics
#                         if topics:
#                             with ui.card().classes('w-full'):
#                                 with ui.row().classes('items-center gap-2 mb-2'):
#                                     ui.icon('topic', size='sm').classes('text-orange-600')
#                                     ui.label('Topics').classes('font-semibold text-lg')
#                                 with ui.row().classes('gap-2'):
#                                     for topic in topics:
#                                         ui.chip(topic, icon='topic').props('outline color=orange')
                        
#                         # Takeaways
#                         if takeaways:
#                             with ui.card().classes('w-full bg-green-50'):
#                                 with ui.row().classes('items-center gap-2 mb-2'):
#                                     ui.icon('lightbulb', size='sm').classes('text-green-600')
#                                     ui.label('Key Takeaways').classes('font-semibold text-lg')
#                                 with ui.column().classes('gap-2'):
#                                     for i, takeaway in enumerate(takeaways, 1):
#                                         with ui.row().classes('items-start gap-2'):
#                                             ui.label(f'{i}.').classes('font-bold text-green-600')
#                                             ui.label(takeaway).classes('text-gray-700')
            
#             preview_dialog.open()
            
#         except Exception as e:
#             logger.error(f"Error showing preview dialog: {e}")
#             ui.notify(f'Error showing preview: {str(e)}', type='negative')
    
#     async def _generate_ai_content(self):
#         """Generate content using AI based on user prompt"""
#         prompt = self.generator_prompt.value
#         gen_type = self.gen_type.value
        
#         if not prompt or not prompt.strip():
#             ui.notify('Please enter a prompt', type='warning')
#             return
        
#         try:
#             # Show loading
#             self.generator_output_container.clear()
#             with self.generator_output_container:
#                 with ui.card().classes('w-full text-center p-8'):
#                     ui.spinner(size='xl', color='primary')
#                     ui.label('🤖 AI is generating content...').classes('text-xl font-semibold mt-4')
#                     progress_label = ui.label('Processing your prompt...').classes('text-sm text-gray-600 mt-2')
            
#             # Generate content
#             import asyncio
#             loop = asyncio.get_event_loop()
            
#             if gen_type == 'Text/Notes':
#                 # Generate text content using Gemini
#                 generation_prompt = f"Generate professional content based on this prompt:\n\n{prompt}\n\nProvide a well-structured, detailed response."
                
#                 result = await loop.run_in_executor(
#                     None,
#                     gemini_client.generate_content,
#                     generation_prompt
#                 )
                
#                 generated_text = result.get('text', 'No content generated')
                
#                 # Display generated text
#                 self.generator_output_container.clear()
#                 with self.generator_output_container:
#                     with ui.card().classes('w-full'):
#                         with ui.row().classes('items-center justify-between mb-3'):
#                             ui.label('Generated Text').classes('text-lg font-semibold')
#                             ui.button(
#                                 icon='content_copy',
#                                 on_click=lambda: self._copy_to_clipboard(generated_text)
#                             ).props('flat dense round').tooltip('Copy to clipboard')
                        
#                         with ui.scroll_area().classes('h-96 w-full'):
#                             ui.label(generated_text).classes('text-sm text-gray-700 whitespace-pre-wrap')
                        
#                         # Action buttons
#                         with ui.row().classes('gap-2 mt-3'):
#                             ui.button(
#                                 'Analyze This Content',
#                                 icon='psychology',
#                                 on_click=lambda: self._analyze_content(generated_text)
#                             ).props('color=primary')
#                             ui.button(
#                                 'Use in Transformer',
#                                 icon='transform',
#                                 on_click=lambda: self._use_in_transformer(generated_text)
#                             ).props('flat')
                
#                 ui.notify('✅ Content generated successfully!', type='positive')
            
#             elif gen_type == 'Image':
#                 # Generate actual image using Hugging Face Inference Client
#                 progress_label.set_text('Generating image with AI...')
                
#                 from src.config import config
#                 from pathlib import Path
#                 import uuid
                
#                 # Check if token is available
#                 if not config.HUGGINGFACE_TOKEN:
#                     raise Exception("HUGGINGFACE_TOKEN not found in .env file")
                
#                 try:
#                     from huggingface_hub import InferenceClient
#                 except ImportError:
#                     raise Exception("huggingface_hub not installed. Run: pip install huggingface_hub")
                
#                 # Initialize Hugging Face Inference Client
#                 client = InferenceClient(token=config.HUGGINGFACE_TOKEN)
                
#                 # Generate image
#                 def generate_image(prompt_text):
#                     # Use text-to-image with the FLUX model
#                     image = client.text_to_image(
#                         prompt=prompt_text,
#                         model=config.HUGGINGFACE_MODEL
#                     )
#                     return image
                
#                 image = await loop.run_in_executor(None, generate_image, prompt)
                
#                 # Save image to uploads folder
#                 uploads_dir = Path("data/uploads")
#                 uploads_dir.mkdir(parents=True, exist_ok=True)
                
#                 image_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
#                 image_path = uploads_dir / image_filename
                
#                 # Save the PIL Image
#                 image.save(str(image_path))
                
#                 # Display generated image
#                 self.generator_output_container.clear()
#                 with self.generator_output_container:
#                     with ui.card().classes('w-full'):
#                         ui.label('Generated Image').classes('text-lg font-semibold mb-3')
                        
#                         # Display the image
#                         ui.image(str(image_path)).classes('w-full max-h-96 object-contain rounded')
                        
#                         # Image info
#                         with ui.row().classes('items-center gap-2 mt-3 text-sm text-gray-600'):
#                             ui.icon('info', size='sm')
#                             ui.label(f'Prompt: {prompt[:100]}{"..." if len(prompt) > 100 else ""}')
                        
#                         # Action buttons
#                         with ui.row().classes('gap-2 mt-3'):
#                             ui.button(
#                                 'Download Image',
#                                 icon='download',
#                                 on_click=lambda: ui.download(str(image_path), image_filename)
#                             ).props('color=primary')
#                             ui.button(
#                                 'Generate Another',
#                                 icon='refresh',
#                                 on_click=lambda: self.generator_prompt.set_value('')
#                             ).props('flat')
                
#                 ui.notify('✅ Image generated successfully!', type='positive')
        
#         except Exception as e:
#             logger.error(f"Generation error: {e}")
#             self.generator_output_container.clear()
#             with self.generator_output_container:
#                 with ui.card().classes('w-full text-center p-8 bg-red-50'):
#                     ui.icon('error', size='xl').classes('text-red-600')
#                     ui.label('Generation Failed').classes('text-xl font-semibold text-red-600 mt-2')
#                     ui.label(str(e)).classes('text-sm text-gray-700 mt-2')
                    
#                     if 'HUGGINGFACE_TOKEN' in str(e):
#                         ui.label('Make sure HUGGINGFACE_TOKEN is set in your .env file').classes('text-xs text-gray-600 mt-2')
#             ui.notify(f'Generation failed: {str(e)}', type='negative')
    
#     def _copy_to_clipboard(self, text: str):
#         """Copy text to clipboard"""
#         ui.run_javascript(f'navigator.clipboard.writeText({json.dumps(text)})')
#         ui.notify('Copied to clipboard!', type='positive')
    
#     def _use_in_transformer(self, text: str):
#         """Use generated text in the transformer"""
#         if hasattr(self, 'transform_input'):
#             self.transform_input.set_value(text)
#             ui.notify('Text loaded into transformer', type='info')
#         else:
#             ui.notify('Transformer not available', type='warning')
    
#     def _create_metric_card(self, title: str, value: str, icon: str, color: str, subtitle: str = ''):
#         """Create a metric card"""
#         with ui.card().classes('flex-1 dashboard-card'):
#             with ui.row().classes('items-center gap-3'):
#                 ui.icon(icon, size='lg').classes(color)
#                 with ui.column().classes('gap-1'):
#                     ui.label(title).classes('text-sm opacity-90')
#                     ui.label(value).classes('text-3xl font-bold')
#                     if subtitle:
#                         ui.label(subtitle).classes('text-xs opacity-75')
    
#     def _create_activity_item(self, title: str, description: str, time: str, icon: str, icon_color: str):
#         """Create an activity item"""
#         with ui.row().classes('items-start gap-3 p-3 content-card'):
#             ui.icon(icon, size='md').classes(icon_color)
#             with ui.column().classes('flex-1 gap-1'):
#                 ui.label(title).classes('font-semibold')
#                 ui.label(description).classes('text-sm text-gray-600')
#                 ui.label(time).classes('text-xs text-gray-500')


# def launch_dashboard():
#     """Launch the Ashoka dashboard"""
#     dashboard = AshokaGovDashboard()
#     dashboard.create_dashboard()
    
#     ui.run(
#         title='Ashoka - GenAI Governance Platform',
#         favicon='🛡️',
#         dark=False,
#         reload=False,
#         port=8080
#     )


# if __name__ in {"__main__", "__mp_main__"}:
#     launch_dashboard()


"""Ashoka GenAI Governance Dashboard - NiceGUI Implementation"""
from nicegui import ui, app
from datetime import datetime, timedelta
from typing import Optional
import json

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
        self.current_user_role = 'creator'
        self.current_username = 'demo'
        self.current_email = 'demo@ashoka.ai'
        self.current_analysis = None
        self.dark_mode = False
        self.uploaded_file_path = None
        
        # Analysis history for Content Intelligence
        self.analysis_history = []
        
        # Session management
        self.session_duration = 30 * 60  # 30 minutes in seconds
        self.session_start_time = datetime.now()
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
            'session_timeout': 30
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
                "title": "अशोक",
                "subtitle": "जेनएआई गवर्नेंस और ऑब्जर्वेबिलिटी प्लेटफॉर्म",
                "overview": "अवलोकन",
                "content_intelligence": "सामग्री बुद्धिमत्ता",
                "transform": "रूपांतरण",
                "monitoring": "निगरानी",
                "alerts": "अलर्ट",
                "security": "सुरक्षा",
                "profile": "प्रोफ़ाइल",
                "settings": "सेटिंग्स",
                "logout": "लॉगआउट",
                "user_profile": "उपयोगकर्ता प्रोफ़ाइल",
                "username": "उपयोगकर्ता नाम",
                "email": "ईमेल",
                "role": "भूमिका",
                "member_since": "सदस्य बने",
                "close": "बंद करें",
                "language_settings": "भाषा सेटिंग्स",
                "select_language": "भाषा चुनें",
                "apply": "लागू करें",
                # Overview Panel
                "platform_overview": "प्लेटफ़ॉर्म अवलोकन",
                "total_content": "कुल सामग्री",
                "this_week": "इस सप्ताह",
                "quality_score": "गुणवत्ता स्कोर",
                "excellent": "उत्कृष्ट",
                "risk_alerts": "जोखिम अलर्ट",
                "resolved": "हल किया गया",
                "ai_operations": "एआई संचालन",
                "success": "सफलता",
                "recent_activity": "हाल की गतिविधि",
                "content_analyzed": "सामग्री विश्लेषण",
                "article_ai_ethics": "एआई नैतिकता पर लेख",
                "min_ago": "मिनट पहले",
                "risk_detected": "जोखिम का पता चला",
                "policy_violation": "संभावित नीति उल्लंघन",
                "content_transformed": "सामग्री रूपांतरित",
                "linkedin_twitter": "लिंक्डइन + ट्विटर पोस्ट",
                "hour_ago": "घंटे पहले",
                "quality_alert": "गुणवत्ता अलर्ट",
                "readability_below": "पठनीयता सीमा से नीचे",
                "hours_ago": "घंटे पहले",
                "system_health": "सिस्टम स्वास्थ्य",
                "ai_model_performance": "एआई मॉडल प्रदर्शन",
                "content_processing_rate": "सामग्री प्रसंस्करण दर",
                "storage_utilization": "भंडारण उपयोग",
                "api_healthy": "एपीआई: स्वस्थ",
                "database_healthy": "डेटाबेस: स्वस्थ",
                "ai_healthy": "एआई: स्वस्थ",
                # Settings Dialog
                "settings_preferences": "सेटिंग्स और प्राथमिकताएं",
                "language": "भाषा",
                "notifications": "सूचनाएं",
                "enable_notifications": "सूचनाएं सक्षम करें",
                "email_alerts_critical": "महत्वपूर्ण मुद्दों के लिए ईमेल अलर्ट",
                "content_management": "सामग्री प्रबंधन",
                "auto_save_drafts": "सामग्री ड्राफ्ट स्वतः सहेजें",
                "session": "सत्र",
                "session_timeout_minutes": "सत्र समय समाप्ति (मिनट)",
                "paused_tasks": "रोके गए कार्य",
                "you_have_paused_tasks": "आपके पास {count} रोके गए कार्य हैं",
                "view_paused_tasks": "रोके गए कार्य देखें",
                "cancel": "रद्द करें",
                "save_settings": "सेटिंग्स सहेजें",
                "settings_saved": "सेटिंग्स सफलतापूर्वक सहेजी गईं"
            },
            "Kannada": {
                "title": "ಅಶೋಕ",
                "subtitle": "ಜೆನ್‌ಎಐ ಆಡಳಿತ ಮತ್ತು ವೀಕ್ಷಣಾ ವೇದಿಕೆ",
                "overview": "ಅವಲೋಕನ",
                "content_intelligence": "ವಿಷಯ ಬುದ್ಧಿವಂತಿಕೆ",
                "transform": "ಪರಿವರ್ತನೆ",
                "monitoring": "ಮೇಲ್ವಿಚಾರಣೆ",
                "alerts": "ಎಚ್ಚರಿಕೆಗಳು",
                "security": "ಭದ್ರತೆ",
                "profile": "ಪ್ರೊಫೈಲ್",
                "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
                "logout": "ಲಾಗ್ಔಟ್",
                "user_profile": "ಬಳಕೆದಾರ ಪ್ರೊಫೈಲ್",
                "username": "ಬಳಕೆದಾರ ಹೆಸರು",
                "email": "ಇಮೇಲ್",
                "role": "ಪಾತ್ರ",
                "member_since": "ಸದಸ್ಯರಾದ ದಿನಾಂಕ",
                "close": "ಮುಚ್ಚಿ",
                "language_settings": "ಭಾಷಾ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
                "select_language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
                "apply": "ಅನ್ವಯಿಸಿ",
                # Overview Panel
                "platform_overview": "ವೇದಿಕೆ ಅವಲೋಕನ",
                "total_content": "ಒಟ್ಟು ವಿಷಯ",
                "this_week": "ಈ ವಾರ",
                "quality_score": "ಗುಣಮಟ್ಟ ಸ್ಕೋರ್",
                "excellent": "ಅತ್ಯುತ್ತಮ",
                "risk_alerts": "ಅಪಾಯ ಎಚ್ಚರಿಕೆಗಳು",
                "resolved": "ಪರಿಹರಿಸಲಾಗಿದೆ",
                "ai_operations": "ಎಐ ಕಾರ್ಯಾಚರಣೆಗಳು",
                "success": "ಯಶಸ್ಸು",
                "recent_activity": "ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ",
                "content_analyzed": "ವಿಷಯ ವಿಶ್ಲೇಷಣೆ",
                "article_ai_ethics": "ಎಐ ನೀತಿಶಾಸ್ತ್ರದ ಲೇಖನ",
                "min_ago": "ನಿಮಿಷಗಳ ಹಿಂದೆ",
                "risk_detected": "ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
                "policy_violation": "ಸಂಭಾವ್ಯ ನೀತಿ ಉಲ್ಲಂಘನೆ",
                "content_transformed": "ವಿಷಯ ಪರಿವರ್ತನೆ",
                "linkedin_twitter": "ಲಿಂಕ್ಡ್‌ಇನ್ + ಟ್ವಿಟರ್ ಪೋಸ್ಟ್‌ಗಳು",
                "hour_ago": "ಗಂಟೆ ಹಿಂದೆ",
                "quality_alert": "ಗುಣಮಟ್ಟ ಎಚ್ಚರಿಕೆ",
                "readability_below": "ಓದುವಿಕೆ ಮಿತಿಗಿಂತ ಕಡಿಮೆ",
                "hours_ago": "ಗಂಟೆಗಳ ಹಿಂದೆ",
                "system_health": "ವ್ಯವಸ್ಥೆ ಆರೋಗ್ಯ",
                "ai_model_performance": "ಎಐ ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ",
                "content_processing_rate": "ವಿಷಯ ಪ್ರಕ್ರಿಯೆ ದರ",
                "storage_utilization": "ಸಂಗ್ರಹಣೆ ಬಳಕೆ",
                "api_healthy": "ಎಪಿಐ: ಆರೋಗ್ಯಕರ",
                "database_healthy": "ಡೇಟಾಬೇಸ್: ಆರೋಗ್ಯಕರ",
                "ai_healthy": "ಎಐ: ಆರೋಗ್ಯಕರ",
                # Settings Dialog
                "settings_preferences": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು ಮತ್ತು ಆದ್ಯತೆಗಳು",
                "language": "ಭಾಷೆ",
                "notifications": "ಅಧಿಸೂಚನೆಗಳು",
                "enable_notifications": "ಅಧಿಸೂಚನೆಗಳನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ",
                "email_alerts_critical": "ನಿರ್ಣಾಯಕ ಸಮಸ್ಯೆಗಳಿಗೆ ಇಮೇಲ್ ಎಚ್ಚರಿಕೆಗಳು",
                "content_management": "ವಿಷಯ ನಿರ್ವಹಣೆ",
                "auto_save_drafts": "ವಿಷಯ ಕರಡುಗಳನ್ನು ಸ್ವಯಂ-ಉಳಿಸಿ",
                "session": "ಅಧಿವೇಶನ",
                "session_timeout_minutes": "ಅಧಿವೇಶನ ಅವಧಿ ಮುಗಿಯುವಿಕೆ (ನಿಮಿಷಗಳು)",
                "paused_tasks": "ವಿರಾಮಗೊಳಿಸಿದ ಕಾರ್ಯಗಳು",
                "you_have_paused_tasks": "ನೀವು {count} ವಿರಾಮಗೊಳಿಸಿದ ಕಾರ್ಯಗಳನ್ನು ಹೊಂದಿದ್ದೀರಿ",
                "view_paused_tasks": "ವಿರಾಮಗೊಳಿಸಿದ ಕಾರ್ಯಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
                "cancel": "ರದ್ದುಮಾಡಿ",
                "save_settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಉಳಿಸಿ",
                "settings_saved": "ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ"
            },
            "Tamil": {
                "title": "அசோகா",
                "subtitle": "ஜென்ஏஐ ஆளுமை மற்றும் கண்காணிப்பு தளம்",
                "overview": "மேலோட்டம்",
                "content_intelligence": "உள்ளடக்க நுண்ணறிவு",
                "transform": "மாற்றம்",
                "monitoring": "கண்காணிப்பு",
                "alerts": "எச்சரிக்கைகள்",
                "security": "பாதுகாப்பு",
                "profile": "சுயவிவரம்",
                "settings": "அமைப்புகள்",
                "logout": "வெளியேறு",
                "user_profile": "பயனர் சுயவிவரம்",
                "username": "பயனர் பெயர்",
                "email": "மின்னஞ்சல்",
                "role": "பங்கு",
                "member_since": "உறுப்பினரான தேதி",
                "close": "மூடு",
                "language_settings": "மொழி அமைப்புகள்",
                "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
                "apply": "பயன்படுத்து",
                # Overview Panel
                "platform_overview": "தள மேலோட்டம்",
                "total_content": "மொத்த உள்ளடக்கம்",
                "this_week": "இந்த வாரம்",
                "quality_score": "தர மதிப்பெண்",
                "excellent": "சிறந்தது",
                "risk_alerts": "அபாய எச்சரிக்கைகள்",
                "resolved": "தீர்க்கப்பட்டது",
                "ai_operations": "ஏஐ செயல்பாடுகள்",
                "success": "வெற்றி",
                "recent_activity": "சமீபத்திய செயல்பாடு",
                "content_analyzed": "உள்ளடக்க பகுப்பாய்வு",
                "article_ai_ethics": "ஏஐ நெறிமுறைகள் பற்றிய கட்டுரை",
                "min_ago": "நிமிடங்களுக்கு முன்",
                "risk_detected": "அபாயம் கண்டறியப்பட்டது",
                "policy_violation": "சாத்தியமான கொள்கை மீறல்",
                "content_transformed": "உள்ளடக்க மாற்றம்",
                "linkedin_twitter": "லிங்க்ட்இன் + ட்விட்டர் இடுகைகள்",
                "hour_ago": "மணி நேரத்திற்கு முன்",
                "quality_alert": "தர எச்சரிக்கை",
                "readability_below": "வாசிப்புத்திறன் வரம்புக்குக் கீழே",
                "hours_ago": "மணி நேரங்களுக்கு முன்",
                "system_health": "அமைப்பு ஆரோக்கியம்",
                "ai_model_performance": "ஏஐ மாதிரி செயல்திறன்",
                "content_processing_rate": "உள்ளடக்க செயலாக்க விகிதம்",
                "storage_utilization": "சேமிப்பக பயன்பாடு",
                "api_healthy": "ஏபிஐ: ஆரோக்கியமானது",
                "database_healthy": "தரவுத்தளம்: ஆரோக்கியமானது",
                "ai_healthy": "ஏஐ: ஆரோக்கியமானது",
                # Settings Dialog
                "settings_preferences": "அமைப்புகள் மற்றும் விருப்பத்தேர்வுகள்",
                "language": "மொழி",
                "notifications": "அறிவிப்புகள்",
                "enable_notifications": "அறிவிப்புகளை இயக்கு",
                "email_alerts_critical": "முக்கியமான சிக்கல்களுக்கு மின்னஞ்சல் எச்சரிக்கைகள்",
                "content_management": "உள்ளடக்க மேலாண்மை",
                "auto_save_drafts": "உள்ளடக்க வரைவுகளை தானாக சேமி",
                "session": "அமர்வு",
                "session_timeout_minutes": "அமர்வு காலாவதி (நிமிடங்கள்)",
                "paused_tasks": "இடைநிறுத்தப்பட்ட பணிகள்",
                "you_have_paused_tasks": "நீங்கள் {count} இடைநிறுத்தப்பட்ட பணிகளை கொண்டுள்ளீர்கள்",
                "view_paused_tasks": "இடைநிறுத்தப்பட்ட பணிகளைக் காண்க",
                "cancel": "ரத்துசெய்",
                "save_settings": "அமைப்புகளைச் சேமி",
                "settings_saved": "அமைப்புகள் வெற்றிகரமாக சேமிக்கப்பட்டன"
            }
        }
        
        # Initialize database
        db_schema.connect()
        db_schema.initialize_schema()
        self._load_current_user_context()

    def _load_current_user_context(self):
        """Load current user details and role for role-based visibility."""
        try:
            # Get username from session storage
            username = app.storage.general.get('username', '')
            if not username:
                # Fallback to user_id if username not available
                username = app.storage.general.get('user_id', 'demo_user')
            
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
                logger.info(f"Loaded user context: {self.current_username}, role: {self.current_user_role}")
            else:
                # Default values if user not found
                self.current_username = username or 'demo'
                self.current_email = f"{self.current_username}@ashoka.ai"
                self.current_user_role = 'user'
                logger.warning(f"User {username} not found in database, using defaults")
        except Exception as e:
            logger.warning(f"Failed to load current user context: {e}")
            self.current_user_role = 'user'
    
    def t(self, key: str) -> str:
        """Get translation for current language"""
        return self.translations.get(self.current_language, self.translations["English"]).get(key, key)
    
    def create_dashboard(self):
        """Create the main dashboard UI"""
        
        # Reload user context to get current logged-in user details
        self._load_current_user_context()
        
        # Custom CSS aligned with auth theme (cream + teal + blue)
        ui.add_head_html('''
            <style>
                :root {
                    --bg-primary: #ded5c4;
                    --bg-secondary: #efeeeb;
                    --text-primary: #102d32;
                    --text-secondary: #4e6b71;
                    --accent-color: #2d8a84;
                    --accent-soft: #5b93c9;
                    --card-bg: #f8f6f2;
                    --line: rgba(16, 45, 50, 0.16);
                    --header-from: #2d8a84;
                    --header-to: #176a66;
                }
                
                .dark-mode {
                    --bg-primary: #102124;
                    --bg-secondary: #173037;
                    --text-primary: #e7f3f4;
                    --text-secondary: #b5cfd1;
                    --accent-color: #70b8b2;
                    --accent-soft: #7caede;
                    --card-bg: #1c3438;
                    --line: rgba(231, 243, 244, 0.18);
                    --header-from: #1f7d78;
                    --header-to: #145f5b;
                }
                
                body {
                    background: linear-gradient(150deg, var(--bg-primary), #d9d0c0) !important;
                    color: var(--text-primary) !important;
                    transition: background 0.3s ease, color 0.3s ease;
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
                    padding: 24px !important;
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
            </style>
        ''')
        
        # Header
        with ui.header().classes('app-header'):
            with ui.row().classes('w-full items-center'):
                ui.icon('shield_with_heart', size='lg').classes('text-white')
                self.title_label = ui.label(self.t('title')).classes('text-2xl font-bold text-white ml-2')
                self.subtitle_label = ui.label(self.t('subtitle')).classes('text-sm text-cyan-50 ml-4')
                ui.space()
                
                # Session timer
                with ui.card().classes('timer-shell px-4 py-2 shadow-lg'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='sm').classes('text-white')
                        self.timer_label = ui.label('30:00').classes('timer-text font-mono text-lg font-bold')
                
                # Dark mode toggle
                self.theme_toggle = ui.button(
                    icon='dark_mode',
                    on_click=self._toggle_theme
                ).props('flat round').classes('text-white ml-2')
                
                with ui.button(icon='account_circle').props('flat round').classes('text-white'):
                    with ui.menu():
                        ui.menu_item(self.t('profile'), on_click=self._show_profile_dialog)
                        ui.menu_item(self.t('settings'), on_click=self._show_settings_dialog)
                        ui.separator()
                        ui.menu_item(self.t('logout'), on_click=self._handle_logout)
        
        # Start session timer
        self._start_session_timer()
        
        # Start auto-refresh timers for real-time updates
        self._start_auto_refresh_timers()
        
        # Main content with tabs
        with ui.tabs().classes('w-full justify-center') as tabs:
            self.overview_tab = ui.tab(self.t('overview'), icon='dashboard')
            self.content_tab = ui.tab(self.t('content_intelligence'), icon='psychology')
            self.transform_tab = ui.tab(self.t('transform'), icon='transform')
            self.monitor_tab = ui.tab(self.t('monitoring'), icon='bar_chart')
            self.alerts_tab = ui.tab(self.t('alerts'), icon='notifications')
            self.security_tab = None
            if self.current_user_role == 'admin':
                self.security_tab = ui.tab(self.t('security'), icon='security')
        
        with ui.tab_panels(tabs, value=self.overview_tab).classes('w-full'):
            # Overview Panel
            with ui.tab_panel(self.overview_tab):
                self._create_overview_panel()
            
            # Content Intelligence Panel
            with ui.tab_panel(self.content_tab):
                self._create_content_intelligence_panel()
            
            # Transform Panel
            with ui.tab_panel(self.transform_tab):
                self._create_transform_panel()
            
            # Monitoring Panel
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
    
    def _toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            ui.run_javascript('document.body.classList.add("dark-mode")')
            self.theme_toggle.props('icon=light_mode')
        else:
            ui.run_javascript('document.body.classList.remove("dark-mode")')
            self.theme_toggle.props('icon=dark_mode')
    
    def _handle_logout(self):
        """Handle user logout - clear session and redirect to login"""
        # Clear session storage
        app.storage.general.clear()
        
        # Notify user
        ui.notify('Logged out successfully', type='info')
        
        # Redirect to login page
        ui.navigate.to('/')
    
    def _start_session_timer(self):
        """Start the session countdown timer"""
        def update_timer():
            elapsed = (datetime.now() - self.session_start_time).total_seconds()
            remaining = self.session_duration - elapsed
            
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
        
        # Refresh monitoring metrics every 60 seconds
        def refresh_monitoring():
            try:
                if hasattr(self, 'quality_metrics_container'):
                    self._refresh_monitoring_metrics()
            except Exception as e:
                logger.error(f"Auto-refresh monitoring error: {e}")
        
        ui.timer(60.0, refresh_monitoring)
        
        # Refresh alerts every 90 seconds
        def refresh_alerts():
            try:
                if hasattr(self, 'alerts_container'):
                    self._refresh_alerts()
            except Exception as e:
                logger.error(f"Auto-refresh alerts error: {e}")
        
        ui.timer(90.0, refresh_alerts)
        
        # Refresh security logs every 120 seconds
        def refresh_security():
            try:
                if hasattr(self, 'security_metrics_container'):
                    self._refresh_security_logs()
            except Exception as e:
                logger.error(f"Auto-refresh security error: {e}")
        
        ui.timer(120.0, refresh_security)
        
        logger.info("Auto-refresh timers started: Monitoring (60s), Alerts (90s), Security (120s)")
    
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
        self.operation_paused = False
        dialog.close()
        ui.notify('Session extended by 30 minutes', type='positive')
    
    def _toggle_theme_old(self):
        
        if self.dark_mode:
            ui.run_javascript('document.body.classList.add("dark-mode")')
            self.theme_toggle.props('icon=light_mode')
        else:
            ui.run_javascript('document.body.classList.remove("dark-mode")')
            self.theme_toggle.props('icon=dark_mode')
    
    def _show_profile_dialog(self):
        """Show user profile dialog with functional features"""
        with ui.dialog() as profile_dialog, ui.card().classes('w-[500px]'):
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
                        ui.label(self.current_username).classes('text-lg font-semibold')
                
                # Email
                with ui.row().classes('w-full items-center'):
                    ui.icon('email').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('email')).classes('text-sm text-gray-600')
                        ui.label(self.current_email).classes('text-lg font-semibold')
                
                # Role
                with ui.row().classes('w-full items-center'):
                    ui.icon('badge').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('role')).classes('text-sm text-gray-600')
                        ui.label(self.current_user_role.title()).classes('text-lg font-semibold')
                
                # Member Since
                with ui.row().classes('w-full items-center'):
                    ui.icon('calendar_today').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label(self.t('member_since')).classes('text-sm text-gray-600')
                        ui.label('February 2026').classes('text-lg font-semibold')
                
                ui.separator().classes('my-3')
                
                # Session Info
                ui.label('Session Information').classes('text-md font-semibold mb-2')
                with ui.row().classes('w-full items-center'):
                    ui.icon('access_time').classes('text-gray-600')
                    with ui.column().classes('ml-3'):
                        ui.label('Session Started').classes('text-sm text-gray-600')
                        ui.label(self.session_start_time.strftime('%I:%M %p')).classes('text-md')
                
                # Activity Stats
                ui.separator().classes('my-3')
                ui.label('Activity Statistics').classes('text-md font-semibold mb-2')
                with ui.grid(columns=2).classes('w-full gap-3'):
                    with ui.card().classes('p-3 text-center'):
                        ui.label('Content Analyzed').classes('text-xs text-gray-600')
                        ui.label('24').classes('text-2xl font-bold text-blue-600')
                    with ui.card().classes('p-3 text-center'):
                        ui.label('Transformations').classes('text-xs text-gray-600')
                        ui.label('18').classes('text-2xl font-bold text-purple-600')
                    with ui.card().classes('p-3 text-center'):
                        ui.label('Paused Tasks').classes('text-xs text-gray-600')
                        ui.label(str(len(self.paused_tasks))).classes('text-2xl font-bold text-orange-600')
                    with ui.card().classes('p-3 text-center'):
                        ui.label('Alerts Viewed').classes('text-xs text-gray-600')
                        ui.label('12').classes('text-2xl font-bold text-green-600')
            
            ui.separator().classes('mt-4')
            
            with ui.row().classes('w-full justify-end mt-4'):
                ui.button(self.t('close'), on_click=profile_dialog.close).props('flat')
        
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
        """Show settings dialog with functional features"""
        with ui.dialog() as settings_dialog, ui.card().classes('w-[500px]'):
            with ui.row().classes('w-full items-center mb-4'):
                ui.icon('settings', size='xl').classes('text-amber-900')
                ui.label(self.t('settings_preferences')).classes('text-2xl font-bold ml-2')
            
            ui.separator()
            
            with ui.column().classes('w-full gap-4 mt-4'):
                # Language Settings
                ui.label(self.t('language')).classes('text-lg font-semibold')
                language_select = ui.select(
                    ['English', 'Hindi', 'Kannada', 'Tamil'],
                    value=self.current_language,
                    label=self.t('select_language')
                ).classes('w-full')
                
                ui.separator().classes('my-3')
                
                # Notification Settings
                ui.label(self.t('notifications')).classes('text-lg font-semibold')
                notif_enabled = ui.checkbox(
                    self.t('enable_notifications'),
                    value=self.user_preferences.get('notifications', True)
                )
                email_alerts = ui.checkbox(
                    self.t('email_alerts_critical'),
                    value=self.user_preferences.get('email_alerts', False)
                )
                
                ui.separator().classes('my-3')
                
                # Auto-save Settings
                ui.label(self.t('content_management')).classes('text-lg font-semibold')
                auto_save = ui.checkbox(
                    self.t('auto_save_drafts'),
                    value=self.user_preferences.get('auto_save', True)
                )
                
                ui.separator().classes('my-3')
                
                # Session Settings
                ui.label(self.t('session')).classes('text-lg font-semibold')
                session_timeout = ui.select(
                    [15, 30, 60, 120],
                    value=self.user_preferences.get('session_timeout', 30),
                    label=self.t('session_timeout_minutes')
                ).classes('w-full')
                
                ui.separator().classes('my-3')
                
                # Paused Tasks
                ui.label(self.t('paused_tasks')).classes('text-lg font-semibold')
                paused_count_text = self.t('you_have_paused_tasks').replace('{count}', str(len(self.paused_tasks)))
                ui.label(paused_count_text).classes('text-sm text-gray-600')
                if self.paused_tasks:
                    ui.button(
                        self.t('view_paused_tasks'),
                        icon='pause_circle',
                        on_click=lambda: self._show_paused_tasks_dialog()
                    ).props('flat color=primary').classes('w-full')
            
            ui.separator().classes('mt-4')
            
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                ui.button(self.t('cancel'), on_click=settings_dialog.close).props('flat')
                ui.button(
                    self.t('save_settings'),
                    on_click=lambda: self._save_settings(
                        language_select.value,
                        notif_enabled.value,
                        email_alerts.value,
                        auto_save.value,
                        session_timeout.value,
                        settings_dialog
                    )
                ).props('color=primary')
        
        settings_dialog.open()
    
    def _save_settings(self, language, notifications, email_alerts, auto_save, session_timeout, dialog):
        """Save user settings"""
        # Update preferences
        self.user_preferences['notifications'] = notifications
        self.user_preferences['email_alerts'] = email_alerts
        self.user_preferences['auto_save'] = auto_save
        self.user_preferences['session_timeout'] = session_timeout
        
        # Update session duration if changed
        if session_timeout != self.session_duration // 60:
            self.session_duration = session_timeout * 60
            self.session_start_time = datetime.now()
        
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
        
        with ui.row().classes('w-full gap-4'):
            # Recent Activity - Real data
            with ui.card().classes('flex-1'):
                ui.label(self.t('recent_activity')).classes('text-xl font-semibold mb-4')
                with ui.column().classes('gap-2'):
                    for activity in metrics['recent_activities']:
                        self._create_activity_item(
                            activity['title'],
                            activity['description'],
                            activity['time'],
                            activity['icon'],
                            activity['color']
                        )
            
            # System Health
            with ui.card().classes('flex-1'):
                ui.label(self.t('system_health')).classes('text-xl font-semibold mb-4')
                
                ui.label(self.t('ai_model_performance')).classes('text-sm text-gray-600 mb-2')
                ui.linear_progress(0.95).classes('mb-4').props('color=green')
                
                ui.label(self.t('content_processing_rate')).classes('text-sm text-gray-600 mb-2')
                ui.linear_progress(metrics['processing_rate']).classes('mb-4').props('color=blue')
                
                ui.label(self.t('storage_utilization')).classes('text-sm text-gray-600 mb-2')
                ui.linear_progress(metrics['storage_utilization']).classes('mb-4').props('color=orange')
                
                with ui.row().classes('gap-2 mt-4'):
                    ui.badge(self.t('api_healthy'), color='green')
                    ui.badge(self.t('database_healthy'), color='green')
                    ui.badge(self.t('ai_healthy'), color='green')
    
    def _get_dashboard_metrics(self):
        """Fetch real metrics from database"""
        if not db_schema.conn:
            db_schema.connect()
        
        try:
            # Total content count
            total_content = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint
            """).fetchone()[0]
            
            # Content this week
            content_this_week = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint
                WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
            """).fetchone()[0]
            
            # Average quality (based on sentiment confidence)
            avg_quality_result = db_schema.conn.execute("""
                SELECT AVG(sentiment_confidence * 100) FROM ashoka_contentint
                WHERE sentiment_confidence IS NOT NULL
            """).fetchone()[0]
            avg_quality = avg_quality_result if avg_quality_result else 85.0
            
            # Risk alerts (negative sentiment content)
            risk_alerts = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint
                WHERE sentiment = 'negative'
            """).fetchone()[0]
            
            # Resolved risks (assuming older negative content is resolved)
            resolved_risks = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint
                WHERE sentiment = 'negative' 
                AND created_at < CURRENT_DATE - INTERVAL '7 days'
            """).fetchone()[0]
            
            # AI operations (total analyses)
            ai_operations = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint
                WHERE analyzed_at IS NOT NULL
            """).fetchone()[0]
            
            # Success rate (content with analysis)
            success_rate = (ai_operations / total_content * 100) if total_content > 0 else 100.0
            
            # Content trend (last 5 weeks)
            trend_data = []
            for i in range(4, -1, -1):
                week_start = f"CURRENT_DATE - INTERVAL '{i*7 + 7} days'"
                week_end = f"CURRENT_DATE - INTERVAL '{i*7} days'"
                count = db_schema.conn.execute(f"""
                    SELECT COUNT(*) FROM ashoka_contentint
                    WHERE created_at >= {week_start} AND created_at < {week_end}
                """).fetchone()[0]
                trend_data.append((f'Week {5-i}', count))
            
            # Sentiment distribution
            positive_count = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'positive'
            """).fetchone()[0]
            neutral_count = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'neutral'
            """).fetchone()[0]
            negative_count = db_schema.conn.execute("""
                SELECT COUNT(*) FROM ashoka_contentint WHERE sentiment = 'negative'
            """).fetchone()[0]
            
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
            storage_result = db_schema.conn.execute("""
                SELECT SUM(file_size_mb) FROM ashoka_contentint
                WHERE file_size_mb IS NOT NULL
            """).fetchone()[0]
            storage_mb = storage_result if storage_result else 0
            storage_utilization = min(storage_mb / 1000, 0.95)  # Assume 1GB limit
            
            return {
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
            
        except Exception as e:
            logger.error(f"Error fetching dashboard metrics: {e}")
            # Return default values on error
            return {
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
    
    def _create_content_intelligence_panel(self):
        """Create content intelligence panel"""
        ui.label('Content Intelligence & Analysis').classes('text-3xl font-bold mb-4')
        
        with ui.row().classes('w-full gap-4'):
            # Input Section
            with ui.card().classes('flex-1'):
                ui.label('Submit Content for Analysis').classes('text-xl font-semibold mb-4')
                
                # Tab selector for input type with modern icons
                with ui.tabs().classes('w-full') as input_tabs:
                    text_tab = ui.tab('TEXT', icon='article')
                    audio_tab = ui.tab('AUDIO', icon='audiotrack')
                    image_tab = ui.tab('IMAGE', icon='photo')
                    video_tab = ui.tab('VIDEO', icon='movie')
                    document_tab = ui.tab('DOCUMENT', icon='description')
                
                with ui.tab_panels(input_tabs, value=text_tab).classes('w-full'):
                    # Text input panel
                    with ui.tab_panel(text_tab):
                        self.content_input = ui.textarea(
                            label='Enter your content',
                            placeholder='Paste your content here for AI-powered analysis...'
                        ).classes('w-full').props('rows=10')
                        
                        with ui.row().classes('gap-2 mt-4'):
                            ui.button(
                                'Analyze Text',
                                icon='psychology',
                                on_click=lambda: self._analyze_content(self.content_input.value)
                            ).props('color=primary')
                            ui.button('Clear', icon='clear', on_click=lambda: self.content_input.set_value('')).props('flat')
                    
                    # Audio upload panel
                    with ui.tab_panel(audio_tab):
                        ui.label('Upload an audio file to extract transcription and analyze content').classes('text-sm text-gray-600 mb-3')
                        
                        # Audio preview container
                        self.audio_preview_container = ui.column().classes('w-full mb-4')
                        
                        # Upload button with custom styling to hide checkmarks
                        upload_audio = ui.upload(
                            label='Choose Audio',
                            on_upload=self._handle_audio_upload,
                            auto_upload=True
                        ).props('accept="audio/*" hide-upload-btn').classes('w-full')
                        
                        ui.label('Supported formats: MP3, WAV, M4A, OGG').classes('text-xs text-gray-500 mt-2')
                    
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
            
            # Analysis Results
            with ui.card().classes('flex-1'):
                ui.label('Analysis Results').classes('text-xl font-semibold mb-4')
                
                self.analysis_container = ui.column().classes('w-full gap-3')
                with self.analysis_container:
                    ui.label('Submit content to see analysis results').classes('text-gray-500 text-center py-8')
        
        # AI Content Generator Section (moved here - right after Submit Content)
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
        
        # Analysis & Generator History Section (renamed and combined - at the bottom)
        with ui.card().classes('w-full mt-4'):
            with ui.row().classes('items-center justify-between mb-4'):
                ui.label('Analysis & Generator History').classes('text-xl font-semibold')
                ui.label('History of analyzed and generated content - Click any row to preview').classes('text-sm text-gray-500')
            
            self.history_table_container = ui.column().classes('w-full')
            # Load initial history from database
            self._update_history_table()
    
    def _create_transform_panel(self):
        """Create content transformation panel"""
        ui.label('Multi-Platform Content Transformer').classes('text-3xl font-bold mb-4')
        
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
        
        # Transform History Section
        with ui.card().classes('w-full mt-4'):
            ui.label('Transform History').classes('text-xl font-semibold mb-4')
            ui.label('Click any row to load that transformation').classes('text-sm text-gray-600 mb-2')
            
            self.transform_history_container = ui.column().classes('w-full')
            self._update_transform_history()
    
    def _create_monitoring_panel(self):
        """Create monitoring dashboard panel"""
        from src.services.monitoring_service import monitoring_service
        
        with ui.column().classes('w-full gap-4'):
            # Header with refresh button
            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label('Quality, Risk & Operations Monitoring').classes('text-3xl font-bold')
                ui.button(
                    'Refresh Metrics',
                    icon='refresh',
                    on_click=self._refresh_monitoring_metrics
                ).props('flat color=primary')
            
            # Performance Trend Chart
            with ui.card().classes('w-full'):
                ui.label('Performance Trends (Last 24 Hours)').classes('text-xl font-semibold mb-4')
                
                # Mock hourly performance data
                hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00']
                success_rates = [98.5, 97.8, 99.2, 98.9, 99.5, 98.3, 99.1]
                max_rate = 100
                
                with ui.column().classes('w-full gap-2'):
                    for hour, rate in zip(hours, success_rates):
                        with ui.row().classes('w-full items-center gap-3'):
                            ui.label(hour).classes('w-12 text-xs font-medium')
                            bar_width = (rate / max_rate * 100)
                            color = 'green' if rate >= 98 else 'orange' if rate >= 95 else 'red'
                            with ui.element('div').classes('flex-1 bg-gray-200 rounded h-6 relative'):
                                with ui.element('div').classes(f'bg-{color}-500 h-full rounded').style(f'width: {bar_width}%'):
                                    pass
                            ui.label(f'{rate}%').classes(f'w-12 text-xs font-bold text-{color}-600')
            
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
    
    def _refresh_monitoring_metrics(self):
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
                    change_icon = '↑' if quality.readability_change > 0 else '↓'
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
            
            ui.notify('Metrics refreshed', type='positive')
            
        except Exception as e:
            logger.error(f"Error refreshing metrics: {e}")
            ui.notify(f'Failed to refresh metrics: {str(e)}', type='negative')
    
    def _create_alerts_panel(self):
        """Create alerts panel with real data from Content Intelligence, Transformations, and Quality checks"""
        
        with ui.column().classes('w-full gap-4'):
            # Header with refresh button
            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label('Alerts & Notifications').classes('text-3xl font-bold')
                ui.button(
                    'Refresh Alerts',
                    icon='refresh',
                    on_click=self._refresh_alerts
                ).props('flat color=primary')
            
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
    
    def _refresh_alerts(self):
        """Refresh alerts list with real data from database"""
        from datetime import datetime, timedelta
        
        try:
            alerts = []
            
            # Get recent content analysis (last 24 hours)
            result = db_schema.conn.execute("""
                SELECT id, content_type, sentiment, sentiment_confidence, 
                       quality_score, analyzed_at, summary
                FROM ashoka_contentint
                WHERE analyzed_at >= ?
                ORDER BY analyzed_at DESC
                LIMIT 10
            """, [datetime.now() - timedelta(hours=24)]).fetchall()
            
            for row in result:
                content_id, content_type, sentiment, confidence, quality, analyzed_at, summary = row
                time_ago = self._format_time_ago(analyzed_at)
                
                # Quality alerts
                if quality and quality < 60:
                    alerts.append({
                        'title': f'Low Quality Content Detected',
                        'description': f'{content_type.title()} content has quality score of {quality:.0f}%. Review recommended.',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': analyzed_at
                    })
                
                # Sentiment alerts
                if sentiment == 'negative' and confidence > 0.7:
                    alerts.append({
                        'title': f'Negative Sentiment Detected',
                        'description': f'{content_type.title()} content shows negative sentiment ({confidence*100:.0f}% confidence).',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': analyzed_at
                    })
                
                # Success notifications
                if quality and quality >= 85:
                    alerts.append({
                        'title': f'High Quality Content Analyzed',
                        'description': f'{content_type.title()} content achieved {quality:.0f}% quality score.',
                        'type': 'success',
                        'time_ago': time_ago,
                        'timestamp': analyzed_at
                    })
            
            # Get recent transformations (last 24 hours)
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
                
                import json
                platform_list = json.loads(platforms) if isinstance(platforms, str) else platforms
                platform_names = ', '.join(platform_list)
                
                alerts.append({
                    'title': f'Content Transformed Successfully',
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
                        'title': f'High Risk Content Blocked',
                        'description': f'Content flagged for review due to {policy_risk} policy risk and {backlash_risk} backlash risk.',
                        'type': 'critical',
                        'time_ago': time_ago,
                        'timestamp': assessed_at
                    })
                elif policy_risk == 'high' or backlash_risk == 'high':
                    alerts.append({
                        'title': f'Risk Alert: Review Required',
                        'description': f'Content has {policy_risk} policy risk. Manual review recommended.',
                        'type': 'warning',
                        'time_ago': time_ago,
                        'timestamp': assessed_at
                    })
            
            # Sort alerts by timestamp (most recent first)
            alerts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Filter if needed
            filter_type = self.alert_filter.value.lower()
            if filter_type != 'all':
                alerts = [a for a in alerts if a['type'] == filter_type]
            
            # Update stats
            self._update_alert_stats(alerts)
            
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
            
            ui.notify('Alerts refreshed', type='positive')
            
        except Exception as e:
            logger.error(f"Error refreshing alerts: {e}")
            self.alerts_container.clear()
            with self.alerts_container:
                ui.label('No alerts available yet. Start analyzing or transforming content to see alerts here.').classes('text-gray-500 text-center py-8')
    
    def _update_alert_stats(self, alerts):
        """Update alert statistics summary"""
        critical_count = sum(1 for a in alerts if a['type'] == 'critical')
        warning_count = sum(1 for a in alerts if a['type'] == 'warning')
        success_count = sum(1 for a in alerts if a['type'] == 'success')
        info_count = sum(1 for a in alerts if a['type'] == 'info')
        
        self.alert_stats_container.clear()
        with self.alert_stats_container:
            with ui.card().classes('flex-1 metric-card risk-high' if critical_count > 0 else 'flex-1 metric-card'):
                ui.label('Critical').classes('text-sm text-gray-600')
                ui.label(str(critical_count)).classes('text-3xl font-bold text-red-600')
                ui.label('Requires immediate action').classes('text-xs text-gray-500')
            
            with ui.card().classes('flex-1 metric-card risk-medium' if warning_count > 0 else 'flex-1 metric-card'):
                ui.label('Warnings').classes('text-sm text-gray-600')
                ui.label(str(warning_count)).classes('text-3xl font-bold text-orange-600')
                ui.label('Review recommended').classes('text-xs text-gray-500')
            
            with ui.card().classes('flex-1 metric-card risk-low'):
                ui.label('Success').classes('text-sm text-gray-600')
                ui.label(str(success_count)).classes('text-3xl font-bold text-green-600')
                ui.label('Operations completed').classes('text-xs text-gray-500')
            
            with ui.card().classes('flex-1 metric-card'):
                ui.label('Total Alerts').classes('text-sm text-gray-600')
                ui.label(str(len(alerts))).classes('text-3xl font-bold text-blue-600')
                ui.label('Last 24 hours').classes('text-xs text-gray-500')
    
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
        
        # Load initial data
        self._refresh_security_logs()
    
    def _refresh_security_logs(self):
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
                            ui.label(timestamp.strftime('%Y-%m-%d %H:%M:%S')).classes('w-40 text-gray-700')
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
            
            ui.notify('Security logs refreshed', type='positive')
            
        except Exception as e:
            logger.error(f"Error refreshing security logs: {e}")
            ui.notify(f'Failed to refresh security logs: {str(e)}', type='negative')
    
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
    
    async def _analyze_content(self, content: str):
        """Analyze content and display results (async to prevent UI blocking)"""
        if not content or not content.strip():
            ui.notify('Please enter content to analyze', type='warning')
            return
        
        # Track operation
        self.current_operation = {
            'type': 'Analysis',
            'content': content,
            'progress': 0
        }
        
        try:
            # Show loading state with animation
            self.analysis_container.clear()
            with self.analysis_container:
                with ui.card().classes('w-full text-center p-8'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('🤖 AI is analyzing your content...').classes('text-xl font-semibold mt-4')
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
            
            # Analyze content (run in executor to not block UI)
            analysis = await loop.run_in_executor(
                None,
                self.analyzer.analyze_content,
                version.version_id,
                content
            )
            self.current_analysis = analysis
            self.current_operation['progress'] = 100
            progress_label.set_text('Complete!')
            
            # Store in ashoka_contentint table
            content_id = str(uuid.uuid4())
            word_count = len(content.split())
            char_count = len(content)
            
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
                None,  # quality_score (can be calculated later)
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
            
            ui.notify('✅ Content analyzed successfully!', type='positive')
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            self.analysis_container.clear()
            with self.analysis_container:
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
                    ui.label('🔄 Transforming content for social media...').classes('text-xl font-semibold mt-4')
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
                include_hashtags
            )
            
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
            
            ui.notify(f'✅ Content transformed for {len(platforms)} platforms!', type='positive')
            
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
                            ui.label('•').classes('text-gray-400')
                            ui.label(f"Format: {platform_content.metadata.get('format', 'N/A').title()}").classes('text-sm text-gray-600')
                            
                            # Tweet count for Twitter
                            if 'tweet_count' in platform_content.metadata:
                                ui.label('•').classes('text-gray-400')
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
                                    ui.chip(f'#{hashtag}', icon='tag').props(f'outline color={badge_color}').classes('text-xs')
                        
                        # Copy button
                        ui.button(
                            'Copy to Clipboard',
                            icon='content_copy',
                            on_click=lambda c=platform_content.content: self._copy_to_clipboard(c)
                        ).props('flat').classes('mt-3')
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        payload = json.dumps(text)
        ui.run_javascript(
            f"navigator.clipboard.writeText({payload}).then(() => {{ console.log('Copied to clipboard'); }});"
        )
        ui.notify('Copied to clipboard!', type='positive')
    
    def _update_transform_history(self):
        """Update transform history table"""
        try:
            if not db_schema.conn:
                db_schema.connect()
            
            # Get last 20 transformations
            rows = db_schema.conn.execute("""
                SELECT id, original_content, platforms, tone, created_at, transformed_results
                FROM transform_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 20
            """, [self.current_user]).fetchall()
            
            self.transform_history_container.clear()
            
            if not rows:
                with self.transform_history_container:
                    ui.label('No transform history yet').classes('text-gray-500 text-center py-4')
                return
            
            with self.transform_history_container:
                # Create table
                columns = [
                    {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'left', 'sortable': True},
                    {'name': 'content', 'label': 'Original Content', 'field': 'content', 'align': 'left'},
                    {'name': 'platforms', 'label': 'Platforms', 'field': 'platforms', 'align': 'left'},
                    {'name': 'tone', 'label': 'Tone', 'field': 'tone', 'align': 'left'},
                    {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'}
                ]
                
                table_rows = []
                for row in rows:
                    transform_id, content, platforms_json, tone, created_at, results_json = row
                    
                    # Parse platforms
                    platforms_list = json.loads(platforms_json) if platforms_json else []
                    platforms_str = ', '.join([p.title() for p in platforms_list])
                    
                    # Truncate content preview
                    content_preview = content[:80] + '...' if len(content) > 80 else content
                    
                    table_rows.append({
                        'id': transform_id,
                        'timestamp': created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(created_at, 'strftime') else str(created_at),
                        'content': content_preview,
                        'platforms': platforms_str,
                        'tone': tone.title(),
                        'actions': transform_id,
                        '_full_content': content,
                        '_platforms': platforms_list,
                        '_results': results_json
                    })
                
                table = ui.table(
                    columns=columns,
                    rows=table_rows,
                    row_key='id'
                ).classes('w-full')
                
                # Add custom slot for actions column
                table.add_slot('body-cell-actions', '''
                    <q-td :props="props">
                        <q-btn flat dense icon="visibility" color="primary" size="sm" @click="$parent.$emit('preview', props.row)" />
                        <q-btn flat dense icon="folder_open" color="secondary" size="sm" @click="$parent.$emit('load', props.row)" />
                    </q-td>
                ''')
                
                # Handle preview button click
                table.on('preview', lambda e: self._show_transform_preview_dialog(e.args))
                
                # Handle load button click
                table.on('load', lambda e: self._load_transform_from_history(e.args))
                
        except Exception as e:
            logger.error(f"Error updating transform history: {e}")
            self.transform_history_container.clear()
            with self.transform_history_container:
                ui.label(f'Error loading history: {str(e)}').classes('text-red-600')
    
    def _show_transform_preview_dialog(self, row_data):
        """Show transform preview in a dialog"""
        try:
            results_json = row_data.get('_results')
            if not results_json:
                ui.notify('No results available', type='warning')
                return
            
            results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
            
            with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Transform Preview').classes('text-2xl font-bold')
                    ui.button(icon='close', on_click=dialog.close).props('flat round')
                
                ui.label(f"Original: {row_data.get('_full_content', '')[:200]}...").classes('text-sm text-gray-600 mb-4')
                
                # Display each platform result
                with ui.scroll_area().classes('h-96 w-full'):
                    for platform, content in results_dict.items():
                        if content:
                            with ui.card().classes('w-full mb-3 bg-gray-50'):
                                ui.label(platform.title()).classes('text-lg font-semibold mb-2')
                                ui.label(content).classes('text-gray-700 whitespace-pre-wrap')
                
                ui.button('Close', on_click=dialog.close).props('color=primary').classes('mt-4')
            
            dialog.open()
            
        except Exception as e:
            logger.error(f"Error showing transform preview: {e}")
            ui.notify(f'Error: {str(e)}', type='negative')
    
    def _load_transform_from_history(self, row_data):
        """Load a past transformation into the main view"""
        try:
            # Load original content
            self.transform_input.value = row_data.get('_full_content', '')
            
            # Load platforms
            platforms = row_data.get('_platforms', [])
            self.platform_linkedin.value = 'linkedin' in platforms
            self.platform_twitter.value = 'twitter' in platforms
            self.platform_instagram.value = 'instagram' in platforms
            self.platform_facebook.value = 'facebook' in platforms
            self.platform_threads.value = 'threads' in platforms
            
            # Load tone
            tone = row_data.get('tone', 'Professional')
            self.tone_selector.value = tone.title()
            
            # Load and display results
            results_json = row_data.get('_results')
            if results_json:
                results_dict = json.loads(results_json) if isinstance(results_json, str) else results_json
                
                # Convert dict to PlatformContent objects
                from src.services.content_transformer import PlatformContent
                results = {}
                for platform, content in results_dict.items():
                    if content:
                        results[platform] = PlatformContent(
                            platform=platform.title(),
                            content=content,
                            character_count=len(content),
                            within_limit=True,
                            hashtags=[],
                            metadata={'tone': tone, 'format': 'loaded'}
                        )
                
                self._display_transform_results(results)
            
            ui.notify(f'Loaded transformation from {row_data.get("timestamp")}', type='positive')
            
        except Exception as e:
            logger.error(f"Error loading transform from history: {e}")
            ui.notify(f'Error: {str(e)}', type='negative')
    
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

    def _handle_audio_upload(self, e):
        """Handle audio file upload"""
        filename = e.name if hasattr(e, 'name') else (e.filename if hasattr(e, 'filename') else 'audio file')
        self._render_upload_preview(self.audio_preview_container, f'Audio: {filename}')
        self._show_coming_soon_dialog('Audio analysis')

    def _handle_image_upload(self, e):
        """Handle image file upload"""
        filename = e.name if hasattr(e, 'name') else (e.filename if hasattr(e, 'filename') else 'image file')
        self._render_upload_preview(self.image_preview_container, f'Image: {filename}')
        self._show_coming_soon_dialog('Image analysis')

    def _handle_video_upload(self, e):
        """Handle video file upload"""
        filename = e.name if hasattr(e, 'name') else (e.filename if hasattr(e, 'filename') else 'video file')
        self._render_upload_preview(self.video_preview_container, f'Video: {filename}')
        self._show_coming_soon_dialog('Video analysis')

    def _handle_document_upload(self, e):
        """Handle document file upload"""
        filename = e.name if hasattr(e, 'name') else (e.filename if hasattr(e, 'filename') else 'document file')
        self._render_upload_preview(self.document_preview_container, f'Document: {filename}')

    def _display_analysis_results(self, analysis, content: str):
        """Display comprehensive analysis results"""
        self.analysis_container.clear()
        with self.analysis_container:
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
                with ui.row().classes('gap-2'):
                    for topic in analysis.topics:
                        ui.chip(topic, icon='topic').props('outline color=orange')
            
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
                                with ui.column().classes('w-32'):
                                    ui.label(analyzed_at.strftime('%Y-%m-%d')).classes('text-sm font-medium')
                                    ui.label(analyzed_at.strftime('%H:%M:%S')).classes('text-xs text-gray-500')
                                
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
                                ui.label(f"Analyzed: {analyzed_at.strftime('%Y-%m-%d %H:%M:%S')}").classes('text-sm')
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
                                with ui.row().classes('gap-2'):
                                    for topic in topics:
                                        ui.chip(topic, icon='topic').props('outline color=orange')
                        
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
        
        try:
            # Show loading
            self.generator_output_container.clear()
            with self.generator_output_container:
                with ui.card().classes('w-full text-center p-8'):
                    ui.spinner(size='xl', color='primary')
                    ui.label('🤖 AI is generating content...').classes('text-xl font-semibold mt-4')
                    progress_label = ui.label('Processing your prompt...').classes('text-sm text-gray-600 mt-2')
            
            # Generate content
            import asyncio
            loop = asyncio.get_event_loop()
            
            if gen_type == 'Text/Notes':
                # Generate text content using Gemini
                generation_prompt = f"Generate professional content based on this prompt:\n\n{prompt}\n\nProvide a well-structured, detailed response."
                
                result = await loop.run_in_executor(
                    None,
                    gemini_client.generate_content,
                    generation_prompt
                )
                
                generated_text = result.get('text', 'No content generated')
                
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
                
                ui.notify('✅ Content generated successfully!', type='positive')
            
            elif gen_type == 'Image':
                # Image generation - Coming Soon
                self.generator_output_container.clear()
                with self.generator_output_container:
                    with ui.card().classes('w-full text-center p-8 bg-amber-50'):
                        ui.icon('construction', size='xl').classes('text-amber-600 mb-3')
                        ui.label('Image Generation Coming Soon').classes('text-xl font-semibold mb-2')
                        ui.label('AI image generation feature is under development').classes('text-gray-600 mb-2')
                        ui.label('This feature will be available in a future update').classes('text-sm text-gray-500')
                ui.notify('Image generation coming soon', type='info')
            
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
                    
                    if 'HUGGINGFACE_TOKEN' in str(e):
                        ui.label('Make sure HUGGINGFACE_TOKEN is set in your .env file').classes('text-xs text-gray-600 mt-2')
            ui.notify(f'Generation failed: {str(e)}', type='negative')
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        ui.run_javascript(f'navigator.clipboard.writeText({json.dumps(text)})')
        ui.notify('Copied to clipboard!', type='positive')
    
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
        port=8080
    )


if __name__ in {"__main__", "__mp_main__"}:
    launch_dashboard()

