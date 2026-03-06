"""Feature usage tracking service for personalization"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from src.database.duckdb_schema import db_schema
from src.utils.logging import logger


class FeatureUsageTracker:
    """Tracks user feature access for personalization"""
    
    def __init__(self):
        self.db = db_schema.get_connection()
        self.current_sessions = {}  # user_id -> current_feature
    
    def track_feature_access(self, user_id: str, feature_name: str) -> Optional[str]:
        """
        Record feature access event
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature being accessed
            
        Returns:
            usage_id if event was tracked, None if duplicate was prevented
        """
        # Check if should track (prevent duplicates on refresh)
        if not self.should_track_event(user_id, feature_name):
            logger.debug(f"Skipping duplicate event: user={user_id}, feature={feature_name}")
            return None
        
        usage_id = str(uuid.uuid4())
        accessed_at = datetime.now()
        
        try:
            self.db.execute("""
                INSERT INTO feature_usage_history 
                (usage_id, user_id, feature_name, accessed_at)
                VALUES (?, ?, ?, ?)
            """, [usage_id, user_id, feature_name, accessed_at])
            
            # Update current session
            self.current_sessions[user_id] = feature_name
            
            logger.info(f"Tracked feature access: user={user_id}, feature={feature_name}, usage_id={usage_id}")
            return usage_id
        except Exception as e:
            logger.error(f"Error tracking feature access: {e}")
            return None
    
    def should_track_event(self, user_id: str, feature_name: str) -> bool:
        """
        Determine if event should be tracked
        
        Prevents duplicate tracking when user refreshes data within same feature
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature
            
        Returns:
            True if event should be tracked, False if it's a duplicate
        """
        current_feature = self.current_sessions.get(user_id)
        
        # Track if navigating to different feature or first access
        return current_feature != feature_name
    
    def get_recent_features(self, user_id: str, limit: int = 3) -> List[Dict]:
        """
        Get user's most recently accessed features
        
        Args:
            user_id: User identifier
            limit: Maximum number of features to return (default 3)
            
        Returns:
            List of dicts with feature_name, last_accessed, usage_count
        """
        try:
            result = self.db.execute("""
                SELECT 
                    feature_name,
                    MAX(accessed_at) as last_accessed,
                    COUNT(*) as usage_count
                FROM feature_usage_history
                WHERE user_id = ?
                GROUP BY feature_name
                ORDER BY last_accessed DESC
                LIMIT ?
            """, [user_id, limit]).fetchall()
            
            features = []
            for row in result:
                features.append({
                    'feature_name': row[0],
                    'last_accessed': row[1],
                    'usage_count': row[2]
                })
            
            logger.debug(f"Retrieved {len(features)} recent features for user {user_id}")
            return features
        except Exception as e:
            logger.error(f"Error getting recent features: {e}")
            return []
    
    def get_usage_count(self, user_id: str, feature_name: str) -> int:
        """
        Get total usage count for a feature
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature
            
        Returns:
            Total number of times user accessed the feature
        """
        try:
            result = self.db.execute("""
                SELECT COUNT(*) 
                FROM feature_usage_history
                WHERE user_id = ? AND feature_name = ?
            """, [user_id, feature_name]).fetchone()
            
            count = result[0] if result else 0
            logger.debug(f"Usage count for user={user_id}, feature={feature_name}: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting usage count: {e}")
            return 0
    
    def get_last_accessed(self, user_id: str, feature_name: str) -> Optional[datetime]:
        """
        Get last accessed timestamp for a feature
        
        Args:
            user_id: User identifier
            feature_name: Name of the feature
            
        Returns:
            Last accessed timestamp or None if never accessed
        """
        try:
            result = self.db.execute("""
                SELECT MAX(accessed_at)
                FROM feature_usage_history
                WHERE user_id = ? AND feature_name = ?
            """, [user_id, feature_name]).fetchone()
            
            last_accessed = result[0] if result and result[0] else None
            logger.debug(f"Last accessed for user={user_id}, feature={feature_name}: {last_accessed}")
            return last_accessed
        except Exception as e:
            logger.error(f"Error getting last accessed: {e}")
            return None


# Global instance
feature_usage_tracker = FeatureUsageTracker()
