"""Configuration management for Ashoka Platform"""
import os
from typing import Optional


class Config:
    """Application configuration"""
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # S3 Configuration
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "ashoka-content-bucket")
    
    # DynamoDB Configuration
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "ashoka_contentint")
    DYNAMODB_SESSIONS_TABLE: str = os.getenv("DYNAMODB_SESSIONS_TABLE", os.getenv("DYNAMODB_TABLE", "ashoka_contentint"))
    DYNAMODB_AUDIT_TABLE: str = os.getenv("DYNAMODB_AUDIT_TABLE", os.getenv("DYNAMODB_TABLE", "ashoka_contentint"))
    DYNAMODB_ALERTS_TABLE: str = os.getenv("DYNAMODB_ALERTS_TABLE", os.getenv("DYNAMODB_TABLE", "ashoka_contentint"))
    DYNAMODB_USERS_TABLE: str = os.getenv("DYNAMODB_USERS_TABLE", os.getenv("DYNAMODB_TABLE", "ashoka_contentint"))
    DYNAMODB_CONTENT_TABLE: str = os.getenv("DYNAMODB_CONTENT_TABLE", os.getenv("DYNAMODB_TABLE", "ashoka_contentint"))
    
    # DuckDB Configuration (local development)
    DUCKDB_PATH: str = os.getenv("DUCKDB_PATH", "data/ashoka.duckdb")
    
    # Database Mode Configuration
    USE_REAL_DYNAMODB: bool = os.getenv("USE_REAL_DYNAMODB", "false").lower() == "true"
    
    # Google Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    USE_GEMINI: bool = os.getenv("USE_GEMINI", "true").lower() == "true"
    
    # Hugging Face Configuration (FREE!)
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "black-forest-labs/FLUX.1-schnell")
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    OTP_EXPIRATION_MINUTES: int = int(os.getenv("OTP_EXPIRATION_MINUTES", "5"))
    
    # API Configuration
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "100"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
