"""Multi-Engine AI Client with Fallback Support
Supports: Gemini AI, OpenAI, Sarvam AI
"""
import os
import json
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

from src.utils.logging import logger

# Import AI SDKs
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-genai not installed")


class AIEngine(Enum):
    """Available AI engines"""
    GEMINI = "gemini"
    SARVAM = "sarvam"
    GEMINI3 = "gemini3"


class MultiEngineAIClient:
    """Multi-engine AI client with automatic fallback"""
    
    # Rate limits per day (free tier)
    RATE_LIMITS = {
        AIEngine.GEMINI: {
            "gemini-2.0-flash": 50,
            "gemini-2.5-flash": 20,
            "gemini-2.0-flash-exp": 50,
        },
        AIEngine.SARVAM: {
            "sarvam-m": "Check https://www.sarvam.ai",
            "sarvam-30b": "Check https://www.sarvam.ai",
            "sarvam-30b-16k": "Check https://www.sarvam.ai",
            "sarvam-105b": "Check https://www.sarvam.ai",
            "sarvam-105b-32k": "Check https://www.sarvam.ai",
        },
        AIEngine.GEMINI3: {
            "gemini-2.0-flash": 50,
            "gemini-2.5-flash": 20,
            "gemini-2.0-flash-exp": 50,
        }
    }
    
    def __init__(self):
        """Initialize multi-engine AI client"""
        self.primary_engine = os.getenv('PRIMARY_AI_ENGINE', 'gemini').lower()
        self.engines = {}
        
        # Initialize Gemini (Engine 1)
        self._init_gemini()
        
        # Initialize Sarvam AI (Engine 2)
        self._init_sarvam()
        
        # Initialize Gemini Engine 3 (Backup Gemini)
        self._init_gemini3()
        
        # Set engine priority
        self.engine_priority = [
            AIEngine.GEMINI,
            AIEngine.SARVAM,
            AIEngine.GEMINI3
        ]
        
        # Reorder based on primary engine
        if self.primary_engine == 'sarvam':
            self.engine_priority = [AIEngine.SARVAM, AIEngine.GEMINI, AIEngine.GEMINI3]
        
        logger.info(f"Multi-engine AI initialized. Priority: {[e.value for e in self.engine_priority]}")
        logger.info(f"Available engines: {list(self.engines.keys())}")
    
    def _init_gemini(self):
        """Initialize Gemini engine"""
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini: SDK not installed")
            return
        
        api_key = os.getenv('GEMINI_API_KEY', '')
        model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        
        if not api_key:
            logger.warning("Gemini: API key not set")
            return
        
        try:
            client = genai.Client(api_key=api_key)
            self.engines[AIEngine.GEMINI] = {
                'client': client,
                'model': model,
                'type': 'gemini'
            }
            logger.info(f"✓ Gemini initialized: {model}")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
    
    
    def _init_sarvam(self):
        """Initialize Sarvam AI engine"""
        api_key = os.getenv('SARVAM_API_KEY', '')
        model = os.getenv('SARVAM_MODEL', 'sarvam-m')
        
        if not api_key or api_key == 'your_sarvam_key_here':
            logger.warning("Sarvam AI: API key not set or using placeholder")
            return
        
        self.engines[AIEngine.SARVAM] = {
            'api_key': api_key,
            'model': model,
            'type': 'sarvam',
            'endpoint': 'https://api.sarvam.ai/v1/chat/completions'
        }
        logger.info(f"✓ Sarvam AI initialized: {model}")
    
    def _init_gemini3(self):
        """Initialize Gemini Engine 3 (Backup Gemini)"""
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini Engine 3: SDK not installed")
            return
        
        api_key = os.getenv('GEMINI_ENGINE3', '')
        model = os.getenv('GEMINI_MODEL_ENGINE3', 'gemini-2.0-flash')
        
        if not api_key or api_key == 'YOUR_SECOND_GEMINI_KEY_HERE':
            logger.warning("Gemini Engine 3: API key not set or using placeholder")
            return
        
        try:
            client = genai.Client(api_key=api_key)
            self.engines[AIEngine.GEMINI3] = {
                'client': client,
                'model': model,
                'type': 'gemini'
            }
            logger.info(f"✓ Gemini Engine 3 initialized: {model}")
        except Exception as e:
            logger.error(f"Gemini Engine 3 initialization failed: {e}")
    
    def is_available(self) -> bool:
        """Check if any AI engine is available"""
        return len(self.engines) > 0
    
    def get_available_engines(self) -> List[str]:
        """Get list of available engine names"""
        return [engine.value for engine in self.engines.keys()]
    
    def get_rate_limits(self) -> Dict[str, Any]:
        """Get rate limits for all engines"""
        limits = {}
        for engine, config in self.engines.items():
            model = config.get('model', 'unknown')
            limit = self.RATE_LIMITS.get(engine, {}).get(model, "Unknown")
            limits[f"{engine.value} ({model})"] = limit
        return limits
    
    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        preferred_engine: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate content using available AI engines with fallback
        
        Args:
            prompt: User prompt
            system_instruction: System instruction for context
            temperature: Sampling temperature
            preferred_engine: Preferred engine name (optional)
            
        Returns:
            Dict with response and metadata
        """
        if not self.is_available():
            raise Exception("No AI engines available. Check API keys and installation.")
        
        # Determine engine order
        engine_order = self.engine_priority.copy()
        if preferred_engine:
            try:
                pref_enum = AIEngine(preferred_engine.lower())
                if pref_enum in self.engines:
                    engine_order.remove(pref_enum)
                    engine_order.insert(0, pref_enum)
            except ValueError:
                pass
        
        # Try each engine in order
        last_error = None
        for engine in engine_order:
            if engine not in self.engines:
                continue
            
            try:
                logger.info(f"Attempting generation with {engine.value}")
                
                if engine == AIEngine.GEMINI or engine == AIEngine.GEMINI3:
                    result = self._generate_gemini(prompt, system_instruction, temperature, engine)
                elif engine == AIEngine.SARVAM:
                    result = self._generate_sarvam(prompt, system_instruction, temperature)
                else:
                    continue
                
                result['engine_used'] = engine.value
                logger.info(f"✓ Generation successful with {engine.value}")
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"✗ {engine.value} failed: {str(e)}")
                continue
        
        # All engines failed
        raise Exception(f"All AI engines failed. Last error: {last_error}")
    
    def _generate_gemini(
            self,
            prompt: str,
            system_instruction: Optional[str],
            temperature: float,
            engine: AIEngine
        ) -> Dict[str, Any]:
            """Generate content using Gemini (Engine 1 or Engine 3)

            Args:
                prompt: User prompt
                system_instruction: Optional system instruction
                temperature: Sampling temperature
                engine: Which Gemini engine to use (AIEngine.GEMINI or AIEngine.GEMINI3)

            Returns:
                Dict with response and metadata
            """
            config = self.engines[engine]
            client = config['client']
            model = config['model']

            # Prepare prompt
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt

            # Generate
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=4096,
                )
            )

            return {
                'success': True,
                'text': response.text,
                'content': response.text,
                'model': model,
                'engine': 'gemini'
            }

    
    
    def _generate_sarvam(
        self,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float
    ) -> Dict[str, Any]:
        """Generate content using Sarvam AI"""
        config = self.engines[AIEngine.SARVAM]
        api_key = config['api_key']
        model = config['model']
        endpoint = config['endpoint']
        
        # Prepare request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': 4096
        }
        
        # Make request
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            text = data['choices'][0]['message']['content']
            
            return {
                'success': True,
                'text': text,
                'content': text,
                'model': model,
                'engine': 'sarvam'
            }
        except requests.exceptions.HTTPError as e:
            # Log the actual error response for debugging
            error_detail = ""
            try:
                error_detail = response.json()
                logger.error(f"Sarvam AI error response: {error_detail}")
            except:
                error_detail = response.text
                logger.error(f"Sarvam AI error text: {error_detail}")
            raise Exception(f"Sarvam AI HTTP {response.status_code}: {error_detail}")
    
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """Simple text generation (returns just the text)"""
        result = self.generate_content(prompt, temperature=temperature)
        return result.get('text', '')
    
    def analyze_content(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for sentiment, keywords, topics, etc.
        
        Returns structured analysis compatible with existing code
        """
        prompt = f"""Analyze the following content and provide a structured response in JSON format:

Content: {content}

Provide analysis in this exact JSON format (respond ONLY with valid JSON, no other text):
{{
    "summary": "Brief summary of the content",
    "sentiment": {{
        "classification": "positive or negative or neutral",
        "confidence": 0.85,
        "scores": {{
            "positive": 0.4,
            "neutral": 0.3,
            "negative": 0.3
        }}
    }},
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "topics": ["topic1", "topic2", "topic3"],
    "takeaways": ["takeaway1", "takeaway2", "takeaway3"]
}}"""
        
        system_instruction = "You are a content analysis expert. Respond ONLY with valid JSON. Do not include any explanations, thinking process, or markdown formatting."
        
        result = self.generate_content(prompt, system_instruction, temperature=0.3)
        
        try:
            # Parse JSON from response
            text = result['text']
            
            # Remove any <think> tags or reasoning tokens
            if '<think>' in text:
                # Extract content after </think> tag
                if '</think>' in text:
                    text = text.split('</think>')[1].strip()
                else:
                    # If no closing tag, try to find JSON starting with {
                    text = text[text.find('{'):] if '{' in text else text
            
            # Extract JSON from markdown code blocks if present
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            # Find the first { and last } to extract JSON object
            if '{' in text and '}' in text:
                start = text.find('{')
                end = text.rfind('}') + 1
                text = text[start:end]
            
            analysis = json.loads(text)
            
            # Ensure sentiment is properly structured
            if 'sentiment' in analysis:
                if isinstance(analysis['sentiment'], str):
                    # Convert string sentiment to dict format
                    sentiment_str = analysis['sentiment'].lower()
                    analysis['sentiment'] = {
                        'classification': sentiment_str,
                        'confidence': 0.8,
                        'scores': {
                            'positive': 0.4 if sentiment_str == 'positive' else 0.2,
                            'neutral': 0.4 if sentiment_str == 'neutral' else 0.3,
                            'negative': 0.4 if sentiment_str == 'negative' else 0.2
                        }
                    }
            
            analysis['engine_used'] = result.get('engine_used', 'unknown')
            return analysis
        except Exception as e:
            logger.error(f"Failed to parse analysis JSON: {e}")
            logger.error(f"Raw response text: {result.get('text', '')[:500]}")
            # Return fallback structure with proper format
            return {
                'summary': result.get('text', '')[:200] if isinstance(result, dict) else str(result)[:200],
                'sentiment': {
                    'classification': 'neutral',
                    'confidence': 0.5,
                    'scores': {'positive': 0.33, 'neutral': 0.34, 'negative': 0.33}
                },
                'confidence': 0.5,
                'keywords': [],
                'topics': [],
                'takeaways': [],
                'engine_used': result.get('engine_used', 'unknown') if isinstance(result, dict) else 'unknown'
            }


# Global instance
ai_client = MultiEngineAIClient()
