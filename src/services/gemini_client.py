"""Google Gemini AI Client for Content Analysis"""
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from src.utils.logging import logger


class GeminiClient:
    """Google Gemini client wrapper"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        
        if not GEMINI_AVAILABLE:
            logger.warning("google-genai package not installed. Run: pip install google-genai")
            self.client = None
            return
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set in environment")
            self.client = None
            return
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized: model={self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Gemini client is available"""
        return self.client is not None and GEMINI_AVAILABLE
    
    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate content using Gemini
        
        Args:
            prompt: User prompt/message
            system_instruction: System instruction for context
            temperature: Sampling temperature (0-2)
            
        Returns:
            Dict with response text and metadata
        """
        if not self.is_available():
            raise Exception("Gemini client not initialized. Check API key and installation.")
        
        try:
            start_time = datetime.now()
            
            # Add system instruction if provided
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=4096,
                )
            )
            
            # Calculate metrics
            elapsed_time = (datetime.now() - start_time).total_seconds()
            
            # Extract text
            text = response.text if hasattr(response, 'text') else ''
            
            # Build result
            result = {
                'text': text,
                'model': self.model_name,
                'latency_seconds': elapsed_time
            }
            
            logger.info(f"Gemini generated content: {len(text)} chars, {elapsed_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}")
            raise
    
    def analyze_content(
        self,
        content: str,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Analyze content using Gemini
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis
            
        Returns:
            Analysis results
        """
        system_instruction = """You are an expert content analyst. Analyze the provided content and return 
        a structured JSON response with the following fields:
        - summary: A concise summary (2-3 sentences)
        - sentiment: Object with classification (positive/neutral/negative), confidence (0-1), and scores for each emotion
        - keywords: List of 10-15 most important keywords
        - topics: List of 3-5 main topics
        - takeaways: List of 3-5 key takeaways
        - quality_score: Overall quality score (0-100)
        - readability_score: Readability score (0-100)
        - tone: Detected tone (professional, casual, technical, etc.)
        
        Return ONLY valid JSON, no additional text or markdown."""
        
        prompt = f"""Analyze this content:

{content}

Provide a comprehensive analysis in JSON format."""
        
        try:
            result = self.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=0.3
            )
            
            # Extract JSON from response (handle markdown code blocks)
            response_text = result['text']
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            elif '```' in response_text:
                start = response_text.find('```') + 3
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            
            # Parse JSON response
            analysis = json.loads(response_text)
            
            # Add metadata
            analysis['_metadata'] = {
                'model': result['model'],
                'latency': result['latency_seconds'],
                'provider': 'Google Gemini'
            }
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            return {
                'error': 'Failed to parse response',
                'raw_response': result.get('text', ''),
                '_metadata': {
                    'model': result.get('model'),
                    'latency': result.get('latency_seconds')
                }
            }
    
    def transform_content(
        self,
        content: str,
        target_platform: str,
        tone: str = "professional",
        include_hashtags: bool = True
    ) -> Dict[str, Any]:
        """
        Transform content for a specific platform using Gemini
        
        Args:
            content: Original content
            target_platform: Target platform
            tone: Desired tone
            include_hashtags: Whether to include hashtags
            
        Returns:
            Transformed content with metadata
        """
        platform_specs = {
            'linkedin': {
                'max_chars': 3000,
                'style': 'Professional networking post with clear value proposition',
                'hashtag_count': '3-5'
            },
            'twitter': {
                'max_chars': 280,
                'style': 'Concise, engaging tweet that captures attention',
                'hashtag_count': '1-3'
            },
            'instagram': {
                'max_chars': 2200,
                'style': 'Visual storytelling with engaging narrative',
                'hashtag_count': '10-15'
            },
            'facebook': {
                'max_chars': 63206,
                'style': 'Conversational and community-focused',
                'hashtag_count': '2-5'
            },
            'threads': {
                'max_chars': 500,
                'style': 'Casual, authentic, and conversational',
                'hashtag_count': '1-3'
            }
        }
        
        spec = platform_specs.get(target_platform.lower(), platform_specs['linkedin'])
        
        system_instruction = f"""You are an expert social media content creator. Transform content for {target_platform} 
        following these specifications:
        - Maximum characters: {spec['max_chars']}
        - Style: {spec['style']}
        - Tone: {tone}
        - Hashtags: {'Include ' + spec['hashtag_count'] + ' relevant hashtags' if include_hashtags else 'No hashtags'}
        
        Return a JSON object with:
        - content: The transformed content
        - character_count: Number of characters
        - hashtags: List of hashtags used (if any)
        - within_limit: Boolean indicating if within character limit
        
        Return ONLY valid JSON, no markdown."""
        
        prompt = f"""Transform this content for {target_platform}:

{content}

Apply the specified style, tone, and constraints."""
        
        try:
            result = self.generate_content(
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=0.7
            )
            
            # Extract JSON from response
            response_text = result['text']
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            elif '```' in response_text:
                start = response_text.find('```') + 3
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            
            # Parse JSON response
            transformed = json.loads(response_text)
            
            # Add metadata
            transformed['_metadata'] = {
                'model': result['model'],
                'latency': result['latency_seconds'],
                'platform': target_platform,
                'tone': tone,
                'provider': 'Google Gemini'
            }
            
            return transformed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            return {
                'error': 'Failed to parse response',
                'raw_response': result.get('text', ''),
                '_metadata': {
                    'model': result.get('model'),
                    'latency': result.get('latency_seconds')
                }
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model_name': self.model_name,
            'provider': 'Google Gemini',
            'available': self.is_available(),
            'api_key_set': bool(self.api_key)
        }


# Global Gemini client instance
gemini_client = GeminiClient()
