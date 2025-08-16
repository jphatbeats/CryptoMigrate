#!/usr/bin/env python3
"""
TradingView Web Scraper Integration
Based on proven Medium article approach for direct data extraction
Bypasses authentication and rate limiting issues completely
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.parse

logger = logging.getLogger(__name__)

class TradingViewWebScraper:
    """Direct TradingView web scraping - bypasses authentication completely"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        })
        self.last_request_time = 0
        self.min_interval = 2.0  # 2 seconds between requests
        
        logger.info("✅ TradingView Web Scraper initialized - Direct data extraction enabled")
    
    def _wait_for_rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def get_symbol_data(self, symbol: str, exchange: str = 'BINANCE', timeframe: str = '240') -> Optional[Dict[str, Any]]:
        """
        Get real-time symbol data directly from TradingView
        
        Args:
            symbol: Symbol like BTCUSDT
            exchange: Exchange name like BINANCE
            timeframe: Timeframe in minutes (240 = 4h)
        """
        try:
            self._wait_for_rate_limit()
            
            # TradingView symbol format
            tv_symbol = f"{exchange}:{symbol}"
            
            # Build the direct API URL (based on Medium article approach)
            url = "https://scanner.tradingview.com/crypto/scan"
            
            # Payload for scanner API
            payload = {
                "filter": [
                    {"left": "name", "operation": "match", "right": tv_symbol}
                ],
                "columns": [
                    "name",
                    "close",
                    "change",
                    "change_abs",
                    "Recommend.All",
                    "RSI",
                    "MACD.macd",
                    "MACD.signal",
                    "BB.upper",
                    "BB.lower",
                    "EMA20",
                    "EMA50",
                    "SMA20",
                    "SMA50",
                    "Stoch.K",
                    "Stoch.D",
                    "volume"
                ],
                "sort": {"sortBy": "name", "sortOrder": "asc"},
                "range": [0, 1]
            }
            
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('data') and len(data['data']) > 0:
                    result = data['data'][0]
                    
                    # Map the response to our format
                    return {
                        'status': 'success',
                        'symbol': symbol,
                        'exchange': exchange,
                        'timestamp': datetime.utcnow().isoformat(),
                        'price': result.get('d', [None, None, None, None])[1],  # close price
                        'change': result.get('d', [None, None, None, None])[2],  # change %
                        'recommendation': result.get('d', [None] * 5)[4],  # overall recommendation
                        'technical_indicators': {
                            'rsi': result.get('d', [None] * 6)[5],
                            'macd': result.get('d', [None] * 7)[6],
                            'macd_signal': result.get('d', [None] * 8)[7],
                            'bb_upper': result.get('d', [None] * 9)[8],
                            'bb_lower': result.get('d', [None] * 10)[9],
                            'ema_20': result.get('d', [None] * 11)[10],
                            'ema_50': result.get('d', [None] * 12)[11],
                            'sma_20': result.get('d', [None] * 13)[12],
                            'sma_50': result.get('d', [None] * 14)[13],
                            'stoch_k': result.get('d', [None] * 15)[14],
                            'stoch_d': result.get('d', [None] * 16)[15],
                            'volume': result.get('d', [None] * 17)[16]
                        }
                    }
                else:
                    logger.warning(f"No data returned for {tv_symbol}")
                    return None
            else:
                logger.error(f"TradingView scraper error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"TradingView scraper error for {symbol}: {e}")
            return None
    
    def get_market_data(self, symbols: List[str], exchange: str = 'BINANCE') -> Dict[str, Any]:
        """Get market data for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            data = self.get_symbol_data(symbol, exchange)
            if data:
                results[symbol] = data
        
        return results
    
    def get_recommendations(self, symbol: str, exchange: str = 'BINANCE') -> Optional[Dict[str, Any]]:
        """Get trading recommendations for a symbol"""
        data = self.get_symbol_data(symbol, exchange)
        
        if not data:
            return None
        
        rsi = data['technical_indicators'].get('rsi', 50)
        recommendation = data.get('recommendation', 0)
        
        # Convert numeric recommendation to text
        if recommendation > 0.5:
            rec_text = 'STRONG_BUY'
            confidence = min(95, 50 + (recommendation * 45))
        elif recommendation > 0.1:
            rec_text = 'BUY'
            confidence = min(75, 50 + (recommendation * 25))
        elif recommendation < -0.5:
            rec_text = 'STRONG_SELL'
            confidence = min(95, 50 + (abs(recommendation) * 45))
        elif recommendation < -0.1:
            rec_text = 'SELL'
            confidence = min(75, 50 + (abs(recommendation) * 25))
        else:
            rec_text = 'NEUTRAL'
            confidence = 50
        
        return {
            'status': 'success',
            'symbol': symbol,
            'overall_recommendation': rec_text,
            'confidence_score': round(confidence, 1),
            'technical_indicators': data['technical_indicators'],
            'price_data': {
                'current_price': data.get('price'),
                'change_percent': data.get('change')
            }
        }

# Global instance
tradingview_scraper = TradingViewWebScraper()

# Helper functions for server integration
def get_scraper_analysis(symbol: str, exchange: str = 'BINANCE') -> Optional[Dict[str, Any]]:
    """Get analysis using web scraper - no authentication needed"""
    return tradingview_scraper.get_recommendations(symbol, exchange)

def get_scraper_market_data(symbols: List[str], exchange: str = 'BINANCE') -> Dict[str, Any]:
    """Get market data for multiple symbols"""
    return tradingview_scraper.get_market_data(symbols, exchange)

async def initialize_tradingview_scraper():
    """Initialize the scraper for server use"""
    logger.info("🚀 TradingView Web Scraper ready - Direct data extraction without authentication")
    return True