# """Authentication service with OTP"""
# import bcrypt
# from datetime import datetime, timedelta
# from typing import Optional, Tuple
# import random

# from src.models.auth import User, OTP, Session, AuthResult
# from src.database.mock_storage import mock_dynamodb
# from src.utils.id_generator import generate_session_token
# from src.utils.timestamp import utc_now
# from src.config import config
# from src.utils.logging import logger


# class AuthService:
#     """Authentication service"""
    
#     def __init__(self):
#         self.dynamodb = mock_dynamodb
#         self.active_otps = {}  # user_id -> OTP object
#         self.security_service = None  # Lazy load to avoid circular import
    
#     def _get_security_service(self):
#         """Lazy load security service"""
#         if self.security_service is None:
#             from src.services.security_service import security_service
#             self.security_service = security_service
#         return self.security_service
    
#     def signup(self, username: str, email: str, password: str) -> Tuple[bool, str]:
#         """Register new user"""
#         # Check if user exists
#         existing_user = self._get_user_by_username(username)
#         if existing_user:
#             return False, "Username already exists"
        
#         # Hash password
#         password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
#         # Create user
#         user_id = f"user_{username}"
#         user = User(
#             user_id=user_id,
#             username=username,
#             password_hash=password_hash,
#             email=email,
#             created_at=utc_now(),
#             is_active=True,
#             role="creator"
#         )
        
#         # Store in database
#         self.dynamodb.put_item(
#             config.DYNAMODB_USERS_TABLE,
#             {
#                 "user_id": user.user_id,
#                 "username": user.username,
#                 "password_hash": user.password_hash,
#                 "email": user.email,
#                 "created_at": user.created_at.isoformat(),
#                 "is_active": user.is_active,
#                 "role": user.role
#             }
#         )
        
#         logger.info(f"User registered: {username}")
#         return True, "Registration successful"
    
#     def authenticate(self, username: str, password: str) -> AuthResult:
#         """Authenticate user credentials"""
#         user = self._get_user_by_username(username)
        
#         security = self._get_security_service()
        
#         if not user:
#             # Log failed login
#             security.log_login_attempt(
#                 username=username,
#                 ip_address='192.168.1.100',  # Mock IP
#                 location='Bangalore, IN',
#                 device_info='Chrome/Windows',
#                 status='Failed'
#             )
#             return AuthResult(
#                 success=False,
#                 error_message="Invalid username or password"
#             )
        
#         # Verify password
#         if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
#             # Log failed login
#             security.log_login_attempt(
#                 username=username,
#                 ip_address='192.168.1.100',  # Mock IP
#                 location='Bangalore, IN',
#                 device_info='Chrome/Windows',
#                 status='Failed'
#             )
#             return AuthResult(
#                 success=False,
#                 error_message="Invalid username or password"
#             )
        
#         # Generate OTP
#         otp = self.generate_otp(user.user_id)
        
#         # Log security event
#         security.log_security_event(
#             username=username,
#             event_type='password_verified',
#             event_description='Password verified successfully'
#         )
        
#         logger.info(f"Authentication successful for {username}, OTP generated")
#         return AuthResult(
#             success=True,
#             user_id=user.user_id,
#             requires_otp=True
#         )
    
#     def generate_otp(self, user_id: str) -> OTP:
#         """Generate 5-digit OTP"""
#         code = f"{random.randint(10000, 99999)}"
#         created_at = utc_now()
#         expires_at = created_at + timedelta(minutes=config.OTP_EXPIRATION_MINUTES)
        
#         otp = OTP(
#             code=code,
#             user_id=user_id,
#             created_at=created_at,
#             expires_at=expires_at,
#             is_used=False
#         )
        
#         # Store OTP
#         self.active_otps[user_id] = otp
        
#         logger.info(f"OTP generated for user {user_id}: {code}")
#         return otp
    
