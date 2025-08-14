#!/usr/bin/env python3
"""
Taapi.io Technical Indicators Integration
Provides comprehensive technical analysis for AI trading intelligence
"""

import requests
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TaapiIndicators:
    """Technical indicators provider using taapi.io API"""
    
    def __init__(self):
        self.api_key = os.getenv('TAAPI_API_KEY')
        self.base_url = "https://api.taapi.io"
        self.timeout = 10
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests to avoid rate limits
        
        if not self.api_key:
            logger.warning("TAAPI_API_KEY not found in environment variables")
            self.api_key = None
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make authenticated request to taapi.io API with rate limiting (legacy method)"""
        if not self.api_key:
            return {'error': 'TAAPI_API_KEY not configured'}
        
        # Rate limiting - ensure minimum interval between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        params['secret'] = self.api_key
        
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=self.timeout
            )
            self.last_request_time = time.time()
            
            if response.status_code == 429:
                logger.warning("Taapi.io rate limit reached - will use simulated indicators")
                return {'error': 'Rate limit reached - using fallback indicators', 'rate_limited': True}
            elif response.status_code == 403:
                logger.warning("Taapi.io API access forbidden - check API key permissions")
                return {'error': 'API access forbidden - check permissions', 'forbidden': True}
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Taapi.io API error: {e}")
            return {'error': str(e)}
    
    def _make_bulk_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make bulk POST request to taapi.io API - more efficient method"""
        if not self.api_key:
            return {'error': 'TAAPI_API_KEY not configured'}
        
        # Rate limiting - ensure minimum interval between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        payload['secret'] = self.api_key
        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/bulk",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            self.last_request_time = time.time()
            
            if response.status_code == 429:
                logger.warning("Taapi.io rate limit reached - will use simulated indicators")
                return {'error': 'Rate limit reached - using fallback indicators', 'rate_limited': True}
            elif response.status_code == 403:
                logger.warning("Taapi.io API access forbidden - check API key permissions")
                return {'error': 'API access forbidden - check permissions', 'forbidden': True}
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Taapi.io bulk API error: {e}")
            return {'error': str(e)}
    
    def get_rsi(self, symbol: str, interval: str = "1h", period: int = 14) -> Dict[str, Any]:
        """Get RSI (Relative Strength Index)"""
        params = {
            'indicator': 'rsi',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('rsi', params)
    
    def get_macd(self, symbol: str, interval: str = "1h", 
                 fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, Any]:
        """Get MACD (Moving Average Convergence Divergence)"""
        params = {
            'indicator': 'macd',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'fast_period': fast_period,
            'slow_period': slow_period,
            'signal_period': signal_period
        }
        return self._make_request('macd', params)
    
    def get_bollinger_bands(self, symbol: str, interval: str = "1h", 
                           period: int = 20, std_dev: float = 2.0) -> Dict[str, Any]:
        """Get Bollinger Bands"""
        params = {
            'indicator': 'bbands',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period,
            'stddev': std_dev
        }
        return self._make_request('bbands', params)
    
    def get_stochastic(self, symbol: str, interval: str = "1h", 
                      k_period: int = 14, d_period: int = 3) -> Dict[str, Any]:
        """Get Stochastic Oscillator"""
        params = {
            'indicator': 'stoch',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'k_period': k_period,
            'd_period': d_period
        }
        return self._make_request('stoch', params)
    
    def get_williams_r(self, symbol: str, interval: str = "1h", period: int = 14) -> Dict[str, Any]:
        """Get Williams %R"""
        params = {
            'indicator': 'willr',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('willr', params)
    
    def get_ema(self, symbol: str, interval: str = "1h", period: int = 20) -> Dict[str, Any]:
        """Get Exponential Moving Average"""
        params = {
            'indicator': 'ema',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('ema', params)
    
    def get_sma(self, symbol: str, interval: str = "1h", period: int = 20) -> Dict[str, Any]:
        """Get Simple Moving Average"""
        params = {
            'indicator': 'sma',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('sma', params)
    
    def get_adx(self, symbol: str, interval: str = "1h", period: int = 14) -> Dict[str, Any]:
        """Get Average Directional Index (trend strength)"""
        params = {
            'indicator': 'adx',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('adx', params)
    
    def get_cci(self, symbol: str, interval: str = "1h", period: int = 20) -> Dict[str, Any]:
        """Get Commodity Channel Index"""
        params = {
            'indicator': 'cci',
            'exchange': 'binance',
            'symbol': symbol,
            'interval': interval,
            'period': period
        }
        return self._make_request('cci', params)
    
    def get_comprehensive_analysis(self, symbol: str, interval: str = "1h") -> Dict[str, Any]:
        """Get comprehensive technical analysis for a symbol using bulk API"""
        logger.info(f"🔍 Fetching comprehensive technical analysis for {symbol}")
        
        analysis = {
            'symbol': symbol,
            'interval': interval,
            'timestamp': datetime.now().isoformat(),
            'indicators': {},
            'signals': {},
            'summary': {}
        }
        
        # Use bulk API for efficiency - up to 20 indicators in one request
        bulk_payload = {
            'construct': {
                'exchange': 'binance',
                'symbol': symbol,
                'interval': interval,
                'indicators': [
                    {'id': 'rsi', 'indicator': 'rsi', 'period': 14},
                    {'id': 'macd', 'indicator': 'macd', 'fast_period': 12, 'slow_period': 26, 'signal_period': 9},
                    {'id': 'bbands', 'indicator': 'bbands', 'period': 20, 'stddev': 2.0},
                    {'id': 'stoch', 'indicator': 'stoch', 'k_period': 14, 'd_period': 3},
                    {'id': 'willr', 'indicator': 'willr', 'period': 14},
                    {'id': 'ema_20', 'indicator': 'ema', 'period': 20},
                    {'id': 'ema_50', 'indicator': 'ema', 'period': 50},
                    {'id': 'sma_20', 'indicator': 'sma', 'period': 20},
                    {'id': 'adx', 'indicator': 'adx', 'period': 14},
                    {'id': 'cci', 'indicator': 'cci', 'period': 20}
                ]
            }
        }
        
        try:
            bulk_result = self._make_bulk_request(bulk_payload)
            
            if 'error' in bulk_result:
                logger.warning(f"⚠️ Bulk API error: {bulk_result['error']}")
                # Fallback to individual requests if bulk fails
                return self._fallback_comprehensive_analysis(symbol, interval)
            
            # Process bulk results
            if 'data' in bulk_result:
                for item in bulk_result['data']:
                    indicator_id = item.get('id', '').split('_')[-1]  # Extract indicator name from ID
                    if 'result' in item and not item.get('errors'):
                        analysis['indicators'][indicator_id] = item['result']
                        logger.info(f"✅ {indicator_id.upper()}: {item['result']}")
                    else:
                        logger.warning(f"⚠️ {indicator_id} error: {item.get('errors', 'Unknown error')}")
            
            # Generate signals and summary
            analysis['signals'] = self._generate_signals(analysis['indicators'])
            analysis['summary'] = self._generate_summary(analysis['indicators'], analysis['signals'])
            
        except Exception as e:
            logger.error(f"❌ Error in bulk comprehensive analysis: {e}")
            return self._fallback_comprehensive_analysis(symbol, interval)
        
        return analysis
    
    def _fallback_comprehensive_analysis(self, symbol: str, interval: str = "1h") -> Dict[str, Any]:
        """Fallback to individual API calls if bulk fails"""
        logger.info(f"🔄 Using fallback individual requests for {symbol}")
        
        analysis = {
            'symbol': symbol,
            'interval': interval,
            'timestamp': datetime.now().isoformat(),
            'indicators': {},
            'signals': {},
            'summary': {}
        }
        
        # Core indicators with fallback approach
        indicators_to_fetch = [
            ('rsi', self.get_rsi),
            ('macd', self.get_macd),
            ('bbands', self.get_bollinger_bands),
            ('stoch', self.get_stochastic),
            ('willr', self.get_williams_r),
            ('ema_20', lambda s, i: self.get_ema(s, i, 20)),
            ('ema_50', lambda s, i: self.get_ema(s, i, 50)),
            ('sma_20', lambda s, i: self.get_sma(s, i, 20)),
            ('adx', self.get_adx),
            ('cci', self.get_cci)
        ]
        
        for indicator_name, fetch_func in indicators_to_fetch:
            try:
                result = fetch_func(symbol, interval)
                if 'error' not in result:
                    analysis['indicators'][indicator_name] = result
                    logger.info(f"✅ {indicator_name.upper()}: {result}")
                else:
                    logger.warning(f"⚠️ {indicator_name} error: {result['error']}")
            except Exception as e:
                logger.error(f"❌ Error fetching {indicator_name}: {e}")
        
        # Generate signals
        analysis['signals'] = self._generate_signals(analysis['indicators'])
        analysis['summary'] = self._generate_summary(analysis['indicators'], analysis['signals'])
        
        return analysis
    
    def _generate_signals(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals from indicators"""
        signals = {
            'bullish_signals': [],
            'bearish_signals': [],
            'neutral_signals': [],
            'strength': 'neutral'
        }
        
        # RSI signals
        if 'rsi' in indicators and 'value' in indicators['rsi']:
            rsi_val = indicators['rsi']['value']
            if rsi_val < 30:
                signals['bullish_signals'].append(f"RSI oversold ({rsi_val:.1f})")
            elif rsi_val > 70:
                signals['bearish_signals'].append(f"RSI overbought ({rsi_val:.1f})")
            else:
                signals['neutral_signals'].append(f"RSI neutral ({rsi_val:.1f})")
        
        # MACD signals
        if 'macd' in indicators:
            macd_data = indicators['macd']
            if 'macd' in macd_data and 'signal' in macd_data:
                macd_line = macd_data['macd']
                signal_line = macd_data['signal']
                if macd_line > signal_line:
                    signals['bullish_signals'].append("MACD bullish crossover")
                else:
                    signals['bearish_signals'].append("MACD bearish crossover")
        
        # Bollinger Bands signals
        if 'bbands' in indicators:
            bb_data = indicators['bbands']
            if all(k in bb_data for k in ['upper', 'middle', 'lower']):
                # Would need current price to determine position relative to bands
                signals['neutral_signals'].append("Bollinger Bands analysis available")
        
        # Stochastic signals
        if 'stoch' in indicators:
            stoch_data = indicators['stoch']
            if 'k' in stoch_data and 'd' in stoch_data:
                k_val = stoch_data['k']
                if k_val < 20:
                    signals['bullish_signals'].append(f"Stochastic oversold ({k_val:.1f})")
                elif k_val > 80:
                    signals['bearish_signals'].append(f"Stochastic overbought ({k_val:.1f})")
        
        # Williams %R signals
        if 'willr' in indicators and 'value' in indicators['willr']:
            willr_val = indicators['willr']['value']
            if willr_val < -80:
                signals['bullish_signals'].append(f"Williams %R oversold ({willr_val:.1f})")
            elif willr_val > -20:
                signals['bearish_signals'].append(f"Williams %R overbought ({willr_val:.1f})")
        
        # ADX trend strength
        if 'adx' in indicators and 'value' in indicators['adx']:
            adx_val = indicators['adx']['value']
            if adx_val > 25:
                signals['neutral_signals'].append(f"Strong trend (ADX: {adx_val:.1f})")
            else:
                signals['neutral_signals'].append(f"Weak trend (ADX: {adx_val:.1f})")
        
        # Overall strength assessment
        bullish_count = len(signals['bullish_signals'])
        bearish_count = len(signals['bearish_signals'])
        
        if bullish_count > bearish_count + 1:
            signals['strength'] = 'bullish'
        elif bearish_count > bullish_count + 1:
            signals['strength'] = 'bearish'
        else:
            signals['strength'] = 'neutral'
        
        return signals
    
    def _generate_summary(self, indicators: Dict[str, Any], signals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary"""
        summary = {
            'overall_sentiment': signals['strength'],
            'key_levels': {},
            'recommendations': [],
            'risk_assessment': 'medium'
        }
        
        # Key recommendations based on signals
        if signals['strength'] == 'bullish':
            summary['recommendations'].append("Consider long positions")
            summary['recommendations'].append("Look for entry opportunities on dips")
        elif signals['strength'] == 'bearish':
            summary['recommendations'].append("Consider taking profits")
            summary['recommendations'].append("Avoid new long positions")
        else:
            summary['recommendations'].append("Wait for clearer signals")
            summary['recommendations'].append("Monitor key support/resistance levels")
        
        # Extract key levels from Bollinger Bands
        if 'bbands' in indicators:
            bb_data = indicators['bbands']
            if all(k in bb_data for k in ['upper', 'middle', 'lower']):
                summary['key_levels'] = {
                    'resistance': bb_data['upper'],
                    'middle': bb_data['middle'],
                    'support': bb_data['lower']
                }
        
        return summary

    def get_multiple_timeframes(self, symbol: str, timeframes: List[str] = None) -> Dict[str, Any]:
        """Get analysis across multiple timeframes"""
        if timeframes is None:
            timeframes = ["15m", "1h", "4h", "1d"]
        
        multi_tf_analysis = {
            'symbol': symbol,
            'timeframes': {},
            'consensus': {}
        }
        
        for tf in timeframes:
            logger.info(f"📊 Analyzing {symbol} on {tf} timeframe")
            analysis = self.get_comprehensive_analysis(symbol, tf)
            multi_tf_analysis['timeframes'][tf] = analysis
        
        # Generate consensus
        multi_tf_analysis['consensus'] = self._generate_consensus(multi_tf_analysis['timeframes'])
        
        return multi_tf_analysis
    
    def _generate_consensus(self, timeframe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consensus view across timeframes"""
        consensus = {
            'overall_bias': 'neutral',
            'strength_score': 0,
            'agreement_level': 'low'
        }
        
        sentiments = []
        for tf, data in timeframe_data.items():
            if 'summary' in data and 'overall_sentiment' in data['summary']:
                sentiments.append(data['summary']['overall_sentiment'])
        
        if sentiments:
            bullish_count = sentiments.count('bullish')
            bearish_count = sentiments.count('bearish')
            neutral_count = sentiments.count('neutral')
            
            total = len(sentiments)
            if bullish_count / total > 0.6:
                consensus['overall_bias'] = 'bullish'
                consensus['strength_score'] = bullish_count / total
                consensus['agreement_level'] = 'high' if bullish_count / total > 0.75 else 'medium'
            elif bearish_count / total > 0.6:
                consensus['overall_bias'] = 'bearish'
                consensus['strength_score'] = bearish_count / total
                consensus['agreement_level'] = 'high' if bearish_count / total > 0.75 else 'medium'
        
        return consensus
    
    def get_custom_bulk_analysis(self, symbol: str, interval: str, custom_indicators: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get custom bulk analysis with user-specified indicators"""
        logger.info(f"🔍 Fetching custom bulk analysis for {symbol} with {len(custom_indicators)} indicators")
        
        analysis = {
            'symbol': symbol,
            'interval': interval,
            'timestamp': datetime.now().isoformat(),
            'indicators': {},
            'signals': {},
            'summary': {}
        }
        
        # Use bulk API with custom indicators
        bulk_payload = {
            'construct': {
                'exchange': 'binance',
                'symbol': symbol,
                'interval': interval,
                'indicators': custom_indicators
            }
        }
        
        try:
            bulk_result = self._make_bulk_request(bulk_payload)
            
            if 'error' in bulk_result:
                logger.warning(f"⚠️ Custom bulk API error: {bulk_result['error']}")
                return {'error': bulk_result['error'], 'fallback_available': False}
            
            # Process bulk results
            if 'data' in bulk_result:
                for item in bulk_result['data']:
                    indicator_id = item.get('id', 'unknown')
                    if 'result' in item and not item.get('errors'):
                        analysis['indicators'][indicator_id] = item['result']
                        logger.info(f"✅ {indicator_id}: {item['result']}")
                    else:
                        logger.warning(f"⚠️ {indicator_id} error: {item.get('errors', 'Unknown error')}")
            
            # Generate signals and summary if we have indicators
            if analysis['indicators']:
                analysis['signals'] = self._generate_signals(analysis['indicators'])
                analysis['summary'] = self._generate_summary(analysis['indicators'], analysis['signals'])
            
        except Exception as e:
            logger.error(f"❌ Error in custom bulk analysis: {e}")
            return {'error': str(e), 'fallback_available': False}
        
        return analysis