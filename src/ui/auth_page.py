# """Beautiful Full-Screen Authentication Page with OTP"""
# from nicegui import ui, app
# from datetime import datetime, timedelta
# import asyncio

# from src.services.auth_service import auth_service
# from src.utils.logging import logger


# class AuthPageV2:
#     """Modern full-screen authentication page"""
    
#     def __init__(self):
#         self.current_user_id = None
#         self.otp_timer = None
#         self.otp_expiry = None
#         self.show_signup = False
        
#     def create_auth_page(self):
#         """Create the authentication page"""
        
#         # Custom CSS for split-screen design with skinish brown theme
#         ui.add_head_html('''
#             <style>
#                 * {
#                     box-sizing: border-box;
#                 }
                
#                 html, body {
#                     margin: 0;
#                     height: 100%;
#                     font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
#                     overflow: hidden;
#                 }
                
#                 /* Background - Skinish Brown Theme with subtle animation */
#                 body {
#                     background: linear-gradient(135deg, #f5e6d3 0%, #e8d4b8 50%, #d4b896 100%);
#                     animation: gradientShift 15s ease infinite;
#                 }
                
#                 @keyframes gradientShift {
#                     0%, 100% { background-position: 0% 50%; }
#                     50% { background-position: 100% 50%; }
#                 }
                
#                 /* Layout */
#                 .split-container {
#                     display: flex;
#                     height: 100vh;
#                 }
                
#                 /* Left Side with smooth entrance */
#                 .left-panel {
#                     flex: 1;
#                     display: flex;
#                     align-items: center;
#                     justify-content: center;
#                     background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
#                     color: white;
#                     padding: 60px;
#                     animation: slideInLeft 0.8s ease-out;
#                 }
                
#                 @keyframes slideInLeft {
#                     from {
#                         opacity: 0;
#                         transform: translateX(-50px);
#                     }
#                     to {
#                         opacity: 1;
#                         transform: translateX(0);
#                     }
#                 }
                
#                 .left-content h1 {
#                     font-size: 48px;
#                     margin-bottom: 20px;
#                     font-weight: 700;
#                     animation: fadeInUp 1s ease-out 0.3s both;
#                 }
                
#                 .left-content p {
#                     font-size: 18px;
#                     opacity: 0.9;
#                     max-width: 400px;
#                     line-height: 1.6;
#                     animation: fadeInUp 1s ease-out 0.5s both;
#                 }
                
#                 .left-content .logo-icon {
#                     font-size: 80px;
#                     margin-bottom: 30px;
#                     animation: fadeInUp 1s ease-out 0.1s both;
#                     filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
#                 }
                
#                 @keyframes fadeInUp {
#                     from {
#                         opacity: 0;
#                         transform: translateY(20px);
#                     }
#                     to {
#                         opacity: 1;
#                         transform: translateY(0);
#                     }
#                 }
                
#                 /* Right Side with smooth entrance */
#                 .right-panel {
#                     flex: 1;
#                     display: flex;
#                     align-items: center;
#                     justify-content: center;
#                     background: #fff8f0;
#                     padding: 60px;
#                     animation: slideInRight 0.8s ease-out;
#                 }
                
#                 @keyframes slideInRight {
#                     from {
#                         opacity: 0;
#                         transform: translateX(50px);
#                     }
#                     to {
#                         opacity: 1;
#                         transform: translateX(0);
#                     }
#                 }
                
#                 /* Login Card - Now integrated into right panel */
#                 .login-card {
#                     width: 100%;
#                     max-width: 420px;
#                     color: #3e2723;
#                     animation: scaleIn 0.6s ease-out 0.3s both;
#                 }
                
#                 @keyframes scaleIn {
#                     from {
#                         opacity: 0;
#                         transform: scale(0.9);
#                     }
#                     to {
#                         opacity: 1;
#                         transform: scale(1);
#                     }
#                 }
                
#                 .title {
#                     font-size: 28px;
#                     font-weight: 600;
#                     margin-bottom: 8px;
#                     color: #78350f;
#                 }
                
#                 .subtitle {
#                     opacity: 0.7;
#                     margin-bottom: 25px;
#                     color: #5d4037;
#                     font-size: 14px;
#                 }
                
#                 /* Input fields with smooth transitions */
#                 .input-style {
#                     margin-bottom: 16px;
#                 }
                
#                 .input-style input,
#                 .input-style .q-field__control {
#                     background: #f5e6d3 !important;
#                     color: #3e2723 !important;
#                     border: 1px solid #d4b896 !important;
#                     border-radius: 10px !important;
#                     transition: all 0.3s ease !important;
#                 }
                
