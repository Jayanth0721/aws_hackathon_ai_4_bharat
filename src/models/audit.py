"""Audit and logging models"""
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field


class LoginAttempt(BaseModel):
    """Login attempt record"""
    username: str
    timestamp: datetime
    success: bool
    failure_reason: Optional[str] = None
    ip_address: str = "0.0.0.0"


class MonthlyReport(BaseModel):
    """Monthly login activity report"""
    user_id: str
    period: str = Field(pattern=r"^\d{4}-\d{2}$")  # YYYY-MM format
    successful_logins: int = 0
    failed_attempts: int = 0
    total_session_duration: timedelta = timedelta()
    average_session_duration: timedelta = timedelta()
    login_attempts: List[LoginAttempt] = Field(default_factory=list)
