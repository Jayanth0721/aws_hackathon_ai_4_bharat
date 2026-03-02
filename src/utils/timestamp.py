"""Timestamp handling utilities"""
from datetime import datetime, timedelta
from typing import Optional


def utc_now() -> datetime:
    """Get current UTC timestamp"""
    return datetime.utcnow()


def add_minutes(dt: datetime, minutes: int) -> datetime:
    """Add minutes to datetime"""
    return dt + timedelta(minutes=minutes)


def is_expired(dt: datetime, expiration_minutes: int) -> bool:
    """Check if datetime has expired"""
    expiration_time = add_minutes(dt, expiration_minutes)
    return utc_now() > expiration_time


def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO string"""
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string"""
    return datetime.fromisoformat(timestamp_str)


def calculate_duration(start: datetime, end: Optional[datetime] = None) -> timedelta:
    """Calculate duration between timestamps"""
    if end is None:
        end = utc_now()
    return end - start