#                 .input-style input:focus,
#                 .input-style .q-field__control:focus-within {
#                     border-color: #78350f !important;
#                     box-shadow: 0 0 0 3px rgba(120, 53, 15, 0.1) !important;
#                     transform: translateY(-1px);
#                 }
                
#                 .input-style input:hover,
#                 .input-style .q-field__control:hover {
#                     border-color: #8d6e63 !important;
#                 }
                
#                 /* Button - Brown Theme with smooth effects */
#                 .btn-style,
#                 .btn-style .q-btn__content {
#                     background: linear-gradient(135deg, #78350f 0%, #92400e 100%) !important;
#                     border: none !important;
#                     border-radius: 12px !important;
#                     font-weight: 600 !important;
#                     height: 50px !important;
#                     color: white !important;
#                     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
#                     box-shadow: 0 4px 12px rgba(120, 53, 15, 0.3) !important;
#                 }
                
#                 .btn-style:hover {
#                     transform: translateY(-2px) !important;
#                     box-shadow: 0 8px 20px rgba(120, 53, 15, 0.4) !important;
#                 }
                
#                 .btn-style:active {
#                     transform: translateY(0) !important;
#                     box-shadow: 0 2px 8px rgba(120, 53, 15, 0.3) !important;
#                 }
                
#                 /* Override Quasar button defaults */
#                 .q-btn {
#                     background: linear-gradient(135deg, #78350f 0%, #92400e 100%) !important;
#                 }
                
#                 .q-btn .q-btn__content {
#                     color: white !important;
#                 }
                
#                 .footer-text {
#                     margin-top: 20px;
#                     font-size: 14px;
#                     text-align: center;
#                     opacity: 0.8;
#                     color: #5d4037;
#                 }
                
#                 .link {
#                     color: #78350f;
#                     cursor: pointer;
#                     text-decoration: underline;
#                     font-weight: 600;
#                     transition: all 0.2s ease;
#                 }
                
#                 .link:hover {
#                     color: #92400e;
#                     text-decoration-thickness: 2px;
#                 }
                
#                 /* OTP Styles - Brown Theme with smooth animations */
#                 .otp-display-box {
#                     background: #f5e6d3;
#                     border: 2px dashed #8d6e63;
#                     border-radius: 12px;
#                     padding: 20px;
#                     margin: 20px 0;
#                     text-align: center;
#                     animation: fadeIn 0.5s ease-out;
#                 }
                
#                 @keyframes fadeIn {
#                     from { opacity: 0; }
#                     to { opacity: 1; }
#                 }
                
#                 .otp-label {
#                     opacity: 0.7;
#                     font-size: 14px;
#                     margin-bottom: 10px;
#                     color: #5d4037;
#                 }
                
#                 .otp-code-display {
#                     font-size: 2.5rem;
#                     font-weight: bold;
#                     letter-spacing: 10px;
#                     color: #78350f;
#                     font-family: 'Courier New', monospace;
#                     animation: slideDown 0.5s ease-out;
#                 }
                
#                 @keyframes slideDown {
#                     from {
#                         opacity: 0;
#                         transform: translateY(-10px);
#                     }
#                     to {
#                         opacity: 1;
#                         transform: translateY(0);
#                     }
#                 }
                
#                 .otp-inputs {
#                     display: flex;
#                     justify-content: center;
#                     gap: 15px;
#                     margin: 30px 0;
#                 }
                
#                 .otp-digit-input {
#                     width: 50px !important;
#                     height: 60px !important;
#                     font-size: 2rem !important;
#                     text-align: center !important;
#                     border: none !important;
#                     border-bottom: 3px solid #d4b896 !important;
#                     border-radius: 0 !important;
#                     background: transparent !important;
#                     color: #3e2723 !important;
#                     font-weight: bold !important;
#                     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
#                 }
                
#                 .otp-digit-input:focus {
#                     border-bottom-color: #78350f !important;
#                     outline: none !important;
#                     box-shadow: 0 4px 0 0 rgba(120, 53, 15, 0.3) !important;
#                     transform: scale(1.05);
#                 }
                
#                 .otp-digit-input:hover {
#                     border-bottom-color: #8d6e63 !important;
#                 }
                
#                 .otp-timer {
#                     font-size: 1.8rem;
#                     font-weight: bold;
#                     color: #78350f;
#                     margin: 20px 0;
#                     text-align: center;
#                     font-family: 'Courier New', monospace;
#                     transition: color 0.3s ease;
#                 }
                
#                 .otp-timer.expiring {
#                     color: #dc2626;
#                     animation: pulse 1s infinite;
#                 }
                
#                 @keyframes pulse {
#                     0%, 100% { 
#                         opacity: 1;
#                         transform: scale(1);
#                     }
#                     50% { 
#                         opacity: 0.7;
#                         transform: scale(1.05);
#                     }
#                 }
#             </style>
#         ''')
        
