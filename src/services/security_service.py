"""Security logging and monitoring service"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

from src.database.duckdb_schema import db_schema
from src.utils.logging import logger


class SecurityService:
    """Security logging and monitoring"""
    
    def __init__(self):
        self.conn = None
    
    def _get_connection(self):
        """Get database connection"""
        if not self.conn:
            self.conn = db_schema.get_connection()
        return self.conn
    
    def log_login_attempt(
        self,
        username: str,
        ip_address: str,
        location: str,
        device_info: str,
        status: str,
        session_id: Optional[str] = None
    ) -> int:
        """Log a login attempt"""
        conn = self._get_connection()
        
        try:
            # Get next log_id
            result = conn.execute("SELECT COALESCE(MAX(log_id), 0) + 1 FROM security_login_logs").fetchone()
            log_id = result[0]
            
            # Insert login log
            conn.execute("""
                INSERT INTO security_login_logs 
                (log_id, username, ip_address, location, device_info, status, timestamp, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (log_id, username, ip_address, location, device_info, status, datetime.now(), session_id))
            
            logger.info(f"Login attempt logged: {username} - {status}")
            return log_id
            
        except Exception as e:
            logger.error(f"Error logging login attempt: {e}")
            return -1
    
    def log_security_event(
        self,
        username: str,
        event_type: str,
        event_description: str,
        metadata: Optional[Dict] = None
    ) -> int:
        """Log a security event"""
        conn = self._get_connection()
        
        try:
            # Get next event_id
            result = conn.execute("SELECT COALESCE(MAX(event_id), 0) + 1 FROM security_events").fetchone()
            event_id = result[0]
            
            # Insert security event
            conn.execute("""
                INSERT INTO security_events 
                (event_id, username, event_type, event_description, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event_id, username, event_type, event_description, datetime.now(), json.dumps(metadata or {})))
            
            logger.info(f"Security event logged: {username} - {event_type}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
            return -1
    
    def get_recent_login_logs(self, limit: int = 10) -> List[Dict]:
        """Get recent login logs"""
        conn = self._get_connection()
        
        try:
            result = conn.execute("""
                SELECT log_id, username, ip_address, location, device_info, status, timestamp, session_id
                FROM security_login_logs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()
            
            logs = []
            for row in result:
                logs.append({
                    'log_id': row[0],
                    'username': row[1],
                    'ip_address': row[2],
                    'location': row[3],
                    'device_info': row[4],
                    'status': row[5],
                    'timestamp': row[6],
                    'session_id': row[7]
                })
            
            return logs
            
        except Exception as e:
            logger.error(f"Error getting login logs: {e}")
            return []
    
    def get_recent_security_events(self, limit: int = 10) -> List[Dict]:
        """Get recent security events"""
        conn = self._get_connection()
        
        try:
            result = conn.execute("""
                SELECT event_id, username, event_type, event_description, timestamp, metadata
                FROM security_events
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()
            
            events = []
            for row in result:
                events.append({
                    'event_id': row[0],
                    'username': row[1],
                    'event_type': row[2],
                    'event_description': row[3],
                    'timestamp': row[4],
                    'metadata': json.loads(row[5]) if row[5] else {}
                })
            
            return events
            
        except Exception as e:
            logger.error(f"Error getting security events: {e}")
            return []
    
    def get_login_activity_stats(self, days: int = 7) -> List[Dict]:
        """Get login activity statistics for the last N days"""
        conn = self._get_connection()
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            result = conn.execute("""
                SELECT 
                    DATE(timestamp) as login_date,
                    COUNT(*) as login_count
                FROM security_login_logs
                WHERE timestamp >= ? AND status = 'Success'
                GROUP BY DATE(timestamp)
                ORDER BY login_date
            """, (cutoff_date,)).fetchall()
            
            stats = []
            for row in result:
                stats.append({
                    'date': row[0],
                    'count': row[1]
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting login activity stats: {e}")
            return []
    
    def get_failed_login_count(self, hours: int = 24) -> int:
        """Get count of failed login attempts in last N hours"""
        conn = self._get_connection()
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            result = conn.execute("""
                SELECT COUNT(*) 
                FROM security_login_logs
                WHERE timestamp >= ? AND status = 'Failed'
            """, (cutoff_time,)).fetchone()
            
            return result[0] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting failed login count: {e}")
            return 0
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        # For now, return 1 (current user)
        # In a real implementation, query sessions table
        return 1
    
    def get_security_score(self) -> float:
        """Calculate security score based on various factors"""
        # Simple calculation based on recent activity
        failed_logins = self.get_failed_login_count(24)
        
        # Start with 100%
        score = 100.0
        
        # Deduct points for failed logins
        score -= min(failed_logins * 5, 20)  # Max 20 points deduction
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))


# Global security service instance
security_service = SecurityService()
