"""DuckDB schema definitions and initialization"""
import duckdb
from pathlib import Path
from src.config import config
from src.utils.logging import logger


class DuckDBSchema:
    """DuckDB schema manager"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DUCKDB_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
    
    def connect(self):
        """Connect to DuckDB"""
        self.conn = duckdb.connect(self.db_path)
        logger.info(f"Connected to DuckDB at {self.db_path}")
        return self.conn
    
    def initialize_schema(self):
        """Create all tables and indexes"""
        if not self.conn:
            self.connect()
        
        # Content Analysis Results Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS content_analysis (
                version_id VARCHAR PRIMARY KEY,
                summary TEXT,
                takeaways JSON,
                keywords JSON,
                topics JSON,
                sentiment_classification VARCHAR,
                sentiment_confidence FLOAT,
                sentiment_scores JSON,
                analyzed_at TIMESTAMP
            )
        """)
        
        # Outcome Classifications Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS outcome_classifications (
                version_id VARCHAR PRIMARY KEY,
                outcome VARCHAR,
                confidence FLOAT,
                risk_factors JSON,
                flagged_for_review BOOLEAN,
                diagnostic_info JSON,
                classified_at TIMESTAMP
            )
        """)
        
        # Quality Metrics Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS quality_metrics (
                version_id VARCHAR PRIMARY KEY,
                readability_score FLOAT,
                tone_consistency_score FLOAT,
                duplicate_count INTEGER,
                similar_content JSON,
                quality_grade VARCHAR,
                measured_at TIMESTAMP
            )
        """)
        
        # Risk Assessments Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS risk_assessments (
                version_id VARCHAR PRIMARY KEY,
                toxicity_score FLOAT,
                contains_hate_speech BOOLEAN,
                policy_risk_level VARCHAR,
                backlash_risk_level VARCHAR,
                risk_factors JSON,
                should_block BOOLEAN,
                assessed_at TIMESTAMP
            )
        """)
        
        # Operation Metrics Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS operation_metrics (
                id INTEGER PRIMARY KEY,
                operation VARCHAR,
                timestamp TIMESTAMP,
                success BOOLEAN,
                latency_ms FLOAT,
                error_type VARCHAR
            )
        """)
        
        # Reactions Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS reactions (
                reaction_id VARCHAR PRIMARY KEY,
                content_id VARCHAR,
                platform VARCHAR,
                user_handle VARCHAR,
                text TEXT,
                timestamp TIMESTAMP,
                reaction_type VARCHAR,
                sentiment VARCHAR
            )
        """)
        
        # Engagement Analysis Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS engagement_analysis (
                content_id VARCHAR PRIMARY KEY,
                total_reactions INTEGER,
                positive_count INTEGER,
                neutral_count INTEGER,
                toxic_count INTEGER,
                high_backlash_count INTEGER,
                engagement_rate FLOAT,
                sentiment_distribution JSON,
                trending_topics JSON,
                analyzed_at TIMESTAMP
            )
        """)
        
        # Security Login Logs Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS security_login_logs (
                log_id INTEGER PRIMARY KEY,
                username VARCHAR,
                ip_address VARCHAR,
                location VARCHAR,
                device_info VARCHAR,
                status VARCHAR,
                timestamp TIMESTAMP,
                session_id VARCHAR
            )
        """)
        
        # Security Events Table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                event_id INTEGER PRIMARY KEY,
                username VARCHAR,
                event_type VARCHAR,
                event_description TEXT,
                timestamp TIMESTAMP,
                metadata JSON
            )
        """)
        
        # Content Intelligence Table - stores all analyzed content
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ashoka_contentint (
                id VARCHAR PRIMARY KEY,
                user_id VARCHAR,
                content_type VARCHAR,
                content_text TEXT,
                file_path VARCHAR,
                file_name VARCHAR,
                file_size_mb FLOAT,
                metadata JSON,
                summary TEXT,
                sentiment VARCHAR,
                sentiment_confidence FLOAT,
                keywords JSON,
                topics JSON,
                takeaways JSON,
                word_count INTEGER,
                char_count INTEGER,
                quality_score FLOAT,
                created_at TIMESTAMP,
                analyzed_at TIMESTAMP
            )
        """)
        
        # Transform History Table - stores all transformed content
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transform_history (
                id VARCHAR PRIMARY KEY,
                user_id VARCHAR,
                original_content TEXT,
                platforms JSON,
                tone VARCHAR,
                include_hashtags BOOLEAN,
                transformed_results JSON,
                created_at TIMESTAMP
            )
        """)
        
        # Users Table - stores user accounts
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
        
        # Sessions Table - stores user sessions
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
        
        # Create indexes for efficient querying
        self._create_indexes()
        
        logger.info("DuckDB schema initialized successfully")
    
    def _create_indexes(self):
        """Create indexes for performance"""
        # Index on analyzed_at for time-based queries
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_content_analysis_time 
            ON content_analysis(analyzed_at)
        """)
        
        # Index on username for fast user lookups
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON ashoka_users(username)
        """)
        
        # Index on session user_id for fast session lookups
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_user_id 
            ON ashoka_sessions(user_id)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_quality_metrics_time 
            ON quality_metrics(measured_at)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_risk_assessments_time 
            ON risk_assessments(assessed_at)
        """)
        
        # Index on operation for metrics aggregation
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_operation_metrics_op 
            ON operation_metrics(operation, timestamp)
        """)
        
        # Index on content_id for reactions
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_reactions_content 
            ON reactions(content_id, timestamp)
        """)
        
        # Index on security logs
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_security_login_logs_time 
            ON security_login_logs(timestamp)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_security_events_time 
            ON security_events(timestamp)
        """)
        
        # Index on content intelligence
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_contentint_user_time 
            ON ashoka_contentint(user_id, created_at)
        """)
        
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_contentint_type 
            ON ashoka_contentint(content_type, created_at)
        """)
        
        # Index on transform history
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_transform_history_user_time 
            ON transform_history(user_id, created_at)
        """)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("DuckDB connection closed")
    
    def get_connection(self):
        """Get database connection"""
        if not self.conn:
            self.connect()
        return self.conn


# Global schema instance
db_schema = DuckDBSchema()
