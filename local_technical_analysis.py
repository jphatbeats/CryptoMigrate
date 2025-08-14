#!/usr/bin/env python3
"""
Local Technical Analysis Calculator
Uses the 'ta' library to calculate indicators locally without API rate limits
Fetches price data from Yahoo Finance or Binance and calculates RSI, MACD, etc.
"""

import pandas as pd
import yfinance as yf
import requests
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands
from ta.utils import dropna
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional, List
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class LocalTechnicalAnalysis:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
    
    async def get_technical_indicators(self, symbol: str, timeframe: str = "4h") -> Optional[Dict]:
        """
        Calculate technical indicators locally using real price data
        Returns RSI, MACD, Bollinger Bands, EMA, SMA
        """
        try:
            # Get price data
            df = await self._get_price_data(symbol, timeframe)
            if df is None or len(df) < 50:
                logger.warning(f"Insufficient price data for {symbol}")
                return None
            
            # Calculate indicators
            indicators = self._calculate_indicators(df)
            
            # Process into signals
            signals = self._process_signals(indicators, df)
            
            return signals
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            return None
    
    async def _get_price_data(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """
        Get OHLCV price data from multiple sources with fallback
        """
        cache_key = f"{symbol}_{timeframe}"
        now = datetime.now()
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (now - cached_time).seconds < self.cache_duration:
                return cached_data
        
        # Try Binance first (more crypto-focused)
        df = await self._get_binance_data(symbol)
        
        # Fallback to Yahoo Finance
        if df is None:
            df = self._get_yahoo_data(symbol)
        
        # Cache the result
        if df is not None:
            self.cache[cache_key] = (df, now)
        
        return df
    
    async def _get_binance_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Get price data from Binance API (free, no authentication required)
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Format symbol for Binance (e.g., BTCUSDT)
                binance_symbol = f"{symbol}USDT"
                url = "https://api.binance.com/api/v3/klines"
                
                params = {
                    'symbol': binance_symbol,
                    'interval': '4h',  # 4-hour candles
                    'limit': 100       # Last 100 candles (enough for indicators)
                }
                
                timeout = aiohttp.ClientTimeout(total=10)
                async with session.get(url, params=params, timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Convert to DataFrame
                        df = pd.DataFrame(data, columns=[
                            'timestamp', 'open', 'high', 'low', 'close', 'volume',
                            'close_time', 'quote_asset_volume', 'number_of_trades',
                            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                        ])
                        
                        # Convert to proper types
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                        for col in ['open', 'high', 'low', 'close', 'volume']:
                            df[col] = df[col].astype(float)
                        
                        # Set timestamp as index
                        df.set_index('timestamp', inplace=True)
                        
                        return df[['open', 'high', 'low', 'close', 'volume']]
                    
        except Exception as e:
            logger.warning(f"Binance API failed for {symbol}: {e}")
            return None
    
    def _get_yahoo_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Fallback to Yahoo Finance for price data
        """
        try:
            # Format symbol for Yahoo Finance
            yahoo_symbol = f"{symbol}-USD"
            
            # Get last 30 days of 4-hour data
            ticker = yf.Ticker(yahoo_symbol)
            df = ticker.history(period="30d", interval="4h")
            
            if len(df) > 0:
                # Yahoo Finance returns Open, High, Low, Close, Volume
                df.columns = [col.lower() for col in df.columns]
                return df[['open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            logger.warning(f"Yahoo Finance failed for {symbol}: {e}")
            return None
    
    def _calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """
        Calculate technical indicators using the 'ta' library
        """
        indicators = {}
        
        try:
            # Clean the data
            df = dropna(df)
            
            # RSI (14 periods)
            rsi_indicator = RSIIndicator(close=df['close'], window=14)
            indicators['rsi'] = rsi_indicator.rsi().iloc[-1]
            
            # MACD
            macd_indicator = MACD(close=df['close'])
            indicators['macd'] = macd_indicator.macd().iloc[-1]
            indicators['macd_signal'] = macd_indicator.macd_signal().iloc[-1]
            indicators['macd_histogram'] = macd_indicator.macd_diff().iloc[-1]
            
            # Bollinger Bands (20 periods)
            bb_indicator = BollingerBands(close=df['close'], window=20)
            indicators['bb_upper'] = bb_indicator.bollinger_hband().iloc[-1]
            indicators['bb_middle'] = bb_indicator.bollinger_mavg().iloc[-1]
            indicators['bb_lower'] = bb_indicator.bollinger_lband().iloc[-1]
            
            # EMAs
            ema20 = EMAIndicator(close=df['close'], window=20)
            ema50 = EMAIndicator(close=df['close'], window=50)
            indicators['ema20'] = ema20.ema_indicator().iloc[-1]
            indicators['ema50'] = ema50.ema_indicator().iloc[-1]
            
            # Current price
            indicators['current_price'] = df['close'].iloc[-1]
            
            # Volume
            indicators['volume_24h'] = df['volume'].tail(6).sum()  # Last 6 4-hour periods = 24h
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
    
    def _process_signals(self, indicators: Dict, df: pd.DataFrame) -> Dict:
        """
        Process raw indicator values into trading signals
        """
        if not indicators:
            return {}
        
        signals = {
            'rsi_signal': 'neutral',
            'macd_signal': 'neutral',
            'bb_signal': 'neutral',
            'trend_signal': 'neutral',
            'bullish_signals': 0,
            'technical_score': 0,
            'raw_indicators': indicators
        }
        
        # RSI Analysis
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            signals['rsi_signal'] = 'oversold_bullish'
            signals['bullish_signals'] += 1
        elif rsi < 45:
            signals['rsi_signal'] = 'accumulation_zone'
            signals['bullish_signals'] += 0.5
        elif rsi > 70:
            signals['rsi_signal'] = 'overbought_bearish'
        
        # MACD Analysis
        macd_histogram = indicators.get('macd_histogram', 0)
        if macd_histogram > 0:
            signals['macd_signal'] = 'bullish_momentum'
            signals['bullish_signals'] += 1
        elif macd_histogram < 0:
            signals['macd_signal'] = 'bearish_momentum'
        
        # Bollinger Bands Analysis
        current_price = indicators.get('current_price', 0)
        bb_lower = indicators.get('bb_lower', 0)
        bb_upper = indicators.get('bb_upper', 0)
        bb_middle = indicators.get('bb_middle', 0)
        
        if current_price and bb_lower and bb_upper:
            if current_price <= bb_lower:
                signals['bb_signal'] = 'oversold_bounce'
                signals['bullish_signals'] += 1
            elif current_price >= bb_upper:
                signals['bb_signal'] = 'overbought_rejection'
            elif current_price > bb_middle:
                signals['bb_signal'] = 'above_middle'
                signals['bullish_signals'] += 0.3
        
        # Trend Analysis (EMA crossover)
        ema20 = indicators.get('ema20', 0)
        ema50 = indicators.get('ema50', 0)
        
        if ema20 and ema50:
            if ema20 > ema50:
                signals['trend_signal'] = 'uptrend'
                signals['bullish_signals'] += 1
            else:
                signals['trend_signal'] = 'downtrend'
        
        # Calculate technical score (0-40 points)
        signals['technical_score'] = min(40, signals['bullish_signals'] * 10)
        
        return signals

# Global instance
local_ta = LocalTechnicalAnalysis()

async def get_local_technical_analysis(symbol: str, timeframe: str = "4h") -> Optional[Dict]:
    """
    Public interface for getting local technical analysis
    """
    return await local_ta.get_technical_indicators(symbol, timeframe)

if __name__ == "__main__":
    # Test the system
    async def test():
        result = await get_local_technical_analysis("BTC")
        print(f"BTC Analysis: {result}")
    
    asyncio.run(test())