#     def verify_otp(self, user_id: str, otp_code: str) -> Tuple[bool, str]:
#         """Verify OTP code"""
#         if user_id not in self.active_otps:
#             return False, "No OTP found. Please login again."
        
#         otp = self.active_otps[user_id]
        
#         # Check if expired
#         if utc_now() > otp.expires_at:
#             del self.active_otps[user_id]
#             return False, "OTP expired. Please login again."
        
#         # Check if already used
#         if otp.is_used:
#             return False, "OTP already used. Please login again."
        
#         # Verify code
#         if otp.code != otp_code:
#             # Don't mark as used on incorrect code - allow retry
#             return False, "Invalid OTP code"
        
#         # Mark as used only on successful verification
#         otp.is_used = True
        
#         logger.info(f"OTP verified for user {user_id}")
#         return True, "OTP verified successfully"
    
#     def create_session(self, user_id: str) -> Session:
#         """Create user session"""
#         session_token = generate_session_token()
#         created_at = utc_now()
#         expires_at = created_at + timedelta(minutes=config.SESSION_TIMEOUT_MINUTES)
        
#         session = Session(
#             session_token=session_token,
#             user_id=user_id,
#             created_at=created_at,
#             last_activity=created_at,
#             expires_at=expires_at,
#             is_active=True
#         )
        
#         # Store session
#         self.dynamodb.put_item(
#             config.DYNAMODB_SESSIONS_TABLE,
#             {
#                 "session_token": session.session_token,
#                 "user_id": session.user_id,
#                 "created_at": session.created_at.isoformat(),
#                 "last_activity": session.last_activity.isoformat(),
#                 "expires_at": session.expires_at.isoformat(),
#                 "is_active": session.is_active
#             }
#         )
        
#         # Log successful login
#         security = self._get_security_service()
#         user = self._get_user_by_id(user_id)
#         if user:
#             security.log_login_attempt(
#                 username=user.username,
#                 ip_address='192.168.1.100',  # Mock IP
#                 location='Bangalore, IN',
#                 device_info='Chrome/Windows',
#                 status='Success',
#                 session_id=session_token
#             )
            
#             security.log_security_event(
#                 username=user.username,
#                 event_type='login',
#                 event_description='Successful login',
#                 metadata={'session_id': session_token}
#             )
        
#         logger.info(f"Session created for user {user_id}")
#         return session
    
#     def _get_user_by_id(self, user_id: str) -> Optional[User]:
#         """Get user by user_id"""
#         user_data = self.dynamodb.get_item(
#             config.DYNAMODB_USERS_TABLE,
#             {"user_id": user_id}
#         )
        
#         if not user_data:
#             return None
        
#         return User(
#             user_id=user_data["user_id"],
#             username=user_data["username"],
#             password_hash=user_data["password_hash"],
#             email=user_data["email"],
#             created_at=datetime.fromisoformat(user_data["created_at"]),
#             is_active=user_data["is_active"],
#             role=user_data["role"]
#         )
    
#     def get_otp_for_user(self, user_id: str) -> Optional[OTP]:
#         """Get active OTP for user"""
#         return self.active_otps.get(user_id)
    
#     def _get_user_by_username(self, username: str) -> Optional[User]:
#         """Get user by username"""
#         user_id = f"user_{username}"
#         user_data = self.dynamodb.get_item(
#             config.DYNAMODB_USERS_TABLE,
#             {"user_id": user_id}
#         )
        
#         if not user_data:
#             return None
        
#         return User(
#             user_id=user_data["user_id"],
#             username=user_data["username"],
#             password_hash=user_data["password_hash"],
#             email=user_data["email"],
#             created_at=datetime.fromisoformat(user_data["created_at"]),
#             is_active=user_data["is_active"],
#             role=user_data["role"]
#         )


# # Global auth service instance
# auth_service = AuthService()




"""Authentication service with OTP"""
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Tuple
import random

