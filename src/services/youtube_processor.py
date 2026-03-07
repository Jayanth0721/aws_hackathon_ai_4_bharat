"""YouTube Video Processor - Download and analyze YouTube videos"""
import os
import tempfile
import shutil
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from src.utils.logging import logger


class YouTubeProcessor:
    """Process YouTube videos by URL"""
    
    def __init__(self):
        self.yt_dlp_available = False
        self._check_yt_dlp()
        self._temp_files = []  # Track temporary files for cleanup
    
    def _check_yt_dlp(self):
        """Check if yt-dlp is available"""
        try:
            import yt_dlp
            self.yt_dlp_available = True
            logger.info("yt-dlp is available for YouTube processing")
        except ImportError:
            logger.warning("yt-dlp not installed. Run: pip install yt-dlp")
            self.yt_dlp_available = False
    
    def cleanup_temp_files(self, file_path: Optional[str] = None, temp_dir: Optional[str] = None):
        """
        Clean up temporary files and directories
        
        Args:
            file_path: Specific file to delete
            temp_dir: Temporary directory to delete
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            
            # Remove from tracking list
            if file_path in self._temp_files:
                self._temp_files.remove(file_path)
        
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {e}")
    
    def schedule_cleanup(self, file_path: str, temp_dir: str, delay_seconds: int = 300):
        """
        Schedule cleanup after a delay (fallback mechanism)
        
        Args:
            file_path: File to clean up
            temp_dir: Directory to clean up
            delay_seconds: Delay before cleanup (default 5 minutes)
        """
        def delayed_cleanup():
            import time
            time.sleep(delay_seconds)
            self.cleanup_temp_files(file_path, temp_dir)
        
        cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
        cleanup_thread.start()
        logger.info(f"Scheduled cleanup for {file_path} in {delay_seconds} seconds")
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Supports formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - URLs with query parameters and timestamps
        """
        import re
        
        # Sanitize URL - limit length and remove dangerous characters
        if len(url) > 2048:
            return None
        
        # Whitelist YouTube domains
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        if not any(domain in url.lower() for domain in youtube_domains):
            return None
        
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # Validate video ID format (11 chars, alphanumeric + - and _)
                if re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
                    return video_id
        
        return None
    
    def validate_youtube_url(self, url: str) -> bool:
        """Validate if URL is a valid YouTube URL"""
        video_id = self.extract_video_id(url)
        return video_id is not None
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get video metadata without downloading
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dict with video metadata
        """
        if not self.yt_dlp_available:
            return {
                "success": False,
                "error": "yt-dlp not installed. Run: pip install yt-dlp",
                "error_code": "YTDLP_NOT_INSTALLED"
            }
        
        # Validate URL first
        if not self.validate_youtube_url(url):
            return {
                "success": False,
                "error": "Invalid YouTube URL format. Please enter a valid YouTube link.",
                "error_code": "INVALID_URL"
            }
        
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False  # Get full metadata
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                duration = info.get('duration', 0)
                
                # Check if video is too long (>2 hours = 7200 seconds)
                if duration > 7200:
                    return {
                        "success": False,
                        "error": "Video duration exceeds the 2-hour limit. Please select a shorter video.",
                        "error_code": "VIDEO_TOO_LONG",
                        "duration": duration
                    }
                
                return {
                    "success": True,
                    "title": info.get('title', 'Unknown'),
                    "duration": duration,
                    "uploader": info.get('uploader', 'Unknown'),
                    "upload_date": info.get('upload_date', 'Unknown'),
                    "view_count": info.get('view_count', 0),
                    "description": info.get('description', ''),
                    "thumbnail": info.get('thumbnail', ''),
                    "video_id": self.extract_video_id(url)
                }
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for specific error types
            if 'private' in error_msg or 'unavailable' in error_msg or 'deleted' in error_msg:
                return {
                    "success": False,
                    "error": "Video unavailable. The video may be private, deleted, or restricted in your region.",
                    "error_code": "VIDEO_UNAVAILABLE"
                }
            elif 'network' in error_msg or 'connection' in error_msg:
                return {
                    "success": False,
                    "error": "Network error. Please check your connection and try again.",
                    "error_code": "NETWORK_ERROR"
                }
            else:
                logger.error(f"Error getting video info: {e}")
                return {
                    "success": False,
                    "error": f"Failed to retrieve video information: {str(e)}",
                    "error_code": "METADATA_RETRIEVAL_FAILED"
                }
    
    def download_video(self, url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Download YouTube video
        
        Args:
            url: YouTube video URL
            output_path: Optional output directory (uses temp dir if not specified)
            
        Returns:
            Dict with download status and file path
        """
        if not self.yt_dlp_available:
            return {
                "success": False,
                "error": "yt-dlp not installed. Run: pip install yt-dlp",
                "file_path": None
            }
        
        try:
            import yt_dlp
            
            # Create output directory
            if output_path is None:
                output_path = tempfile.mkdtemp()
            
            output_template = os.path.join(output_path, '%(id)s.%(ext)s')
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # Prefer MP4
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True
            }
            
            logger.info(f"Downloading YouTube video: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info.get('id', 'video')
                ext = info.get('ext', 'mp4')
                file_path = os.path.join(output_path, f"{video_id}.{ext}")
                
                logger.info(f"Video downloaded successfully: {file_path}")
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "video_id": video_id,
                    "title": info.get('title', 'Unknown'),
                    "duration": info.get('duration', 0)
                }
        
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return {
                "success": False,
                "error": str(e),
                "file_path": None
            }
    
    def download_audio_only(self, url: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Download only audio from YouTube video (faster and smaller)
        
        Args:
            url: YouTube video URL
            output_path: Optional output directory
            
        Returns:
            Dict with download status and file path
        """
        if not self.yt_dlp_available:
            return {
                "success": False,
                "error": "yt-dlp not installed. Run: pip install yt-dlp",
                "error_code": "YTDLP_NOT_INSTALLED",
                "file_path": None
            }
        
        try:
            import yt_dlp
            
            # Create secure temporary directory if not specified
            if output_path is None:
                output_path = tempfile.mkdtemp(prefix='youtube_audio_')
                # Set restrictive permissions (owner only)
                os.chmod(output_path, 0o700)
            
            output_template = os.path.join(output_path, '%(id)s.%(ext)s')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # 192kbps for good quality
                }],
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,  # 30 second timeout
                'retries': 3  # Retry on network errors
            }
            
            logger.info(f"Downloading audio from YouTube video: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info.get('id', 'audio')
                file_path = os.path.join(output_path, f"{video_id}.mp3")
                
                # Verify file exists and has content
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    return {
                        "success": False,
                        "error": "Audio file is empty or missing",
                        "error_code": "EMPTY_AUDIO_FILE",
                        "file_path": None
                    }
                
                # Track temp file for cleanup
                self._temp_files.append(file_path)
                
                # Schedule automatic cleanup after 5 minutes as fallback
                self.schedule_cleanup(file_path, output_path, delay_seconds=300)
                
                logger.info(f"Audio downloaded successfully: {file_path}")
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "video_id": video_id,
                    "title": info.get('title', 'Unknown'),
                    "duration": info.get('duration', 0),
                    "temp_dir": output_path
                }
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for bot detection first
            if self._is_bot_detection_error(error_msg):
                logger.warning(f"Bot detection error for URL: {url}")
                return {
                    "success": False,
                    "error": "YouTube has detected automated access and blocked this request. Please try again in a few minutes or use a different video.",
                    "error_code": "BOT_DETECTION",
                    "file_path": None
                }
            
            # Categorize other errors
            if 'disk' in error_msg or 'space' in error_msg:
                return {
                    "success": False,
                    "error": "Insufficient disk space",
                    "error_code": "DISK_SPACE_ERROR",
                    "file_path": None
                }
            elif 'timeout' in error_msg:
                return {
                    "success": False,
                    "error": "Download timed out. Please try again.",
                    "error_code": "DOWNLOAD_TIMEOUT",
                    "file_path": None
                }
            elif 'network' in error_msg or 'connection' in error_msg:
                return {
                    "success": False,
                    "error": "Network error during download",
                    "error_code": "NETWORK_ERROR",
                    "file_path": None
                }
            else:
                logger.error(f"Error downloading audio: {e}")
                return {
                    "success": False,
                    "error": "Failed to extract audio from video. Please try again or contact support.",
                    "error_code": "DOWNLOAD_FAILED",
                    "file_path": None
                }
    
    def process_youtube_url(self, url: str, audio_only: bool = True) -> Dict[str, Any]:
        """
        Process YouTube video: download and prepare for transcription
        
        Args:
            url: YouTube video URL
            audio_only: If True, download only audio (faster, recommended)
            
        Returns:
            Dict with file path and metadata
        """
        # Validate URL
        if not self.validate_youtube_url(url):
            return {
                "success": False,
                "error": "Invalid YouTube URL",
                "file_path": None
            }
        
        # Get video info first
        info = self.get_video_info(url)
        if not info.get("success"):
            return info
        
        # Download
        if audio_only:
            result = self.download_audio_only(url)
        else:
            result = self.download_video(url)
        
        if result.get("success"):
            result["metadata"] = {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count"),
                "description": info.get("description")
            }
        
        return result

    def _is_bot_detection_error(self, error_msg: str) -> bool:
        """
        Detect if error is due to bot detection/blocking

        Args:
            error_msg: Error message from yt-dlp (lowercased)

        Returns:
            True if error indicates bot detection
        """
        bot_keywords = [
            'bot',
            'blocked',
            'captcha',
            'too many requests',
            'rate limit',
            'forbidden',
            '429',
            'sign in to confirm',
            'unusual traffic'
        ]

        return any(keyword in error_msg for keyword in bot_keywords)


# Global instance
youtube_processor = YouTubeProcessor()
