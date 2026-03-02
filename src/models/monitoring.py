"""Monitoring and quality models"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SimilarityMatch(BaseModel):
    """Content similarity match"""
    version_id: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    content_preview: str


class ToneShift(BaseModel):
    """Tone inconsistency detection"""
    section: str
    expected_tone: str
    detected_tone: str
    position: int


class ToneConsistencyResult(BaseModel):
    """Tone consistency check result"""
    is_consistent: bool
    consistency_score: float = Field(ge=0.0, le=1.0)
    tone_shifts: List[ToneShift] = Field(default_factory=list)


class QualityMetrics(BaseModel):
    """Content quality metrics"""
    version_id: str
    readability_score: float
    tone_consistency_score: float = Field(ge=0.0, le=1.0)
    duplicate_count: int = 0
    similar_content: List[SimilarityMatch] = Field(default_factory=list)
    quality_grade: str = Field(pattern="^(Excellent|Good|Fair|Poor)$")
    measured_at: datetime


class ToxicityScore(BaseModel):
    """Toxicity detection result"""
    overall_score: float = Field(ge=0.0, le=1.0)
    categories: Dict[str, float] = Field(default_factory=dict)
    flagged_phrases: List[str] = Field(default_factory=list)


class PolicyRiskAssessment(BaseModel):
    """Policy risk assessment"""
    risk_level: str = Field(pattern="^(None|Low|Medium|High)$")
    violated_policies: List[str] = Field(default_factory=list)
    borderline_policies: List[str] = Field(default_factory=list)
    explanation: str


class BacklashRisk(BaseModel):
    """Backlash risk estimation"""
    risk_level: str = Field(pattern="^(Low|Medium|High|Critical)$")
    estimated_probability: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str] = Field(default_factory=list)
    sensitive_topics: List[str] = Field(default_factory=list)


class RiskAssessment(BaseModel):
    """Comprehensive risk assessment"""
    version_id: str
    toxicity_score: float = Field(ge=0.0, le=1.0)
    contains_hate_speech: bool = False
    policy_risk_level: str = Field(pattern="^(None|Low|Medium|High)$")
    backlash_risk_level: str = Field(pattern="^(Low|Medium|High|Critical)$")
    risk_factors: List[str] = Field(default_factory=list)
    should_block: bool = False
    assessed_at: datetime


class Alert(BaseModel):
    """System alert"""
    alert_id: str
    alert_type: str = Field(pattern="^(quality|risk|operations|reaction)$")
    severity: str = Field(pattern="^(info|warning|critical)$")
    title: str
    message: str
    related_content: Optional[str] = None
    created_at: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


class OperationMetric(BaseModel):
    """Operation performance metric"""
    operation: str
    timestamp: datetime
    success: bool
    latency_ms: float
    error_type: Optional[str] = None


class QualityDriftAnalysis(BaseModel):
    """Quality drift detection result"""
    drift_detected: bool
    baseline_quality: float
    current_quality: float
    drift_percentage: float
    time_period: str
    contributing_factors: List[str] = Field(default_factory=list)


class Reaction(BaseModel):
    """Audience reaction"""
    reaction_id: str
    content_id: str
    platform: str
    user_handle: str
    text: str
    timestamp: datetime
    reaction_type: str = Field(pattern="^(comment|reply|like|share)$")
    sentiment: str


class EngagementAnalysis(BaseModel):
    """Engagement analysis result"""
    content_id: str
    total_reactions: int
    positive_count: int
    neutral_count: int
    toxic_count: int
    high_backlash_count: int
    engagement_rate: float
    sentiment_distribution: Dict[str, float] = Field(default_factory=dict)
    trending_topics: List[str] = Field(default_factory=list)
    analyzed_at: datetime
