"""
Fixed get_indicator_by_name function for Railway TAAPI deployment
Handles ChatGPT invalid indicator names and maps them to correct TAAPI format
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_indicator_by_name(taapi_instance, symbol: str, indicator_name: str, interval: str = '1h') -> Dict[str, Any]:
    """
    Get indicator by name with ChatGPT compatibility
    Maps invalid indicator names like 'ema20', 'SMA50' to correct TAAPI format
    """
    try:
        # ChatGPT sends these invalid names - map them to correct TAAPI format
        indicator_fixes = {
            'ema20': {'indicator': 'ema', 'period': 20},
            'ema50': {'indicator': 'ema', 'period': 50},
            'sma20': {'indicator': 'sma', 'period': 20},
            'sma50': {'indicator': 'sma', 'period': 50},
            'EMA20': {'indicator': 'ema', 'period': 20},
            'SMA50': {'indicator': 'sma', 'period': 50},
            'BBANDS': {'indicator': 'bbands'},
            'STOCH': {'indicator': 'stoch'},
            'WILLR': {'indicator': 'willr'},
            'ADX': {'indicator': 'adx'},
            'RSI': {'indicator': 'rsi'},
            'MACD': {'indicator': 'macd'},
        }
        
        original_name = indicator_name
        period = None
        
        # Fix invalid indicator names
        if indicator_name in indicator_fixes:
            fix = indicator_fixes[indicator_name]
            indicator_name = fix['indicator']
            period = fix.get('period')
            logger.info(f"🔧 Fixed indicator: {original_name} → {indicator_name}" + (f" (period={period})" if period else ""))
        else:
            # Ensure lowercase for valid indicators
            indicator_name = indicator_name.lower()
        
        # Call the corrected TAAPI function
        result = taapi_instance.get_single_indicator(symbol, indicator_name, interval, period)
        
        if result.get('status') == 'success':
            # CRITICAL FIX: Return the entire result object, not just 'value'
            return {
                "status": "success",
                "result": result.get('result', result.get('value', {})),  # Handle both formats
                "symbol": symbol,
                "indicator": indicator_name,
                "original_request": original_name,
                "interval": interval,
                "timestamp": result.get('timestamp')
            }
        else:
            logger.warning(f"⚠️ {original_name} API error: {result.get('error', 'Unknown error')}")
            return {
                "status": "error",
                "error": result.get('error', 'Failed to fetch indicator'),
                "symbol": symbol,
                "indicator": indicator_name,
                "original_request": original_name
            }
            
    except Exception as e:
        logger.error(f"❌ Indicator error for {original_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "symbol": symbol,
            "indicator": indicator_name,
            "original_request": original_name
        }