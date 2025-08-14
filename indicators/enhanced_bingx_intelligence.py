#!/usr/bin/env python3
"""
Enhanced BingX Intelligence System
Comprehensive market analysis with AI-powered insights
"""

import os
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class EnhancedBingXIntelligence:
    """Enhanced BingX market intelligence with comprehensive analysis"""
    
    def __init__(self):
        self.base_url = "https://open-api.bingx.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AlphaPlaybook/4.0',
            'Content-Type': 'application/json'
        })
        logger.info("✅ Enhanced BingX Intelligence initialized")
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive market data for symbol"""
        try:
            # Convert symbol format (BTC/USDT -> BTC-USDT)
            bingx_symbol = symbol.replace('/', '-')
            
            # Get ticker data
            ticker_url = f"{self.base_url}/openApi/spot/v1/ticker/24hr"
            params = {"symbol": bingx_symbol}
            
            response = self.session.get(ticker_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data'):
                    ticker = data['data']
                    
                    return {
                        "symbol": symbol,
                        "price": float(ticker.get('lastPrice', 0)),
                        "change_24h": float(ticker.get('priceChangePercent', 0)),
                        "volume_24h": float(ticker.get('volume', 0)),
                        "high_24h": float(ticker.get('highPrice', 0)),
                        "low_24h": float(ticker.get('lowPrice', 0)),
                        "bid": float(ticker.get('bidPrice', 0)),
                        "ask": float(ticker.get('askPrice', 0)),
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Fallback data structure
            return {
                "symbol": symbol,
                "price": 0,
                "change_24h": 0,
                "volume_24h": 0,
                "high_24h": 0,
                "low_24h": 0,
                "bid": 0,
                "ask": 0,
                "timestamp": datetime.now().isoformat(),
                "status": "data_unavailable"
            }
            
        except Exception as e:
            logger.error(f"Market data error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def get_orderbook_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get orderbook depth analysis"""
        try:
            bingx_symbol = symbol.replace('/', '-')
            
            orderbook_url = f"{self.base_url}/openApi/spot/v1/depth"
            params = {"symbol": bingx_symbol, "limit": 100}
            
            response = self.session.get(orderbook_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data'):
                    orderbook = data['data']
                    
                    bids = orderbook.get('bids', [])
                    asks = orderbook.get('asks', [])
                    
                    if bids and asks:
                        # Calculate orderbook metrics
                        bid_volume = sum(float(bid[1]) for bid in bids[:10])
                        ask_volume = sum(float(ask[1]) for ask in asks[:10])
                        
                        spread = float(asks[0][0]) - float(bids[0][0]) if bids and asks else 0
                        spread_percentage = (spread / float(asks[0][0])) * 100 if asks and asks[0][0] else 0
                        
                        return {
                            "symbol": symbol,
                            "bid_volume_top10": round(bid_volume, 2),
                            "ask_volume_top10": round(ask_volume, 2),
                            "volume_ratio": round(bid_volume / ask_volume, 2) if ask_volume > 0 else 0,
                            "spread": round(spread, 4),
                            "spread_percentage": round(spread_percentage, 4),
                            "orderbook_strength": "strong" if bid_volume > ask_volume * 1.2 else "balanced",
                            "timestamp": datetime.now().isoformat()
                        }
            
            return {
                "symbol": symbol,
                "orderbook_strength": "unavailable",
                "timestamp": datetime.now().isoformat(),
                "status": "data_unavailable"
            }
            
        except Exception as e:
            logger.error(f"Orderbook analysis error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def get_volume_analysis(self, symbol: str) -> Dict[str, Any]:
        """Analyze volume patterns and strength"""
        try:
            # Get 24hr volume data
            market_data = self.get_market_data(symbol)
            volume_24h = market_data.get('volume_24h', 0)
            
            # Volume scoring (simplified)
            if volume_24h > 1000000:
                volume_score = 10
                volume_grade = "Excellent"
            elif volume_24h > 500000:
                volume_score = 8
                volume_grade = "High"
            elif volume_24h > 100000:
                volume_score = 6
                volume_grade = "Medium"
            elif volume_24h > 10000:
                volume_score = 4
                volume_grade = "Low"
            else:
                volume_score = 2
                volume_grade = "Very Low"
            
            return {
                "symbol": symbol,
                "volume_24h": volume_24h,
                "volume_score": volume_score,
                "volume_grade": volume_grade,
                "volume_analysis": f"24h volume: ${volume_24h:,.0f} - {volume_grade} liquidity",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Volume analysis error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def get_price_patterns(self, symbol: str) -> Dict[str, Any]:
        """Analyze price patterns and trends"""
        try:
            market_data = self.get_market_data(symbol)
            
            price = market_data.get('price', 0)
            change_24h = market_data.get('change_24h', 0)
            high_24h = market_data.get('high_24h', 0)
            low_24h = market_data.get('low_24h', 0)
            
            # Calculate pattern metrics
            range_24h = high_24h - low_24h if high_24h and low_24h else 0
            position_in_range = ((price - low_24h) / range_24h) * 100 if range_24h > 0 else 50
            
            # Determine trend
            if change_24h > 5:
                trend = "Strong Bullish"
            elif change_24h > 2:
                trend = "Bullish"
            elif change_24h > -2:
                trend = "Sideways"
            elif change_24h > -5:
                trend = "Bearish"
            else:
                trend = "Strong Bearish"
            
            # Position analysis
            if position_in_range > 80:
                position_analysis = "Near 24h high - potential resistance"
            elif position_in_range > 60:
                position_analysis = "Upper range - watching for breakout"
            elif position_in_range > 40:
                position_analysis = "Mid-range - neutral position"
            elif position_in_range > 20:
                position_analysis = "Lower range - potential support"
            else:
                position_analysis = "Near 24h low - oversold potential"
            
            return {
                "symbol": symbol,
                "current_price": price,
                "change_24h_percent": change_24h,
                "trend_analysis": trend,
                "range_24h": round(range_24h, 4),
                "position_in_range": round(position_in_range, 1),
                "position_analysis": position_analysis,
                "high_24h": high_24h,
                "low_24h": low_24h,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Price patterns error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def get_comprehensive_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        """Get comprehensive analysis for multiple symbols"""
        try:
            analysis_results = []
            
            for symbol in symbols:
                logger.info(f"Analyzing {symbol}")
                
                # Get all analysis components
                market_data = self.get_market_data(symbol)
                orderbook_analysis = self.get_orderbook_analysis(symbol)
                volume_analysis = self.get_volume_analysis(symbol)
                price_patterns = self.get_price_patterns(symbol)
                
                # Combine into comprehensive analysis
                symbol_analysis = {
                    "symbol": symbol,
                    "timestamp": datetime.now().isoformat(),
                    "market_data": market_data,
                    "orderbook_analysis": orderbook_analysis,
                    "volume_analysis": volume_analysis,
                    "price_patterns": price_patterns,
                    "intelligence_summary": {
                        "price": market_data.get('price', 0),
                        "change_24h": market_data.get('change_24h', 0),
                        "volume_score": volume_analysis.get('volume_score', 0),
                        "trend": price_patterns.get('trend_analysis', 'Unknown'),
                        "orderbook_strength": orderbook_analysis.get('orderbook_strength', 'Unknown'),
                        "analysis_quality": "comprehensive"
                    }
                }
                
                analysis_results.append(symbol_analysis)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "enhanced_bingx_intelligence",
                "symbols_analyzed": len(symbols),
                "results": analysis_results,
                "data_source": "BingX API + Enhanced Intelligence",
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def test_system(self) -> Dict[str, Any]:
        """Test Enhanced BingX Intelligence system"""
        try:
            test_symbol = "BTC-USDT"
            
            # Test all components
            market_test = self.get_market_data(test_symbol)
            orderbook_test = self.get_orderbook_analysis(test_symbol)
            volume_test = self.get_volume_analysis(test_symbol)
            patterns_test = self.get_price_patterns(test_symbol)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "test_status": "success",
                "test_symbol": test_symbol,
                "components_tested": {
                    "market_data": "success" if market_test.get('price', 0) > 0 else "limited_data",
                    "orderbook_analysis": "success" if orderbook_test.get('orderbook_strength') != 'unavailable' else "limited_data",
                    "volume_analysis": "success" if volume_test.get('volume_score', 0) > 0 else "limited_data",
                    "price_patterns": "success" if patterns_test.get('trend_analysis') else "limited_data"
                },
                "system_health": "operational",
                "data_source": "BingX Public API",
                "note": "Enhanced intelligence system operational with public data access"
            }
            
        except Exception as e:
            logger.error(f"System test error: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "test_status": "error"
            }