#         # Split container
#         with ui.element('div').classes('split-container'):
#             # LEFT SIDE (Welcome message with logo)
#             with ui.element('div').classes('left-panel'):
#                 with ui.element('div').classes('left-content'):
#                     ui.html('<div class="logo-icon">🛡️</div>')
#                     ui.html('<h1>Ashoka</h1>')
#                     ui.html('<p>GenAI Governance & Observability Platform. Log in to your dashboard to continue where you left off.</p>')
            
#             # RIGHT SIDE (Login form)
#             with ui.element('div').classes('right-panel'):
#                 self.card_container = ui.column().classes('login-card')
                
#                 with self.card_container:
#                     self._create_login_form()
    
#     def _create_login_form(self):
#         """Create login form"""
#         self.login_container = ui.column().classes('w-full')
        
#         with self.login_container:
#             ui.label('Welcome Back').classes('title')
#             ui.label('Sign in to continue').classes('subtitle')
            
#             # Username
#             self.username_input = ui.input(
#                 label='Username'
#             ).props('outlined').classes('w-full input-style')
            
#             # Password
#             self.password_input = ui.input(
#                 label='Password',
#                 password=True,
#                 password_toggle_button=True
#             ).props('outlined').classes('w-full input-style')
            
#             ui.space()
            
#             # Login button
#             ui.button(
#                 'SIGN IN',
#                 on_click=self._handle_login
#             ).props('no-caps').classes('btn-style w-full').style('background: linear-gradient(135deg, #78350f 0%, #92400e 100%) !important; color: white !important;')
            
#             # Signup link
#             with ui.element('div').classes('footer-text'):
#                 ui.html("Don't have an account? ")
#                 ui.html('<span class="link" id="signup-link">Sign up</span>').on('click', self._show_signup_form)
    
#     def _create_signup_form(self):
#         """Create signup form"""
#         self.login_container = ui.column().classes('w-full')
        
#         with self.login_container:
#             ui.label('Create Account').classes('title')
#             ui.label('Sign up to get started').classes('subtitle')
            
#             # Username
#             self.signup_username_input = ui.input(
#                 label='Username'
#             ).props('outlined').classes('w-full input-style')
            
#             # Email
#             self.signup_email_input = ui.input(
#                 label='Email'
#             ).props('outlined').classes('w-full input-style')
            
#             # Password
#             self.signup_password_input = ui.input(
#                 label='Password',
#                 password=True,
#                 password_toggle_button=True
#             ).props('outlined').classes('w-full input-style')
            
#             # Confirm Password
#             self.signup_confirm_password_input = ui.input(
#                 label='Confirm Password',
#                 password=True,
#                 password_toggle_button=True
#             ).props('outlined').classes('w-full input-style')
            
#             ui.space()
            
#             # Signup button
#             ui.button(
#                 'SIGN UP',
#                 on_click=self._handle_signup
#             ).props('no-caps').classes('btn-style w-full').style('background: linear-gradient(135deg, #78350f 0%, #92400e 100%) !important; color: white !important;')
            
#             # Login link
#             with ui.element('div').classes('footer-text'):
#                 ui.html("Already have an account? ")
#                 ui.html('<span class="link" id="login-link">Sign in</span>').on('click', self._show_login_form)
    
#     def _create_otp_form(self, otp_code: str):
#         """Create OTP verification form"""
#         self.otp_container = ui.column().classes('w-full')
        
#         with self.otp_container:
#             ui.label('Enter OTP').classes('title')
#             ui.label('We sent a code to verify your identity').classes('subtitle')
            
#             # Display OTP code in a box
#             with ui.element('div').classes('otp-display-box'):
#                 ui.label('Your OTP Code:').classes('otp-label')
#                 self.otp_code_label = ui.label(otp_code).classes('otp-code-display')
            
#             # OTP Input fields with underline style
#             with ui.element('div').classes('otp-inputs'):
#                 self.otp_digits = []
#                 for i in range(5):
#                     digit = ui.input().props('maxlength=1 outlined=false').classes('otp-digit-input')
#                     # Use keyup event for immediate response
#                     digit.on('keyup', lambda e, idx=i: self._handle_otp_keyup(e, idx))
#                     digit.on('keydown', lambda e, idx=i: self._handle_backspace(e, idx))
#                     self.otp_digits.append(digit)
            
#             # Timer
#             self.timer_label = ui.label('05:00').classes('otp-timer')
            
#             # Start countdown
#             self.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
#             ui.timer(1.0, self._update_timer)
            
#             ui.space()
            
