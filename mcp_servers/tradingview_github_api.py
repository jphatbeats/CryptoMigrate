#!/usr/bin/env python3
"""
TradingView GitHub API Integration
Based on Mathieu2301/TradingView-API proven approach
Provides real-time data access through websocket connection
"""

import asyncio
import websockets
import json
import logging
import time
import string
import random
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class TradingViewGitHubAPI:
    """TradingView API based on Mathieu2301/TradingView-API implementation"""
    
    def __init__(self):
        self.ws_url = "wss://data.tradingview.com/socket.io/websocket"
        self.session_id = None
        self.chart_session_id = None
        self.ws = None
        self.last_request_time = 0
        self.min_interval = 2.0  # 2 seconds between requests
        
        logger.info("✅ TradingView GitHub API initialized - Real-time websocket access")
    
    def _generate_session_id(self, prefix="qs_"):
        """Generate session ID similar to TradingView format"""
        chars = string.ascii_letters + string.digits
        return prefix + ''.join(random.choice(chars) for _ in range(12))
    
    def _generate_chart_session_id(self):
        """Generate chart session ID"""
        return "cs_" + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    
    def _wait_for_rate_limit(self):
        """Rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    async def _connect_websocket(self):
        """Establish websocket connection to TradingView"""
        try:
            self.ws = await websockets.connect(
                self.ws_url,
                origin="https://data.tradingview.com",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            # Generate session IDs
            self.session_id = self._generate_session_id()
            self.chart_session_id = self._generate_chart_session_id()
            
            # Send initial authentication
            auth_message = json.dumps({
                "m": "set_auth_token",
                "p": ["unauthorized_user_token"]
            })
            await self.ws.send(f"~m~{len(auth_message)}~m~{auth_message}")
            
            # Create chart session
            chart_message = json.dumps({
                "m": "chart_create_session", 
                "p": [self.chart_session_id, ""]
            })
            await self.ws.send(f"~m~{len(chart_message)}~m~{chart_message}")
            
            logger.info(f"✅ WebSocket connected with session: {self.session_id}")
            return True
            
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False
    
    async def _send_message(self, message_type, params):
        """Send formatted message to TradingView websocket"""
        try:
            if not self.ws:
                await self._connect_websocket()
            
            message = json.dumps({
                "m": message_type,
                "p": params
            })
            
            formatted_message = f"~m~{len(message)}~m~{message}"
            await self.ws.send(formatted_message)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message {message_type}: {e}")
            return False
    
    async def get_symbol_data(self, symbol: str, exchange: str = "BINANCE", interval: str = "240") -> Optional[Dict[str, Any]]:
        """
        Get real-time symbol data using GitHub API approach
        
        Args:
            symbol: Symbol like BTCUSDT
            exchange: Exchange name like BINANCE  
            interval: Interval in minutes (240 = 4h)
        """
        try:
            self._wait_for_rate_limit()
            
            if not self.ws:
                connected = await self._connect_websocket()
                if not connected:
                    return None
            
            # Format symbol for TradingView
            tv_symbol = f"{exchange}:{symbol}"
            
            # Request symbol data
            await self._send_message("resolve_symbol", [
                self.chart_session_id,
                "symbol_1",
                f"={tv_symbol}"
            ])
            
            # Request study data (technical indicators)
            await self._send_message("create_study", [
                self.chart_session_id,
                "st1", 
                "st2",
                "Script$STD;Relative%1Strength%1Index",
                {"length": 14}
            ])
            
            # Create series for price data
            await self._send_message("create_series", [
                self.chart_session_id,
                "s1",
                "s1",
                "symbol_1",
                interval,
                300  # Number of bars
            ])
            
            # Wait for response
            await asyncio.sleep(3)
            
            # Read response messages
            response_data = await self._read_websocket_response()
            
            if response_data:
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'exchange': exchange,
                    'timestamp': datetime.utcnow().isoformat(),
                    'data': response_data,
                    'source': 'tradingview_github_api'
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"GitHub API error for {symbol}: {e}")
            return None
    
    async def _read_websocket_response(self) -> Optional[Dict[str, Any]]:
        """Read and parse websocket response"""
        try:
            if not self.ws:
                return None
            
            # Read multiple messages
            messages = []
            timeout = 5  # 5 second timeout
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(self.ws.recv(), timeout=1)
                    messages.append(message)
                except asyncio.TimeoutError:
                    break
            
            # Parse messages for useful data
            parsed_data = {}
            for message in messages:
                try:
                    if "~m~" in message:
                        # Extract JSON from TradingView format
                        parts = message.split("~m~")
                        for part in parts:
                            if part.startswith("{") and part.endswith("}"):
                                try:
                                    json_data = json.loads(part)
                                    if "p" in json_data and json_data.get("p"):
                                        parsed_data.update(self._extract_technical_data(json_data["p"]))
                                except json.JSONDecodeError:
                                    continue
                except Exception:
                    continue
            
            return parsed_data if parsed_data else None
            
        except Exception as e:
            logger.error(f"Error reading websocket response: {e}")
            return None
    
    def _extract_technical_data(self, data_array: List) -> Dict[str, Any]:
        """Extract technical indicators from response data"""
        extracted = {}
        
        try:
            if isinstance(data_array, list) and len(data_array) > 0:
                # Look for price data
                for item in data_array:
                    if isinstance(item, dict):
                        # Extract price information
                        if "lp" in item:  # Last price
                            extracted["price"] = item["lp"]
                        if "ch" in item:  # Change
                            extracted["change"] = item["ch"]
                        if "chp" in item:  # Change percentage
                            extracted["change_percent"] = item["chp"]
                        if "volume" in item:
                            extracted["volume"] = item["volume"]
                    
                    elif isinstance(item, list):
                        # Look for OHLCV data
                        if len(item) >= 6:
                            extracted["ohlcv"] = {
                                "open": item[1] if len(item) > 1 else None,
                                "high": item[2] if len(item) > 2 else None,
                                "low": item[3] if len(item) > 3 else None,
                                "close": item[4] if len(item) > 4 else None,
                                "volume": item[5] if len(item) > 5 else None
                            }
        
        except Exception as e:
            logger.warning(f"Error extracting technical data: {e}")
        
        return extracted
    
    async def get_multiple_symbols(self, symbols: List[str], exchange: str = "BINANCE") -> Dict[str, Any]:
        """Get data for multiple symbols efficiently"""
        results = {}
        
        for symbol in symbols:
            data = await self.get_symbol_data(symbol, exchange)
            if data:
                results[symbol] = data
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        return results
    
    async def close_connection(self):
        """Close websocket connection"""
        try:
            if self.ws:
                await self.ws.close()
                self.ws = None
                logger.info("✅ WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error closing websocket: {e}")
    
    def get_recommendations(self, symbol: str, exchange: str = "BINANCE") -> Optional[Dict[str, Any]]:
        """
        Get trading recommendations synchronously
        This is a wrapper for async functionality
        """
        try:
            # Run async function in new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(self.get_symbol_data(symbol, exchange))
                
                if result and result.get('status') == 'success':
                    # Generate recommendation based on available data
                    data = result.get('data', {})
                    price = data.get('price')
                    change_percent = data.get('change_percent', 0)
                    
                    # Simple recommendation logic
                    if change_percent > 5:
                        recommendation = 'STRONG_BUY'
                        confidence = min(90, 50 + abs(change_percent) * 2)
                    elif change_percent > 2:
                        recommendation = 'BUY' 
                        confidence = min(75, 50 + abs(change_percent) * 1.5)
                    elif change_percent < -5:
                        recommendation = 'STRONG_SELL'
                        confidence = min(90, 50 + abs(change_percent) * 2)
                    elif change_percent < -2:
                        recommendation = 'SELL'
                        confidence = min(75, 50 + abs(change_percent) * 1.5)
                    else:
                        recommendation = 'NEUTRAL'
                        confidence = 50
                    
                    return {
                        'status': 'success',
                        'symbol': symbol,
                        'exchange': exchange,
                        'overall_recommendation': recommendation,
                        'confidence_score': round(confidence, 1),
                        'price_data': {
                            'current_price': price,
                            'change_percent': change_percent
                        },
                        'raw_data': data,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                
                return None
                
            finally:
                loop.run_until_complete(self.close_connection())
                loop.close()
                
        except Exception as e:
            logger.error(f"GitHub API recommendations error for {symbol}: {e}")
            return None

# Global instance
tradingview_github = TradingViewGitHubAPI()

# Helper functions for server integration
def get_github_analysis(symbol: str, exchange: str = 'BINANCE') -> Optional[Dict[str, Any]]:
    """Get analysis using GitHub API approach"""
    return tradingview_github.get_recommendations(symbol, exchange)

def get_github_market_data(symbols: List[str], exchange: str = 'BINANCE') -> Dict[str, Any]:
    """Get market data for multiple symbols using async approach"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(tradingview_github.get_multiple_symbols(symbols, exchange))
            return result
        finally:
            loop.run_until_complete(tradingview_github.close_connection())
            loop.close()
            
    except Exception as e:
        logger.error(f"GitHub API multi-symbol error: {e}")
        return {}

async def initialize_github_tradingview():
    """Initialize the GitHub API for server use"""
    logger.info("🚀 TradingView GitHub API ready - Real-time websocket data access")
    return True