"""
DynamoDB Connection Module
Handles connections to AWS DynamoDB
"""

import os
import boto3
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class DynamoDBConnection:
    """Manages DynamoDB connections and operations with MockDynamoDB-compatible API"""
    
    def __init__(self):
        self.region = os.getenv('DYNAMODB_REGION', 'us-east-1')
        
        # Initialize DynamoDB client
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=self.region,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Table name mapping for different table types
        # All tables map to the same DynamoDB table for single-table design
        default_table = os.getenv('DYNAMODB_TABLE', 'ashoka_contentint')
        self.table_mapping = {
            'ashoka-users': os.getenv('DYNAMODB_USERS_TABLE', default_table),
            'ashoka_users': os.getenv('DYNAMODB_USERS_TABLE', default_table),
            'ashoka-sessions': os.getenv('DYNAMODB_SESSIONS_TABLE', default_table),
            'ashoka_sessions': os.getenv('DYNAMODB_SESSIONS_TABLE', default_table),
            'ashoka-content': os.getenv('DYNAMODB_CONTENT_TABLE', default_table),
            'ashoka_content': os.getenv('DYNAMODB_CONTENT_TABLE', default_table),
            'ashoka-audit-logs': os.getenv('DYNAMODB_AUDIT_TABLE', default_table),
            'ashoka_audit_logs': os.getenv('DYNAMODB_AUDIT_TABLE', default_table),
            'ashoka-alerts': os.getenv('DYNAMODB_ALERTS_TABLE', default_table),
            'ashoka_alerts': os.getenv('DYNAMODB_ALERTS_TABLE', default_table),
            'ashoka_contentint': default_table,  # Direct table name
        }
        
        logger.info(f"Connected to DynamoDB in {self.region}, default table: {default_table}")
    
    def _get_table(self, table_name: str):
        """Get DynamoDB table resource"""
        actual_table_name = self.table_mapping.get(table_name, table_name)
        return self.dynamodb.Table(actual_table_name)
    
    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """Insert or update an item in DynamoDB (MockDynamoDB-compatible API)"""
        try:
            table = self._get_table(table_name)
            # Convert datetime objects to ISO format strings
            item = self._serialize_item(item)
            
            # Add diff_data key and entity_type based on item type
            if 'user_id' in item and 'username' in item:
                # This is a user record
                item['diff_data'] = f"USER#{item['user_id']}"
                item['entity_type'] = 'user'
            elif 'session_token' in item:
                # This is a session record
                item['diff_data'] = f"SESSION#{item['session_token']}"
                item['entity_type'] = 'session'
            elif 'content_id' in item:
                # This is a content record
                item['diff_data'] = f"CONTENT#{item['content_id']}"
                item['entity_type'] = 'content'
            elif 'alert_id' in item:
                # This is an alert record
                item['diff_data'] = f"ALERT#{item['alert_id']}"
                item['entity_type'] = 'alert'
            elif 'audit_id' in item:
                # This is an audit record
                item['diff_data'] = f"AUDIT#{item['audit_id']}"
                item['entity_type'] = 'audit'
            else:
                # Generate a unique key if none exists
                import uuid
                item['diff_data'] = f"ITEM#{uuid.uuid4().hex[:8]}"
                item['entity_type'] = 'unknown'
            
            table.put_item(Item=item)
            logger.info(f"Item added to {table_name} with diff_data={item['diff_data']}")
            return True
        except Exception as e:
            logger.error(f"Failed to put item in {table_name}: {e}")
            return False
    
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get an item from DynamoDB by key (MockDynamoDB-compatible API)"""
        try:
            table = self._get_table(table_name)
            
            # Convert the key to use diff_data with entity type prefix
            if 'user_id' in key:
                dynamodb_key = {'diff_data': f"USER#{key['user_id']}"}
            elif 'session_token' in key:
                dynamodb_key = {'diff_data': f"SESSION#{key['session_token']}"}
            elif 'content_id' in key:
                dynamodb_key = {'diff_data': f"CONTENT#{key['content_id']}"}
            elif 'diff_data' in key:
                dynamodb_key = key
            else:
                # Use the first key value
                dynamodb_key = {'diff_data': list(key.values())[0]}
            
            response = table.get_item(Key=dynamodb_key)
            item = response.get('Item')
            
            if item:
                return self._deserialize_item(item)
            return None
        except Exception as e:
            logger.error(f"Failed to get item from {table_name}: {e}")
            return None
    
    def query(self, table_name: str, **kwargs) -> List[Dict[str, Any]]:
        """Query items from DynamoDB (MockDynamoDB-compatible API)"""
        try:
            table = self._get_table(table_name)
            
            # For simple queries without parameters, do a scan
            if not kwargs:
                response = table.scan()
                items = response.get('Items', [])
                return [self._deserialize_item(item) for item in items]
            
            # Otherwise use query parameters
            response = table.query(**kwargs)
            items = response.get('Items', [])
            
            return [self._deserialize_item(item) for item in items]
        except Exception as e:
            logger.error(f"Failed to query {table_name}: {e}")
            return []
    
    def delete_item(self, table_name: str, key: Dict[str, Any]) -> bool:
        """Delete an item from DynamoDB (MockDynamoDB-compatible API)"""
        try:
            table = self._get_table(table_name)
            
            # Convert the key to use diff_data with entity type prefix
            if 'user_id' in key:
                dynamodb_key = {'diff_data': f"USER#{key['user_id']}"}
            elif 'session_token' in key:
                dynamodb_key = {'diff_data': f"SESSION#{key['session_token']}"}
            elif 'content_id' in key:
                dynamodb_key = {'diff_data': f"CONTENT#{key['content_id']}"}
            elif 'diff_data' in key:
                dynamodb_key = key
            else:
                # Use the first key value
                dynamodb_key = {'diff_data': list(key.values())[0]}
            
            table.delete_item(Key=dynamodb_key)
            logger.info(f"Item deleted from {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete item from {table_name}: {e}")
            return False
    
    def query_items(self, 
                    table_name: str,
                    key_condition_expression,
                    expression_attribute_values: Dict[str, Any],
                    filter_expression=None,
                    limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Query items from DynamoDB (advanced API)"""
        try:
            table = self._get_table(table_name)
            query_params = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values
            }
            
            if filter_expression:
                query_params['FilterExpression'] = filter_expression
            
            if limit:
                query_params['Limit'] = limit
            
            response = table.query(**query_params)
            items = response.get('Items', [])
            
            return [self._deserialize_item(item) for item in items]
        except Exception as e:
            logger.error(f"Failed to query items from {table_name}: {e}")
            return []
    
    def scan_items(self,
                   table_name: str, 
                   filter_expression=None,
                   expression_attribute_values: Optional[Dict[str, Any]] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scan all items from DynamoDB (use sparingly)"""
        try:
            table = self._get_table(table_name)
            scan_params = {}
            
            if filter_expression:
                scan_params['FilterExpression'] = filter_expression
            
            if expression_attribute_values:
                scan_params['ExpressionAttributeValues'] = expression_attribute_values
            
            if limit:
                scan_params['Limit'] = limit
            
            response = table.scan(**scan_params)
            items = response.get('Items', [])
            
            return [self._deserialize_item(item) for item in items]
        except Exception as e:
            logger.error(f"Failed to scan items from {table_name}: {e}")
            return []
    
    def update_item(self,
                    table_name: str, 
                    key: Dict[str, Any],
                    update_expression: str,
                    expression_attribute_values: Dict[str, Any],
                    expression_attribute_names: Optional[Dict[str, str]] = None) -> bool:
        """Update an item in DynamoDB"""
        try:
            table = self._get_table(table_name)
            update_params = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnValues': 'UPDATED_NEW'
            }
            
            if expression_attribute_names:
                update_params['ExpressionAttributeNames'] = expression_attribute_names
            
            table.update_item(**update_params)
            logger.info(f"Item updated in {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update item in {table_name}: {e}")
            return False
    
    def batch_write_items(self, table_name: str, items: List[Dict[str, Any]]) -> bool:
        """Batch write multiple items to DynamoDB"""
        try:
            table = self._get_table(table_name)
            with table.batch_writer() as batch:
                for item in items:
                    item = self._serialize_item(item)
                    batch.put_item(Item=item)
            
            logger.info(f"Batch wrote {len(items)} items to {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to batch write items to {table_name}: {e}")
            return False
    
    def _serialize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Python types to DynamoDB compatible types"""
        serialized = {}
        for key, value in item.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, float):
                serialized[key] = Decimal(str(value))
            elif isinstance(value, dict):
                serialized[key] = self._serialize_item(value)
            elif isinstance(value, list):
                serialized[key] = [self._serialize_value(v) for v in value]
            else:
                serialized[key] = value
        return serialized
    
    def _serialize_value(self, value: Any) -> Any:
        """Serialize a single value"""
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, float):
            return Decimal(str(value))
        elif isinstance(value, dict):
            return self._serialize_item(value)
        return value
    
    def _deserialize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert DynamoDB types back to Python types"""
        deserialized = {}
        for key, value in item.items():
            if isinstance(value, Decimal):
                deserialized[key] = float(value)
            elif isinstance(value, dict):
                deserialized[key] = self._deserialize_item(value)
            elif isinstance(value, list):
                deserialized[key] = [self._deserialize_value(v) for v in value]
            else:
                deserialized[key] = value
        return deserialized
    
    def _deserialize_value(self, value: Any) -> Any:
        """Deserialize a single value"""
        if isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, dict):
            return self._deserialize_item(value)
        return value


# Global connection instance
_dynamodb_connection: Optional[DynamoDBConnection] = None


def get_dynamodb_connection() -> DynamoDBConnection:
    """Get or create DynamoDB connection singleton"""
    global _dynamodb_connection
    if _dynamodb_connection is None:
        _dynamodb_connection = DynamoDBConnection()
    return _dynamodb_connection


def close_dynamodb_connection():
    """Close global DynamoDB connection"""
    global _dynamodb_connection
    if _dynamodb_connection:
        logger.info("DynamoDB connection closed")
        _dynamodb_connection = None


# Example usage functions
def test_connection() -> bool:
    """Test DynamoDB connection"""
    try:
        conn = get_dynamodb_connection()
        # Try to describe a table
        test_table_name = list(conn.table_mapping.values())[0]
        table = conn._get_table(test_table_name)
        table_status = table.table_status
        logger.info(f"DynamoDB connection test successful. Table status: {table_status}")
        return True
    except Exception as e:
        logger.error(f"DynamoDB connection test failed: {e}")
        return False


def create_sample_item(table_name: str = 'ashoka-content'):
    """Create a sample item for testing"""
    conn = get_dynamodb_connection()
    
    sample_item = {
        'content_id': 'test_001',
        'user_id': 'user_001',
        'content_text': 'This is a test content',
        'summary': 'Test summary',
        'keywords': ['test', 'sample', 'demo'],
        'sentiment': 'positive',
        'sentiment_score': 0.85,
        'quality_score': 0.92,
        'toxicity_score': 0.05,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    
    return conn.put_item(table_name, sample_item)
