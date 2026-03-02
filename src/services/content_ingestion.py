"""Content ingestion service"""
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
import PyPDF2
import docx

from src.models.content import ContentVersion
from src.utils.id_generator import generate_version_id
from src.utils.timestamp import utc_now
from src.database.mock_storage import mock_s3
from src.database.db_factory import get_dynamodb
from src.config import config
from src.utils.logging import logger


class ContentIngestionService:
    """Service for ingesting and versioning content"""
    
    def __init__(self):
        # Always use mock storage for now (real S3/DynamoDB requires AWS setup)
        self.s3 = mock_s3
        self.dynamodb = get_dynamodb()
    
    def ingest_text(self, user_id: str, text: str, metadata: Dict = None) -> ContentVersion:
        """Ingest text content directly"""
        version_id = generate_version_id()
        created_at = utc_now()
        
        version = ContentVersion(
            version_id=version_id,
            user_id=user_id,
            content=text,
            created_at=created_at,
            metadata=metadata or {},
            s3_uri=f"s3://{config.S3_BUCKET_NAME}/content/{version_id}.txt"
        )
        
        # Store in S3
        self._store_content(version_id, text)
        
        # Store metadata in DynamoDB
        self._store_metadata(version)
        
        logger.info(f"Ingested text content: {version_id}")
        return version
    
    def ingest_file(self, user_id: str, file_path: str, metadata: Dict = None) -> ContentVersion:
        """Ingest content from file"""
        text = self.extract_text_from_file(file_path)
        return self.ingest_text(user_id, text, metadata)
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT file"""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif extension == '.pdf':
            text = []
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        
        elif extension in ['.docx', '.doc']:
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def create_version(self, user_id: str, content: str, parent_version: Optional[str] = None) -> ContentVersion:
        """Create new version with parent linkage"""
        version_id = generate_version_id()
        created_at = utc_now()
        
        version = ContentVersion(
            version_id=version_id,
            user_id=user_id,
            content=content,
            created_at=created_at,
            parent_version=parent_version,
            s3_uri=f"s3://{config.S3_BUCKET_NAME}/content/{version_id}.txt"
        )
        
        self._store_content(version_id, content)
        self._store_metadata(version)
        
        logger.info(f"Created version: {version_id} (parent: {parent_version})")
        return version
    
    def get_version(self, version_id: str) -> Optional[ContentVersion]:
        """Retrieve content version"""
        metadata = self.dynamodb.get_item(
            config.DYNAMODB_CONTENT_TABLE,
            {"version_id": version_id}
        )
        
        if not metadata:
            return None
        
        content = self._retrieve_content(version_id)
        
        return ContentVersion(
            version_id=metadata["version_id"],
            user_id=metadata["user_id"],
            content=content,
            created_at=datetime.fromisoformat(metadata["created_at"]),
            parent_version=metadata.get("parent_version"),
            metadata=metadata.get("metadata", {}),
            s3_uri=metadata.get("s3_uri")
        )
    
    def _store_content(self, version_id: str, content: str):
        """Store content in S3"""
        key = f"content/{version_id}.txt"
        self.s3.put_object(
            config.S3_BUCKET_NAME,
            key,
            content.encode('utf-8')
        )
    
    def _retrieve_content(self, version_id: str) -> str:
        """Retrieve content from S3"""
        key = f"content/{version_id}.txt"
        content_bytes = self.s3.get_object(config.S3_BUCKET_NAME, key)
        return content_bytes.decode('utf-8') if content_bytes else ""
    
    def _store_metadata(self, version: ContentVersion):
        """Store version metadata in DynamoDB"""
        self.dynamodb.put_item(
            config.DYNAMODB_CONTENT_TABLE,
            {
                "version_id": version.version_id,
                "user_id": version.user_id,
                "created_at": version.created_at.isoformat(),
                "parent_version": version.parent_version,
                "metadata": version.metadata,
                "s3_uri": version.s3_uri
            }
        )
