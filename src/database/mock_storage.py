"""Mock storage implementations for local development"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from src.utils.logging import logger


class MockDynamoDB:
    """Mock DynamoDB using DuckDB for persistence"""
    
    def __init__(self, db_path: str = "data/ashoka.duckdb"):
        import duckdb
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._ensure_tables_exist()
        logger.info(f"Initialized MockDynamoDB with DuckDB at {db_path}")
    
    def _ensure_tables_exist(self):
        """Ensure user and session tables exist"""
        try:
            # Create users table if not exists
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ashoka_users (
                    user_id VARCHAR PRIMARY KEY,
                    username VARCHAR UNIQUE NOT NULL,
                    password_hash VARCHAR NOT NULL,
                    email VARCHAR NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    role VARCHAR DEFAULT 'user'
                )
            """)
            
            # Create sessions table if not exists
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ashoka_sessions (
                    session_token VARCHAR PRIMARY KEY,
                    user_id VARCHAR NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    last_activity TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Create indexes
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_username 
                ON ashoka_users(username)
            """)
            
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id 
                ON ashoka_sessions(user_id)
            """)
            
            logger.debug("User and session tables ensured in DuckDB")
        except Exception as e:
            logger.error(f"Error ensuring tables exist: {e}")
    
    def put_item(self, table_name: str, item: Dict[str, Any]):
        """Store item in DuckDB table"""
        try:
            # Convert item to match DuckDB table structure
            # Handle both hyphenated and underscored table names
            if table_name in ["ashoka-users", "ashoka_users"]:
                # First try to update existing user
                result = self.conn.execute("""
                    SELECT user_id FROM ashoka_users WHERE user_id = ?
                """, [item.get('user_id')]).fetchone()
                
                if result:
                    # Update existing user
                    self.conn.execute("""
                        UPDATE ashoka_users 
                        SET username = ?, password_hash = ?, email = ?, 
                            last_login = ?, is_active = ?, role = ?
                        WHERE user_id = ?
                    """, [
                        item.get('username'),
                        item.get('password_hash'),
                        item.get('email'),
                        item.get('last_login'),
                        item.get('is_active', True),
                        item.get('role', 'user'),
                        item.get('user_id')
                    ])
                else:
                    # Insert new user
                    self.conn.execute("""
                        INSERT INTO ashoka_users 
                        (user_id, username, password_hash, email, created_at, last_login, is_active, role)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        item.get('user_id'),
                        item.get('username'),
                        item.get('password_hash'),
                        item.get('email'),
                        item.get('created_at'),
                        item.get('last_login'),
                        item.get('is_active', True),
                        item.get('role', 'user')
                    ])
            elif table_name in ["ashoka-sessions", "ashoka_sessions"]:
                # First try to update existing session
                result = self.conn.execute("""
                    SELECT session_token FROM ashoka_sessions WHERE session_token = ?
                """, [item.get('session_token')]).fetchone()
                
                if result:
                    # Update existing session
                    self.conn.execute("""
                        UPDATE ashoka_sessions 
                        SET user_id = ?, last_activity = ?, expires_at = ?, is_active = ?
                        WHERE session_token = ?
                    """, [
                        item.get('user_id'),
                        item.get('last_activity'),
                        item.get('expires_at'),
                        item.get('is_active', True),
                        item.get('session_token')
                    ])
                else:
                    # Insert new session
                    self.conn.execute("""
                        INSERT INTO ashoka_sessions 
                        (session_token, user_id, created_at, last_activity, expires_at, is_active)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, [
                        item.get('session_token'),
                        item.get('user_id'),
                        item.get('created_at'),
                        item.get('last_activity'),
                        item.get('expires_at'),
                        item.get('is_active', True)
                    ])
            else:
                logger.warning(f"Table {table_name} not supported in DuckDB MockDynamoDB")
                return
            
            logger.debug(f"MockDynamoDB: Put item in {table_name}")
        except Exception as e:
            logger.error(f"Error putting item in {table_name}: {e}")
            raise
    
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve item from DuckDB table"""
        try:
            pk_value = list(key.values())[0]
            
            if table_name in ["ashoka-users", "ashoka_users"]:
                result = self.conn.execute("""
                    SELECT user_id, username, password_hash, email, created_at, 
                           last_login, is_active, role
                    FROM ashoka_users
                    WHERE user_id = ?
                """, [pk_value]).fetchone()
                
                if result:
                    return {
                        'user_id': result[0],
                        'username': result[1],
                        'password_hash': result[2],
                        'email': result[3],
                        'created_at': result[4],
                        'last_login': result[5],
                        'is_active': result[6],
                        'role': result[7]
                    }
            elif table_name in ["ashoka-sessions", "ashoka_sessions"]:
                result = self.conn.execute("""
                    SELECT session_token, user_id, created_at, last_activity, 
                           expires_at, is_active
                    FROM ashoka_sessions
                    WHERE session_token = ?
                """, [pk_value]).fetchone()
                
                if result:
                    return {
                        'session_token': result[0],
                        'user_id': result[1],
                        'created_at': result[2],
                        'last_activity': result[3],
                        'expires_at': result[4],
                        'is_active': result[5]
                    }
            
            return None
        except Exception as e:
            logger.error(f"Error getting item from {table_name}: {e}")
            return None
    
    def query(self, table_name: str, **kwargs) -> List[Dict[str, Any]]:
        """Query items from DuckDB table"""
        try:
            if table_name in ["ashoka-users", "ashoka_users"]:
                results = self.conn.execute("""
                    SELECT user_id, username, password_hash, email, created_at, 
                           last_login, is_active, role
                    FROM ashoka_users
                """).fetchall()
                
                return [{
                    'user_id': r[0],
                    'username': r[1],
                    'password_hash': r[2],
                    'email': r[3],
                    'created_at': r[4],
                    'last_login': r[5],
                    'is_active': r[6],
                    'role': r[7]
                } for r in results]
            elif table_name in ["ashoka-sessions", "ashoka_sessions"]:
                results = self.conn.execute("""
                    SELECT session_token, user_id, created_at, last_activity, 
                           expires_at, is_active
                    FROM ashoka_sessions
                """).fetchall()
                
                return [{
                    'session_token': r[0],
                    'user_id': r[1],
                    'created_at': r[2],
                    'last_activity': r[3],
                    'expires_at': r[4],
                    'is_active': r[5]
                } for r in results]
            
            return []
        except Exception as e:
            logger.error(f"Error querying {table_name}: {e}")
            return []
    
    def delete_item(self, table_name: str, key: Dict[str, Any]):
        """Delete item from DuckDB table"""
        try:
            pk_value = list(key.values())[0]
            
            if table_name in ["ashoka-users", "ashoka_users"]:
                self.conn.execute("""
                    DELETE FROM ashoka_users WHERE user_id = ?
                """, [pk_value])
            elif table_name in ["ashoka-sessions", "ashoka_sessions"]:
                self.conn.execute("""
                    DELETE FROM ashoka_sessions WHERE session_token = ?
                """, [pk_value])
            
            logger.debug(f"MockDynamoDB: Deleted item from {table_name}")
        except Exception as e:
            logger.error(f"Error deleting item from {table_name}: {e}")


class MockS3:
    """Mock S3 for local development"""
    
    def __init__(self):
        self.buckets: Dict[str, Dict[str, bytes]] = {}
        # Silently initialize - no log message needed
    
    def put_object(self, bucket: str, key: str, body: bytes):
        """Store object in mock bucket"""
        if bucket not in self.buckets:
            self.buckets[bucket] = {}
        
        self.buckets[bucket][key] = body
        logger.debug(f"MockS3: Put object {key} in bucket {bucket}")
    
    def get_object(self, bucket: str, key: str) -> Optional[bytes]:
        """Retrieve object from mock bucket"""
        if bucket not in self.buckets:
            return None
        
        return self.buckets[bucket].get(key)
    
    def delete_object(self, bucket: str, key: str):
        """Delete object from mock bucket"""
        if bucket in self.buckets and key in self.buckets[bucket]:
            del self.buckets[bucket][key]
            logger.debug(f"MockS3: Deleted object {key} from bucket {bucket}")


# Global mock instances
mock_dynamodb = MockDynamoDB()
mock_s3 = MockS3()
