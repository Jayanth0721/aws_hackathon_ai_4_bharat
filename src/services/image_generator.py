"""Image Generation Service using Son of Ashoka API"""
import requests
import base64
from io import BytesIO
from src.utils.logging import logger


class ImageGenerator:
    """Service for generating images from text prompts"""
    
    def __init__(self):
        self.api_url = "https://son-of-ashoka.guymovie89.workers.dev/"
        self.api_token = "img888"
    
    def generate_image(self, prompt: str) -> dict:
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            
        Returns:
            dict with 'success', 'image_data' (base64), 'error' keys
        """
        try:
            logger.info(f"Generating image for prompt: {prompt[:50]}...")
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": prompt
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=60  # 60 second timeout for image generation
            )
            
            if response.status_code == 200:
                # Convert image bytes to base64 for display in UI
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                
                logger.info(f"Image generated successfully, size: {len(response.content)} bytes")
                
                return {
                    'success': True,
                    'image_data': image_base64,
                    'image_bytes': response.content,
                    'prompt': prompt
                }
            else:
                error_msg = f"API returned status {response.status_code}"
                logger.error(f"Image generation failed: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Image generation timed out (60s)"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(f"Image generation failed: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Image generation failed: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def save_image(self, image_bytes: bytes, filepath: str) -> bool:
        """
        Save generated image to file
        
        Args:
            image_bytes: Raw image bytes
            filepath: Path to save the image
            
        Returns:
            bool: True if saved successfully
        """
        try:
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            logger.info(f"Image saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return False


# Global instance
image_generator = ImageGenerator()