#             # Verify button
#             ui.button(
#                 'VERIFY OTP',
#                 on_click=self._handle_otp_verification
#             ).props('no-caps').classes('btn-style w-full').style('background: linear-gradient(135deg, #78350f 0%, #92400e 100%) !important; color: white !important;')
            
#             # Resend link - make it functional
#             with ui.element('div').classes('footer-text'):
#                 ui.html("Didn't receive code? ")
#                 ui.html('<span class="link" id="resend-link">Resend OTP</span>').on('click', self._handle_resend_otp)
    
#     def _handle_otp_keyup(self, e, index):
#         """Handle OTP digit input with immediate auto-focus"""
#         if not e.args:
#             return
        
#         key = e.args.get('key', '')
        
#         # Ignore special keys
#         if key in ['Backspace', 'Delete', 'Tab', 'Enter', 'Escape', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']:
#             return
        
#         # Get current value
#         current_value = self.otp_digits[index].value or ''
        
#         # If a digit was entered, move to next input immediately
#         if current_value and len(current_value) >= 1:
#             # Keep only the last character
#             self.otp_digits[index].value = current_value[-1]
            
#             # Move to next digit if not last
#             if index < 4:
#                 self.otp_digits[index + 1].run_method('focus')
#             else:
#                 # Last digit - blur to show completion
#                 self.otp_digits[index].run_method('blur')
    
#     def _handle_otp_input(self, e, index):
#         """Handle OTP digit input with auto-focus"""
#         if not e.args:
#             return
            
#         value = e.args.get('value', '')
        
#         # If user typed a digit, move to next input
#         if value and len(value) >= 1:
#             # Take only the last character if multiple were pasted
#             self.otp_digits[index].value = value[-1]
            
#             # Move to next digit if not last
#             if index < 4:
#                 # Use JavaScript to focus next input
#                 self.otp_digits[index + 1].run_method('focus')
#             else:
#                 # Last digit - blur
#                 self.otp_digits[index].run_method('blur')
    
#     def _handle_backspace(self, e, index):
#         """Handle backspace to move to previous digit"""
#         if not e.args:
#             return
            
#         key = e.args.get('key', '')
        
#         if key == 'Backspace':
#             current_value = self.otp_digits[index].value or ''
#             if not current_value and index > 0:
#                 # Move to previous digit and clear it
#                 self.otp_digits[index - 1].value = ''
#                 self.otp_digits[index - 1].run_method('focus')
    
#     def _update_timer(self):
#         """Update OTP countdown timer"""
#         if datetime.utcnow() < self.otp_expiry:
#             remaining = self.otp_expiry - datetime.utcnow()
#             minutes = int(remaining.total_seconds() // 60)
#             seconds = int(remaining.total_seconds() % 60)
            
#             self.timer_label.set_text(f'{minutes:02d}:{seconds:02d}')
            
#             if remaining.total_seconds() <= 60:
#                 self.timer_label.classes(add='expiring')
#         else:
#             # Timer expired
#             self.timer_label.set_text('00:00')
#             ui.notify('OTP expired. Please login again.', type='negative')
    
#     async def _handle_login(self):
#         """Handle login submission"""
#         username = self.username_input.value
#         password = self.password_input.value
        
#         if not username or not password:
#             ui.notify('Please enter username and password', type='warning')
#             return
        
#         # Authenticate
#         result = auth_service.authenticate(username, password)
        
#         if not result.success:
#             ui.notify(result.error_message, type='negative')
#             return
        
#         if result.requires_otp:
#             self.current_user_id = result.user_id
            
#             # Get OTP
#             otp = auth_service.get_otp_for_user(result.user_id)
            
#             # Clear login form and show OTP form
#             self.login_container.clear()
#             with self.login_container:
#                 self._create_otp_form(otp.code)
            
#             # Auto-focus first digit
#             self.otp_digits[0].run_method('focus')
            
#             ui.notify('OTP sent! Check the code above.', type='positive')
    
#     async def _handle_signup(self):
#         """Handle signup submission"""
#         username = self.signup_username_input.value
#         email = self.signup_email_input.value
#         password = self.signup_password_input.value
#         confirm_password = self.signup_confirm_password_input.value
        
#         if not username or not email or not password or not confirm_password:
#             ui.notify('Please fill in all fields', type='warning')
#             return
        
#         if password != confirm_password:
#             ui.notify('Passwords do not match', type='negative')
#             return
        
#         # Register user
#         success, message = auth_service.signup(username, email, password)
        
#         if success:
#             ui.notify('Account created successfully! Please sign in.', type='positive')
#             await asyncio.sleep(1)
#             # Show login form
#             self._show_login_form()
#         else:
#             ui.notify(message, type='negative')
    
