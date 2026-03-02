"""ID generation utilities"""
import uuid
from datetime import datetime


def generate_id(prefix: str = "") -> str:
    """Generate unique identifier with optional prefix"""
    unique_id = str(uuid.uuid4())
    return f"{prefix}{unique_id}" if prefix else unique_id


def generate_version_id() -> str:
    """Generate version identifier"""
    return generate_id("ver_")


def generate_session_token() -> str:
    """Generate session token"""
    return generate_id("sess_")


def generate_otp_code() -> str:
    """Generate 6-digit OTP code"""
    import random
    return f"{random.randint(100000, 999999)}"


def generate_content_id() -> str:
    """Generate content identifier"""
    return generate_id("cnt_")


def generate_alert_id() -> str:
    """Generate alert identifier"""
    return generate_id("alt_")
