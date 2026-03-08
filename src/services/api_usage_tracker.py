"""API Usage Tracker Service
Tracks API usage per engine per day for quota management
"""
from datetime import datetime, date
from typing import Dict, Optional
from src.database.duckdb_schema import db_schema
from src.utils.id_generator import generate_id
from src.utils.logging import logger


class APIUsageTracker:
    """Track API usage for all AI engines"""
    
    # Daily limits for free tier
    DAILY_LIMITS = {
        'gemini': 50,      # Gemini Engine 1
        'sarvam': 1000,    # Sarvam AI (estimated)
        'gemini3': 50,     # Gemini Engine 3
    }
    
    def __init__(self):
        """Initialize API usage tracker"""
        self.db = db_schema
    
    def track_request(
        self,
        user_id: str,
        engine_name: str,
        model_name: str,
        success: bool = True
    ) -> None:
        """
        Track an API request
        
        Args:
            user_id: User ID making the request
            engine_name: Engine name (gemini, sarvam, gemini3)
            model_name: Model name used
            success: Whether the request was successful
        """
        try:
            today = date.today()
            
            # Check if record exists for today
            result = self.db.conn.execute("""
                SELECT usage_id, request_count, success_count, failure_count
                FROM ai_engine_usage
                WHERE user_id = ? AND engine_name = ? AND request_date = ?
            """, [user_id, engine_name, today]).fetchone()
            
            if result:
                # Update existing record
                usage_id, count, success_count, failure_count = result
                new_count = count + 1
                new_success = success_count + (1 if success else 0)
                new_failure = failure_count + (0 if success else 1)
                
                self.db.conn.execute("""
                    UPDATE ai_engine_usage
                    SET request_count = ?,
                        success_count = ?,
                        failure_count = ?,
                        last_request_at = ?
                    WHERE usage_id = ?
                """, [new_count, new_success, new_failure, datetime.now(), usage_id])
            else:
                # Create new record
                usage_id = generate_id()
                self.db.conn.execute("""
                    INSERT INTO ai_engine_usage (
                        usage_id, user_id, engine_name, model_name,
                        request_date, request_count, last_request_at,
                        success_count, failure_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    usage_id, user_id, engine_name, model_name,
                    today, 1, datetime.now(),
                    1 if success else 0,
                    0 if success else 1
                ])
            
            logger.info(f"Tracked {engine_name} request for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error tracking API usage: {e}")
    
    def get_usage_today(self, user_id: str, engine_name: str) -> Dict:
        """
        Get today's usage for a specific engine
        
        Args:
            user_id: User ID
            engine_name: Engine name
            
        Returns:
            Dict with usage stats
        """
        try:
            today = date.today()
            
            result = self.db.conn.execute("""
                SELECT request_count, success_count, failure_count, last_request_at
                FROM ai_engine_usage
                WHERE user_id = ? AND engine_name = ? AND request_date = ?
            """, [user_id, engine_name, today]).fetchone()
            
            limit = self.DAILY_LIMITS.get(engine_name, 0)
            
            if result:
                count, success, failure, last_request = result
                remaining = max(0, limit - count)
                
                return {
                    'used': count,
                    'limit': limit,
                    'remaining': remaining,
                    'success': success,
                    'failure': failure,
                    'last_request': last_request,
                    'percentage': (count / limit * 100) if limit > 0 else 0
                }
            else:
                return {
                    'used': 0,
                    'limit': limit,
                    'remaining': limit,
                    'success': 0,
                    'failure': 0,
                    'last_request': None,
                    'percentage': 0
                }
                
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            limit = self.DAILY_LIMITS.get(engine_name, 0)
            return {
                'used': 0,
                'limit': limit,
                'remaining': limit,
                'success': 0,
                'failure': 0,
                'last_request': None,
                'percentage': 0
            }
    
    def get_all_usage_today(self, user_id: str) -> Dict[str, Dict]:
        """
        Get today's usage for all engines
        
        Args:
            user_id: User ID
            
        Returns:
            Dict mapping engine names to usage stats
        """
        usage = {}
        for engine_name in self.DAILY_LIMITS.keys():
            usage[engine_name] = self.get_usage_today(user_id, engine_name)
        return usage
    
    def can_use_engine(self, user_id: str, engine_name: str) -> bool:
        """
        Check if user can use an engine (hasn't exceeded quota)
        
        Args:
            user_id: User ID
            engine_name: Engine name
            
        Returns:
            True if user can use the engine
        """
        usage = self.get_usage_today(user_id, engine_name)
        return usage['remaining'] > 0
    
    def get_recommended_engine(self, user_id: str) -> Optional[str]:
        """
        Get recommended engine based on available quota
        
        Args:
            user_id: User ID
            
        Returns:
            Engine name with available quota, or None
        """
        all_usage = self.get_all_usage_today(user_id)
        
        # Priority order
        priority = ['gemini', 'sarvam', 'gemini3']
        
        for engine in priority:
            if all_usage[engine]['remaining'] > 0:
                return engine
        
        return None


# Global instance
api_usage_tracker = APIUsageTracker()
