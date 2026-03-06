"""YouTube Video Analyzer - Complete pipeline for YouTube video analysis"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from src.services.youtube_processor import youtube_processor
from src.services.media_processor import media_processor
from src.services.gemini_client import gemini_client
from src.database.duckdb_schema import db_schema
from src.utils.logging import logger
from src.utils.id_generator import generate_id
from src.utils.timestamp import utc_now


class YouTubeAnalyzer:
    """Analyze YouTube videos: download → transcribe → analyze"""
    
    def __init__(self):
        self.youtube_processor = youtube_processor
        self.media_processor = media_processor
        self.gemini_client = gemini_client
        self.db = db_schema
    
    def get_quick_summary(self, url: str) -> Dict[str, Any]:
        """
        Get quick summary without full analysis (metadata only)
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dict with video metadata
        """
        logger.info(f"Getting quick summary for: {url}")
        
        # Get video metadata
        info = self.youtube_processor.get_video_info(url)
        
        if not info.get("success"):
            return info
        
        return {
            "success": True,
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "description": info.get("description"),
            "thumbnail": info.get("thumbnail"),
            "video_id": info.get("video_id")
        }
    
    def analyze_youtube_video(self, url: str, user_id: str, audio_only: bool = True) -> Dict[str, Any]:
        """
        Complete YouTube video analysis pipeline
        
        Args:
            url: YouTube video URL
            user_id: User ID for tracking
            audio_only: Download only audio (faster, recommended)
            
        Returns:
            Dict with complete analysis results
        """
        logger.info(f"Starting YouTube video analysis for user {user_id}: {url}")
        
        start_time = datetime.now()
        file_path = None
        temp_dir = None
        
        try:
            # Stage 1: URL validation
            if not self.youtube_processor.validate_youtube_url(url):
                return {
                    "success": False,
                    "error": "Invalid YouTube URL format. Please enter a valid YouTube link.",
                    "error_code": "INVALID_URL",
                    "stage": "validation"
                }
            
            video_id = self.youtube_processor.extract_video_id(url)
            
            # Stage 2: Check transcription cache
            cached_transcript = self._get_cached_transcription(video_id)
            if cached_transcript:
                logger.info(f"Using cached transcription for video {video_id}")
                transcript = cached_transcript["transcript"]
                language = cached_transcript["language"]
                
                # Get metadata
                metadata_result = self.youtube_processor.get_video_info(url)
                if not metadata_result.get("success"):
                    return {
                        "success": False,
                        "error": metadata_result.get("error"),
                        "error_code": metadata_result.get("error_code"),
                        "stage": "metadata"
                    }
                
                metadata = metadata_result
            else:
                # Stage 3: Get video metadata
                metadata_result = self.youtube_processor.get_video_info(url)
                if not metadata_result.get("success"):
                    return {
                        "success": False,
                        "error": metadata_result.get("error"),
                        "error_code": metadata_result.get("error_code"),
                        "stage": "metadata"
                    }
                
                metadata = metadata_result
                
                # Stage 4: Download audio
                logger.info("Downloading audio...")
                download_result = self.youtube_processor.download_audio_only(url)
                
                if not download_result.get("success"):
                    return {
                        "success": False,
                        "error": download_result.get("error"),
                        "error_code": download_result.get("error_code"),
                        "stage": "download",
                        "metadata": metadata
                    }
                
                file_path = download_result.get("file_path")
                temp_dir = download_result.get("temp_dir")
                
                # Stage 5: Transcribe audio
                logger.info("Transcribing audio...")
                transcription_result = self.media_processor.process_audio(file_path)
                
                if not transcription_result.get("success"):
                    return {
                        "success": False,
                        "error": "Transcription failed. Please try again or contact support.",
                        "error_code": "TRANSCRIPTION_FAILED",
                        "stage": "transcription",
                        "metadata": metadata
                    }
                
                transcript = transcription_result.get("transcript")
                language = transcription_result.get("language", "unknown")
                
                # Cache the transcription
                self._save_transcription_to_cache(video_id, transcript, language)
            
            # Stage 6: Analyze content
            logger.info("Analyzing content...")
            analysis_result = self._analyze_transcript(transcript)
            
            if not analysis_result.get("success"):
                # Graceful degradation - return transcript even if analysis fails
                logger.warning("Analysis failed, returning transcript only")
                analysis_result = {
                    "summary": "Analysis unavailable",
                    "sentiment": "neutral",
                    "sentiment_confidence": 0.0,
                    "keywords": [],
                    "topics": [],
                    "takeaways": []
                }
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Stage 7: Store in database
            query_id = generate_id()
            self._save_query_history(
                query_id=query_id,
                user_id=user_id,
                youtube_url=url,
                video_id=video_id,
                analysis_mode="full",
                metadata=metadata,
                transcript=transcript,
                language=language,
                analysis=analysis_result,
                processing_time=processing_time
            )
            
            # Combine all results
            result = {
                "success": True,
                "url": url,
                "metadata": {
                    "title": metadata.get("title"),
                    "duration": metadata.get("duration"),
                    "uploader": metadata.get("uploader"),
                    "view_count": metadata.get("view_count"),
                    "thumbnail": metadata.get("thumbnail"),
                    "language": language
                },
                "transcript": transcript,
                "analysis": analysis_result,
                "word_count": len(transcript.split()),
                "char_count": len(transcript),
                "processing_time": processing_time
            }
            
            logger.info(f"YouTube analysis complete in {processing_time:.2f}s")
            return result
        
        except Exception as e:
            logger.error(f"Unexpected error in YouTube analysis: {e}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}",
                "error_code": "UNEXPECTED_ERROR",
                "stage": "unknown"
            }
        
        finally:
            # Stage 8: Cleanup temporary files
            if file_path and temp_dir:
                self.youtube_processor.cleanup_temp_files(file_path, temp_dir)
    
    def _analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript using Gemini AI"""
        try:
            if not self.gemini_client.is_available():
                return {
                    "success": False,
                    "error": "Gemini AI not available"
                }
            
            # Use Gemini to analyze the transcript
            analysis = self.gemini_client.analyze_content(transcript)
            
            return {
                "success": True,
                "summary": analysis.get("summary", ""),
                "sentiment": analysis.get("sentiment", {}).get("classification", "neutral"),
                "sentiment_confidence": analysis.get("sentiment", {}).get("confidence", 0.0),
                "keywords": analysis.get("keywords", []),
                "topics": analysis.get("topics", []),
                "takeaways": analysis.get("takeaways", [])
            }
        
        except Exception as e:
            logger.error(f"Content analysis error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_cached_transcription(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get cached transcription if available and fresh (<24 hours)"""
        try:
            if not self.db.conn:
                self.db.connect()
            
            result = self.db.conn.execute("""
                SELECT transcript, transcript_language, cached_at, access_count
                FROM youtube_transcription_cache
                WHERE video_id = ?
            """, [video_id]).fetchone()
            
            if result:
                transcript, language, cached_at, access_count = result
                
                # Check if cache is still fresh (<24 hours)
                cache_age = datetime.now() - cached_at
                if cache_age < timedelta(hours=24):
                    # Update access count and last accessed time
                    self.db.conn.execute("""
                        UPDATE youtube_transcription_cache
                        SET access_count = ?, last_accessed_at = ?
                        WHERE video_id = ?
                    """, [access_count + 1, utc_now(), video_id])
                    
                    logger.info(f"Cache hit for video {video_id} (age: {cache_age})")
                    return {
                        "transcript": transcript,
                        "language": language
                    }
                else:
                    logger.info(f"Cache expired for video {video_id} (age: {cache_age})")
            
            return None
        
        except Exception as e:
            logger.error(f"Error checking cache: {e}")
            return None
    
    def _save_transcription_to_cache(self, video_id: str, transcript: str, language: str):
        """Save transcription to cache"""
        try:
            if not self.db.conn:
                self.db.connect()
            
            now = datetime.now()
            
            self.db.conn.execute("""
                INSERT OR REPLACE INTO youtube_transcription_cache
                (video_id, transcript, transcript_language, cached_at, access_count, last_accessed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [video_id, transcript, language, now, 1, now])
            
            logger.info(f"Cached transcription for video {video_id}")
            
            # Implement LRU eviction (keep max 1000 entries)
            count_result = self.db.conn.execute("SELECT COUNT(*) FROM youtube_transcription_cache").fetchone()
            if count_result and count_result[0] > 1000:
                self.db.conn.execute("""
                    DELETE FROM youtube_transcription_cache
                    WHERE video_id IN (
                        SELECT video_id FROM youtube_transcription_cache
                        ORDER BY last_accessed_at ASC
                        LIMIT ?
                    )
                """, [count_result[0] - 1000])
        
        except Exception as e:
            logger.error(f"Error caching transcription: {e}")
    
    def _save_query_history(self, query_id: str, user_id: str, youtube_url: str,
                           video_id: str, analysis_mode: str, metadata: Dict,
                           transcript: str, language: str, analysis: Dict,
                           processing_time: float):
        """Save query history to database"""
        try:
            if not self.db.conn:
                self.db.connect()
            
            self.db.conn.execute("""
                INSERT INTO youtube_query_history
                (query_id, user_id, youtube_url, video_id, analysis_mode,
                 video_title, video_duration, video_uploader, video_view_count, video_thumbnail_url,
                 transcript, transcript_language,
                 summary, sentiment, sentiment_confidence, keywords, topics, takeaways,
                 created_at, processing_time_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                query_id, user_id, youtube_url, video_id, analysis_mode,
                metadata.get("title"), metadata.get("duration"), metadata.get("uploader"),
                metadata.get("view_count"), metadata.get("thumbnail"),
                transcript, language,
                analysis.get("summary"), analysis.get("sentiment"), analysis.get("sentiment_confidence"),
                json.dumps(analysis.get("keywords", [])), json.dumps(analysis.get("topics", [])),
                json.dumps(analysis.get("takeaways", [])),
                utc_now(), processing_time
            ])
            
            logger.info(f"Saved query history: {query_id}")
        
        except Exception as e:
            logger.error(f"Error saving query history: {e}")
    
    def get_user_query_history(self, user_id: str, limit: int = 10, offset: int = 0) -> list:
        """Get user's YouTube analysis history"""
        try:
            if not self.db.conn:
                self.db.connect()
            
            results = self.db.conn.execute("""
                SELECT query_id, youtube_url, video_id, video_title, video_thumbnail_url,
                       created_at, analysis_mode
                FROM youtube_query_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, [user_id, limit, offset]).fetchall()
            
            history = []
            for row in results:
                history.append({
                    "query_id": row[0],
                    "youtube_url": row[1],
                    "video_id": row[2],
                    "video_title": row[3],
                    "video_thumbnail_url": row[4],
                    "created_at": row[5],
                    "analysis_mode": row[6]
                })
            
            return history
        
        except Exception as e:
            logger.error(f"Error getting query history: {e}")
            return []


# Global instance
youtube_analyzer = YouTubeAnalyzer()
