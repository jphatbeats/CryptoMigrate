#!/usr/bin/env python3
"""
Degen/Meme Coin News Sources Integration
Alternative sources for off-the-cuff and emerging crypto projects
"""

import requests
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DegenNewsAggregator:
    """Aggregates news from multiple degen-friendly sources"""
    
    def __init__(self):
        self.sources = {
            'cryptonews': self._get_cryptonews_degen,
            'coingecko_trending': self._get_coingecko_trending,
            'dexscreener_trending': self._get_dexscreener_trending,
        }
    
    def _get_cryptonews_degen(self, limit=10):
        """Get degen content from CryptoNews with specific search terms"""
        try:
            # Import our existing CryptoNews functions
            import sys
            sys.path.append('.')
            from crypto_news_alerts import get_general_crypto_news
            
            # Search for degen-related content
            degen_keywords = ['meme coin', 'altcoin pump', 'new listing', 'presale', 'launch']
            
            all_articles = []
            for keyword in degen_keywords[:2]:  # Limit to avoid rate limits
                try:
                    result = get_general_crypto_news(items=5, search=keyword)
                    if result and 'data' in result:
                        for article in result['data']:
                            article['source_type'] = 'cryptonews_degen'
                            article['keyword'] = keyword
                            all_articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to get {keyword} news: {e}")
            
            return all_articles[:limit]
            
        except Exception as e:
            logger.error(f"CryptoNews degen search failed: {e}")
            return []
    
    def _get_coingecko_trending(self, limit=10):
        """Get trending coins from CoinGecko API (free tier)"""
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                trending_coins = data.get('coins', [])[:limit]
                
                # Format for consistency
                formatted = []
                for coin in trending_coins:
                    item = coin.get('item', {})
                    formatted.append({
                        'title': f"Trending: {item.get('name', 'Unknown')} ({item.get('symbol', '').upper()})",
                        'tickers': [item.get('symbol', '').upper()],
                        'source_name': 'CoinGecko Trending',
                        'source_type': 'coingecko_trending',
                        'rank': item.get('market_cap_rank', 999),
                        'price_btc': item.get('price_btc', 0),
                        'url': f"https://coingecko.com/en/coins/{item.get('id', '')}"
                    })
                
                return formatted
            else:
                logger.warning(f"CoinGecko trending failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"CoinGecko trending error: {e}")
            return []
    
    def _get_dexscreener_trending(self, limit=10):
        """Get trending tokens from DEXScreener (new/hot tokens)"""
        try:
            # DEXScreener trending endpoint (if available)
            url = "https://api.dexscreener.com/latest/dex/tokens/trending"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; TitanBot/1.0)'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])[:limit]
                
                formatted = []
                for pair in pairs:
                    base_token = pair.get('baseToken', {})
                    formatted.append({
                        'title': f"DEX Trending: {base_token.get('name', 'Unknown')} ({base_token.get('symbol', '').upper()})",
                        'tickers': [base_token.get('symbol', '').upper()],
                        'source_name': 'DEXScreener',
                        'source_type': 'dexscreener_trending',
                        'price_usd': pair.get('priceUsd', 0),
                        'volume_24h': pair.get('volume', {}).get('h24', 0),
                        'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                        'url': pair.get('url', '')
                    })
                
                return formatted
            else:
                logger.warning(f"DEXScreener failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"DEXScreener error: {e}")
            return []
    
    def get_degen_roundup(self, limit_per_source=5):
        """Get comprehensive degen news from all sources"""
        all_degen_news = []
        
        for source_name, source_func in self.sources.items():
            try:
                source_data = source_func(limit_per_source)
                if source_data:
                    logger.info(f"Got {len(source_data)} items from {source_name}")
                    all_degen_news.extend(source_data)
                else:
                    logger.warning(f"No data from {source_name}")
            except Exception as e:
                logger.error(f"Error from {source_name}: {e}")
        
        # Sort by relevance/recency
        all_degen_news.sort(key=lambda x: x.get('rank', 999))
        
        return {
            'data': all_degen_news,
            'total_sources': len(self.sources),
            'total_items': len(all_degen_news),
            'timestamp': datetime.now().isoformat()
        }

# Main functions for easy import
def get_degen_news(limit=15):
    """Get degen/meme coin news from multiple sources"""
    aggregator = DegenNewsAggregator()
    return aggregator.get_degen_roundup(limit_per_source=limit//3)

def get_trending_degen_coins(limit=10):
    """Get specifically trending degen coins"""
    aggregator = DegenNewsAggregator()
    
    # Focus on trending sources
    trending_data = []
    trending_data.extend(aggregator._get_coingecko_trending(limit//2))
    trending_data.extend(aggregator._get_dexscreener_trending(limit//2))
    
    return {
        'data': trending_data[:limit],
        'source': 'degen_trending_aggregator',
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Test the degen news aggregator
    print("🚀 Testing Degen News Aggregator...")
    
    degen_news = get_degen_news(limit=10)
    print(f"Found {len(degen_news['data'])} degen news items")
    
    for item in degen_news['data'][:5]:
        title = item.get('title', 'No title')
        source = item.get('source_name', 'Unknown')
        tickers = item.get('tickers', [])
        print(f"• {title[:60]}... ({source}) {tickers}")