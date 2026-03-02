"""Content models"""
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ContentVersion(BaseModel):
    """Content version model"""
    version_id: str
    user_id: str
    content: str
    created_at: datetime
    parent_version: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
    s3_uri: Optional[str] = None


class Sentiment(BaseModel):
    """Sentiment analysis result"""
    classification: str = Field(pattern="^(positive|neutral|negative)$")
    confidence: float = Field(ge=0.0, le=1.0)
    scores: Dict[str, float] = Field(default_factory=dict)


class ContentAnalysis(BaseModel):
    """Content analysis result"""
    version_id: str
    summary: str
    takeaways: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    sentiment: Sentiment
    analyzed_at: datetime


class OutcomeClassification(BaseModel):
    """GenAI outcome classification"""
    version_id: str
    outcome: str = Field(pattern="^(Successful|Partially correct|Policy/guideline risk|Failed)$")
    confidence: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str] = Field(default_factory=list)
    flagged_for_review: bool = False
    diagnostic_info: Optional[Dict] = None
    classified_at: datetime


class PlatformOutput(BaseModel):
    """Platform-specific content output"""
    platform: str = Field(pattern="^(linkedin|twitter|instagram)$")
    content: Union[str, List[str]]  # String for single post, List for threads
    character_count: int
    meets_requirements: bool = True
    warnings: List[str] = Field(default_factory=list)


class TransformationResult(BaseModel):
    """Content transformation result"""
    version_id: str
    original_content: str
    tone: str = Field(pattern="^(professional|casual|storytelling)$")
    platforms: Dict[str, PlatformOutput] = Field(default_factory=dict)
    transformed_at: datetime


class Content(BaseModel):
    """Content entity"""
    content_id: str
    user_id: str
    current_version_id: str
    versions: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    status: str = Field(default="draft", pattern="^(draft|analyzed|transformed|published)$")
