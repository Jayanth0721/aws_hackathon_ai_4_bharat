"""Database Factory - Supports Hybrid Mode (DynamoDB for content, DuckDB for auth)"""
from typing import Union
from src.config import config
from src.utils.logging import logger


class HybridDatabase:
    """Hybrid database that routes to DynamoDB or DuckDB based on table type"""
    
    def __init__(self):
        """Initialize both DynamoDB and DuckDB"""
        from src.database.dynamodb_connection import get_dynamodb_connection
        from src.database.mock_storage import mock_dynamodb
        
        self.real_dynamodb = get_dynamodb_connection()
        self.mock_dynamodb = mock_dynamodb
        
        # Define which tables use which database
        self.auth_tables = [
            'ashoka-users', 'ashoka_users',
            'ashoka-sessions', 'ashoka_sessions'
        ]
        
        self.content_tables = [
            'ashoka-content', 'ashoka_content',
            'ashoka-audit-logs', 'ashoka_audit_logs',
            'ashoka-alerts', 'ashoka_alerts'
        ]
        
        logger.info("Using Hybrid Mode: DynamoDB for content, DuckDB for authentication")
    
    def _get_db_for_table(self, table_name: str):
        """Route to appropriate database based on table name"""
        if table_name in self.auth_tables:
            return self.mock_dynamodb
        else:
            return self.real_dynamodb
    
    def put_item(self, table_name: str, item: dict):
        """Put item - routes to appropriate database"""
        db = self._get_db_for_table(table_name)
        return db.put_item(table_name, item)
    
    def get_item(self, table_name: str, key: dict):
        """Get item - routes to appropriate database"""
        db = self._get_db_for_table(table_name)
        return db.get_item(table_name, key)
    
    def query(self, table_name: str, **kwargs):
        """Query items - routes to appropriate database"""
        db = self._get_db_for_table(table_name)
        return db.query(table_name, **kwargs)
    
    def delete_item(self, table_name: str, key: dict):
        """Delete item - routes to appropriate database"""
        db = self._get_db_for_table(table_name)
        return db.delete_item(table_name, key)


class DatabaseFactory:
    """Factory to provide appropriate database implementation"""
    
    _instance = None
    
    def __init__(self):
        """Initialize database based on configuration"""
        use_hybrid = config.USE_HYBRID_MODE if hasattr(config, 'USE_HYBRID_MODE') else False
        
        if use_hybrid:
            # Hybrid mode: DynamoDB for content, DuckDB for auth
            self.db = HybridDatabase()
            self.db_type = "hybrid"
        elif config.USE_REAL_DYNAMODB:
            # Full DynamoDB mode
            from src.database.dynamodb_connection import get_dynamodb_connection
            self.db = get_dynamodb_connection()
            self.db_type = "real"
            logger.info("Using Real DynamoDB for all tables")
        else:
            # Full MockDynamoDB mode
            from src.database.mock_storage import mock_dynamodb
            self.db = mock_dynamodb
            self.db_type = "mock"
            logger.info("Using MockDynamoDB (local DuckDB) for all tables")
    
    def get_dynamodb(self):
        """Get the database instance"""
        return self.db
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_db():
    """Get database instance (MockDynamoDB, Real DynamoDB, or Hybrid)"""
    factory = DatabaseFactory.get_instance()
    return factory.get_dynamodb()


# Convenience alias
get_dynamodb = get_db
