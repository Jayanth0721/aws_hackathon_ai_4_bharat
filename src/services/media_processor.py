"""Media Processor - Audio and Video Analysis using Whisper"""
import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from src.utils.logging import logger

class MediaProcessor:
    """Process audio and video files using Whisper for transcription"""
    
    def __init__(self):
        self.whisper_available = False
        self.model = None
        self._initialize_whisper()
    
    def _initialize_whisper(self):
        """Initialize Whisper model"""
        try:
            import whisper
            # Use base model for speed (can upgrade to 'small' or 'medium' for better accuracy)
            self.model = whisper.load_model("base")
            self.whisper_available = True
            logger.info("Whisper model loaded successfully (base)")
        except ImportError:
            logger.warning("Whisper not installed. Run: pip install openai-whisper")
            self.whisper_available = False
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.whisper_available = False
    
    def process_audio(self, file_path: str) -> Dict[str, Any]:
        """
        Process audio file and extract transcript
        
        Args:
            file_path: Path to audio file (mp3, wav, m4a, etc.)
            
        Returns:
            Dict with transcript and metadata
        """
        if not self.whisper_available:
            return {
                "success": False,
                "error": "Whisper not available. Install with: pip install openai-whisper",
                "transcript": None
            }
        
        try:
            logger.info(f"Transcribing audio file: {file_path}")
            
            # Transcribe using Whisper
            result = self.model.transcribe(file_path)
            
            transcript = result["text"]
            language = result.get("language", "unknown")
            
            logger.info(f"Audio transcription complete. Language: {language}, Length: {len(transcript)} chars")
            
            return {
                "success": True,
                "transcript": transcript,
                "language": language,
                "file_type": "audio",
                "duration": None  # Whisper doesn't provide duration directly
            }
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": None
            }
    
    def process_video(self, file_path: str) -> Dict[str, Any]:
        """
        Process video file - extract audio and transcribe
        
        Args:
            file_path: Path to video file (mp4, mov, avi, etc.)
            
        Returns:
            Dict with transcript and metadata
        """
        if not self.whisper_available:
            return {
                "success": False,
                "error": "Whisper not available. Install with: pip install openai-whisper",
                "transcript": None
            }
        
        try:
            # Check if moviepy is available
            try:
                from moviepy.editor import VideoFileClip
            except ImportError:
                return {
                    "success": False,
                    "error": "moviepy not installed. Run: pip install moviepy",
                    "transcript": None
                }
            
            logger.info(f"Processing video file: {file_path}")
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
            
            try:
                # Extract audio from video
                logger.info("Extracting audio from video...")
                video = VideoFileClip(file_path)
                video.audio.write_audiofile(temp_audio_path, logger=None)
                duration = video.duration
                video.close()
                
                # Transcribe the extracted audio
                logger.info("Transcribing extracted audio...")
                result = self.model.transcribe(temp_audio_path)
                
                transcript = result["text"]
                language = result.get("language", "unknown")
                
                logger.info(f"Video transcription complete. Language: {language}, Length: {len(transcript)} chars")
                
                return {
                    "success": True,
                    "transcript": transcript,
                    "language": language,
                    "file_type": "video",
                    "duration": duration
                }
                
            finally:
                # Clean up temporary audio file
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
            
        except Exception as e:
            logger.error(f"Video processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": None
            }
    
    def process_media_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Process media file based on type
        
        Args:
            file_path: Path to media file
            file_type: 'audio' or 'video'
            
        Returns:
            Dict with transcript and metadata
        """
        if file_type == "audio":
            return self.process_audio(file_path)
        elif file_type == "video":
            return self.process_video(file_path)
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {file_type}",
                "transcript": None
            }


# Global instance
media_processor = MediaProcessor()
