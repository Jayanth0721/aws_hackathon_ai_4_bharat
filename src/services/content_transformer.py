"""Content transformation service for multi-platform optimization"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from src.utils.logging import logger
from src.config import config

# Import AI client
from src.services.gemini_client import gemini_client


@dataclass
class PlatformContent:
    """Transformed content for a specific platform"""
    platform: str
    content: str
    character_count: int
    within_limit: bool
    hashtags: List[str]
    metadata: Dict


class ContentTransformer:
    """Service for transforming content across multiple platforms"""
    
    # Platform character limits
    PLATFORM_LIMITS = {
        'linkedin': 3000,
        'twitter': 280,
        'instagram': 2200,
        'facebook': 63206,
        'threads': 500
    }
    
    def __init__(self):
        # Use Gemini as the only AI provider
        if config.USE_GEMINI and gemini_client.is_available():
            self.ai_client = gemini_client
            self.use_real_ai = True
            self.ai_provider = 'Gemini'
            logger.info("ContentTransformer initialized with Google Gemini")
        else:
            self.ai_client = None
            self.use_real_ai = False
            self.ai_provider = 'Manual'
            logger.warning("ContentTransformer initialized without AI - configure Gemini API key")
        
        self.tone_styles = {
            'professional': {
                'prefix': '',
                'style': 'formal and business-oriented',
                'emoji_level': 'minimal'
            },
            'casual': {
                'prefix': '',
                'style': 'friendly and conversational',
                'emoji_level': 'moderate'
            },
            'storytelling': {
                'prefix': '',
                'style': 'narrative and engaging',
                'emoji_level': 'high'
            }
        }
    
    def transform_for_platforms(
        self,
        content: str,
        platforms: List[str],
        tone: str = 'professional',
        include_hashtags: bool = True
    ) -> Dict[str, PlatformContent]:
        """
        Transform content for multiple platforms
        
        Args:
            content: Original content to transform
            platforms: List of target platforms
            tone: Desired tone (professional, casual, storytelling)
            include_hashtags: Whether to include hashtags
            
        Returns:
            Dictionary mapping platform names to transformed content
        """
        results = {}
        
        for platform in platforms:
            try:
                transformed = self._transform_for_platform(
                    content, platform, tone, include_hashtags
                )
                results[platform] = transformed
            except Exception as e:
                logger.error(f"Error transforming for {platform}: {e}")
                results[platform] = None
        
        return results
    
    def _transform_for_platform(
        self,
        content: str,
        platform: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for a specific platform"""
        
        platform_lower = platform.lower()
        
        # Use real AI if available
        if self.use_real_ai:
            try:
                ai_result = self.ai_client.transform_content(
                    content=content,
                    target_platform=platform_lower,
                    tone=tone,
                    include_hashtags=include_hashtags
                )
                
                # Extract data from AI response
                transformed_content = ai_result.get('content', content)
                char_count = ai_result.get('character_count', len(transformed_content))
                within_limit = ai_result.get('within_limit', True)
                hashtags = ai_result.get('hashtags', [])
                
                return PlatformContent(
                    platform=platform,
                    content=transformed_content,
                    character_count=char_count,
                    within_limit=within_limit,
                    hashtags=hashtags,
                    metadata={
                        'tone': tone,
                        'ai_generated': True,
                        'provider': self.ai_provider
                    }
                )
            except Exception as e:
                logger.error(f"AI transformation failed for {platform}, falling back to manual: {e}")
                # Fall through to manual transformation
        
        # Manual transformation (fallback or when AI not available)
        if platform_lower == 'linkedin':
            return self._transform_linkedin(content, tone, include_hashtags)
        elif platform_lower == 'twitter':
            return self._transform_twitter(content, tone, include_hashtags)
        elif platform_lower == 'instagram':
            return self._transform_instagram(content, tone, include_hashtags)
        elif platform_lower == 'facebook':
            return self._transform_facebook(content, tone, include_hashtags)
        elif platform_lower == 'threads':
            return self._transform_threads(content, tone, include_hashtags)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
    
    def _transform_linkedin(
        self,
        content: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for LinkedIn"""
        
        # Mock transformation - in production, use AI model
        transformed = self._apply_tone(content, tone)
        
        # Add professional formatting
        if len(transformed) > 500:
            # Add line breaks for readability
            paragraphs = transformed.split('\n\n')
            transformed = '\n\n'.join(paragraphs[:3])
        
        # Generate hashtags
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, platform='linkedin', count=5)
            transformed += '\n\n' + ' '.join([f'#{tag}' for tag in hashtags])
        
        char_count = len(transformed)
        within_limit = char_count <= self.PLATFORM_LIMITS['linkedin']
        
        return PlatformContent(
            platform='LinkedIn',
            content=transformed,
            character_count=char_count,
            within_limit=within_limit,
            hashtags=hashtags,
            metadata={
                'tone': tone,
                'limit': self.PLATFORM_LIMITS['linkedin'],
                'format': 'single_post'
            }
        )
    
    def _transform_twitter(
        self,
        content: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for Twitter/X (thread format)"""
        
        # Mock transformation - create thread
        transformed = self._apply_tone(content, tone)
        
        # Split into tweets
        tweets = self._split_into_tweets(transformed, include_hashtags)
        
        # Format as thread
        thread_content = '\n\n---\n\n'.join([
            f"Tweet {i+1}/{len(tweets)}:\n{tweet}"
            for i, tweet in enumerate(tweets)
        ])
        
        # Generate hashtags
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, platform='twitter', count=3)
        
        total_chars = sum(len(tweet) for tweet in tweets)
        
        return PlatformContent(
            platform='Twitter/X',
            content=thread_content,
            character_count=total_chars,
            within_limit=True,  # Already split into valid tweets
            hashtags=hashtags,
            metadata={
                'tone': tone,
                'limit': self.PLATFORM_LIMITS['twitter'],
                'format': 'thread',
                'tweet_count': len(tweets)
            }
        )
    
    def _transform_instagram(
        self,
        content: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for Instagram"""
        
        # Mock transformation
        transformed = self._apply_tone(content, tone)
        
        # Add visual-friendly formatting
        if tone == 'casual' or tone == 'storytelling':
            transformed = self._add_emojis(transformed)
        
        # Generate hashtags (Instagram loves hashtags!)
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, platform='instagram', count=15)
            transformed += '\n\n' + ' '.join([f'#{tag}' for tag in hashtags])
        
        char_count = len(transformed)
        within_limit = char_count <= self.PLATFORM_LIMITS['instagram']
        
        return PlatformContent(
            platform='Instagram',
            content=transformed,
            character_count=char_count,
            within_limit=within_limit,
            hashtags=hashtags,
            metadata={
                'tone': tone,
                'limit': self.PLATFORM_LIMITS['instagram'],
                'format': 'caption',
                'hashtag_count': len(hashtags)
            }
        )
    
    def _transform_facebook(
        self,
        content: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for Facebook"""
        
        # Mock transformation
        transformed = self._apply_tone(content, tone)
        
        # Facebook allows longer content
        # Add engaging opening
        if tone == 'storytelling':
            transformed = "Here's something interesting...\n\n" + transformed
        
        # Generate hashtags (fewer for Facebook)
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, platform='facebook', count=5)
            transformed += '\n\n' + ' '.join([f'#{tag}' for tag in hashtags])
        
        char_count = len(transformed)
        within_limit = char_count <= self.PLATFORM_LIMITS['facebook']
        
        return PlatformContent(
            platform='Facebook',
            content=transformed,
            character_count=char_count,
            within_limit=within_limit,
            hashtags=hashtags,
            metadata={
                'tone': tone,
                'limit': self.PLATFORM_LIMITS['facebook'],
                'format': 'post'
            }
        )
    
    def _transform_threads(
        self,
        content: str,
        tone: str,
        include_hashtags: bool
    ) -> PlatformContent:
        """Transform content for Threads"""
        
        # Mock transformation
        transformed = self._apply_tone(content, tone)
        
        # Threads is more casual
        if tone == 'professional':
            transformed = self._make_more_casual(transformed)
        
        # Truncate if needed
        if len(transformed) > self.PLATFORM_LIMITS['threads']:
            transformed = transformed[:self.PLATFORM_LIMITS['threads']-3] + '...'
        
        # Generate hashtags (minimal for Threads)
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, platform='threads', count=3)
            if len(transformed) + len(' '.join([f'#{tag}' for tag in hashtags])) <= self.PLATFORM_LIMITS['threads']:
                transformed += '\n\n' + ' '.join([f'#{tag}' for tag in hashtags])
        
        char_count = len(transformed)
        within_limit = char_count <= self.PLATFORM_LIMITS['threads']
        
        return PlatformContent(
            platform='Threads',
            content=transformed,
            character_count=char_count,
            within_limit=within_limit,
            hashtags=hashtags,
            metadata={
                'tone': tone,
                'limit': self.PLATFORM_LIMITS['threads'],
                'format': 'post'
            }
        )
    
    def _apply_tone(self, content: str, tone: str) -> str:
        """Apply tone transformation to content"""
        # Mock implementation - in production, use AI model
        
        if tone == 'professional':
            # Keep formal, remove casual language
            return content
        elif tone == 'casual':
            # Make more conversational
            casual_content = content.replace('Furthermore,', 'Also,')
            casual_content = casual_content.replace('Therefore,', 'So,')
            casual_content = casual_content.replace('In conclusion,', 'To wrap up,')
            return casual_content
        elif tone == 'storytelling':
            # Add narrative elements
            return f"Let me share something with you...\n\n{content}\n\nWhat do you think?"
        
        return content
    
    def _split_into_tweets(self, content: str, include_hashtags: bool) -> List[str]:
        """Split content into tweet-sized chunks"""
        max_length = self.PLATFORM_LIMITS['twitter'] - 20  # Reserve space for hashtags
        
        # Simple splitting by sentences
        sentences = content.replace('\n', ' ').split('. ')
        tweets = []
        current_tweet = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Add period back if not present
            if not sentence.endswith('.'):
                sentence += '.'
            
            if len(current_tweet) + len(sentence) + 1 <= max_length:
                current_tweet += (' ' if current_tweet else '') + sentence
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = sentence
        
        if current_tweet:
            tweets.append(current_tweet.strip())
        
        # Ensure at least one tweet
        if not tweets:
            tweets = [content[:max_length]]
        
        return tweets
    
    def _generate_hashtags(self, content: str, platform: str, count: int) -> List[str]:
        """Generate relevant hashtags for content"""
        # Mock implementation - in production, use AI model
        
        # Extract potential keywords
        words = content.lower().split()
        
        # Common hashtags by platform
        platform_hashtags = {
            'linkedin': ['Leadership', 'Innovation', 'Business', 'Technology', 'Growth'],
            'twitter': ['Tech', 'AI', 'Innovation', 'News', 'Trending'],
            'instagram': ['InstaGood', 'PhotoOfTheDay', 'Inspiration', 'Motivation', 'Life'],
            'facebook': ['Community', 'Family', 'Friends', 'Life', 'Love'],
            'threads': ['Thoughts', 'Discussion', 'Community', 'Share', 'Connect']
        }
        
        # Get platform-specific hashtags
        base_hashtags = platform_hashtags.get(platform, ['Content', 'Social', 'Share'])
        
        # Add content-specific hashtags
        content_keywords = []
        if 'ai' in words or 'artificial' in words:
            content_keywords.extend(['AI', 'ArtificialIntelligence', 'MachineLearning'])
        if 'content' in words:
            content_keywords.extend(['ContentCreation', 'ContentMarketing'])
        if 'business' in words:
            content_keywords.extend(['Business', 'Entrepreneurship'])
        if 'technology' in words or 'tech' in words:
            content_keywords.extend(['Technology', 'TechNews'])
        
        # Combine and limit
        all_hashtags = content_keywords + base_hashtags
        return all_hashtags[:count]
    
    def _add_emojis(self, content: str) -> str:
        """Add relevant emojis to content"""
        # Simple emoji addition for visual appeal
        emoji_map = {
            'ai': '🤖',
            'technology': '💻',
            'innovation': '💡',
            'success': '🎉',
            'growth': '📈',
            'learning': '📚',
            'idea': '💭',
            'important': '⚡',
            'new': '✨'
        }
        
        words = content.lower().split()
        for word, emoji in emoji_map.items():
            if word in words:
                content = content.replace(word, f"{word} {emoji}", 1)
                break  # Add only one emoji
        
        return content
    
    def _make_more_casual(self, content: str) -> str:
        """Make content more casual"""
        casual = content.replace('Furthermore,', 'Plus,')
        casual = casual.replace('Therefore,', 'So,')
        casual = casual.replace('However,', 'But,')
        casual = casual.replace('In addition,', 'Also,')
        return casual


# Global instance
content_transformer = ContentTransformer()
