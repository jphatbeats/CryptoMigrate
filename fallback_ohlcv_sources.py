#!/usr/bin/env python3
"""
Fallback OHLCV Data Sources
DexScreener and Coinalyze integration for when BingX fails
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class FallbackOHLCVSources:
    """Alternative OHLCV data sources when primary exchanges fail"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AlphaPlaybook/4.0',
            'Accept': 'application/json'
        })
        logger.info("✅ Fallback OHLCV sources initialized")
    
    def get_dexscreener_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 200) -> Dict[str, Any]:
        """
        Get OHLCV data from DexScreener API
        Works well for popular trading pairs
        """
        try:
            # Convert symbol format for DexScreener
            base_symbol = symbol.replace('/USDT', '').replace('-USDT', '')
            
            # DexScreener search endpoint
            search_url = f"https://api.dexscreener.com/latest/dex/search/?q={base_symbol}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('pairs') and len(data['pairs']) > 0:
                    # Find best matching pair (prefer major exchanges)
                    best_pair = None
                    for pair in data['pairs']:
                        if 'USDT' in pair.get('baseToken', {}).get('symbol', '').upper():
                            best_pair = pair
                            break
                    
                    if not best_pair:
                        best_pair = data['pairs'][0]  # Fallback to first pair
                    
                    # Convert DexScreener data to OHLCV format
                    current_price = float(best_pair.get('priceUsd', 0))
                    volume_24h = float(best_pair.get('volume', {}).get('h24', 0))
                    
                    # Generate approximate OHLCV based on current data
                    # Note: DexScreener doesn't provide historical candles via free API
                    timestamp = int(datetime.now().timestamp() * 1000)
                    
                    # Create single current candle
                    ohlcv = [[
                        timestamp,
                        current_price,      # open (approximated)
                        current_price * 1.01,  # high (approximated)
                        current_price * 0.99,  # low (approximated)
                        current_price,      # close (actual)
                        volume_24h / 24     # volume per hour (approximated)
                    ]]
                    
                    return {
                        'symbol': symbol,
                        'timeframe': interval,
                        'ohlcv': ohlcv,
                        'count': len(ohlcv),
                        'source': 'dexscreener_api',
                        'accuracy': 'moderate',
                        'note': 'Current price data only - no historical candles',
                        'pair_info': {
                            'dex': best_pair.get('dexId'),
                            'pair_address': best_pair.get('pairAddress'),
                            'price_usd': current_price,
                            'volume_24h': volume_24h
                        }
                    }
            
            raise Exception(f"DexScreener API returned {response.status_code}")
            
        except Exception as e:
            logger.error(f"DexScreener OHLCV error for {symbol}: {e}")
            raise Exception(f"DexScreener fetch failed: {str(e)}")
    
    def get_coinalyze_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 200) -> Dict[str, Any]:
        """
        Get OHLCV data from Coinalyze API
        Excellent for futures market data
        """
        try:
            # Convert symbol format for Coinalyze
            coinalyze_symbol = symbol.replace('/', '').replace('-', '').upper()
            
            # Coinalyze OHLCV endpoint
            # Note: This is a placeholder - actual Coinalyze API may require authentication
            base_url = "https://api.coinalyze.net/v1"
            
            # Try to get basic market data first
            market_url = f"{base_url}/futures-data/{coinalyze_symbol}/market-data"
            
            response = self.session.get(market_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract available data
                current_price = data.get('price', 0)
                volume_24h = data.get('volume24h', 0)
                
                if current_price > 0:
                    timestamp = int(datetime.now().timestamp() * 1000)
                    
                    # Create approximate OHLCV based on available data
                    ohlcv = [[
                        timestamp,
                        current_price,
                        current_price * 1.005,  # Conservative high estimate
                        current_price * 0.995,  # Conservative low estimate
                        current_price,
                        volume_24h / 24
                    ]]
                    
                    return {
                        'symbol': symbol,
                        'timeframe': interval,
                        'ohlcv': ohlcv,
                        'count': len(ohlcv),
                        'source': 'coinalyze_api',
                        'accuracy': 'moderate',
                        'note': 'Futures market data - approximate candles',
                        'market_info': data
                    }
            
            raise Exception(f"Coinalyze API returned {response.status_code}")
            
        except Exception as e:
            logger.error(f"Coinalyze OHLCV error for {symbol}: {e}")
            raise Exception(f"Coinalyze fetch failed: {str(e)}")
    
    def get_fallback_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 200) -> Dict[str, Any]:
        """
        Try multiple fallback sources in order of preference
        Returns first successful result
        """
        fallback_sources = [
            ('DexScreener', self.get_dexscreener_ohlcv),
            ('Coinalyze', self.get_coinalyze_ohlcv)
        ]
        
        errors = []
        
        for source_name, source_func in fallback_sources:
            try:
                logger.info(f"Trying {source_name} for {symbol} OHLCV data...")
                result = source_func(symbol, interval, limit)
                logger.info(f"✅ Successfully got OHLCV from {source_name}")
                return result
                
            except Exception as e:
                error_msg = f"{source_name} failed: {str(e)}"
                errors.append(error_msg)
                logger.warning(error_msg)
                continue
        
        # If all sources fail, return empty structure
        raise Exception(f"All fallback sources failed: {'; '.join(errors)}")
    
    def create_synthetic_ohlcv(self, symbol: str, current_price: float, interval: str = '1h', limit: int = 200) -> Dict[str, Any]:
        """
        Create basic OHLCV structure from just current price
        Used as last resort when no market data is available
        """
        logger.warning(f"Creating synthetic OHLCV for {symbol} - using current price only")
        
        timestamp = int(datetime.now().timestamp() * 1000)
        
        # Create minimal OHLCV with just current price
        ohlcv = [[
            timestamp,
            current_price,
            current_price,
            current_price,
            current_price,
            0  # No volume data
        ]]
        
        return {
            'symbol': symbol,
            'timeframe': interval,
            'ohlcv': ohlcv,
            'count': 1,
            'source': 'synthetic_fallback',
            'accuracy': 'low',
            'note': 'Synthetic data from current price only - no historical data available',
            'warning': 'Technical indicators may not be accurate with limited data'
        }

# Global instance for easy importing
fallback_sources = FallbackOHLCVSources()