#     def _show_signup_form(self):
#         """Switch to signup form"""
#         self.login_container.clear()
#         with self.login_container:
#             self._create_signup_form()
    
#     def _show_login_form(self):
#         """Switch to login form"""
#         self.login_container.clear()
#         with self.login_container:
#             self._create_login_form()
    
#     def _handle_resend_otp(self):
#         """Handle resend OTP request"""
#         if not self.current_user_id:
#             ui.notify('Session expired. Please login again.', type='warning')
#             self._show_login_form()
#             return
        
#         # Generate new OTP
#         from src.services.auth_service import auth_service
#         otp = auth_service.generate_otp(self.current_user_id)
        
#         # Update the displayed OTP code
#         self.otp_code_label.set_text(otp.code)
        
#         # Clear OTP input fields
#         for digit in self.otp_digits:
#             digit.value = ''
        
#         # Reset timer
#         self.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
#         self.timer_label.set_text('05:00')
#         self.timer_label.classes(remove='expiring')
        
#         # Focus first digit
#         self.otp_digits[0].run_method('focus')
        
#         ui.notify('New OTP sent! Check the code above.', type='positive')
#         logger.info(f"OTP resent for user {self.current_user_id}: {otp.code}")
    
#     async def _handle_otp_verification(self):
#         """Handle OTP verification"""
#         # Prevent double-click
#         if hasattr(self, '_verifying') and self._verifying:
#             return
        
#         self._verifying = True
        
#         try:
#             # Collect OTP digits
#             otp_code = ''.join([digit.value or '' for digit in self.otp_digits])
            
#             if len(otp_code) != 5:
#                 ui.notify('Please enter all 5 digits', type='warning')
#                 return
            
#             logger.info(f"Verifying OTP for user {self.current_user_id}: {otp_code}")
            
#             # Verify OTP
#             success, message = auth_service.verify_otp(self.current_user_id, otp_code)
            
#             logger.info(f"OTP verification result: success={success}, message={message}")
            
#             if success:
#                 # Create session
#                 session = auth_service.create_session(self.current_user_id)
                
#                 logger.info(f"Session created: {session.session_token}")
                
#                 # Store session token in app storage (use session_token not session_id!)
#                 app.storage.general['session_token'] = session.session_token
#                 app.storage.general['user_id'] = self.current_user_id
                
#                 ui.notify('Login successful! Redirecting to dashboard...', type='positive')
                
#                 # Redirect to main dashboard
#                 await asyncio.sleep(1)
#                 ui.navigate.to('/dashboard')
#             else:
#                 ui.notify(message, type='negative')
#                 # Clear OTP fields on error to allow retry
#                 for digit in self.otp_digits:
#                     digit.value = ''
#                 self.otp_digits[0].run_method('focus')
#         finally:
#             self._verifying = False


# def create_auth_page_v2():
#     """Create modern authentication page"""
#     auth_page = AuthPageV2()
#     auth_page.create_auth_page()


from nicegui import ui, app
from datetime import datetime, timedelta
import asyncio

from src.services.auth_service import auth_service
from src.utils.logging import logger