from src.models.auth import User, OTP, Session, AuthResult
from src.database.db_factory import get_dynamodb
from src.utils.id_generator import generate_session_token
from src.utils.timestamp import utc_now
from src.config import config
from src.utils.logging import logger


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.dynamodb = get_dynamodb()
        self.active_otps = {}  # user_id -> OTP object
        self.security_service = None  # Lazy load to avoid circular import
    
    def _get_security_service(self):
        """Lazy load security service"""
        if self.security_service is None:
            from src.services.security_service import security_service
            self.security_service = security_service
        return self.security_service
    
    def signup(self, username: str, email: str, password: str, role: str = "user") -> Tuple[bool, str]:
        """Register new user"""
        # Validate role
        valid_roles = ["user", "creator", "admin"]
        if role.lower() not in valid_roles:
            role = "user"  # Default to user if invalid role provided
        
        # Check if user exists
        existing_user = self._get_user_by_username(username)
        if existing_user:
            return False, "Username already exists"
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        user_id = f"user_{username}"
        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            email=email,
            created_at=utc_now(),
            is_active=True,
            role=role.lower()
        )
        
        # Store in database
        self.dynamodb.put_item(
            config.DYNAMODB_USERS_TABLE,
            {
                "user_id": user.user_id,
                "username": user.username,
                "password_hash": user.password_hash,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "is_active": user.is_active,
                "role": user.role
            }
        )
        
        logger.info(f"User registered: {username} with role: {role}")
        return True, "Registration successful"
    
    def authenticate(self, username: str, password: str) -> AuthResult:
        """Authenticate user credentials"""
        user = self._get_user_by_username(username)
        
        security = self._get_security_service()
        
        if not user:
            # Log failed login
            security.log_login_attempt(
                username=username,
                ip_address='192.168.1.100',  # Mock IP
                location='Bangalore, IN',
                device_info='Chrome/Windows',
                status='Failed'
            )
            return AuthResult(
                success=False,
                error_message="Invalid username or password"
            )
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            # Log failed login
            security.log_login_attempt(
                username=username,
                ip_address='192.168.1.100',  # Mock IP
                location='Bangalore, IN',
                device_info='Chrome/Windows',
                status='Failed'
            )
            return AuthResult(
                success=False,
                error_message="Invalid username or password"
            )
        
        # Generate OTP
        otp = self.generate_otp(user.user_id)
        
        # Log security event
        security.log_security_event(
            username=username,
            event_type='password_verified',
            event_description='Password verified successfully'
        )
        
        logger.info(f"Authentication successful for {username}, OTP generated")
        return AuthResult(
            success=True,
            user_id=user.user_id,
            requires_otp=True
        )
    
    def generate_otp(self, user_id: str) -> OTP:
        """Generate 5-digit OTP"""
        code = f"{random.randint(10000, 99999)}"
        created_at = utc_now()
        expires_at = created_at + timedelta(minutes=config.OTP_EXPIRATION_MINUTES)
        
        otp = OTP(
            code=code,
            user_id=user_id,
            created_at=created_at,
            expires_at=expires_at,
            is_used=False
        )
        
        # Store OTP
        self.active_otps[user_id] = otp
        
        logger.info(f"OTP generated for user {user_id}: {code}")
        return otp
    
    def verify_otp(self, user_id: str, otp_code: str) -> Tuple[bool, str]:
        """Verify OTP code"""
        if user_id not in self.active_otps:
            return False, "No OTP found. Please login again."
        
        otp = self.active_otps[user_id]
        
        # Check if expired
        if utc_now() > otp.expires_at:
            del self.active_otps[user_id]
            return False, "OTP expired. Please login again."
        
        # Check if already used
        if otp.is_used:
            return False, "OTP already used. Please login again."
        
        # Verify code
        if otp.code != otp_code:
            # Don't mark as used on incorrect code - allow retry
            return False, "Invalid OTP code"
        
        # Mark as used only on successful verification
        otp.is_used = True
        
        logger.info(f"OTP verified for user {user_id}")
        return True, "OTP verified successfully"
    
    def create_session(self, user_id: str) -> Session:
        """Create user session"""
        session_token = generate_session_token()
        created_at = utc_now()
        expires_at = created_at + timedelta(minutes=config.SESSION_TIMEOUT_MINUTES)
        
        session = Session(
            session_token=session_token,
            user_id=user_id,
            created_at=created_at,
            last_activity=created_at,
            expires_at=expires_at,
            is_active=True
        )
        
        # Store session
        self.dynamodb.put_item(
            config.DYNAMODB_SESSIONS_TABLE,
            {
                "session_token": session.session_token,
                "user_id": session.user_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "is_active": session.is_active
            }
        )
        
        # Log successful login
        security = self._get_security_service()
        user = self._get_user_by_id(user_id)
        if user:
            security.log_login_attempt(
                username=user.username,
                ip_address='192.168.1.100',  # Mock IP
                location='Bangalore, IN',
                device_info='Chrome/Windows',
                status='Success',
                session_id=session_token
            )
            
            security.log_security_event(
                username=user.username,
                event_type='login',
                event_description='Successful login',
                metadata={'session_id': session_token}
            )
        
        logger.info(f"Session created for user {user_id}")
        return session

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Public accessor for user by id."""
        return self._get_user_by_id(user_id)

    def get_user_role(self, user_id: str) -> Optional[str]:
        """Get role for a user_id."""
        user = self._get_user_by_id(user_id)
        return user.role if user else None

    def set_user_role(self, user_id: str, role: str) -> Tuple[bool, str]:
        """Set user role for access control."""
        allowed_roles = {"creator", "admin", "operator"}
        if role not in allowed_roles:
            return False, f"Invalid role: {role}"

        user_data = self.dynamodb.get_item(
            config.DYNAMODB_USERS_TABLE,
            {"user_id": user_id}
        )
        if not user_data:
            return False, f"User not found: {user_id}"

        user_data["role"] = role
        self.dynamodb.put_item(config.DYNAMODB_USERS_TABLE, user_data)
        logger.info(f"Updated role for {user_id} to {role}")
        return True, "Role updated"
    
    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by user_id"""
        user_data = self.dynamodb.get_item(
            config.DYNAMODB_USERS_TABLE,
            {"user_id": user_id}
        )
        
        if not user_data:
            logger.warning(f"User not found: {user_id}")
            return None
        
        # Debug: Log the retrieved data
        logger.debug(f"Retrieved user data keys: {list(user_data.keys())}")
        
        # Check if required fields exist
        required_fields = ['user_id', 'username', 'password_hash', 'email', 'created_at', 'is_active', 'role']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            logger.error(f"Missing fields in user data: {missing_fields}")
            logger.error(f"Available fields: {list(user_data.keys())}")
            logger.error(f"User data: {user_data}")
            return None
        
        # Handle datetime conversion - DuckDB returns datetime objects, not strings
        created_at = user_data["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        last_login = user_data.get("last_login")
        if last_login and isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login)
        
        return User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            password_hash=user_data["password_hash"],
            email=user_data["email"],
            created_at=created_at,
            last_login=last_login,
            is_active=user_data["is_active"],
            role=user_data["role"]
        )
    
    def get_otp_for_user(self, user_id: str) -> Optional[OTP]:
        """Get active OTP for user"""
        return self.active_otps.get(user_id)
    
    def _get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        user_id = f"user_{username}"
        user_data = self.dynamodb.get_item(
            config.DYNAMODB_USERS_TABLE,
            {"user_id": user_id}
        )
        
        if not user_data:
            return None
        
        # Handle datetime conversion - DuckDB returns datetime objects, not strings
        created_at = user_data["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        last_login = user_data.get("last_login")
        if last_login and isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login)
        
        return User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            password_hash=user_data["password_hash"],
            email=user_data["email"],
            created_at=created_at,
            last_login=last_login,
            is_active=user_data["is_active"],
            role=user_data["role"]
        )


# Global auth service instance
auth_service = AuthService()
