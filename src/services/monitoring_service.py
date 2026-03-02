"""Monitoring and observability service for content operations"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
from src.utils.logging import logger


@dataclass
class QualityMetrics:
    """Quality metrics for content"""
    readability_score: float
    readability_change: float
    tone_consistency: float
    tone_status: str
    duplicate_count: int
    duplicate_status: str


@dataclass
class RiskMetrics:
    """Risk and safety metrics"""
    toxicity_score: float
    toxicity_level: str
    hate_speech_count: int
    hate_speech_status: str
    backlash_risk: str
    backlash_status: str


@dataclass
class OperationsMetrics:
    """AI operations performance metrics"""
    success_rate: float
    total_operations: int
    avg_latency: float
    latency_status: str
    quality_drift: float
    drift_status: str


@dataclass
class SystemHealth:
    """Overall system health status"""
    api_status: str
    database_status: str
    ai_status: str
    storage_usage: float
    processing_rate: float
    model_performance: float


class MonitoringService:
    """Service for monitoring content operations and system health"""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_threshold = {
            'toxicity': 0.3,
            'readability': 60.0,
            'success_rate': 95.0,
            'latency': 2.0
        }
    
    def get_quality_metrics(self) -> QualityMetrics:
        """
        Get current quality metrics
        In production, this would query DuckDB for real metrics
        """
        # Mock data with realistic variations
        readability = random.uniform(78.0, 88.0)
        readability_change = random.uniform(-2.0, 5.0)
        tone_consistency = random.uniform(88.0, 96.0)
        duplicate_count = random.randint(0, 5)
        
        return QualityMetrics(
            readability_score=readability,
            readability_change=readability_change,
            tone_consistency=tone_consistency,
            tone_status='Excellent' if tone_consistency > 90 else 'Good',
            duplicate_count=duplicate_count,
            duplicate_status='Similar content found' if duplicate_count > 0 else 'No duplicates'
        )
    
    def get_risk_metrics(self) -> RiskMetrics:
        """
        Get current risk and safety metrics
        In production, this would analyze content for risks
        """
        # Mock data - mostly safe with occasional warnings
        toxicity = random.uniform(0.05, 0.25)
        hate_speech = random.randint(0, 1)
        backlash_risks = ['Low', 'Low', 'Low', 'Medium', 'Medium', 'High']
        backlash = random.choice(backlash_risks)
        
        toxicity_level = 'Low risk' if toxicity < 0.2 else 'Medium risk' if toxicity < 0.3 else 'High risk'
        
        return RiskMetrics(
            toxicity_score=toxicity,
            toxicity_level=toxicity_level,
            hate_speech_count=hate_speech,
            hate_speech_status='No violations' if hate_speech == 0 else 'Violations detected',
            backlash_risk=backlash,
            backlash_status='Review recommended' if backlash != 'Low' else 'Acceptable'
        )
    
    def get_operations_metrics(self) -> OperationsMetrics:
        """
        Get AI operations performance metrics
        In production, this would track actual operations
        """
        # Mock data with realistic performance
        success_rate = random.uniform(97.5, 99.8)
        total_ops = random.randint(5000, 6000)
        latency = random.uniform(0.8, 1.8)
        drift = random.uniform(-1.0, 3.5)
        
        latency_status = 'Within SLA' if latency < 2.0 else 'Exceeds SLA'
        drift_status = 'Improving' if drift > 0 else 'Declining'
        
        return OperationsMetrics(
            success_rate=success_rate,
            total_operations=total_ops,
            avg_latency=latency,
            latency_status=latency_status,
            quality_drift=drift,
            drift_status=drift_status
        )
    
    def get_system_health(self) -> SystemHealth:
        """
        Get overall system health status
        In production, this would check actual system components
        """
        # Mock data - mostly healthy
        statuses = ['Healthy', 'Healthy', 'Healthy', 'Degraded']
        
        return SystemHealth(
            api_status=random.choice(statuses),
            database_status=random.choice(statuses),
            ai_status=random.choice(statuses),
            storage_usage=random.uniform(0.55, 0.75),
            processing_rate=random.uniform(0.70, 0.85),
            model_performance=random.uniform(0.90, 0.98)
        )
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """
        Get recent alerts and notifications
        In production, this would query alert database
        """
        alert_types = [
            {
                'type': 'critical',
                'icon': 'error',
                'color': 'red',
                'title': 'High Toxicity Detected',
                'description': 'Content flagged for toxic language',
                'time': 'minutes'
            },
            {
                'type': 'warning',
                'icon': 'warning',
                'color': 'orange',
                'title': 'Quality Below Threshold',
                'description': 'Readability score dropped below 70',
                'time': 'minutes'
            },
            {
                'type': 'warning',
                'icon': 'warning',
                'color': 'orange',
                'title': 'Duplicate Content',
                'description': 'Similar content detected in database',
                'time': 'hour'
            },
            {
                'type': 'info',
                'icon': 'info',
                'color': 'blue',
                'title': 'Processing Complete',
                'description': 'Batch analysis finished successfully',
                'time': 'hours'
            },
            {
                'type': 'success',
                'icon': 'check_circle',
                'color': 'green',
                'title': 'Quality Improved',
                'description': 'Content quality increased by 15%',
                'time': 'hours'
            }
        ]
        
        # Generate random alerts
        alerts = []
        for i in range(min(limit, len(alert_types) * 2)):
            alert = random.choice(alert_types).copy()
            time_value = random.randint(1, 30)
            alert['time_ago'] = f"{time_value} {alert['time']} ago"
            alert['timestamp'] = datetime.now() - timedelta(minutes=time_value if alert['time'] == 'minutes' else time_value * 60)
            alerts.append(alert)
        
        # Sort by timestamp
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return alerts[:limit]
    
    def get_quality_trend(self, days: int = 7) -> List[Dict]:
        """
        Get quality trend data for charts
        In production, this would query historical data
        """
        trend = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            trend.append({
                'date': date.strftime('%Y-%m-%d'),
                'readability': random.uniform(75, 90),
                'tone_consistency': random.uniform(85, 95),
                'quality_score': random.uniform(80, 92)
            })
        
        return trend
    
    def get_risk_trend(self, days: int = 7) -> List[Dict]:
        """
        Get risk trend data for charts
        In production, this would query historical data
        """
        trend = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            trend.append({
                'date': date.strftime('%Y-%m-%d'),
                'toxicity': random.uniform(0.05, 0.25),
                'violations': random.randint(0, 3),
                'risk_score': random.uniform(10, 40)
            })
        
        return trend
    
    def check_alert_conditions(self, metrics: Dict) -> List[Dict]:
        """
        Check if any metrics exceed alert thresholds
        Returns list of alerts to trigger
        """
        alerts = []
        
        # Check toxicity
        if 'toxicity_score' in metrics and metrics['toxicity_score'] > self.alert_threshold['toxicity']:
            alerts.append({
                'type': 'critical',
                'title': 'High Toxicity Alert',
                'description': f"Toxicity score {metrics['toxicity_score']:.2f} exceeds threshold",
                'metric': 'toxicity'
            })
        
        # Check readability
        if 'readability_score' in metrics and metrics['readability_score'] < self.alert_threshold['readability']:
            alerts.append({
                'type': 'warning',
                'title': 'Low Readability Alert',
                'description': f"Readability score {metrics['readability_score']:.1f} below threshold",
                'metric': 'readability'
            })
        
        # Check success rate
        if 'success_rate' in metrics and metrics['success_rate'] < self.alert_threshold['success_rate']:
            alerts.append({
                'type': 'warning',
                'title': 'Low Success Rate Alert',
                'description': f"Success rate {metrics['success_rate']:.1f}% below threshold",
                'metric': 'success_rate'
            })
        
        # Check latency
        if 'avg_latency' in metrics and metrics['avg_latency'] > self.alert_threshold['latency']:
            alerts.append({
                'type': 'warning',
                'title': 'High Latency Alert',
                'description': f"Average latency {metrics['avg_latency']:.2f}s exceeds SLA",
                'metric': 'latency'
            })
        
        return alerts
    
    def get_compliance_status(self) -> Dict:
        """
        Get compliance status for various regulations
        In production, this would check actual compliance
        """
        return {
            'gdpr': {
                'status': 'Compliant',
                'color': 'green',
                'last_audit': '2026-02-15'
            },
            'ccpa': {
                'status': 'Compliant',
                'color': 'green',
                'last_audit': '2026-02-10'
            },
            'coppa': {
                'status': 'Compliant',
                'color': 'green',
                'last_audit': '2026-02-20'
            },
            'accessibility': {
                'status': 'Review Needed',
                'color': 'orange',
                'last_audit': '2026-01-30'
            }
        }
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        quality = self.get_quality_metrics()
        risk = self.get_risk_metrics()
        ops = self.get_operations_metrics()
        health = self.get_system_health()
        
        # Calculate overall score
        quality_score = (quality.readability_score / 100 + quality.tone_consistency / 100) / 2
        risk_score = 1.0 - risk.toxicity_score
        ops_score = ops.success_rate / 100
        
        overall_score = (quality_score + risk_score + ops_score) / 3
        
        return {
            'overall_score': overall_score * 100,
            'quality_score': quality_score * 100,
            'risk_score': risk_score * 100,
            'operations_score': ops_score * 100,
            'status': 'Excellent' if overall_score > 0.9 else 'Good' if overall_score > 0.8 else 'Needs Attention'
        }


# Global instance
monitoring_service = MonitoringService()