class AuthPage:

    def __init__(self):
        self.current_user_id = None
        self.current_username = None  # Store username for session
        self.otp_expiry = None
        self.otp_digits = []
        self._verifying = False

    # =========================
    # MAIN PAGE
    # =========================

    def _set_story_panel(self, mode: str):
        if mode == "signup":
            self.story_button.set_visibility(True)
            self.story_eyebrow.set_text("Ashoka")
            self.story_title.set_text("Already have an account?")
            self.story_text.set_text(
                "Sign in to continue managing your GenAI governance and observability workflows."
            )
            self.story_button.set_text("Sign In")
            self.story_button.on_click(self._create_login_form)
        elif mode == "otp":
            self.story_button.set_visibility(False)
            self.story_eyebrow.set_text("Ashoka")
            self.story_title.set_text("Complete verification")
            self.story_text.set_text(
                "Use the one-time code to finish secure access to your workspace."
            )
        else:
            self.story_button.set_visibility(True)
            self.story_eyebrow.set_text("Ashoka")
            self.story_title.set_text("New here?")
            self.story_text.set_text(
                "Create your account to access Ashoka's GenAI governance and observability platform."
            )
            self.story_button.set_text("Sign Up")
            self.story_button.on_click(self._show_signup_form)

    def create_auth_page(self):

        ui.add_head_html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

        :root {
            --bg-cream: #ded5c4;
            --panel-cream: #efeeeb;
            --ink: #102d32;
            --ink-soft: #4e6b71;
            --teal: #1f7d78;
            --teal-deep: #176a66;
            --teal-mid: #2d8a84;
            --blue: #5b93c9;
            --blue-deep: #4d86be;
            --line: rgba(16, 45, 50, 0.18);
        }

        body {
            margin: 0;
            font-family: 'IBM Plex Sans', sans-serif;
            background: linear-gradient(150deg, #dfd5c4, var(--bg-cream));
            min-height: 100vh;
            color: var(--ink);
        }

        .layout {
            min-height: 100vh;
            width: min(1200px, 100%);
            margin: 0 auto;
            padding: 24px;
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 24px;
            align-items: stretch;
            box-sizing: border-box;
        }

        .panel-story {
            position: relative;
            border-radius: 30px;
            overflow: hidden;
            background:
                radial-gradient(circle at 86% 8%, rgba(145, 182, 103, 0.55) 0, rgba(145, 182, 103, 0.52) 120px, transparent 170px),
                radial-gradient(circle at 0% 100%, rgba(119, 178, 191, 0.35) 0, rgba(119, 178, 191, 0.32) 110px, transparent 180px),
                linear-gradient(145deg, var(--teal-mid), var(--teal));
            box-shadow: 0 10px 26px rgba(28, 97, 103, 0.2);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 52px;
            color: #ecfeff;
        }

        .story-content {
            position: relative;
            z-index: 2;
            width: min(520px, 100%);
        }

        .story-eyebrow {
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 0.02em;
            text-transform: none;
            font-size: 28px;
            font-weight: 700;
            opacity: 0.98;
            margin-bottom: 22px;
        }

        .cta-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 3vw, 3rem);
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 14px;
            color: #f8fffe;
        }

        .cta-text {
            font-size: 16px;
            line-height: 1.55;
            margin-bottom: 30px;
            opacity: 0.9;
            max-width: 48ch;
        }

        .btn-outline {
            height: 48px;
            border-radius: 12px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--blue), #6aa4db) !important;
            color: #ffffff !important;
            border: 1px solid rgba(200, 230, 255, 0.25);
            transition: box-shadow 0.2s ease;
        }

        .btn-outline:hover {
            box-shadow: 0 10px 22px rgba(30, 83, 129, 0.24);
        }

        .orb {
            position: absolute;
            border-radius: 999px;
            filter: blur(0px);
            z-index: 1;
            opacity: 0.45;
        }

        .orb-a {
            width: 280px;
            height: 280px;
            background: rgba(149, 188, 107, 0.4);
            top: -90px;
            right: -60px;
        }

        .orb-b {
            width: 220px;
            height: 220px;
            background: rgba(136, 196, 208, 0.24);
            bottom: -80px;
            left: -60px;
        }

        .panel-auth {
            border-radius: 30px;
            padding: 22px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: var(--panel-cream);
            border: 1px solid rgba(255,255,255,0.55);
            box-shadow: 0 10px 24px rgba(69, 84, 87, 0.12);
        }

        .form-container {
            width: min(440px, 100%);
            padding: 24px 18px;
        }

        .form-stack {
            gap: 12px;
        }

        .brand {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--teal-deep);
            letter-spacing: 0.03em;
            margin-bottom: 8px;
        }

        .title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 2.4vw, 2.7rem);
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--ink);
            line-height: 1.15;
        }

        .subtitle {
            font-size: 15px;
            color: var(--ink-soft);
            margin-bottom: 18px;
            line-height: 1.55;
        }

        .field {
            width: 100%;
        }

        .form-container .q-field--outlined .q-field__control {
            border-radius: 12px !important;
            background: #f5f6f7 !important;
            border: 1px solid var(--line) !important;
            min-height: 54px;
            transition: border-color .2s ease, box-shadow .2s ease !important;
        }

        .form-container .q-field--focused .q-field__control {
            border-color: rgba(91, 147, 201, 0.65) !important;
            box-shadow: 0 0 0 3px rgba(91, 147, 201, 0.18) !important;
        }

        .btn-main {
            margin-top: 4px;
            height: 50px;
            border-radius: 12px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--blue), var(--blue-deep)) !important;
            color: white !important;
            box-shadow: 0 10px 20px rgba(67, 112, 154, 0.24);
            transition: box-shadow .2s ease;
        }

        .btn-main:hover {
            box-shadow: 0 14px 28px rgba(67, 112, 154, 0.28);
        }

        .btn-link {
            margin-top: 6px;
            color: var(--blue-deep);
            font-weight: 600;
        }

        .social-wrap {
            margin-top: 10px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .social-label {
            color: var(--ink-soft);
            font-size: 14px;
            margin-right: 6px;
        }

        .social-icons {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .social-btn {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            border: 1px solid var(--line);
            background: #f5f6f7;
            display: inline-flex;
            justify-content: center;
            align-items: center;
        }

        .social-btn img {
            width: 18px;
            height: 18px;
            display: block;
        }

        .otp-box {
            text-align: left;
            margin: 8px 0 2px;
            color: var(--ink-soft);
            font-size: 14px;
        }

        .otp-inputs {
            display: flex;
            justify-content: flex-start;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 20px;
        }

        .otp-digit {
            width: 56px;
        }

        .otp-digit .q-field__control {
            width: 56px !important;
            min-height: 56px !important;
            border-radius: 12px !important;
            border: 1px solid var(--line) !important;
            background: #f5f6f7 !important;
            box-shadow: none !important;
        }

        .otp-digit .q-field__native {
            text-align: center !important;
            font-size: 22px !important;
            font-weight: 500;
            padding: 0 !important;
        }

        .timer {
            margin-top: 15px;
            font-weight: 600;
            color: var(--blue-deep);
            letter-spacing: 0.05em;
        }

        @media (max-width: 960px) {
            .layout {
                grid-template-columns: 1fr;
                padding: 14px;
                gap: 14px;
            }
            .panel-story {
                min-height: 320px;
                padding: 30px 24px;
            }
            .panel-auth {
                padding: 10px;
            }
            .form-container {
                padding: 20px 12px;
            }
        }

        @media (max-width: 460px) {
            .story-eyebrow {
                font-size: 24px;
            }
            .cta-title {
                font-size: 1.8rem;
            }
            .btn-main,
            .btn-outline {
                height: 46px;
            }
        }

        </style>
        """)

        with ui.element("div").classes("layout"):

            with ui.element("div").classes("panel-story"):
                ui.element("div").classes("orb orb-a")
                ui.element("div").classes("orb orb-b")
                with ui.column().classes("story-content"):
                    self.story_eyebrow = ui.label().classes("story-eyebrow")
                    self.story_title = ui.label().classes("cta-title")
                    self.story_text = ui.label().classes("cta-text")
                    self.story_button = ui.button().props("no-caps").classes("btn-outline w-48")

            with ui.element("div").classes("panel-auth"):
                self.card = ui.column().classes("form-container form-stack")
                with self.card:
                    self._create_login_form()

    # =========================
    # LOGIN FORM
    # =========================

    def _create_login_form(self):
        self.card.clear()

        with self.card:
            self._set_story_panel("login")
            ui.label("Ashoka").classes("brand")
            ui.label("Login to Your Account").classes("title")
            ui.label("Secure access to your governance dashboard").classes("subtitle")

            self.username_input = ui.input("Username").props("outlined").classes("field")
            self.password_input = ui.input(
                "Password",
                password=True,
                password_toggle_button=True
            ).props("outlined").classes("field")

            ui.button(
                "Sign In",
                on_click=self._handle_login
            ).props("no-caps").classes("btn-main w-full")

            with ui.element("div").classes("social-wrap"):
                ui.label("or").classes("social-label")
                ui.html(
                    '<div class="social-icons">'
                    '<span class="social-btn" title="Adding soon"><img alt="Google" src="https://cdn.simpleicons.org/google"></span>'
                    '<span class="social-btn" title="Adding soon"><img alt="X" src="https://cdn.simpleicons.org/x"></span>'
                    '<span class="social-btn" title="Adding soon"><img alt="Facebook" src="https://cdn.simpleicons.org/facebook"></span>'
                    '</div>'
                )

            ui.button(
                "Need an account? Sign up",
                on_click=self._show_signup_form
            ).props("flat no-caps").classes("btn-link")

    # =========================
    # SIGNUP FORM
    # =========================

    def _show_signup_form(self):
        self.card.clear()

        with self.card:
            self._set_story_panel("signup")
            ui.label("Ashoka").classes("brand")
            ui.label("Create Account").classes("title")
            ui.label("Sign up to get started").classes("subtitle")

            self.signup_username = ui.input("Username").props("outlined").classes("field")
            self.signup_email = ui.input("Email").props("outlined").classes("field")
            self.signup_password = ui.input(
                "Password",
                password=True,
                password_toggle_button=True
            ).props("outlined").classes("field")
            self.signup_confirm = ui.input(
                "Confirm Password",
                password=True,
                password_toggle_button=True
            ).props("outlined").classes("field")
            
            # Role selection dropdown
            self.signup_role = ui.select(
                label="Choose Role",
                options=["User", "Creator"],
                value="User"
            ).props("outlined").classes("field")

            ui.button(
                "Sign Up",
                on_click=self._handle_signup
            ).props("no-caps").classes("btn-main w-full")
            ui.button(
                "Back to Sign In",
                on_click=self._create_login_form
            ).props("flat no-caps").classes("btn-link")

    # =========================
    # OTP FORM
    # =========================

    def _create_otp_form(self, otp_code: str):
        self.card.clear()

        with self.card:
            self._set_story_panel("otp")
            ui.label("Ashoka").classes("brand")
            ui.label("Enter OTP").classes("title")
            ui.label("Check the code sent to you").classes("subtitle")

            with ui.element("div").classes("otp-box"):
                ui.label(f"OTP: {otp_code}")

            with ui.element("div").classes("otp-inputs"):
                self.otp_digits = []
                for i in range(5):
                    digit = ui.input().props("maxlength=1 outlined inputmode=numeric").classes("otp-digit")
                    digit.on("keyup", lambda e, idx=i: self._handle_otp_keyup(idx))
                    self.otp_digits.append(digit)

            self.timer_label = ui.label("05:00").classes("timer")

            self.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
            ui.timer(1.0, self._update_timer)

            ui.button(
                "Verify OTP",
                on_click=self._handle_otp_verification
            ).props("no-caps").classes("btn-main w-full")

            ui.button(
                "Resend OTP",
                on_click=self._handle_resend_otp
            ).props("flat no-caps").classes("btn-link")

            ui.label("Need to change details?").classes("subtitle").style("margin-top: 8px; margin-bottom: 0;")
            ui.button(
                "Sign In",
                on_click=self._create_login_form
            ).props("flat no-caps").classes("btn-link").style("margin-top: 0;")

    # =========================
    # LOGIN LOGIC
    # =========================

    async def _handle_login(self):
        # self.current_user_id = "test-user"
        # self._create_otp_form("12345")
        # ui.notify("OTP sent (test mode)", type="positive")
        username = self.username_input.value
        password = self.password_input.value

        if not username or not password:
            ui.notify("Enter username and password", type="warning")
            return

        result = auth_service.authenticate(username, password)

        if not result.success:
            ui.notify(result.error_message, type="negative")
            return

        if result.requires_otp:
            self.current_user_id = result.user_id
            self.current_username = username  # Store username for later use
            otp = auth_service.get_otp_for_user(result.user_id)
            self._create_otp_form(otp.code)
            ui.notify("OTP sent", type="positive")

    async def _handle_signup(self):
        #ui.notify("Signup functionality is currently disabled for testing", type="info")
        username = self.signup_username.value
        email = self.signup_email.value
        password = self.signup_password.value
        confirm = self.signup_confirm.value
        role = self.signup_role.value.lower()  # Get selected role and convert to lowercase

        if not username or not email or not password or not confirm:
            ui.notify("Fill all fields", type="warning")
            return

        if password != confirm:
            ui.notify("Passwords do not match", type="negative")
            return

        success, message = auth_service.signup(username, email, password, role)

        if success:
            ui.notify("Account created", type="positive")
            await asyncio.sleep(1)
            self._create_login_form()
        else:
            ui.notify(message, type="negative")

    # =========================
    # OTP LOGIC
    # =========================

    def _handle_otp_keyup(self, index):
        if index < 4:
            self.otp_digits[index + 1].run_method("focus")

    def _update_timer(self):
        if datetime.utcnow() < self.otp_expiry:
            remaining = self.otp_expiry - datetime.utcnow()
            mins = int(remaining.total_seconds() // 60)
            secs = int(remaining.total_seconds() % 60)
            self.timer_label.set_text(f"{mins:02d}:{secs:02d}")
        else:
            self.timer_label.set_text("00:00")

    async def _handle_otp_verification(self):
        #ui.notify("OTP verification is currently disabled for testing", type="info")
        if self._verifying:
            return

        self._verifying = True

        otp_code = ''.join([d.value or '' for d in self.otp_digits])

        if len(otp_code) != 5:
            ui.notify("Enter full OTP", type="warning")
            self._verifying = False
            return

        success, message = auth_service.verify_otp(self.current_user_id, otp_code)

        if success:
            session = auth_service.create_session(self.current_user_id)
            app.storage.general["session_token"] = session.session_token
            app.storage.general["user_id"] = self.current_user_id
            app.storage.general["username"] = self.current_username  # Use stored username
            ui.notify("Login successful", type="positive")
            await asyncio.sleep(1)
            ui.navigate.to("/dashboard")
        else:
            ui.notify(message, type="negative")

        self._verifying = False

    def _handle_resend_otp(self):
        #ui.notify("Resend OTP functionality is currently disabled for testing", type="info")
        otp = auth_service.generate_otp(self.current_user_id)
        self._create_otp_form(otp.code)
        ui.notify("OTP resent", type="positive")


def create_auth_page():
    AuthPage().create_auth_page()
# create_auth_page()
# ui.run()
