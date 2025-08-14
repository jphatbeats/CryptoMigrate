#!/usr/bin/env python3
"""
Enhanced BingX Intelligence - Comprehensive market data collection for AI analysis
Leverages full BingX API capabilities to provide rich market context to OpenAI
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

# Import our existing modules
from bingx_direct_api import bingx_direct
from openai_trading_intelligence import TradingIntelligence

logger = logging.getLogger(__name__)

@dataclass
class MarketIntelligence:
    """Comprehensive market intelligence data structure"""
    symbol: str
    timestamp: datetime
    price_data: Dict
    volume_analysis: Dict
    orderbook_analysis: Dict
    candlestick_patterns: Dict
    momentum_indicators: Dict
    volatility_metrics: Dict
    market_structure: Dict

class EnhancedBingXIntelligence:
    """Enhanced BingX market data collection for comprehensive AI analysis"""
    
    def __init__(self):
        self.bingx_api = bingx_direct
        self.ai_analyst = TradingIntelligence()
        self.supported_timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        
    def collect_comprehensive_market_data(self, symbols: List[str], timeframe: str = '1h') -> Dict[str, MarketIntelligence]:
        """
        Collect comprehensive market data for multiple symbols
        This replaces the basic ticker calls with rich market intelligence
        """
        market_intelligence = {}
        
        for symbol in symbols:
            try:
                logger.info(f"Collecting comprehensive data for {symbol}")
                
                # 1. Price & Ticker Data (24h statistics)
                ticker_data = self._get_enhanced_ticker(symbol)
                
                # 2. Volume Analysis (multiple timeframes)
                volume_analysis = self._analyze_volume_patterns(symbol, timeframe)
                
                # 3. Orderbook Depth Analysis
                orderbook_analysis = self._analyze_orderbook_depth(symbol)
                
                # 4. Candlestick Pattern Analysis
                candlestick_patterns = self._analyze_candlestick_patterns(symbol, timeframe)
                
                # 5. Momentum Indicators (calculated from price data)
                momentum_indicators = self._calculate_momentum_indicators(symbol, timeframe)
                
                # 6. Volatility Metrics
                volatility_metrics = self._calculate_volatility_metrics(symbol, timeframe)
                
                # 7. Market Structure Analysis
                market_structure = self._analyze_market_structure(symbol, timeframe)
                
                # Combine into comprehensive intelligence
                market_intelligence[symbol] = MarketIntelligence(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    price_data=ticker_data,
                    volume_analysis=volume_analysis,
                    orderbook_analysis=orderbook_analysis,
                    candlestick_patterns=candlestick_patterns,
                    momentum_indicators=momentum_indicators,
                    volatility_metrics=volatility_metrics,
                    market_structure=market_structure
                )
                
                logger.info(f"✅ Comprehensive data collected for {symbol}")
                
            except Exception as e:
                logger.error(f"Failed to collect data for {symbol}: {str(e)}")
                continue
                
        return market_intelligence
    
    def _get_enhanced_ticker(self, symbol: str) -> Dict:
        """Get enhanced ticker data with additional metrics"""
        try:
            ticker = self.bingx_api.get_ticker(symbol)
            
            # Calculate additional metrics
            spread = ticker.get('ask', 0) - ticker.get('bid', 0)
            spread_pct = (spread / ticker.get('last', 1)) * 100 if ticker.get('last') else 0
            
            return {
                **ticker,
                'spread': spread,
                'spread_percentage': spread_pct,
                'price_precision': len(str(ticker.get('last', 0)).split('.')[-1]) if '.' in str(ticker.get('last', 0)) else 0,
                'volume_usd': ticker.get('volume', 0) * ticker.get('last', 0),
                'market_cap_estimate': None,  # Would need additional data
                'price_bands': {
                    'resistance': ticker.get('high', 0),
                    'support': ticker.get('low', 0),
                    'mid_point': (ticker.get('high', 0) + ticker.get('low', 0)) / 2
                }
            }
        except Exception as e:
            logger.error(f"Enhanced ticker failed for {symbol}: {str(e)}")
            return {}
    
    def _analyze_volume_patterns(self, symbol: str, timeframe: str) -> Dict:
        """Analyze volume patterns across multiple timeframes"""
        try:
            # Get candlestick data for volume analysis
            klines_data = self.bingx_api.get_klines(symbol, timeframe, limit=100)
            ohlcv = klines_data.get('ohlcv', [])
            
            if len(ohlcv) < 20:
                return {'error': 'Insufficient data for volume analysis'}
            
            volumes = [candle[5] for candle in ohlcv]  # Volume is index 5
            prices = [candle[4] for candle in ohlcv]   # Close prices
            
            # Calculate volume metrics
            avg_volume_20 = sum(volumes[-20:]) / 20
            current_volume = volumes[-1]
            volume_ratio = current_volume / avg_volume_20 if avg_volume_20 > 0 else 0
            
            # Price-volume correlation
            volume_price_correlation = self._calculate_correlation(volumes[-20:], prices[-20:])
            
            # Volume spikes detection
            volume_spikes = []
            for i, vol in enumerate(volumes[-20:]):
                if vol > avg_volume_20 * 2:  # 2x average volume = spike
                    volume_spikes.append({
                        'index': i,
                        'volume': vol,
                        'multiplier': vol / avg_volume_20,
                        'price': prices[-(20-i)]
                    })
            
            return {
                'current_volume': current_volume,
                'average_volume_20': avg_volume_20,
                'volume_ratio': volume_ratio,
                'volume_trend': 'increasing' if volumes[-1] > volumes[-5] else 'decreasing',
                'price_volume_correlation': volume_price_correlation,
                'volume_spikes': volume_spikes,
                'volume_score': min(10, volume_ratio * 2),  # Score out of 10
                'analysis_period': f"Last 100 {timeframe} candles"
            }
            
        except Exception as e:
            logger.error(f"Volume analysis failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_orderbook_depth(self, symbol: str) -> Dict:
        """Analyze orderbook depth and liquidity"""
        try:
            orderbook = self.bingx_api.get_orderbook(symbol, limit=50)
            
            bids = orderbook.get('bids', [])
            asks = orderbook.get('asks', [])
            
            if not bids or not asks:
                return {'error': 'Empty orderbook'}
            
            # Calculate depth metrics
            bid_depth_5 = sum([order[1] for order in bids[:5]])  # Top 5 levels
            ask_depth_5 = sum([order[1] for order in asks[:5]])
            total_depth = bid_depth_5 + ask_depth_5
            
            # Calculate imbalance
            depth_imbalance = (bid_depth_5 - ask_depth_5) / total_depth if total_depth > 0 else 0
            
            # Support/resistance levels
            best_bid = bids[0][0] if bids else 0
            best_ask = asks[0][0] if asks else 0
            spread = best_ask - best_bid
            
            # Liquidity score
            liquidity_score = min(10, total_depth / 1000)  # Arbitrary scaling
            
            return {
                'best_bid': best_bid,
                'best_ask': best_ask,
                'spread': spread,
                'bid_depth_5': bid_depth_5,
                'ask_depth_5': ask_depth_5,
                'total_depth': total_depth,
                'depth_imbalance': depth_imbalance,
                'imbalance_direction': 'bullish' if depth_imbalance > 0.1 else 'bearish' if depth_imbalance < -0.1 else 'neutral',
                'liquidity_score': liquidity_score,
                'market_pressure': 'buying' if depth_imbalance > 0.2 else 'selling' if depth_imbalance < -0.2 else 'balanced'
            }
            
        except Exception as e:
            logger.error(f"Orderbook analysis failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_candlestick_patterns(self, symbol: str, timeframe: str) -> Dict:
        """Analyze candlestick patterns for technical signals"""
        try:
            klines_data = self.bingx_api.get_klines(symbol, timeframe, limit=50)
            ohlcv = klines_data.get('ohlcv', [])
            
            if len(ohlcv) < 10:
                return {'error': 'Insufficient data for pattern analysis'}
            
            patterns = []
            recent_candles = ohlcv[-5:]  # Last 5 candles
            
            for i, candle in enumerate(recent_candles):
                timestamp, open_price, high, low, close, volume = candle
                
                # Basic candle analysis
                body_size = abs(close - open_price)
                wick_top = high - max(open_price, close)
                wick_bottom = min(open_price, close) - low
                total_range = high - low
                
                candle_type = 'bullish' if close > open_price else 'bearish'
                
                # Pattern detection
                if body_size < total_range * 0.3:  # Small body
                    if wick_top > body_size * 2 and wick_bottom > body_size * 2:
                        patterns.append('doji')
                    elif wick_top > body_size * 3:
                        patterns.append('hammer' if candle_type == 'bullish' else 'hanging_man')
                
                if body_size > total_range * 0.8:  # Large body
                    patterns.append('strong_' + candle_type)
            
            # Multi-candle patterns
            if len(recent_candles) >= 3:
                last_3 = recent_candles[-3:]
                if (last_3[0][4] > last_3[0][1] and  # First bullish
                    last_3[1][4] < last_3[1][1] and  # Second bearish  
                    last_3[2][4] > last_3[2][1]):    # Third bullish
                    patterns.append('morning_star_formation')
            
            return {
                'detected_patterns': patterns,
                'pattern_count': len(patterns),
                'latest_candle': {
                    'type': 'bullish' if recent_candles[-1][4] > recent_candles[-1][1] else 'bearish',
                    'body_percentage': (abs(recent_candles[-1][4] - recent_candles[-1][1]) / (recent_candles[-1][2] - recent_candles[-1][3])) * 100,
                    'upper_wick_ratio': (recent_candles[-1][2] - max(recent_candles[-1][1], recent_candles[-1][4])) / (recent_candles[-1][2] - recent_candles[-1][3]),
                    'lower_wick_ratio': (min(recent_candles[-1][1], recent_candles[-1][4]) - recent_candles[-1][3]) / (recent_candles[-1][2] - recent_candles[-1][3])
                },
                'pattern_strength': len(patterns) * 2,  # Simple scoring
                'timeframe': timeframe
            }
            
        except Exception as e:
            logger.error(f"Candlestick pattern analysis failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_momentum_indicators(self, symbol: str, timeframe: str) -> Dict:
        """Calculate momentum indicators from price data"""
        try:
            klines_data = self.bingx_api.get_klines(symbol, timeframe, limit=100)
            ohlcv = klines_data.get('ohlcv', [])
            
            if len(ohlcv) < 20:
                return {'error': 'Insufficient data for momentum calculation'}
            
            closes = [candle[4] for candle in ohlcv]
            highs = [candle[2] for candle in ohlcv]
            lows = [candle[3] for candle in ohlcv]
            
            # Simple RSI calculation
            rsi = self._calculate_rsi(closes)
            
            # Price momentum
            momentum_5 = (closes[-1] - closes[-6]) / closes[-6] * 100 if len(closes) >= 6 else 0
            momentum_10 = (closes[-1] - closes[-11]) / closes[-11] * 100 if len(closes) >= 11 else 0
            
            # Simple moving averages
            sma_10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else 0
            sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else 0
            
            return {
                'rsi_14': rsi,
                'rsi_signal': 'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral',
                'momentum_5_periods': momentum_5,
                'momentum_10_periods': momentum_10,
                'sma_10': sma_10,
                'sma_20': sma_20,
                'price_vs_sma10': 'above' if closes[-1] > sma_10 else 'below',
                'price_vs_sma20': 'above' if closes[-1] > sma_20 else 'below',
                'sma_cross': 'bullish' if sma_10 > sma_20 else 'bearish',
                'momentum_score': (momentum_5 + momentum_10) / 2,
                'trend_strength': abs(momentum_10)
            }
            
        except Exception as e:
            logger.error(f"Momentum indicators failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_volatility_metrics(self, symbol: str, timeframe: str) -> Dict:
        """Calculate volatility metrics"""
        try:
            klines_data = self.bingx_api.get_klines(symbol, timeframe, limit=50)
            ohlcv = klines_data.get('ohlcv', [])
            
            if len(ohlcv) < 10:
                return {'error': 'Insufficient data for volatility calculation'}
            
            closes = [candle[4] for candle in ohlcv]
            highs = [candle[2] for candle in ohlcv]
            lows = [candle[3] for candle in ohlcv]
            
            # Price changes
            price_changes = [(closes[i] - closes[i-1]) / closes[i-1] * 100 for i in range(1, len(closes))]
            
            # Volatility metrics
            volatility = (sum([change**2 for change in price_changes]) / len(price_changes))**0.5
            
            # Average True Range (simplified)
            true_ranges = []
            for i in range(1, len(ohlcv)):
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - closes[i-1]),
                    abs(lows[i] - closes[i-1])
                )
                true_ranges.append(tr)
            
            atr = sum(true_ranges[-14:]) / min(14, len(true_ranges)) if true_ranges else 0
            
            return {
                'price_volatility': volatility,
                'atr_14': atr,
                'volatility_percentile': min(100, volatility * 10),  # Arbitrary scaling
                'volatility_rating': 'high' if volatility > 5 else 'medium' if volatility > 2 else 'low',
                'price_stability': 'stable' if volatility < 1 else 'moderate' if volatility < 3 else 'volatile',
                'recent_range': max(highs[-10:]) - min(lows[-10:]),
                'range_percentage': ((max(highs[-10:]) - min(lows[-10:])) / closes[-1]) * 100
            }
            
        except Exception as e:
            logger.error(f"Volatility calculation failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_market_structure(self, symbol: str, timeframe: str) -> Dict:
        """Analyze market structure and trend"""
        try:
            klines_data = self.bingx_api.get_klines(symbol, timeframe, limit=100)
            ohlcv = klines_data.get('ohlcv', [])
            
            if len(ohlcv) < 20:
                return {'error': 'Insufficient data for structure analysis'}
            
            closes = [candle[4] for candle in ohlcv]
            highs = [candle[2] for candle in ohlcv]
            lows = [candle[3] for candle in ohlcv]
            
            # Trend analysis
            short_term_trend = (closes[-1] - closes[-6]) / closes[-6] * 100 if len(closes) >= 6 else 0
            medium_term_trend = (closes[-1] - closes[-21]) / closes[-21] * 100 if len(closes) >= 21 else 0
            
            # Support/Resistance levels (simplified)
            recent_highs = sorted(highs[-20:])[-5:]  # Top 5 highs
            recent_lows = sorted(lows[-20:])[:5]     # Bottom 5 lows
            
            resistance_level = sum(recent_highs) / len(recent_highs)
            support_level = sum(recent_lows) / len(recent_lows)
            
            return {
                'short_term_trend': short_term_trend,
                'medium_term_trend': medium_term_trend,
                'trend_direction': 'bullish' if medium_term_trend > 2 else 'bearish' if medium_term_trend < -2 else 'sideways',
                'trend_strength': abs(medium_term_trend),
                'resistance_level': resistance_level,
                'support_level': support_level,
                'distance_to_resistance': ((resistance_level - closes[-1]) / closes[-1]) * 100,
                'distance_to_support': ((closes[-1] - support_level) / closes[-1]) * 100,
                'position_in_range': ((closes[-1] - support_level) / (resistance_level - support_level)) * 100 if resistance_level != support_level else 50,
                'breakout_probability': 'high' if abs(short_term_trend) > 5 else 'medium' if abs(short_term_trend) > 2 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Market structure analysis failed for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50  # Neutral RSI
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0
        
        return round(numerator / denominator, 3)
    
    def generate_ai_market_analysis(self, symbols: List[str], timeframe: str = '1h') -> Dict:
        """
        Generate comprehensive AI analysis using enhanced BingX market data
        This replaces basic analysis with rich, data-driven insights
        """
        logger.info(f"Generating AI analysis for {len(symbols)} symbols with enhanced BingX data")
        
        # Collect comprehensive market data
        market_intelligence = self.collect_comprehensive_market_data(symbols, timeframe)
        
        # Prepare structured data for AI analysis
        structured_market_data = {}
        for symbol, intelligence in market_intelligence.items():
            structured_market_data[symbol] = {
                'price_data': intelligence.price_data,
                'volume_analysis': intelligence.volume_analysis,
                'orderbook_analysis': intelligence.orderbook_analysis,
                'technical_patterns': intelligence.candlestick_patterns,
                'momentum_indicators': intelligence.momentum_indicators,
                'volatility_metrics': intelligence.volatility_metrics,
                'market_structure': intelligence.market_structure,
                'timestamp': intelligence.timestamp.isoformat()
            }
        
        # Generate AI analysis with enhanced data
        try:
            ai_analysis = self.ai_analyst.scan_opportunities(
                market_data={'real_time_market_data': structured_market_data},
                news_data={}  # Can be enhanced with news data later
            )
            
            return {
                'enhanced_analysis': True,
                'data_sources': ['bingx_official_api', 'comprehensive_technical_analysis'],
                'symbols_analyzed': len(symbols),
                'timeframe': timeframe,
                'raw_market_intelligence': structured_market_data,
                'ai_analysis': ai_analysis,
                'generation_timestamp': datetime.now().isoformat(),
                'analysis_completeness': 'comprehensive'
            }
            
        except Exception as e:
            logger.error(f"AI analysis generation failed: {str(e)}")
            return {
                'enhanced_analysis': False,
                'error': str(e),
                'raw_market_intelligence': structured_market_data,
                'generation_timestamp': datetime.now().isoformat()
            }

# Global instance for use in other modules
enhanced_bingx_intelligence = EnhancedBingXIntelligence()

def test_enhanced_intelligence():
    """Test the enhanced intelligence system"""
    print("🧠 Testing Enhanced BingX Intelligence System...")
    
    test_symbols = ['BTC/USDT', 'ETH/USDT']
    
    try:
        # Test comprehensive data collection
        market_data = enhanced_bingx_intelligence.collect_comprehensive_market_data(test_symbols)
        
        for symbol, intelligence in market_data.items():
            print(f"\n📊 {symbol} Intelligence:")
            print(f"   💰 Price: ${intelligence.price_data.get('last', 0):,.2f}")
            print(f"   📈 Volume Score: {intelligence.volume_analysis.get('volume_score', 0):.1f}/10")
            print(f"   📚 Orderbook Imbalance: {intelligence.orderbook_analysis.get('imbalance_direction', 'unknown')}")
            print(f"   🕯️  Patterns: {intelligence.candlestick_patterns.get('pattern_count', 0)} detected")
            print(f"   ⚡ RSI: {intelligence.momentum_indicators.get('rsi_14', 0):.1f}")
            print(f"   📊 Volatility: {intelligence.volatility_metrics.get('volatility_rating', 'unknown')}")
            print(f"   🎯 Trend: {intelligence.market_structure.get('trend_direction', 'unknown')}")
        
        # Test AI analysis generation
        print(f"\n🤖 Generating AI analysis...")
        ai_analysis = enhanced_bingx_intelligence.generate_ai_market_analysis(test_symbols)
        
        print(f"   ✅ Analysis generated: {ai_analysis.get('enhanced_analysis', False)}")
        print(f"   📊 Symbols analyzed: {ai_analysis.get('symbols_analyzed', 0)}")
        print(f"   🔍 Completeness: {ai_analysis.get('analysis_completeness', 'unknown')}")
        
        if ai_analysis.get('ai_analysis'):
            print(f"   🎯 Opportunities found: {len(ai_analysis['ai_analysis'].get('high_probability_setups', []))}")
        
        print("\n✅ Enhanced BingX Intelligence test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Enhanced intelligence test failed: {e}")
        return False

if __name__ == "__main__":
    test_enhanced_intelligence()