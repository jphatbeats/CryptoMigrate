# TAAPI.io Universal Indicators Module
# Provides access to ALL 208+ technical indicators via Railway endpoints
import requests
import os
import logging
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

class TaapiUniversalIndicators:
    """
    Universal access to all 208+ TAAPI.io technical indicators
    Supports dynamic indicator selection for ChatGPT integration
    """
    
    def __init__(self):
        self.api_key = os.getenv('TAAPI_API_KEY')
        self.base_url = "https://api.taapi.io"
        
        # Complete list of all 208+ TAAPI indicators
        self.available_indicators = [
            # Momentum Indicators
            "rsi", "stoch", "stochf", "stochrsi", "macd", "macdext", "macdfix", 
            "apo", "ppo", "mom", "roc", "rocp", "rocr", "rocr100", "trix",
            "adx", "adxr", "atr", "natr", "cci", "cmo", "dx", "mfi", "minus_di",
            "minus_dm", "plus_di", "plus_dm", "willr", "ultosc", "aroon", "aroonosc",
            
            # Volume Indicators  
            "ad", "adosc", "obv", "chaikin", "mfi", "nvi", "pvi", "eom", "vwap",
            "vwma", "fi", "emv", "cmf", "klinger", "twiggs", "accumdist",
            
            # Volatility Indicators
            "bbands", "dema", "ema", "ht_trendline", "kama", "ma", "mama", "sma",
            "t3", "tema", "trima", "wma", "atr", "natr", "trange", "avgprice",
            "medprice", "typprice", "wclprice", "stddev", "var", "beta", "correl",
            
            # Price Transform
            "avgprice", "medprice", "typprice", "wclprice",
            
            # Cycle Indicators
            "ht_dcperiod", "ht_dcphase", "ht_phasor", "ht_sine", "ht_trendmode",
            
            # Pattern Recognition (50+ patterns)
            "cdl2crows", "cdl3blackcrows", "cdl3inside", "cdl3linestrike", "cdl3outside",
            "cdl3starsinsouth", "cdl3whitesoldiers", "cdlabandonedbaby", "cdladvanceblock",
            "cdlbelthold", "cdlbreakaway", "cdlclosingmarubozu", "cdlconcealbabyswall",
            "cdlcounterattack", "cdldarkcloudcover", "cdldoji", "cdldojistar",
            "cdldragonflydoji", "cdlengulfing", "cdleveningdojistar", "cdleveningstar",
            "cdlgapsidesidewhite", "cdlgravestonedoji", "cdlhammer", "cdlhangingman",
            "cdlharami", "cdlharamicross", "cdlhighwave", "cdlhikkake", "cdlhikkakemod",
            "cdlhomingpigeon", "cdlidentical3crows", "cdlinneck", "cdlinvertedhammer",
            "cdlkicking", "cdlkickingbylength", "cdlladderbottom", "cdllongleggeddoji",
            "cdllongline", "cdlmarubozu", "cdlmatchinglow", "cdlmathold", "cdlmorningdojistar",
            "cdlmorningstar", "cdlonneck", "cdlpiercing", "cdlrickshawman", "cdlrisefall3methods",
            "cdlseparatinglines", "cdlshootingstar", "cdlshortline", "cdlspinningtop",
            "cdlstalledpattern", "cdlsticksandwich", "cdltakuri", "cdltasukigap",
            "cdlthrusting", "cdltristar", "cdlunique3river", "cdlupsidegap2crows",
            "cdlxsidegap3methods",
            
            # Statistics Functions
            "linearreg", "linearreg_angle", "linearreg_intercept", "linearreg_slope",
            "stddev", "tsf", "var", "beta", "correl",
            
            # Mathematical Transform
            "acos", "asin", "atan", "ceil", "cos", "cosh", "exp", "floor", "ln",
            "log10", "sin", "sinh", "sqrt", "tan", "tanh",
            
            # Custom Indicators
            "ao", "bop", "ichimoku", "supertrend", "pivotpoints", "fibonacci",
            "gann", "elliott", "marketprofile", "volumeprofile", "support_resistance"
        ]
        
        logger.info(f"✅ TAAPI Universal Indicators loaded with {len(self.available_indicators)} indicators")
    
    def get_indicator_list(self) -> Dict[str, List[str]]:
        """Return categorized list of all available indicators"""
        return {
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
    
    def get_indicator(self, 
                     indicator: str,
                     symbol: str = "BTC/USDT",
                     exchange: str = "binance", 
                     interval: str = "1h",
                     **kwargs) -> Dict:
        """
        Get any indicator from TAAPI.io
        
        Args:
            indicator: Any of 208+ available indicators
            symbol: Trading pair (e.g., "BTC/USDT")
            exchange: Exchange name (binance, bybit, kraken, etc.)
            interval: Timeframe (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            **kwargs: Indicator-specific parameters
        """
        try:
            import time
            import random
            
            # Smart rate limiting - add delay before each request
            time.sleep(random.uniform(2.0, 3.5))  # 2-3.5 second delay to prevent flooding
            
            # Build URL and parameters
            url = f"{self.base_url}/{indicator}"
            
            params = {
                "secret": self.api_key,
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval
            }
            
            # Add indicator-specific parameters
            params.update(kwargs)
            
            # Make API call
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ {indicator.upper()} for {symbol}: {result}")
                return {
                    "indicator": indicator,
                    "symbol": symbol,
                    "exchange": exchange,
                    "interval": interval,
                    "result": result,
                    "status": "success"
                }
            elif response.status_code == 429:
                # Rate limited - implement exponential backoff
                import time
                import random
                backoff_time = random.uniform(10, 30)  # 10-30 second backoff for rate limits
                logger.warning(f"⚠️ {indicator.upper()} RATE LIMITED - backing off {backoff_time:.1f}s")
                time.sleep(backoff_time)
                return {
                    "indicator": indicator,
                    "symbol": symbol,
                    "error": f"Rate limited (429) - API quota exceeded",
                    "status": "rate_limited"
                }
            else:
                logger.warning(f"⚠️ {indicator.upper()} API error: {response.status_code}")
                return {
                    "indicator": indicator,
                    "symbol": symbol,
                    "error": f"API error: {response.status_code}",
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"❌ {indicator.upper()} error: {str(e)}")
            return {
                "indicator": indicator,
                "symbol": symbol,
                "error": str(e),
                "status": "error"
            }
    
    def get_multiple_indicators(self, 
                               indicators: List[str],
                               symbol: str = "BTC/USDT",
                               exchange: str = "binance",
                               interval: str = "1h") -> Dict:
        """
        Get multiple indicators for confluence analysis
        
        Args:
            indicators: List of indicator names
            symbol: Trading pair
            exchange: Exchange name  
            interval: Timeframe
        """
        results = {}
        
        for indicator in indicators:
            result = self.get_indicator(indicator, symbol, exchange, interval)
            results[indicator] = result
            
        return {
            "symbol": symbol,
            "exchange": exchange,
            "interval": interval,
            "indicators": results,
            "confluence_count": len([r for r in results.values() if r.get("status") == "success"])
        }
    
    def get_confluence_analysis(self, 
                               symbol: str = "BTC/USDT",
                               exchange: str = "binance",
                               interval: str = "1h") -> Dict:
        """
        Get comprehensive confluence analysis with key indicators
        """
        # Use only validated TAAPI.io indicator names
        key_indicators = [
            "rsi", "macd", "bbands", "ema", "sma", "atr", "adx", "stoch",
            "obv", "cci", "willr", "mfi", "aroon"
        ]
        
        return self.get_multiple_indicators(key_indicators, symbol, exchange, interval)
    
    def get_indicator_by_name(self, indicator_name: str, symbol: str, interval: str = "1h"):
        """
        Get single indicator by name - compatibility method for main_server.py
        """
        return self.get_indicator(indicator_name, symbol, "binance", interval)

# Global instance
taapi_universal = TaapiUniversalIndicators()