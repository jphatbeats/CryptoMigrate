#!/usr/bin/env python3
"""
CoinCap MCP Integration for THE ALPHA PLAYBOOK v4
Replaces expensive CoinMarketCap Pro API with FREE CoinCap data

Features:
- FREE crypto market data (no API keys required)
- Real-time prices, market cap, volume
- Top performers identification
- Direct replacement for CoinMarketCap endpoints
"""

import json
import requests
import logging
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class CoinCapMCPClient:
    """FREE CoinCap alternative - Using CoinGecko FREE API (no API keys required!)"""
    
    def __init__(self):
        # Using CoinGecko FREE API instead (much more reliable)
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'THE-ALPHA-PLAYBOOK-v4/1.0',
            'Accept': 'application/json'
        })
        
    async def start_mcp_server(self) -> bool:
        """Initialize CoinCap API client"""
        try:
            # Test the API connection using CoinGecko FREE API
            logger.info("🚀 Testing CoinGecko FREE API connection...")
            response = self.session.get(f"{self.base_url}/ping", timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ CoinGecko FREE API connection successful!")
                return True
            else:
                logger.error(f"❌ CoinGecko API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing CoinGecko API: {e}")
            return False
    
    def get_crypto_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get crypto price data using FREE CoinGecko API - replacement for CMC Pro endpoint"""
        try:
            # Get simple price data using CoinGecko
            coin_id = self._symbol_to_coingecko_id(symbol)
            if not coin_id:
                return None
                
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if coin_id in data:
                    coin_data = data[coin_id]
                    return {
                        'symbol': symbol.upper(),
                        'coin_id': coin_id,
                        'price_usd': float(coin_data.get('usd', 0)),
                        'market_cap_usd': float(coin_data.get('usd_market_cap', 0)),
                        'volume_24h_usd': float(coin_data.get('usd_24h_vol', 0)),
                        'change_percent_24h': float(coin_data.get('usd_24h_change', 0)),
                        'timestamp': datetime.utcnow().isoformat(),
                        'source': 'coingecko_free_api'
                    }
                else:
                    logger.warning(f"Coin ID {coin_id} not found in CoinGecko response")
                    return None
            else:
                logger.error(f"CoinGecko API error for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting {symbol} price from CoinGecko API: {e}")
            return None
    
    def _symbol_to_coingecko_id(self, symbol: str) -> Optional[str]:
        """Convert crypto symbol to CoinGecko coin ID"""
        # Common mappings for major cryptos
        symbol_map = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum', 
            'BNB': 'binancecoin',
            'XRP': 'ripple',
            'ADA': 'cardano',
            'SOL': 'solana',
            'DOGE': 'dogecoin',
            'DOT': 'polkadot',
            'MATIC': 'polygon',
            'AVAX': 'avalanche-2',
            'UNI': 'uniswap',
            'LINK': 'chainlink',
            'ALGO': 'algorand',
            'VET': 'vechain',
            'ICP': 'internet-computer',
            'FIL': 'filecoin',
            'TRX': 'tron',
            'ETC': 'ethereum-classic',
            'XLM': 'stellar',
            'BCH': 'bitcoin-cash'
        }
        
        return symbol_map.get(symbol.upper())
    
    def get_top_cryptocurrencies(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get top cryptocurrencies by market cap using FREE CoinGecko API - replacement for CMC listings endpoint"""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': min(limit, 250),  # CoinGecko max per page
                'page': 1,
                'sparkline': 'false'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                assets = response.json()
                
                formatted_assets = []
                for i, asset in enumerate(assets, 1):
                    try:
                        formatted_assets.append({
                            'symbol': asset.get('symbol', '').upper(),
                            'name': asset.get('name', ''),
                            'price_usd': float(asset.get('current_price', 0)),
                            'market_cap_usd': float(asset.get('market_cap', 0)),
                            'volume_24h_usd': float(asset.get('total_volume', 0)),
                            'change_percent_24h': float(asset.get('price_change_percentage_24h', 0)),
                            'rank': i,  # Use array position as rank
                            'coin_id': asset.get('id', ''),
                            'source': 'coingecko_free_api'
                        })
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error formatting asset {asset.get('symbol', 'UNKNOWN')}: {e}")
                        continue
                
                logger.info(f"✅ Retrieved {len(formatted_assets)} assets from CoinGecko FREE API")
                return formatted_assets
            else:
                logger.error(f"CoinGecko API list error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting top cryptos from CoinGecko API: {e}")
            return []
    
    def get_bitcoin_price(self) -> Optional[float]:
        """Get Bitcoin price specifically using FREE CoinGecko API"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get('bitcoin', {}).get('usd', 0))
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting Bitcoin price from CoinGecko API: {e}")
            return None

# Global instance for use across the system
coincap_client = CoinCapMCPClient()

async def initialize_coincap_mcp():
    """Initialize CoinCap FREE API integration"""
    logger.info("🚀 Initializing CoinCap FREE API integration...")
    success = await coincap_client.start_mcp_server()
    if success:
        logger.info("✅ CoinCap FREE API integration ready - NO API KEYS REQUIRED!")
        logger.info("💰 SAVING $300/month vs CoinMarketCap Pro!")
        return True
    else:
        logger.error("❌ Failed to initialize CoinCap FREE API integration")
        return False

# Convenience functions for easy integration
def get_market_data(symbol: str) -> Optional[Dict[str, Any]]:
    """Get market data for a cryptocurrency symbol"""
    return coincap_client.get_crypto_price(symbol)

def get_top_performers(limit: int = 50) -> List[Dict[str, Any]]:
    """Get top performing cryptocurrencies"""
    return coincap_client.get_top_cryptocurrencies(limit)

def get_btc_price() -> Optional[float]:
    """Get current Bitcoin price"""
    return coincap_client.get_bitcoin_price()

if __name__ == "__main__":
    # Test the integration
    async def test():
        await initialize_coincap_mcp()
        
        # Test Bitcoin price
        btc_price = get_btc_price()
        print(f"Bitcoin Price: ${btc_price}")
        
        # Test individual crypto
        eth_data = get_market_data('ETH')
        print(f"ETH Data: {eth_data}")
        
        # Test top cryptos
        top_10 = get_top_performers(10)
        print(f"Top 10 cryptos: {len(top_10)} retrieved")
        
    asyncio.run(test())