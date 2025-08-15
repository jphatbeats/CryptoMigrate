"""
LunarCrush Social Intelligence MCP Integration
Provides Galaxy Score, social volume, and sentiment analysis for cryptocurrency trading
"""
import os
import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LunarCrushMCP:
    def __init__(self):
        self.api_key = os.environ.get('LUNARCRUSH_API_KEY')
        self.base_url = "https://lunarcrush.com/api4"
        self.session = None
        
        if not self.api_key:
            logger.warning("LunarCrush API key not found in environment variables")
            
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_coin_social_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive social data for a specific coin
        Returns Galaxy Score, social volume, sentiment metrics
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        try:
            # Convert symbol to LunarCrush coin ID format
            coin_id = self._symbol_to_coin_id(symbol)
            
            url = f"{self.base_url}/public/coins/{coin_id}"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'time_series_indicators': 'galaxy_score,social_volume,price_score,volatility',
                'interval': 'day',
                'time_series_limit': 7
            }
            
            async with self.session.get(url, headers=headers, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_coin_data(data, symbol)
                elif response.status == 402:
                    logger.warning(f"LunarCrush subscription level insufficient for {symbol}")
                    return self._fallback_social_data(symbol)
                else:
                    logger.error(f"LunarCrush API error {response.status} for {symbol}")
                    return self._fallback_social_data(symbol)
                    
        except asyncio.TimeoutError:
            logger.warning(f"LunarCrush timeout for {symbol}")
            return self._fallback_social_data(symbol)
        except Exception as e:
            logger.error(f"LunarCrush error for {symbol}: {e}")
            return self._fallback_social_data(symbol)
    
    async def get_trending_coins(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get trending coins by social activity"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        try:
            url = f"{self.base_url}/public/coins"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'sort': 'galaxy_score',
                'limit': limit,
                'time_series_indicators': 'galaxy_score,social_volume,price_score'
            }
            
            async with self.session.get(url, headers=headers, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_trending_data(data)
                else:
                    logger.error(f"LunarCrush trending API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"LunarCrush trending error: {e}")
            return []
    
    async def get_social_momentum(self, symbol: str) -> Dict[str, Any]:
        """Get social momentum score and analysis"""
        social_data = await self.get_coin_social_data(symbol)
        
        if not social_data or social_data.get('galaxy_score', 0) == 0:
            return {
                'social_momentum': 0.0,
                'sentiment_score': 0.5,  # Neutral
                'viral_potential': False,
                'social_score': 0,
                'status': 'limited_data'
            }
        
        # Calculate momentum based on Galaxy Score and social volume
        galaxy_score = social_data.get('galaxy_score', 0)
        social_volume = social_data.get('social_volume', 0)
        price_score = social_data.get('price_score', 50)
        
        # Normalize momentum (0-1 scale)
        momentum = min(galaxy_score / 100.0, 1.0)
        
        # Sentiment from price score (above 50 = positive, below = negative)
        sentiment = max(0.1, min(0.9, price_score / 100.0))
        
        # Viral potential based on high galaxy score + social volume
        viral_potential = galaxy_score > 70 and social_volume > 100
        
        # Calculate final social score (0-20 points for scanner)
        social_score = int((momentum * 0.6 + sentiment * 0.4) * 20)
        
        return {
            'social_momentum': round(momentum, 3),
            'sentiment_score': round(sentiment, 3),
            'viral_potential': viral_potential,
            'social_score': social_score,
            'galaxy_score': galaxy_score,
            'social_volume': social_volume,
            'price_score': price_score,
            'status': 'success'
        }
    
    def _symbol_to_coin_id(self, symbol: str) -> str:
        """Convert trading symbol to LunarCrush coin ID"""
        # Updated symbol mappings based on LunarCrush API structure
        symbol_map = {
            'BTC': 'btc',
            'ETH': 'eth', 
            'XRP': 'xrp',
            'ADA': 'ada',
            'SOL': 'sol',
            'MATIC': 'matic',
            'DOT': 'dot',
            'AVAX': 'avax',
            'LINK': 'link',
            'UNI': 'uni',
            'LTC': 'ltc',
            'BCH': 'bch',
            'ALGO': 'algo',
            'VET': 'vet',
            'ICP': 'icp',
            'FIL': 'fil',
            'TRX': 'trx',
            'ETC': 'etc',
            'XLM': 'xlm',
            'ATOM': 'atom',
            'HBAR': 'hbar',
            'NEAR': 'near',
            'MANA': 'mana',
            'SAND': 'sand',
            'AXS': 'axs',
            'CRV': 'crv',
            'MKR': 'mkr',
            'AAVE': 'aave',
            'COMP': 'comp',
            'YFI': 'yfi',
            'DOGE': 'doge',
            'SHIB': 'shib',
            'XMR': 'xmr',
            'APT': 'apt',
            'OP': 'op',
            'ARB': 'arb',
            'LIDO': 'ldo',
            'QNT': 'qnt'
        }
        
        # Try the mapping first, then fall back to lowercase symbol
        return symbol_map.get(symbol.upper(), symbol.lower())
    
    def _parse_coin_data(self, data: Dict, symbol: str) -> Dict[str, Any]:
        """Parse LunarCrush API response for coin data"""
        try:
            if 'data' in data and data['data']:
                coin_data = data['data'][0] if isinstance(data['data'], list) else data['data']
                
                return {
                    'symbol': symbol,
                    'galaxy_score': coin_data.get('galaxy_score', 0),
                    'social_volume': coin_data.get('social_volume', 0),
                    'price_score': coin_data.get('price_score', 50),
                    'volatility': coin_data.get('volatility', 0),
                    'social_dominance': coin_data.get('social_dominance', 0),
                    'market_dominance': coin_data.get('market_dominance', 0),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error parsing LunarCrush data for {symbol}: {e}")
            
        return self._fallback_social_data(symbol)
    
    def _parse_trending_data(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse trending coins data"""
        try:
            if 'data' in data and data['data']:
                trending = []
                for coin in data['data']:
                    trending.append({
                        'symbol': coin.get('symbol', ''),
                        'name': coin.get('name', ''),
                        'galaxy_score': coin.get('galaxy_score', 0),
                        'social_volume': coin.get('social_volume', 0),
                        'price_score': coin.get('price_score', 50),
                        'rank': coin.get('rank', 0)
                    })
                return trending
        except Exception as e:
            logger.error(f"Error parsing trending data: {e}")
            
        return []
    
    def _fallback_social_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback social data when API fails"""
        return {
            'symbol': symbol,
            'galaxy_score': 0,
            'social_volume': 0,
            'price_score': 50,
            'volatility': 0,
            'social_dominance': 0,
            'market_dominance': 0,
            'timestamp': datetime.now().isoformat(),
            'status': 'fallback'
        }

# Global instance
lunarcrush_mcp = LunarCrushMCP()

async def get_social_analysis(symbol: str) -> Dict[str, Any]:
    """Main function for social analysis integration"""
    async with lunarcrush_mcp:
        return await lunarcrush_mcp.get_social_momentum(symbol)

async def get_trending_social() -> List[Dict[str, Any]]:
    """Get trending coins by social activity"""
    async with lunarcrush_mcp:
        return await lunarcrush_mcp.get_trending_coins(50)