#!/usr/bin/env python3
"""
LunarCrush Official HTTP MCP Integration
Direct integration with https://lunarcrush.ai/mcp for real Galaxy Scores and social data
"""

import asyncio
import aiohttp
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LunarCrushHTTPClient:
    """Official LunarCrush HTTP MCP client for real social data"""
    
    def __init__(self):
        self.base_url = "https://lunarcrush.ai/mcp"
        self.api_key = os.getenv('LUNARCRUSH_API_KEY')
        self.session = None
        
        if not self.api_key:
            logger.warning("⚠️ LUNARCRUSH_API_KEY not found in environment")
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'TitanTrading/1.0'
            }
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def get_galaxy_score(self, symbol: str) -> Dict[str, Any]:
        """Get Galaxy Score and social metrics for a cryptocurrency"""
        try:
            if not self.api_key:
                return self._fallback_response(symbol, "API key not configured")
            
            session = await self._get_session()
            url = f"{self.base_url}?key={self.api_key}"
            
            # Prepare MCP tool call for galaxy score
            mcp_request = {
                "jsonrpc": "2.0",
                "id": f"galaxy-{symbol}-{datetime.now().timestamp()}",
                "method": "call_tool",
                "params": {
                    "name": "get_galaxy_score",
                    "arguments": {
                        "symbol": symbol.upper()
                    }
                }
            }
            
            async with session.post(url, json=mcp_request) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_galaxy_response(symbol, data)
                else:
                    logger.error(f"LunarCrush HTTP error {response.status} for {symbol}")
                    return self._fallback_response(symbol, f"HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"LunarCrush client error for {symbol}: {str(e)}")
            # Close and recreate session if there's an event loop error
            if "Event loop is closed" in str(e):
                try:
                    if self.session and not self.session.closed:
                        await self.session.close()
                    self.session = None
                except:
                    pass
            return self._fallback_response(symbol, str(e))
    
    async def get_social_metrics(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive social metrics"""
        try:
            if not self.api_key:
                return self._fallback_response(symbol, "API key not configured")
            
            session = await self._get_session()
            url = f"{self.base_url}?key={self.api_key}"
            
            # Prepare MCP tool call for social metrics
            mcp_request = {
                "jsonrpc": "2.0",
                "id": f"social-{symbol}-{datetime.now().timestamp()}",
                "method": "call_tool",
                "params": {
                    "name": "get_social_data",
                    "arguments": {
                        "symbol": symbol.upper(),
                        "timeframe": "24h"
                    }
                }
            }
            
            async with session.post(url, json=mcp_request) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_social_response(symbol, data)
                else:
                    logger.error(f"LunarCrush social HTTP error {response.status} for {symbol}")
                    return self._fallback_response(symbol, f"HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"LunarCrush social client error for {symbol}: {str(e)}")
            # Close and recreate session if there's an event loop error
            if "Event loop is closed" in str(e):
                try:
                    if self.session and not self.session.closed:
                        await self.session.close()
                    self.session = None
                except:
                    pass
            return self._fallback_response(symbol, str(e))
    
    def _parse_galaxy_response(self, symbol: str, data: Dict) -> Dict[str, Any]:
        """Parse LunarCrush galaxy score response"""
        try:
            if 'result' in data and 'content' in data['result']:
                content = data['result']['content']
                
                # Extract galaxy score and metrics
                galaxy_score = content.get('galaxy_score', 0)
                social_volume = content.get('social_volume', 0)
                sentiment = content.get('sentiment', 50) / 100.0  # Convert to 0-1
                
                return {
                    'success': True,
                    'symbol': symbol,
                    'galaxy_score': galaxy_score,
                    'social_volume': social_volume,
                    'sentiment_score': sentiment,
                    'social_momentum': min(galaxy_score / 10.0, 10.0),  # Scale to 0-10
                    'viral_potential': galaxy_score > 70,
                    'social_score': min(int(galaxy_score * 0.3), 30),  # Scale to 30 points max
                    'price_score': content.get('price_score', 50),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'LunarCrush Official MCP',
                    'status': 'live_data'
                }
            else:
                return self._fallback_response(symbol, "Invalid response format")
                
        except Exception as e:
            logger.error(f"Error parsing galaxy response for {symbol}: {str(e)}")
            return self._fallback_response(symbol, f"Parse error: {str(e)}")
    
    def _parse_social_response(self, symbol: str, data: Dict) -> Dict[str, Any]:
        """Parse LunarCrush social metrics response"""
        try:
            if 'result' in data and 'content' in data['result']:
                content = data['result']['content']
                
                # Extract social metrics
                social_mentions = content.get('social_mentions', 0)
                sentiment = content.get('sentiment', 50) / 100.0
                engagement = content.get('engagement_rate', 0)
                
                # Calculate social momentum (0-10 scale)
                social_momentum = min((social_mentions / 100) + (engagement * 5), 10.0)
                
                return {
                    'success': True,
                    'symbol': symbol,
                    'social_mentions': social_mentions,
                    'sentiment_score': sentiment,
                    'engagement_rate': engagement,
                    'social_momentum': social_momentum,
                    'viral_potential': social_mentions > 500 and sentiment > 0.6,
                    'social_score': min(int(social_momentum * 3), 30),  # Scale to 30 points
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'LunarCrush Official MCP',
                    'status': 'live_data'
                }
            else:
                return self._fallback_response(symbol, "Invalid social response format")
                
        except Exception as e:
            logger.error(f"Error parsing social response for {symbol}: {str(e)}")
            return self._fallback_response(symbol, f"Social parse error: {str(e)}")
    
    def _fallback_response(self, symbol: str, error: str) -> Dict[str, Any]:
        """Generate fallback response when LunarCrush is unavailable"""
        return {
            'success': False,
            'symbol': symbol,
            'galaxy_score': 0,
            'social_volume': 0,
            'sentiment_score': 0.5,
            'social_momentum': 0.0,
            'viral_potential': False,
            'social_score': 0,
            'price_score': 50,
            'timestamp': datetime.now().isoformat(),
            'data_source': 'LunarCrush Official MCP (Fallback)',
            'status': 'limited_data',
            'error': error
        }
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

# Global client instance
lunarcrush_client = LunarCrushHTTPClient()

async def get_social_analysis(symbol: str) -> Dict[str, Any]:
    """
    Get comprehensive social analysis for a cryptocurrency
    Compatible with existing scanner integration
    """
    try:
        # Try to get both galaxy score and social metrics
        galaxy_data = await lunarcrush_client.get_galaxy_score(symbol)
        social_data = await lunarcrush_client.get_social_metrics(symbol)
        
        # Combine the data for comprehensive analysis
        combined_data = {
            'success': galaxy_data.get('success', False) or social_data.get('success', False),
            'symbol': symbol,
            'galaxy_score': galaxy_data.get('galaxy_score', 0),
            'social_volume': galaxy_data.get('social_volume', 0),
            'sentiment_score': (galaxy_data.get('sentiment_score', 0.5) + social_data.get('sentiment_score', 0.5)) / 2,
            'social_momentum': max(galaxy_data.get('social_momentum', 0), social_data.get('social_momentum', 0)),
            'viral_potential': galaxy_data.get('viral_potential', False) or social_data.get('viral_potential', False),
            'social_score': max(galaxy_data.get('social_score', 0), social_data.get('social_score', 0)),
            'price_score': galaxy_data.get('price_score', 50),
            'timestamp': datetime.now().isoformat(),
            'data_source': 'LunarCrush Official MCP',
            'status': 'live_data' if galaxy_data.get('success') or social_data.get('success') else 'limited_data'
        }
        
        logger.info(f"✅ LunarCrush HTTP integration successful for {symbol}")
        return combined_data
        
    except Exception as e:
        logger.error(f"❌ LunarCrush HTTP integration failed for {symbol}: {str(e)}")
        return lunarcrush_client._fallback_response(symbol, str(e))

if __name__ == "__main__":
    # Test the integration
    async def test_integration():
        print("Testing LunarCrush Official HTTP MCP Integration...")
        
        # Test symbols
        test_symbols = ['BTC', 'ETH', 'ATOM']
        
        for symbol in test_symbols:
            print(f"\n--- Testing {symbol} ---")
            result = await get_social_analysis(symbol)
            print(f"Galaxy Score: {result['galaxy_score']}")
            print(f"Social Momentum: {result['social_momentum']}")
            print(f"Sentiment: {result['sentiment_score']}")
            print(f"Status: {result['status']}")
        
        await lunarcrush_client.close()
    
    # Run the test
    asyncio.run(test_integration())