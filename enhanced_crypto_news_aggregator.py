"""
Enhanced Crypto News Aggregator
Combines CryptoNews API and NewsAPI.ai for comprehensive coverage
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

# Import existing integrations
from crypto_news_api import CryptoNewsAPI
from newsapi_ai_integration import NewsAPIAI

logger = logging.getLogger(__name__)

class EnhancedCryptoNewsAggregator:
    """Aggregates crypto news from multiple sources with image support"""
    
    def __init__(self):
        # Initialize both news APIs
        self.cryptonews_api = CryptoNewsAPI()
        self.newsapi_ai = NewsAPIAI()
        
    def merge_and_deduplicate_articles(self, articles_lists: List[List[Dict]], max_articles: int = 20) -> List[Dict]:
        """Merge articles from multiple sources and remove duplicates"""
        all_articles = []
        seen_urls = set()
        seen_titles = set()
        
        # Combine all articles
        for articles in articles_lists:
            for article in articles:
                # Skip if we've seen this URL or very similar title
                url = article.get('url', article.get('news_url', ''))
                title = article.get('title', '').lower().strip()
                
                # Create a simplified title for duplicate detection
                title_key = ''.join(title.split()[:10])  # First 10 words
                
                if url and url not in seen_urls and title_key not in seen_titles:
                    seen_urls.add(url)
                    seen_titles.add(title_key)
                    all_articles.append(article)
        
        # Sort by recency (if published date available) or by provider priority
        def sort_key(article):
            # Priority order: CryptoNews API first, then NewsAPI.ai
            provider_priority = 0 if article.get('provider') != 'NewsAPI.ai' else 1
            
            # Try to parse date for recency
            pub_date = article.get('published', article.get('date', ''))
            try:
                if pub_date:
                    if 'T' in pub_date:
                        date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.strptime(pub_date[:19], '%Y-%m-%d %H:%M:%S')
                    return (provider_priority, -date_obj.timestamp())
            except:
                pass
            
            return (provider_priority, 0)
        
        all_articles.sort(key=sort_key)
        return all_articles[:max_articles]
    
    def get_comprehensive_crypto_news(self, 
                                    tickers: List[str] = None, 
                                    limit: int = 15,
                                    include_images: bool = True) -> Dict[str, Any]:
        """Get comprehensive crypto news from multiple sources"""
        try:
            all_articles_lists = []
            sources_used = []
            
            # Get articles from CryptoNews API
            try:
                if tickers:
                    cryptonews_result = self.cryptonews_api.get_portfolio_news(tickers, limit=limit)
                else:
                    cryptonews_result = self.cryptonews_api.get_breaking_news(limit=limit)
                
                if cryptonews_result and cryptonews_result.get('data'):
                    cryptonews_articles = cryptonews_result['data']
                    # Ensure consistent format
                    for article in cryptonews_articles:
                        article['provider'] = 'CryptoNews'
                    all_articles_lists.append(cryptonews_articles)
                    sources_used.append('CryptoNews API')
                    
            except Exception as e:
                logger.error(f"CryptoNews API error: {e}")
            
            # Get articles from NewsAPI.ai
            try:
                if tickers:
                    newsapi_result = self.newsapi_ai.search_by_symbols(tickers, limit=limit)
                else:
                    newsapi_result = self.newsapi_ai.get_breaking_crypto_news(hours=12, limit=limit)
                
                newsapi_articles = self.newsapi_ai.process_articles_for_discord(newsapi_result)
                if newsapi_articles:
                    all_articles_lists.append(newsapi_articles)
                    sources_used.append('NewsAPI.ai')
                    
            except Exception as e:
                logger.error(f"NewsAPI.ai error: {e}")
            
            # Merge and deduplicate
            merged_articles = self.merge_and_deduplicate_articles(all_articles_lists, limit)
            
            # Filter for images if requested
            if include_images:
                articles_with_images = [
                    article for article in merged_articles 
                    if article.get('image_url') or article.get('image')
                ]
                # If we don't have enough articles with images, include some without
                if len(articles_with_images) < limit // 2:
                    articles_with_images.extend(merged_articles[:limit - len(articles_with_images)])
                merged_articles = articles_with_images
            
            return {
                'success': True,
                'data': merged_articles,
                'count': len(merged_articles),
                'sources_used': sources_used,
                'include_images': include_images,
                'aggregator': 'Enhanced Multi-Source',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Enhanced aggregator error: {e}")
            return {
                'error': str(e),
                'data': [],
                'sources_used': [],
                'aggregator': 'Enhanced Multi-Source'
            }
    
    def get_breaking_news_enhanced(self, limit: int = 10) -> Dict[str, Any]:
        """Get breaking crypto news from all sources"""
        return self.get_comprehensive_crypto_news(
            tickers=None,
            limit=limit,
            include_images=True
        )
    
    def get_portfolio_news_enhanced(self, symbols: List[str], limit: int = 12) -> Dict[str, Any]:
        """Get portfolio-specific news from all sources"""
        return self.get_comprehensive_crypto_news(
            tickers=symbols,
            limit=limit,
            include_images=True
        )
    
    def get_sentiment_analysis_articles(self, limit: int = 25) -> Dict[str, Any]:
        """Get articles optimized for sentiment analysis from both sources"""
        try:
            sentiment_articles = []
            
            # Get sentiment-focused articles from NewsAPI.ai
            try:
                newsapi_sentiment = self.newsapi_ai.get_market_sentiment_articles(limit=limit//2)
                processed_articles = self.newsapi_ai.process_articles_for_discord(newsapi_sentiment)
                sentiment_articles.extend(processed_articles)
            except Exception as e:
                logger.error(f"NewsAPI.ai sentiment error: {e}")
            
            # Get positive sentiment articles from CryptoNews API
            try:
                crypto_positive = self.cryptonews_api.get_breaking_news(limit=limit//2, sentiment='positive')
                if crypto_positive and crypto_positive.get('data'):
                    for article in crypto_positive['data']:
                        article['provider'] = 'CryptoNews'
                    sentiment_articles.extend(crypto_positive['data'])
            except Exception as e:
                logger.error(f"CryptoNews sentiment error: {e}")
            
            # Deduplicate and limit
            merged_articles = self.merge_and_deduplicate_articles([sentiment_articles], limit)
            
            return {
                'success': True,
                'data': merged_articles,
                'count': len(merged_articles),
                'optimization': 'sentiment_analysis',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis aggregation error: {e}")
            return {'error': str(e), 'data': []}

def format_aggregated_news_for_discord(articles: List[Dict], title: str = "📰 ENHANCED CRYPTO NEWS") -> str:
    """Format aggregated news for Discord with multi-source indicators"""
    if not articles:
        return f"{title}\n\nNo articles available."
    
    message = f"{title} 📰\n\n"
    
    for i, article in enumerate(articles[:5], 1):  # Limit to 5 for Discord
        # Get article data with fallback fields
        title_text = article.get('title', 'No title')
        url = article.get('url', article.get('news_url', ''))
        source = article.get('source_name', article.get('source', 'Unknown'))
        provider = article.get('provider', 'Unknown')
        image_url = article.get('image_url', article.get('image', ''))
        sentiment = article.get('sentiment', 'Neutral')
        
        # Sentiment emoji
        sentiment_emoji = "📈" if sentiment == "Positive" else "📉" if sentiment == "Negative" else "📊"
        
        # Provider indicator
        provider_emoji = "🔥" if provider == "CryptoNews" else "🌐" if provider == "NewsAPI.ai" else "📡"
        
        if url:
            message += f"{sentiment_emoji} **[{title_text}]({url})**\n"
        else:
            message += f"{sentiment_emoji} **{title_text}**\n"
        
        # Add image if available
        if image_url:
            message += f"{image_url}\n"
        
        # Add source and provider info
        message += f"{provider_emoji} {source} | {sentiment_emoji} {sentiment}\n\n"
    
    message += f"📊 Enhanced aggregation from multiple premium sources"
    return message

def test_enhanced_aggregator():
    """Test the enhanced crypto news aggregator"""
    print("🧪 Testing Enhanced Crypto News Aggregator...")
    
    try:
        aggregator = EnhancedCryptoNewsAggregator()
        
        # Test comprehensive news
        result = aggregator.get_comprehensive_crypto_news(
            tickers=['BTC', 'ETH'], 
            limit=10,
            include_images=True
        )
        
        if result.get('success'):
            articles = result['data']
            print(f"✅ Found {len(articles)} articles from sources: {', '.join(result['sources_used'])}")
            
            for i, article in enumerate(articles[:3], 1):
                print(f"\n📰 Article {i}:")
                print(f"   Title: {article.get('title', 'No title')[:60]}...")
                print(f"   Source: {article.get('source_name', article.get('source', 'Unknown'))}")
                print(f"   Provider: {article.get('provider', 'Unknown')}")
                print(f"   Image: {'✅' if article.get('image_url', article.get('image')) else '❌'}")
                print(f"   Sentiment: {article.get('sentiment', 'Unknown')}")
            
            # Test Discord formatting
            discord_message = format_aggregated_news_for_discord(articles[:3])
            print(f"\n💬 Discord Preview:")
            print("=" * 60)
            print(discord_message)
            print("=" * 60)
            
            return True
        else:
            print(f"❌ Aggregator test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_aggregator()