"""
NewsAPI.ai Integration for Enhanced Crypto News Coverage
Provides additional news sources and enhanced article data
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time

logger = logging.getLogger(__name__)

class NewsAPIAI:
    """Integrates with NewsAPI.ai for comprehensive crypto news coverage"""
    
    def __init__(self, api_key: str = "45733984-4543-4869-bc33-590f6ef99bdb"):
        self.base_url = "https://newsapi.ai/api/v1"
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request with error handling"""
        try:
            params['apiKey'] = self.api_key
            response = requests.post(f"{self.base_url}{endpoint}", json=params, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"NewsAPI.ai error: {e}")
            return {'error': str(e), 'articles': {'results': []}}
    
    def get_crypto_articles(self, keywords: List[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Get crypto-related articles with enhanced data"""
        if not keywords:
            keywords = ['bitcoin', 'ethereum', 'cryptocurrency', 'crypto', 'blockchain', 'DeFi']
        
        params = {
            "action": "getArticles",
            "keyword": " OR ".join(keywords),
            "articlesPage": 1,
            "articlesCount": min(limit, 100),
            "articlesSortBy": "date",
            "includeArticleImage": True,
            "includeArticleVideos": True,
            "includeArticleCategories": True,
            "includeArticleLocation": True,
            "includeConceptLabel": True,
            "includeConceptImage": True,
            "includeSourceTitle": True,
            "includeSourceDescription": True,
            "lang": "eng"
        }
        
        return self._make_request("/article/getArticles", params)
    
    def get_trending_crypto_topics(self, limit: int = 20) -> Dict[str, Any]:
        """Get trending crypto topics and concepts"""
        params = {
            "action": "getTrendingConcepts",
            "source": "news",
            "conceptType": "wiki",
            "returnInfo": {
                "conceptInfo": {
                    "type": ["person", "org", "loc"],
                    "label": ["eng"],
                    "synonyms": ["eng"],
                    "image": True,
                    "description": ["eng"]
                }
            },
            "count": limit
        }
        
        return self._make_request("/concept/getTrendingConcepts", params)
    
    def search_by_symbols(self, symbols: List[str], limit: int = 15) -> Dict[str, Any]:
        """Search for articles by specific crypto symbols"""
        if not symbols:
            return {'articles': {'results': []}}
        
        # Create search query for crypto symbols
        symbol_keywords = []
        for symbol in symbols:
            symbol_keywords.extend([
                f'"{symbol}"',
                f'"{symbol}USD"',
                f'"{symbol}/USD"',
                f'"{symbol} price"',
                f'"{symbol} crypto"'
            ])
        
        params = {
            "action": "getArticles",
            "keyword": " OR ".join(symbol_keywords),
            "keywordLoc": "title,body",
            "articlesPage": 1,
            "articlesCount": min(limit, 50),
            "articlesSortBy": "date",
            "includeArticleImage": True,
            "includeArticleCategories": True,
            "includeSourceTitle": True,
            "lang": "eng",
            "dateStart": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "dateEnd": datetime.now().strftime("%Y-%m-%d")
        }
        
        return self._make_request("/article/getArticles", params)
    
    def get_breaking_crypto_news(self, hours: int = 6, limit: int = 20) -> Dict[str, Any]:
        """Get breaking crypto news from recent hours"""
        start_date = datetime.now() - timedelta(hours=hours)
        
        params = {
            "action": "getArticles",
            "keyword": "cryptocurrency OR bitcoin OR ethereum OR crypto OR blockchain OR DeFi",
            "keywordLoc": "title,body",
            "articlesPage": 1,
            "articlesCount": min(limit, 100),
            "articlesSortBy": "date",
            "includeArticleImage": True,
            "includeArticleVideos": True,
            "includeSourceTitle": True,
            "lang": "eng",
            "dateStart": start_date.strftime("%Y-%m-%d"),
            "dateEnd": datetime.now().strftime("%Y-%m-%d")
        }
        
        return self._make_request("/article/getArticles", params)
    
    def get_market_sentiment_articles(self, sentiment_keywords: List[str] = None, limit: int = 25) -> Dict[str, Any]:
        """Get articles for market sentiment analysis"""
        if not sentiment_keywords:
            sentiment_keywords = [
                'bullish', 'bearish', 'rally', 'crash', 'pump', 'dump',
                'adoption', 'regulation', 'institutional', 'ETF', 'futures',
                'breakthrough', 'partnership', 'listing', 'delisting'
            ]
        
        crypto_terms = ['bitcoin', 'ethereum', 'crypto', 'blockchain']
        combined_query = f"({' OR '.join(crypto_terms)}) AND ({' OR '.join(sentiment_keywords)})"
        
        params = {
            "action": "getArticles",
            "keyword": combined_query,
            "keywordLoc": "title,body",
            "articlesPage": 1,
            "articlesCount": min(limit, 100),
            "articlesSortBy": "socialScore",  # Sort by social engagement
            "includeArticleImage": True,
            "includeArticleCategories": True,
            "includeSourceTitle": True,
            "includeSourceDescription": True,
            "lang": "eng",
            "dateStart": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        }
        
        return self._make_request("/article/getArticles", params)
    
    def process_articles_for_discord(self, raw_articles: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process NewsAPI.ai articles for Discord formatting"""
        processed = []
        
        articles = raw_articles.get('articles', {}).get('results', [])
        
        for article in articles:
            try:
                # Extract article data
                title = article.get('title', 'No title')
                url = article.get('url', '')
                image = article.get('image', '')
                body = article.get('body', '')
                source = article.get('source', {}).get('title', 'Unknown')
                pub_date = article.get('dateTime', '')
                
                # Extract concepts for tickers
                concepts = article.get('concepts', [])
                tickers = []
                for concept in concepts:
                    label = concept.get('label', {}).get('eng', '')
                    if any(crypto in label.lower() for crypto in ['bitcoin', 'ethereum', 'btc', 'eth']):
                        tickers.append(label.upper().replace('BITCOIN', 'BTC').replace('ETHEREUM', 'ETH'))
                
                # Determine sentiment based on keywords in title and body
                text_content = f"{title} {body}".lower()
                sentiment = 'Neutral'
                if any(word in text_content for word in ['bullish', 'rally', 'surge', 'breakthrough', 'adoption']):
                    sentiment = 'Positive'
                elif any(word in text_content for word in ['bearish', 'crash', 'dump', 'regulation', 'ban']):
                    sentiment = 'Negative'
                
                processed.append({
                    'title': title,
                    'url': url,
                    'image_url': image,
                    'source_name': source,
                    'published': pub_date,
                    'sentiment': sentiment,
                    'text_preview': body[:300] + '...' if len(body) > 300 else body,
                    'tickers': list(set(tickers))[:5],  # Limit to 5 unique tickers
                    'provider': 'NewsAPI.ai'
                })
                
            except Exception as e:
                logger.error(f"Error processing NewsAPI.ai article: {e}")
                continue
        
        return processed
    
    def get_enhanced_crypto_coverage(self, symbols: List[str] = None, limit: int = 30) -> Dict[str, Any]:
        """Get comprehensive crypto coverage combining multiple search strategies"""
        all_articles = []
        
        try:
            # Get general crypto articles
            general_result = self.get_crypto_articles(limit=limit//2)
            general_articles = self.process_articles_for_discord(general_result)
            all_articles.extend(general_articles)
            
            # Get symbol-specific articles if symbols provided
            if symbols:
                symbol_result = self.search_by_symbols(symbols, limit=limit//2)
                symbol_articles = self.process_articles_for_discord(symbol_result)
                all_articles.extend(symbol_articles)
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_articles = []
            for article in all_articles:
                url = article.get('url', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_articles.append(article)
            
            return {
                'success': True,
                'data': unique_articles[:limit],
                'count': len(unique_articles[:limit]),
                'provider': 'NewsAPI.ai',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced crypto coverage: {e}")
            return {
                'error': str(e),
                'data': [],
                'provider': 'NewsAPI.ai'
            }

def test_newsapi_ai_integration():
    """Test NewsAPI.ai integration"""
    print("Testing NewsAPI.ai integration...")
    
    try:
        newsapi = NewsAPIAI()
        
        # Test crypto articles
        result = newsapi.get_crypto_articles(limit=5)
        articles = newsapi.process_articles_for_discord(result)
        
        print(f"Found {len(articles)} articles from NewsAPI.ai")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title'][:60]}...")
            print(f"   Source: {article['source_name']}")
            print(f"   Image: {'Yes' if article.get('image_url') else 'No'}")
            print(f"   Sentiment: {article['sentiment']}")
            
        return len(articles) > 0
        
    except Exception as e:
        print(f"NewsAPI.ai test error: {e}")
        return False

if __name__ == "__main__":
    test_newsapi_ai_integration()