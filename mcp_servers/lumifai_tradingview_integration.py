#!/usr/bin/env python3
"""
Lumif-ai TradingView Technical Analysis Integration
Enhanced technical analysis using TradingView's comprehensive indicator suite
"""

import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from tradingview_ta import TA_Handler, Interval, Exchange
import time

logger = logging.getLogger(__name__)

class LumifTradingViewClient:
    """Enhanced TradingView technical analysis - Lumif-ai integration for Alpha Playbook v4"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'THE-ALPHA-PLAYBOOK-v4-LUMIF-AI/1.0',
            'Accept': 'application/json'
        })
        
        # TradingView interval mappings (only supported intervals)
        self.interval_map = {
            '1m': Interval.INTERVAL_1_MINUTE,
            '5m': Interval.INTERVAL_5_MINUTES,
            '15m': Interval.INTERVAL_15_MINUTES,
            '30m': Interval.INTERVAL_30_MINUTES,
            '1h': Interval.INTERVAL_1_HOUR,
            '2h': Interval.INTERVAL_2_HOURS,
            '4h': Interval.INTERVAL_4_HOURS,
            '1d': Interval.INTERVAL_1_DAY,
            '1w': Interval.INTERVAL_1_WEEK,
            '1M': Interval.INTERVAL_1_MONTH
        }
        
    async def start_mcp_server(self) -> bool:
        """Initialize Lumif-ai TradingView integration"""
        try:
            logger.info("🚀 Initializing Lumif-ai TradingView integration...")
            
            # Test with Bitcoin on Binance
            test_analysis = self.get_comprehensive_analysis('BTCUSDT', 'crypto', 'BINANCE', '4h')
            
            if test_analysis and test_analysis.get('status') == 'success':
                logger.info("✅ Lumif-ai TradingView integration ready - ENHANCED TECHNICAL ANALYSIS!")
                logger.info("💡 Features: 208+ indicators, pattern recognition, multi-timeframe analysis")
                return True
            else:
                logger.error("❌ TradingView test analysis failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error initializing Lumif-ai TradingView integration: {e}")
            return False
    
    def get_comprehensive_analysis(self, symbol: str, screener: str = 'crypto', 
                                 exchange: str = 'BINANCE', interval: str = '4h') -> Optional[Dict[str, Any]]:
        """Get comprehensive TradingView technical analysis - Enhanced by Lumif-ai"""
        try:
            # Rate limiting to prevent 429 errors
            time.sleep(0.5)  # 500ms delay between requests
            
            # Convert interval to TradingView format
            tv_interval = self.interval_map.get(interval, Interval.INTERVAL_4_HOURS)
            
            # Create TradingView handler with retry logic
            max_retries = 3
            analysis = None
            
            for attempt in range(max_retries):
                try:
                    handler = TA_Handler(
                        symbol=symbol,
                        screener=screener,
                        exchange=exchange,
                        interval=tv_interval
                    )
                    
                    # Get comprehensive analysis
                    analysis = handler.get_analysis()
                    break
                    
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        # Rate limited, wait longer and retry
                        wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                        logger.warning(f"Rate limited for {symbol}, waiting {wait_time}s (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise e
            
            if analysis is None:
                raise Exception("Failed to get analysis after retries")
            
            # Enhanced processing with Lumif-ai approach
            enhanced_data = self._enhance_analysis(analysis, symbol, interval)
            
            return {
                'status': 'success',
                'symbol': symbol,
                'exchange': exchange,
                'interval': interval,
                'timestamp': datetime.utcnow().isoformat(),
                'summary': enhanced_data['summary'],
                'indicators': enhanced_data['indicators'],
                'oscillators': enhanced_data['oscillators'],
                'moving_averages': enhanced_data['moving_averages'],
                'confluence_score': enhanced_data['confluence_score'],
                'pattern_signals': enhanced_data['pattern_signals'],
                'source': 'lumif_tradingview_enhanced'
            }
            
        except Exception as e:
            logger.error(f"Error getting TradingView analysis for {symbol}: {e}")
            return None
    
    def _enhance_analysis(self, analysis, symbol: str, interval: str) -> Dict[str, Any]:
        """Enhanced analysis processing using Lumif-ai methodology"""
        
        # Extract core data
        summary = analysis.summary
        indicators = analysis.indicators
        oscillators = analysis.oscillators  
        moving_averages = analysis.moving_averages
        
        # Calculate enhanced confluence score (Lumif-ai approach)
        confluence_score = self._calculate_confluence_score(summary, indicators)
        
        # Pattern recognition signals
        pattern_signals = self._detect_patterns(indicators, symbol)
        
        return {
            'summary': {
                'recommendation': summary.get('RECOMMENDATION', 'NEUTRAL'),
                'buy_signals': summary.get('BUY', 0),
                'neutral_signals': summary.get('NEUTRAL', 0), 
                'sell_signals': summary.get('SELL', 0),
                'total_signals': summary.get('BUY', 0) + summary.get('NEUTRAL', 0) + summary.get('SELL', 0)
            },
            'indicators': {
                'rsi': indicators.get('RSI'),
                'rsi_signal': self._get_rsi_signal(indicators.get('RSI')),
                'macd': {
                    'value': indicators.get('MACD.macd'),
                    'signal': indicators.get('MACD.signal'),
                    'histogram': indicators.get('Histogram')
                },
                'stoch_k': indicators.get('Stoch.K'),
                'stoch_d': indicators.get('Stoch.D'),
                'cci': indicators.get('CCI20'),
                'adx': indicators.get('ADX'),
                'williams_r': indicators.get('W.R'),
                'ultimate_oscillator': indicators.get('UO'),
                'awesome_oscillator': indicators.get('AO')
            },
            'oscillators': oscillators,
            'moving_averages': moving_averages,
            'confluence_score': confluence_score,
            'pattern_signals': pattern_signals
        }
    
    def _calculate_confluence_score(self, summary: dict, indicators: dict) -> float:
        """Calculate confluence score using Lumif-ai methodology"""
        try:
            total_signals = summary.get('BUY', 0) + summary.get('NEUTRAL', 0) + summary.get('SELL', 0)
            if total_signals == 0:
                return 0.0
            
            buy_ratio = summary.get('BUY', 0) / total_signals
            sell_ratio = summary.get('SELL', 0) / total_signals
            
            # Enhanced scoring with RSI and MACD confluence
            base_score = buy_ratio * 100
            
            # RSI confluence bonus
            rsi = indicators.get('RSI')
            if rsi:
                if 30 <= rsi <= 70:  # Healthy range
                    base_score += 10
                elif rsi > 70:  # Overbought
                    base_score -= 15
                elif rsi < 30:  # Oversold - potential buy opportunity
                    base_score += 5
            
            # MACD confluence bonus  
            macd_value = indicators.get('MACD.macd')
            macd_signal = indicators.get('MACD.signal')
            if macd_value and macd_signal:
                if macd_value > macd_signal:  # Bullish crossover
                    base_score += 10
                else:  # Bearish crossover
                    base_score -= 10
            
            return min(max(base_score, 0), 100)  # Clamp between 0-100
            
        except Exception as e:
            logger.error(f"Error calculating confluence score: {e}")
            return 0.0
    
    def _get_rsi_signal(self, rsi: Optional[float]) -> str:
        """Get RSI signal interpretation"""
        if rsi is None:
            return 'UNKNOWN'
        elif rsi > 70:
            return 'OVERBOUGHT'
        elif rsi < 30:
            return 'OVERSOLD'
        else:
            return 'NEUTRAL'
    
    def _detect_patterns(self, indicators: dict, symbol: str) -> Dict[str, Any]:
        """Enhanced pattern detection using Lumif-ai approach"""
        patterns = {
            'bullish_signals': [],
            'bearish_signals': [],
            'neutral_signals': [],
            'divergence_detected': False
        }
        
        try:
            rsi = indicators.get('RSI')
            macd_value = indicators.get('MACD.macd')
            macd_signal = indicators.get('MACD.signal')
            stoch_k = indicators.get('Stoch.K')
            stoch_d = indicators.get('Stoch.D')
            
            # RSI patterns
            if rsi:
                if rsi < 30:
                    patterns['bullish_signals'].append('RSI_OVERSOLD')
                elif rsi > 70:
                    patterns['bearish_signals'].append('RSI_OVERBOUGHT')
            
            # MACD patterns
            if macd_value and macd_signal:
                if macd_value > macd_signal and macd_value > 0:
                    patterns['bullish_signals'].append('MACD_BULLISH_ABOVE_ZERO')
                elif macd_value < macd_signal and macd_value < 0:
                    patterns['bearish_signals'].append('MACD_BEARISH_BELOW_ZERO')
            
            # Stochastic patterns
            if stoch_k and stoch_d:
                if stoch_k > stoch_d and stoch_k < 20:
                    patterns['bullish_signals'].append('STOCH_BULLISH_CROSSOVER_OVERSOLD')
                elif stoch_k < stoch_d and stoch_k > 80:
                    patterns['bearish_signals'].append('STOCH_BEARISH_CROSSOVER_OVERBOUGHT')
            
            # If no clear signals, mark as neutral
            if not patterns['bullish_signals'] and not patterns['bearish_signals']:
                patterns['neutral_signals'].append('NO_CLEAR_PATTERN')
                
        except Exception as e:
            logger.error(f"Error detecting patterns for {symbol}: {e}")
            patterns['neutral_signals'].append('PATTERN_ANALYSIS_ERROR')
        
        return patterns
    
    def get_multi_timeframe_analysis(self, symbol: str, screener: str = 'crypto', 
                                   exchange: str = 'BINANCE') -> Optional[Dict[str, Any]]:
        """Get multi-timeframe analysis - Lumif-ai enhanced approach"""
        timeframes = ['1h', '4h', '1d']
        results = {}
        
        try:
            logger.info(f"🔍 Multi-timeframe analysis for {symbol}")
            
            for tf in timeframes:
                analysis = self.get_comprehensive_analysis(symbol, screener, exchange, tf)
                if analysis:
                    results[tf] = {
                        'recommendation': analysis['summary']['recommendation'],
                        'confluence_score': analysis['confluence_score'],
                        'rsi': analysis['indicators']['rsi'],
                        'rsi_signal': analysis['indicators']['rsi_signal']
                    }
                    time.sleep(0.5)  # Rate limiting
            
            # Calculate overall confluence
            overall_score = self._calculate_multi_timeframe_confluence(results)
            
            return {
                'status': 'success',
                'symbol': symbol,
                'timeframes': results,
                'overall_confluence_score': overall_score,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'lumif_multi_timeframe_enhanced'
            }
            
        except Exception as e:
            logger.error(f"Error in multi-timeframe analysis for {symbol}: {e}")
            return None
    
    def _calculate_multi_timeframe_confluence(self, timeframe_results: Dict) -> float:
        """Calculate multi-timeframe confluence score"""
        if not timeframe_results:
            return 0.0
        
        total_score = 0
        count = 0
        
        # Weight timeframes differently (higher weight for longer timeframes)
        weights = {'1h': 1.0, '4h': 2.0, '1d': 3.0}
        
        for tf, data in timeframe_results.items():
            if data.get('confluence_score') is not None:
                weight = weights.get(tf, 1.0)
                total_score += data['confluence_score'] * weight
                count += weight
        
        return total_score / count if count > 0 else 0.0
    
    def get_market_scanner_signals(self, symbols: List[str], min_confluence: float = 75.0) -> List[Dict[str, Any]]:
        """Enhanced market scanner using Lumif-ai methodology"""
        signals = []
        
        try:
            logger.info(f"🔍 Scanning {len(symbols)} symbols for confluence >= {min_confluence}%")
            
            for symbol in symbols:
                try:
                    analysis = self.get_comprehensive_analysis(f"{symbol}USDT", 'crypto', 'BINANCE', '4h')
                    
                    if analysis and analysis.get('confluence_score', 0) >= min_confluence:
                        signals.append({
                            'symbol': symbol,
                            'confluence_score': analysis['confluence_score'],
                            'recommendation': analysis['summary']['recommendation'],
                            'rsi': analysis['indicators']['rsi'],
                            'rsi_signal': analysis['indicators']['rsi_signal'],
                            'pattern_signals': analysis['pattern_signals'],
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    
                    time.sleep(0.3)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Error analyzing {symbol}: {e}")
                    continue
            
            # Sort by confluence score
            signals.sort(key=lambda x: x['confluence_score'], reverse=True)
            
            logger.info(f"✅ Found {len(signals)} high-confluence signals")
            return signals
            
        except Exception as e:
            logger.error(f"Error in market scanner: {e}")
            return []

# Global client instance
lumif_tradingview_client = LumifTradingViewClient()

# MCP integration functions
async def initialize_lumif_tradingview() -> bool:
    """Initialize Lumif-ai TradingView integration"""
    return await lumif_tradingview_client.start_mcp_server()

def get_enhanced_technical_analysis(symbol: str, exchange: str = 'BINANCE', interval: str = '4h') -> Optional[Dict[str, Any]]:
    """Get enhanced technical analysis using Lumif-ai methodology"""
    return lumif_tradingview_client.get_comprehensive_analysis(symbol, 'crypto', exchange, interval)

def get_multi_timeframe_confluence(symbol: str, exchange: str = 'BINANCE') -> Optional[Dict[str, Any]]:
    """Get multi-timeframe confluence analysis"""
    return lumif_tradingview_client.get_multi_timeframe_analysis(symbol, 'crypto', exchange)

def scan_market_opportunities(symbols: List[str], min_confluence: float = 75.0) -> List[Dict[str, Any]]:
    """Scan market for high-confluence opportunities"""
    return lumif_tradingview_client.get_market_scanner_signals(symbols, min_confluence)

if __name__ == "__main__":
    import asyncio
    async def test():
        success = await initialize_lumif_tradingview()
        print(f"Lumif-ai TradingView integration: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            # Test Bitcoin analysis
            btc_analysis = get_enhanced_technical_analysis('BTCUSDT')
            print(f"BTC Analysis: {btc_analysis}")
            
    asyncio.run(test())