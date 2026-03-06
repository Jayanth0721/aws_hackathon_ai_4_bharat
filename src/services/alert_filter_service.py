"""Alert filtering service for user-specific alerts"""
from typing import List, Dict
from datetime import datetime, timedelta
from src.database.duckdb_schema import db_schema
from src.utils.logging import logger


class AlertFilterService:
    """Filters alerts to show user-specific information"""
    
    def __init__(self):
        self.db = db_schema.get_connection()
    
    def get_user_alerts(self, user_id: str) -> List[Dict]:
        """
        Get all alerts for a specific user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        # Content Intelligence alerts
        alerts.extend(self.filter_content_intelligence_alerts(user_id))
        
        # Transform alerts
        alerts.extend(self.filter_transform_alerts(user_id))
        
        # Quality alerts
        alerts.extend(self.filter_quality_alerts(user_id))
        
        # Rate limit alerts
        alerts.extend(self.filter_rate_limit_alerts(user_id))
        
        # Sort by timestamp descending
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        logger.debug(f"Retrieved {len(alerts)} alerts for user {user_id}")
        return alerts
    
    def get_personalized_labels(self, user_role: str) -> Dict[str, str]:
        """
        Get personalized label mappings based on user role
        
        Args:
            user_role: User role (admin, creator, viewer)
            
        Returns:
            Dictionary mapping label keys to personalized text
        """
        if user_role == 'admin':
            return {
                'panel_header': 'System-Wide Alerts',
                'quality_score': 'Content Quality Score',
                'analyses': 'Recent Analyses',
                'transformations': 'Transformations',
                'api_usage': 'API Usage'
            }
        else:
            return {
                'panel_header': 'Your Alerts',
                'quality_score': 'Your Content Quality Score',
                'analyses': 'Your Recent Analyses',
                'transformations': 'Your Transformations',
                'api_usage': 'Your API Usage'
            }
    
    def filter_content_intelligence_alerts(self, user_id: str) -> List[Dict]:
        """
        Get Content Intelligence alerts for user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of alert dictionaries
        """
        try:
            result = self.db.execute("""
                SELECT 
                    ci.id,
                    ci.content_type,
                    ci.sentiment,
                    ci.quality_score,
                    ci.analyzed_at
                FROM ashoka_contentint ci
                WHERE ci.user_id = ?
                AND ci.quality_score < 70.0
                ORDER BY ci.analyzed_at DESC
                LIMIT 10
            """, [user_id]).fetchall()
            
            alerts = []
            for row in result:
                alerts.append({
                    'alert_id': f"quality_{row[0]}",
                    'user_id': user_id,
                    'type': 'quality_warning',
                    'source': 'content_intelligence',
                    'message': f"Content quality score {row[3]:.1f} below threshold",
                    'timestamp': row[4],
                    'severity': 'medium'
                })
            
            logger.debug(f"Found {len(alerts)} content intelligence alerts for user {user_id}")
            return alerts
        except Exception as e:
            logger.error(f"Error filtering content intelligence alerts: {e}")
            return []
    
    def filter_transform_alerts(self, user_id: str) -> List[Dict]:
        """
        Get Transform alerts for user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of alert dictionaries
        """
        try:
            # For now, return empty list as transform errors aren't stored separately
            # This can be extended when transform error tracking is implemented
            return []
        except Exception as e:
            logger.error(f"Error filtering transform alerts: {e}")
            return []
    
    def filter_quality_alerts(self, user_id: str) -> List[Dict]:
        """
        Get Quality alerts for user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of alert dictionaries
        """
        try:
            # Quality alerts are already covered by content_intelligence_alerts
            # This method can be extended for additional quality-specific alerts
            return []
        except Exception as e:
            logger.error(f"Error filtering quality alerts: {e}")
            return []
    
    def filter_rate_limit_alerts(self, user_id: str) -> List[Dict]:
        """
        Get Rate Limit alerts for user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of alert dictionaries
        """
        try:
            # Check if user is approaching rate limit (YouTube: 10 requests/hour)
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            result = self.db.execute("""
                SELECT COUNT(*) 
                FROM youtube_rate_limits
                WHERE user_id = ? AND request_timestamp >= ?
            """, [user_id, one_hour_ago]).fetchone()
            
            request_count = result[0] if result else 0
            
            alerts = []
            if request_count >= 8:  # Warning at 80% of limit
                alerts.append({
                    'alert_id': f"rate_limit_{user_id}",
                    'user_id': user_id,
                    'type': 'rate_limit_warning',
                    'source': 'youtube',
                    'message': f"YouTube API usage: {request_count}/10 requests in last hour",
                    'timestamp': datetime.now(),
                    'severity': 'high' if request_count >= 10 else 'medium'
                })
            
            logger.debug(f"Found {len(alerts)} rate limit alerts for user {user_id}")
            return alerts
        except Exception as e:
            logger.error(f"Error filtering rate limit alerts: {e}")
            return []


# Global instance
alert_filter_service = AlertFilterService()
