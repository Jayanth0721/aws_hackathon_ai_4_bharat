"""Content analysis service using AI"""
from typing import List
from datetime import datetime

from src.models.content import ContentAnalysis, Sentiment
from src.database.duckdb_schema import db_schema
from src.config import config
from src.utils.logging import logger
from src.utils.timestamp import utc_now

# Import AI client
from src.services.gemini_client import gemini_client


class ContentAnalyzer:
    """Service for analyzing content using AI"""
    
    def __init__(self):
        # Use Gemini as the only AI provider
        if config.USE_GEMINI and gemini_client.is_available():
            self.ai_client = gemini_client
            self.use_real_ai = True
            self.ai_provider = 'Gemini'
            logger.info("ContentAnalyzer initialized with Google Gemini")
        else:
            self.ai_client = None
            self.use_real_ai = False
            self.ai_provider = 'None'
            logger.warning("ContentAnalyzer initialized without AI - configure Gemini API key")
        
        self.db = db_schema
    
    def analyze_content(self, version_id: str, content: str) -> ContentAnalysis:
        """Perform comprehensive content analysis"""
        logger.info(f"Analyzing content: {version_id} (using {self.ai_provider})")
        
        # Use real AI for comprehensive analysis if available
        if self.use_real_ai:
            try:
                # Use AI client's analyze_content method
                ai_result = self.ai_client.analyze_content(content)
                
                # Extract data from AI response
                summary = ai_result.get('summary', '')
                takeaways = ai_result.get('takeaways', [])
                keywords = ai_result.get('keywords', [])
                topics = ai_result.get('topics', [])
                
                # Extract sentiment
                sentiment_data = ai_result.get('sentiment', {})
                sentiment = Sentiment(
                    classification=sentiment_data.get('classification', 'neutral'),
                    confidence=sentiment_data.get('confidence', 0.8),
                    scores=sentiment_data.get('scores', {
                        'positive': 0.33,
                        'neutral': 0.34,
                        'negative': 0.33
                    })
                )
                
                analysis = ContentAnalysis(
                    version_id=version_id,
                    summary=summary,
                    takeaways=takeaways,
                    keywords=keywords,
                    topics=topics,
                    sentiment=sentiment,
                    analyzed_at=utc_now()
                )
                
                # Store in DuckDB
                self._store_analysis(analysis)
                
                logger.info(f"Analysis complete (real AI - {self.ai_provider}): {version_id}")
                return analysis
                
            except Exception as e:
                logger.error(f"AI analysis failed, falling back to mock: {e}")
                # Fall through to fallback implementation
        
        # Fallback implementation (when AI is not available)
        summary = self.generate_summary(content)
        takeaways = self.extract_takeaways(content)
        keywords = self.extract_keywords(content)
        topics = self.extract_topics(content)
        sentiment = self.analyze_sentiment(content)
        
        analysis = ContentAnalysis(
            version_id=version_id,
            summary=summary,
            takeaways=takeaways,
            keywords=keywords,
            topics=topics,
            sentiment=sentiment,
            analyzed_at=utc_now()
        )
        
        # Store in DuckDB
        self._store_analysis(analysis)
        
        logger.info(f"Analysis complete (mock): {version_id}")
        return analysis
    
    def generate_summary(self, content: str) -> str:
        """Generate content summary"""
        if not self.use_real_ai:
            # Fallback implementation
            words = content.split()[:50]
            return " ".join(words) + "..." if len(content.split()) > 50 else content
        
        # Use AI client for summary
        prompt = f"Summarize the following content in 2-3 sentences:\n\n{content}"
        response = self.ai_client.generate_text(prompt)
        return response
    
    def extract_takeaways(self, content: str) -> List[str]:
        """Extract key takeaways"""
        if not self.use_real_ai:
            # Fallback implementation - extract first sentence of each paragraph
            paragraphs = content.split('\n\n')
            takeaways = []
            for para in paragraphs[:3]:
                sentences = para.split('.')
                if sentences:
                    takeaways.append(sentences[0].strip() + '.')
            return takeaways
        
        # Use AI client for takeaways
        prompt = f"Extract 3-5 key takeaways from:\n\n{content}"
        response = self.ai_client.generate_text(prompt)
        return [response]
    
    def extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords"""
        if not self.use_real_ai:
            # Fallback implementation - simple word frequency
            words = content.lower().split()
            # Filter common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}
            keywords = [w for w in words if len(w) > 4 and w not in stop_words]
            # Return unique keywords (first 10)
            return list(dict.fromkeys(keywords))[:10]
        
        # Use AI client for keywords
        prompt = f"Extract 5-10 keywords from:\n\n{content}"
        response = self.ai_client.generate_text(prompt)
        return response.split(', ')
    
    def extract_topics(self, content: str) -> List[str]:
        """Identify main topics"""
        if not self.use_real_ai:
            # Fallback implementation
            return ["Technology", "Business", "Innovation"]
        
        # Use AI client for topics
        prompt = f"Identify 3-5 main topics in:\n\n{content}"
        response = self.ai_client.generate_text(prompt)
        return response.split(', ')
    
    def analyze_sentiment(self, content: str) -> Sentiment:
        """Perform sentiment analysis"""
        if not self.use_real_ai:
            # Fallback implementation - simple heuristic
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'positive', 'success']
            negative_words = ['bad', 'terrible', 'awful', 'negative', 'failure', 'poor', 'worst']
            
            content_lower = content.lower()
            pos_count = sum(1 for word in positive_words if word in content_lower)
            neg_count = sum(1 for word in negative_words if word in content_lower)
            
            if pos_count > neg_count:
                classification = "positive"
                confidence = min(0.6 + (pos_count * 0.1), 0.95)
            elif neg_count > pos_count:
                classification = "negative"
                confidence = min(0.6 + (neg_count * 0.1), 0.95)
            else:
                classification = "neutral"
                confidence = 0.75
            
            return Sentiment(
                classification=classification,
                confidence=confidence,
                scores={
                    "positive": pos_count / max(pos_count + neg_count, 1),
                    "neutral": 0.3,
                    "negative": neg_count / max(pos_count + neg_count, 1)
                }
            )
        
        # Use AI client for sentiment
        prompt = f"Analyze sentiment (positive/neutral/negative) of:\n\n{content}"
        response = self.ai_client.generate_text(prompt)
        
        return Sentiment(
            classification=response.get("sentiment", "neutral"),
            confidence=response.get("confidence", 0.8),
            scores=response.get("scores", {})
        )
    
    def _store_analysis(self, analysis: ContentAnalysis):
        """Store analysis results in DuckDB"""
        if not self.db.conn:
            self.db.connect()
        
        import json
        
        self.db.conn.execute("""
            INSERT OR REPLACE INTO content_analysis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            analysis.version_id,
            analysis.summary,
            json.dumps(analysis.takeaways),
            json.dumps(analysis.keywords),
            json.dumps(analysis.topics),
            analysis.sentiment.classification,
            analysis.sentiment.confidence,
            json.dumps(analysis.sentiment.scores),
            analysis.analyzed_at
        ])
