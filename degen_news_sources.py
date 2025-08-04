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
        """Get trending tokens directly from DEXScreener API (aligned with docs)"""
        try:
            # Use DEXScreener API directly (aligned with official docs)
            base_url = "https://api.dexscreener.com"
            
            # Try latest boosted tokens first (most likely to be trending/degen)
            boosted_url = f"{base_url}/token-boosts/latest/v1"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; TitanBot/1.0)'}
            response = requests.get(boosted_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # DEXScreener returns array of boost objects per API docs
                tokens = data if isinstance(data, list) else []
                
                formatted = []
                for token in tokens[:limit]:
                    # Extract token info from boost data (per OpenAPI spec)
                    chain_id = token.get('chainId', 'unknown')
                    token_address = token.get('tokenAddress', '')
                    amount = token.get('amount', 0)
                    total_amount = token.get('totalAmount', 0)
                    description = token.get('description', '')
                    url = token.get('url', f"https://dexscreener.com/{chain_id}/{token_address}")
                    
                    # Extract symbol/name from description or use token address
                    symbol = token_address[:8].upper() if token_address else 'UNKNOWN'
                    if description:
                        # Try to extract symbol from description
                        import re
                        symbol_match = re.search(r'\b([A-Z]{2,10})\b', description)
                        if symbol_match:
                            symbol = symbol_match.group(1)
                    
                    formatted.append({
                        'title': f"DEX Boosted: {symbol} (${amount:.0f} boost)",
                        'tickers': [symbol] if symbol != 'UNKNOWN' else [],
                        'source_name': 'DEXScreener Boosted',
                        'source_type': 'dexscreener_boosted',
                        'boost_amount': amount,
                        'total_boost': total_amount,
                        'chain': chain_id,
                        'token_address': token_address,
                        'description': description,
                        'url': url
                    })
                
                return formatted
            else:
                logger.warning(f"DEXScreener boosted failed: {response.status_code}")
                
                # Fallback to top boosted tokens
                top_url = f"{base_url}/token-boosts/top/v1" 
                response = requests.get(top_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    tokens = data if isinstance(data, list) else []
                    
                    formatted = []
                    for token in tokens[:limit]:
                        chain_id = token.get('chainId', 'unknown')
                        token_address = token.get('tokenAddress', '')
                        amount = token.get('amount', 0)
                        description = token.get('description', '')
                        url = token.get('url', f"https://dexscreener.com/{chain_id}/{token_address}")
                        
                        symbol = token_address[:8].upper() if token_address else 'UNKNOWN'
                        if description:
                            import re
                            symbol_match = re.search(r'\b([A-Z]{2,10})\b', description)
                            if symbol_match:
                                symbol = symbol_match.group(1)
                        
                        formatted.append({
                            'title': f"DEX Top Boosted: {symbol} (${amount:.0f})",
                            'tickers': [symbol] if symbol != 'UNKNOWN' else [],
                            'source_name': 'DEXScreener Top',
                            'source_type': 'dexscreener_top_boosted',
                            'boost_amount': amount,
                            'chain': chain_id,
                            'url': url
                        })
                    
                    return formatted
                
                return []
                
        except Exception as e:
            logger.error(f"DEXScreener API error: {e}")
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