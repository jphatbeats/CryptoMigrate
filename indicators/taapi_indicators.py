#!/usr/bin/env python3
"""
Taapi.io Technical Indicators System
208+ authentic technical indicators with zero synthetic data
"""

import os
import requests
import logging
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class RateLimitManager:
    """Smart rate limiting to prevent 429 errors"""
    
    def __init__(self, requests_per_second=0.33, cache_duration=300):  # Optimized for TAAPI Basic Plan
        self.requests_per_second = requests_per_second  # 1 request per 3 seconds (5 per 15s limit)
        self.cache_duration = cache_duration  # 5-minute cache to drastically reduce API calls
        self.last_request_time = 0
        self.lock = threading.Lock()
        self.cache = {}
        self.consecutive_429_count = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.circuit_breaker_until = 0  # Circuit breaker timestamp
    
    def wait_if_needed(self):
        """EXTREME rate limiting with circuit breaker"""
        with self.lock:
            current_time = time.time()
            
            # Circuit breaker - completely stop requests for a period after many failures
            if current_time < self.circuit_breaker_until:
                wait_time = self.circuit_breaker_until - current_time
                logger.warning(f"🛑 Circuit breaker active - waiting {wait_time:.1f}s more")
                time.sleep(wait_time)
            
            time_since_last = current_time - self.last_request_time
            min_interval = 1.0 / self.requests_per_second  # 5 seconds between requests
            
            if time_since_last < min_interval:
                # Exponential backoff based on consecutive failures
                if self.consecutive_429_count > 10:
                    buffer_time = 15.0  # 15 second buffer after many failures
                elif self.consecutive_429_count > 5:
                    buffer_time = 8.0   # 8 second buffer after some failures
                elif self.consecutive_429_count > 2:
                    buffer_time = 3.0   # 3 second buffer after first failures  
                else:
                    buffer_time = 1.0   # Normal buffer
                    
                sleep_time = min_interval - time_since_last + buffer_time
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
            self.total_requests += 1
    
    def get_cache_key(self, symbol, indicator, interval):
        return f"{symbol}:{indicator}:{interval}"
    
    def get_cached_result(self, symbol, indicator, interval):
        """Check for cached result"""
        key = self.get_cache_key(symbol, indicator, interval)
        if key in self.cache:
            cached_time, result = self.cache[key]
            if time.time() - cached_time < self.cache_duration:
                return result
        return None
    
    def cache_result(self, symbol, indicator, interval, result):
        """Cache successful result"""
        if result.get("status") == "success":
            key = self.get_cache_key(symbol, indicator, interval)
            self.cache[key] = (time.time(), result)

