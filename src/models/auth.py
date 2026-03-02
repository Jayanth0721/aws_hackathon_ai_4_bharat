"""Authentication and session models"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    """User model"""
    user_id: str
    username: str
    password_hash: str
    email: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    role: str = Field(default="user", pattern="^(user|creator|admin|operator)$")


class OTP(BaseModel):
    """One-Time Password model"""
    code: str = Field(min_length=5, max_length=6)
    user_id: str
    created_at: datetime
    expires_at: datetime
    is_used: bool = False
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('OTP code must be numeric')
        return v


class Session(BaseModel):
    """User session model"""
    session_token: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    is_active: bool = True


class AuthResult(BaseModel):
    """Authentication result"""
    success: bool
    user_id: Optional[str] = None
    requires_otp: bool = False
    error_message: Optional[str] = None


class SessionValidation(BaseModel):
    """Session validation result"""
    is_valid: bool
    session: Optional[Session] = None
    reason: Optional[str] = None