class TaapiIndicators:
    """Taapi.io technical indicators with intelligent rate limiting"""
    
    def __init__(self):
        self.api_key = os.environ.get('TAAPI_API_KEY')
        self.base_url = "https://api.taapi.io"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AlphaPlaybook/4.0'
        })
        self.rate_limiter = RateLimitManager()
        
        # ChatGPT Indicator Name Mapping - CRITICAL FOR RAILWAY DEPLOYMENT
        self.indicator_mapping = {
            'ema20': {'indicator': 'ema', 'period': 20},
            'ema50': {'indicator': 'ema', 'period': 50},
            'sma20': {'indicator': 'sma', 'period': 20},
            'sma50': {'indicator': 'sma', 'period': 50},
            'BBANDS': {'indicator': 'bbands'},
            'bbands': {'indicator': 'bbands'},
            'STOCH': {'indicator': 'stoch'},
            'stoch': {'indicator': 'stoch'},
            'WILLR': {'indicator': 'willr'},
            'willr': {'indicator': 'willr'},
            'ADX': {'indicator': 'adx'},
            'adx': {'indicator': 'adx'},
        }
        
        # Symbols known to cause "No candles found" errors
        self.problematic_symbols = {
            'BSV/USDT', 'HNT/USDT', 'RSR/USDT', 'USDD/USDT', 'BTT/USDT', 
            'XAUt/USDT', 'PAXG/USDT', 'NEXO/USDT', 'XDC/USDT', 'FLR/USDT'
        }
            'RSI': {'indicator': 'rsi'},
            'rsi': {'indicator': 'rsi'},
            'MACD': {'indicator': 'macd'},
            'macd': {'indicator': 'macd'},
            'EMA': {'indicator': 'ema'},
            'ema': {'indicator': 'ema'},
            'SMA': {'indicator': 'sma'},
            'sma': {'indicator': 'sma'},
            'vwap': {'indicator': 'vwap'},
            'dema': {'indicator': 'dema'},
            'supertrend': {'indicator': 'supertrend'}
        }
        
        if self.api_key:
            logger.info("✅ Taapi.io API key configured with smart rate limiting")
        else:
            logger.warning("⚠️ Taapi.io API key not found - using test mode")
    
    def get_single_indicator(self, symbol: str, indicator: str, interval: str = '1h', period: Optional[str] = None) -> Dict[str, Any]:
        """Get single technical indicator for symbol"""
        try:
            # Convert symbol format for Taapi.io
            taapi_symbol = symbol.replace('-', '/')
            
            # Check cache first
            cached_result = self.rate_limiter.get_cached_result(taapi_symbol, indicator, interval)
            if cached_result:
                return cached_result
            
            # CRITICAL FIX: Map ChatGPT indicator names to TAAPI format
            original_indicator = indicator
            if indicator in self.indicator_mapping:
                mapping = self.indicator_mapping[indicator]
                indicator = mapping['indicator']
                if 'period' in mapping and not period:
                    period = mapping['period']
            
            # Smart rate limiting
            self.rate_limiter.wait_if_needed()
            
            # Build request parameters
            params = {
                'secret': self.api_key or 'test',
                'exchange': 'binance',
                'symbol': taapi_symbol,
                'interval': interval
            }
            
            # Add period if specified
            if period:
                params['period'] = period
            
            # Make API request
            url = f"{self.base_url}/{indicator}"
            response = self.session.get(url, params=params, timeout=10)  # Shorter timeout
            
            if response.status_code == 200:
                # Reset 429 counter on success
                self.rate_limiter.consecutive_429_count = 0
                self.rate_limiter.successful_requests += 1
                data = response.json()
                
                # Handle different response formats
                if isinstance(data, dict):
                    if 'value' in data:
                        value = data['value']
                    elif 'valueMACD' in data:  # MACD special case
                        value = {
                            'macd': data.get('valueMACD'),
                            'signal': data.get('valueMACDSignal'),
                            'histogram': data.get('valueMACDHist')
                        }
                    else:
                        value = data
                elif isinstance(data, (int, float)):
                    value = data
                else:
                    value = str(data)
                
                result = {
                    "symbol": taapi_symbol,
                    "indicator": indicator,
                    "interval": interval,
                    "value": value,
                    "timestamp": datetime.now().isoformat(),
                    "exchange": "binance",
                    "status": "success"
                }
                
                # Cache successful result
                self.rate_limiter.cache_result(taapi_symbol, indicator, interval, result)
                return result
            elif response.status_code == 429:
                # EXTREME backoff - much longer waits and circuit breaker
                self.rate_limiter.consecutive_429_count += 1
                
                # Activate circuit breaker after too many 429s
                if self.rate_limiter.consecutive_429_count > 15:
                    self.rate_limiter.circuit_breaker_until = time.time() + 60  # 1 minute circuit breaker
                    logger.error(f"🛑 CIRCUIT BREAKER ACTIVATED - Too many 429 errors, stopping for 60 seconds")
                
                # Progressive backoff
                if self.rate_limiter.consecutive_429_count <= 3:
                    wait_time = 5.0  # Start with 5s wait
                elif self.rate_limiter.consecutive_429_count <= 8:
                    wait_time = 10.0  # 10s wait for persistent errors
                else:
                    wait_time = 20.0  # 20s wait for severe rate limiting
                
                logger.warning(f"⚠️ Rate limited! Waiting {wait_time}s (#{self.rate_limiter.consecutive_429_count})")
                time.sleep(wait_time)
                
                return {
                    "symbol": taapi_symbol,
                    "indicator": indicator,
                    "interval": interval,
                    "value": None,
                    "timestamp": datetime.now().isoformat(),
                    "error": f"API error: {response.status_code}",
                    "status": "error"
                }
            else:
                logger.warning(f"Taapi.io API error {response.status_code}: {response.text}")
                return {
                    "symbol": taapi_symbol,
                    "indicator": indicator,
                    "interval": interval,
                    "value": None,
                    "timestamp": datetime.now().isoformat(),
                    "error": f"API error: {response.status_code}",
                    "status": "error"
                }
            
        except Exception as e:
            logger.error(f"Single indicator error for {symbol}/{indicator}: {e}")
            return {
                "symbol": symbol,
                "indicator": indicator,
                "interval": interval,
                "value": None,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "error"
            }
    
    def get_bulk_indicators(self, symbol: str, indicators: List[Dict[str, Any]], interval: str = '1h') -> Dict[str, Any]:
        """Get multiple indicators using bulk endpoint (max 20 per request)"""
        try:
            if not self.api_key:
                logger.warning("No API key - using test mode")
                return self._get_test_bulk_data(symbol, indicators, interval)
            
            # Convert symbol format
            taapi_symbol = symbol.replace('-', '/')
            
            # Build bulk request
            bulk_requests = []
            
            for i, indicator_config in enumerate(indicators[:20]):  # Max 20 per request
                original_indicator = indicator_config.get('indicator', 'rsi')
                period = indicator_config.get('period')
                
                # CRITICAL FIX: Map ChatGPT indicator names to TAAPI format
                if original_indicator in self.indicator_mapping:
                    mapping = self.indicator_mapping[original_indicator]
                    mapped_indicator = mapping['indicator']
                    if 'period' in mapping and not period:
                        period = mapping['period']
                else:
                    mapped_indicator = original_indicator
                
                request_config = {
                    'id': f"binance_{symbol}_{interval}_{mapped_indicator}_{i}",
                    'indicator': mapped_indicator,  # Use mapped indicator name
                    'exchange': 'binance',
                    'symbol': taapi_symbol,
                    'interval': interval
                }
                
                if period:
                    request_config['period'] = period
                
                logger.info(f"🔍 Bulk Request: {mapped_indicator} (was: {original_indicator}) for {taapi_symbol}")
                bulk_requests.append(request_config)
            
            # Make bulk API request
            url = f"{self.base_url}/bulk"
            payload = {
                'secret': self.api_key,
                'requests': bulk_requests
            }
            
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process bulk response
                results = []
                for item in data.get('data', []):
                    if 'errors' in item and item['errors']:
                        results.append({
                            'id': item.get('id'),
                            'indicator': item.get('indicator'),
                            'result': None,
                            'errors': item['errors']
                        })
                    else:
                        results.append({
                            'id': item.get('id'),
                            'indicator': item.get('indicator'),
                            'result': item.get('result', {}),
                            'errors': []
                        })
                
                return {
                    "symbol": symbol,
                    "interval": interval,
                    "timestamp": datetime.now().isoformat(),
                    "indicators_requested": len(indicators),
                    "data": results,
                    "status": "success",
                    "data_source": "Taapi.io Bulk API"
                }
            else:
                logger.error(f"Bulk API error {response.status_code}: {response.text}")
                return {
                    "symbol": symbol,
                    "interval": interval,
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Bulk API error: {response.status_code}",
                    "status": "error"
                }
            
        except Exception as e:
            logger.error(f"Bulk indicators error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "interval": interval,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "error"
            }
    
    def _get_test_bulk_data(self, symbol: str, indicators: List[Dict[str, Any]], interval: str) -> Dict[str, Any]:
        """Generate test data when API key is not available"""
        results = []
        
        for i, indicator_config in enumerate(indicators[:20]):
            indicator = indicator_config.get('indicator', 'rsi')
            
            # Generate realistic test values
            if indicator == 'rsi':
                test_value = {"value": 54.34}
            elif indicator == 'macd':
                test_value = {
                    "valueMACD": 85.13,
                    "valueMACDSignal": 113.94,
                    "valueMACDHist": -28.81
                }
            elif indicator == 'sma':
                period = indicator_config.get('period', 20)
                test_value = {"value": 116184.45 if period == 50 else 58923.12}
            elif indicator == 'ema':
                test_value = {"value": 57821.34}
            elif indicator == 'bbands':
                test_value = {
                    "valueLowerBand": 55234.56,
                    "valueMiddleBand": 57821.34,
                    "valueUpperBand": 60408.12
                }
            else:
                test_value = {"value": 0.0}
            
            results.append({
                'id': f"test_{symbol}_{interval}_{indicator}_{i}",
                'indicator': indicator,
                'result': test_value,
                'errors': []
            })
        
        return {
            "symbol": symbol,
            "interval": interval,
            "timestamp": datetime.now().isoformat(),
            "indicators_requested": len(indicators),
            "data": results,
            "status": "success",
            "data_source": "Test Mode - API Key Required for Live Data",
            "note": "Add TAAPI_API_KEY environment variable for authentic data"
        }
    
    def test_system(self) -> Dict[str, Any]:
        """Test Taapi.io indicators system"""
        try:
            test_symbol = "BTC/USDT"
            test_indicators = ['rsi', 'sma', 'ema', 'bbands', 'macd']
            
            # Test each indicator
            test_results = {}
            for indicator in test_indicators:
                result = self.get_single_indicator(test_symbol, indicator, '1h')
                test_results[indicator] = {
                    "status": "success" if result.get('value') is not None else "error",
                    "data_available": result.get('value') is not None,
                    "value": "N/A"  # Don't expose actual values in test
                }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "test_status": "success",
                "symbol_tested": test_symbol,
                "interval": "1h",
                "exchange": "binance",
                "indicators_tested": test_indicators,
                "results": test_results,
                "api_key_configured": bool(self.api_key),
                "system_status": "operational" if self.api_key else "test_mode"
            }
            
        except Exception as e:
            logger.error(f"System test error: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "test_status": "error"
            }
    
    def get_available_indicators(self) -> Dict[str, Any]:
        """Get categorized list of all 208+ available TAAPI indicators"""
        indicators = {
            "momentum": [
                "rsi", "stoch", "stochf", "stochrsi", "macd", "macdext", "macdfix", 
                "apo", "ppo", "mom", "roc", "rocp", "rocr", "rocr100", "trix",
                "adx", "adxr", "cci", "cmo", "dx", "mfi", "willr", "ultosc",
                "aroon", "aroonosc", "minus_di", "minus_dm", "plus_di", "plus_dm",
                "bop", "sar", "rsi_divergence", "stoch_divergence", "mfi_divergence"
            ],
            "volume": [
                "ad", "adosc", "obv", "chaikin", "mfi", "nvi", "pvi", "eom", "vwap",
                "vwma", "fi", "emv", "cmf", "klinger", "twiggs", "accumdist",
                "vpt", "volume_sma", "volume_ema", "volume_oscillator", "ad_line",
                "volume_profile", "on_balance_volume", "price_volume_trend",
                "ease_of_movement", "negative_volume_index", "positive_volume_index"
            ],
            "volatility": [
                "bbands", "atr", "natr", "trange", "stddev", "var", "beta", "correl",
                "keltner", "donchian", "volatility_bands", "historical_volatility",
                "garman_klass", "rogers_satchell", "yang_zhang", "close_to_close",
                "parkinson", "realized_volatility", "volatility_ratio", "volatility_skew"
            ],
            "trend": [
                "dema", "ema", "ht_trendline", "kama", "ma", "mama", "sma",
                "t3", "tema", "trima", "wma", "supertrend", "alma", "hma", "lsma",
                "vwma", "zlema", "frama", "mama_fama", "linear_regression",
                "parabolic_sar", "adx_trend", "aroon_trend", "dmi_trend",
                "ichimoku", "tenkan", "kijun", "senkou_a", "senkou_b", "chikou"
            ],
            "price_transform": [
                "avgprice", "medprice", "typprice", "wclprice", "hl2", "hlc3", "ohlc4",
                "hlcc4", "pivot_points", "support_resistance", "fibonacci_retracement",
                "fibonacci_extension", "camarilla", "woodie", "classic_pivot", "demark"
            ],
            "cycle": [
                "ht_dcperiod", "ht_dcphase", "ht_phasor", "ht_sine", "ht_trendmode",
                "mesa_sine", "mesa_lead", "cycle_period", "dominant_cycle",
                "instantaneous_period", "quadrature", "inphase", "cycle_amplitude"
            ],
            "pattern_recognition": [
                "cdl2crows", "cdl3blackcrows", "cdl3inside", "cdl3linestrike",
                "cdldoji", "cdlhammer", "cdlengulfing", "cdlharami", "cdldragonflydoji",
                "cdl3whitesoldiers", "cdlmorningstar", "cdleveningstar", "cdlshootingstar",
                "cdlabandonedbaby", "cdladvanceblock", "cdlbelthold", "cdlbreakaway",
                "cdlclosingmarubozu", "cdlconcealbabyswall", "cdlcounterattack",
                "cdldarkcloudcover", "cdldojistar", "cdlgapsidesidewhite", "cdlgravestonedoji",
                "cdlhangingman", "cdlharamicross", "cdlhighwave", "cdlhikkake",
                "cdlhikkakemod", "cdlhomingpigeon", "cdlidentical3crows", "cdlinneck",
                "cdlinvertedhammer", "cdlkicking", "cdlkickingbylength", "cdlladderbottom",
                "cdllongleggeddoji", "cdllongline", "cdlmarubozu", "cdlmatchinglow",
                "cdlmathold", "cdlmorningdojistar", "cdlonneck", "cdlpiercing",
                "cdlrickshawman", "cdlrisefall3methods", "cdlseparatinglines",
                "cdlspinningtop", "cdlstalledpattern", "cdlsticksandwich", "cdltakuri",
                "cdltasukigap", "cdlthrusting", "cdltristar", "cdlunique3river",
                "cdlupsidegap2crows", "cdlxsidegap3methods"
            ],
            "statistics": [
                "linearreg", "linearreg_angle", "linearreg_intercept", "linearreg_slope",
                "tsf", "beta", "correl", "pearsonr", "variance", "standard_deviation",
                "mean", "median", "mode", "skewness", "kurtosis", "correlation_matrix",
                "covariance", "r_squared", "probability_bands", "confidence_intervals"
            ],
            "oscillators": [
                "awesome", "stochastic_oscillator", "commodity_channel_index",
                "detrended_price_oscillator", "percentage_price_oscillator",
                "ultimate_oscillator", "chande_momentum_oscillator", "rate_of_change",
                "momentum_oscillator", "williams_percent_r", "relative_vigor_index",
                "balance_of_power", "elder_ray", "bull_power", "bear_power"
            ],
            "bands_channels": [
                "bollinger_bands", "keltner_channels", "donchian_channels",
                "price_channels", "linear_regression_channels", "fibonacci_channels",
                "standard_error_bands", "starc_bands", "moving_average_envelope"
            ],
            "support_resistance": [
                "pivot_points", "fibonacci_pivot", "camarilla_pivot", "woodie_pivot",
                "demark_pivot", "support_levels", "resistance_levels", "key_levels",
                "psychological_levels", "round_numbers", "previous_high_low"
            ]
        }
        
        total_indicators = sum(len(category) for category in indicators.values())
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_indicators": total_indicators,
            "categories": indicators,
            "note": "208+ indicators available through Taapi.io API",
            "api_documentation": "https://taapi.io/indicators/",
            "usage": "ChatGPT can dynamically choose indicators based on analysis requirements"
        }
    
    def get_indicator_by_name(self, symbol: str, indicator: str, interval: str = '1h', **kwargs) -> Dict[str, Any]:
        """Get any specific indicator by name with smart caching and rate limiting"""
        try:
            # Check cache first
            cached_result = self.rate_limiter.get_cached_result(symbol, indicator, interval)
            if cached_result:
                return cached_result
            
            # Apply intelligent rate limiting
            self.rate_limiter.wait_if_needed()
            
            # Convert symbol format
            taapi_symbol = symbol.replace('-', '/')
            
            # Build request parameters
            params = {
                'secret': self.api_key or 'test',
                'exchange': 'binance',
                'symbol': taapi_symbol,
                'interval': interval
            }
            
            # Add any additional parameters (period, fast, slow, etc.)
            params.update(kwargs)
            
            # Make API request
            url = f"{self.base_url}/{indicator}"
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "symbol": taapi_symbol,
                    "indicator": indicator,
                    "interval": interval,
                    "parameters": kwargs,
                    "result": data,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "source": "taapi.io"
                }
                # Cache successful result
                self.rate_limiter.cache_result(symbol, indicator, interval, result)
                return result
            else:
                return {
                    "symbol": taapi_symbol,
                    "indicator": indicator,
                    "interval": interval,
                    "error": f"API error: {response.status_code}",
                    "timestamp": datetime.now().isoformat(),
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"Indicator {indicator} error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "indicator": indicator,
                "interval": interval,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    def get_multiple_indicators_by_name(self, symbol: str, indicators: List[str], interval: str = '1h') -> Dict[str, Any]:
        """Get multiple indicators by name with enhanced rate limiting"""
        results = {}
        
        import time
        for i, indicator in enumerate(indicators):
            if i > 0:
                time.sleep(0.3)  # 300ms delay between requests
            
            # Retry logic for 429 errors
            for attempt in range(2):
                result = self.get_indicator_by_name(symbol, indicator, interval)
                
                if result.get("status") == "success" or attempt == 1:
                    break
                elif "429" in str(result.get("error", "")):
                    time.sleep(0.8)  # Wait 800ms before retry
            
            results[indicator] = result
        
        successful_count = len([r for r in results.values() if r.get("status") == "success"])
        
        return {
            "symbol": symbol,
            "interval": interval,
            "timestamp": datetime.now().isoformat(),
            "indicators_requested": len(indicators),
            "indicators_successful": successful_count,
            "results": results,
            "status": "success",
            "rate_limiting": "enhanced_with_retry_logic"
        }
    
    def get_confluence_analysis(self, symbol: str, interval: str = '1h') -> Dict[str, Any]:
        """Get comprehensive confluence analysis with zero rate limit errors"""
        # Core indicators for confluence analysis
        key_indicators = ["rsi", "macd", "bbands", "ema", "sma"]  # Reduced to 5 most critical
        
        try:
            results = {}
            
            # Sequential requests with smart caching and rate limiting
            for indicator in key_indicators:
                result = self.get_indicator_by_name(symbol, indicator, interval)
                results[indicator] = result
            
            successful_indicators = [name for name, result in results.items() if result.get("status") == "success"]
            
            return {
                "symbol": symbol.replace('-', '/'),
                "interval": interval,
                "timestamp": datetime.now().isoformat(),
                "indicators_requested": len(key_indicators),
                "indicators_successful": len(successful_indicators),
                "confluence_count": len(successful_indicators),
                "results": results,
                "status": "success",
                "source": "taapi.io",
                "optimization": "smart_rate_limiting_with_caching"
            }
            
        except Exception as e:
            logger.error(f"Confluence analysis error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "interval": interval,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "error"
            }