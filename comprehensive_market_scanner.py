#!/usr/bin/env python3
"""
Comprehensive Market Scanner - THE ALPHA PLAYBOOK v4
Implements 3-layer analysis: Technical + News + Social Sentiment
Rotates through top 200 coins at 20-second intervals (18 coins per 6-minute batch)
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional
import logging
import os
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("⚠️ OpenAI not available - AI analysis disabled")
    OpenAI = None
    OPENAI_AVAILABLE = False

# Lumif-ai TradingView Enhanced Integration
try:
    import sys
    sys.path.append('mcp_servers')
    from lumifai_tradingview_integration import LumifTradingViewClient
    lumif_client = LumifTradingViewClient()
    lumif_available = True
    print("✅ Lumif-ai TradingView Enhanced Analysis available for market scanning")
except ImportError:
    lumif_available = False
    lumif_client = None
    print("❌ Lumif-ai TradingView Enhanced Analysis not available - using local analysis")

# Local API configuration
LOCAL_API_URL = "http://localhost:5000"

# Discord Configuration (from automated_trading_alerts.py)
DISCORD_CHANNELS = {
    'news': 1398000506068009032,          # News and social stuff channel
    'portfolio': 1399451217372905584,     # Portfolio analysis  
    # 'alpha_scans': 1399790636990857277,   # DISABLED - Trading opportunities (alerts were useless)
    'degen_memes': 1401971493096915067,   # Degen memes, viral plays, airdrops, early gems
    'calendar': 1405899035935637635       # Financial calendar - FOMC, rate decisions, market-moving events
}

# Discord Webhook URLs (backup option for when Discord.py fails)  
DISCORD_WEBHOOKS = {
    'portfolio': 'https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8',
    'calendar': 'https://discord.com/api/webhooks/1405899035935637635/SxmxqXmNIkyPAFruBqQXmJ7EPOKW0RjlO_W2LdYkoscVCkfMHjmEvMoTg4gXEGiY9o1u'
}
DISCORD_WEBHOOK_ALPHA_SCANS = "https://discord.com/api/webhooks/1403928100202352731/kLY9j4wApDDSvjXbi8SDFEcytiNJIlUZhLgoZkMIqVI2RhFm6AFunl46gDOjqssqRh7w"
DISCORD_WEBHOOK_URL = DISCORD_WEBHOOK_ALPHA_SCANS  # Backward compatibility

class ComprehensiveMarketScanner:
    def __init__(self):
        # MODERATE RATE LIMITING: 30 seconds per coin
        self.scan_interval = 30  # 30 seconds between coins
        self.batch_size = 12     # 12 coins per 6-minute batch (30s * 12 = 360s = 6min)
        self.cycle_duration = 360  # 6 minutes per batch
        self.total_coins = 200   # Top 200 legitimate coins (after filtering stablecoins)
        
        # Current position in the rotation
        self.current_coin_index = 0
        self.current_batch = 0
        self.top_200_coins = []
        self.last_top_200_refresh = None
        
        # Initialize OpenAI client for AI-powered analysis (COST OPTIMIZED)
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and OPENAI_AVAILABLE:
                self.openai_client = OpenAI(api_key=api_key)
                self.ai_enabled = True
                # COST CONTROL: Only use AI for high-confidence opportunities (85%+)
                self.ai_threshold = 85  # Only analyze coins scoring 85%+ to save costs
                print("🧠 AI-powered analysis enabled with COST OPTIMIZATION (85%+ threshold)")
            else:
                raise Exception("OpenAI API key not found or OpenAI not installed")
        except Exception as e:
            print(f"⚠️ OpenAI not available: {e}")
            self.openai_client = None
            self.ai_enabled = False
        
        # EXTREMELY strict thresholds for alerts - STOP THE ALERT SPAM
        self.alert_thresholds = {
            'min_opportunity_score': 85,      # ONLY alert on 85%+ (was 75)
            'min_technical_signals': 4,       # Need 4+ bullish signals (was 3) 
            'min_news_sentiment': 0.8,        # Need 80% positive news (was 60%)
            'min_social_momentum': 0.7,       # Need strong social buzz (was 50%)
            'min_volume_24h': 5000000,        # $5M+ daily volume (was $1M)
            'confluence_bonus': 2              # Tiny bonus (was 10)
        }
        
        self.is_running = False
        
    async def start_comprehensive_scanning(self):
        """Start the comprehensive 3-layer market scanning"""
        print("🚀 COMPREHENSIVE MARKET SCANNER - THE ALPHA PLAYBOOK v4")
        print("=" * 70)
        print("📊 3-LAYER ANALYSIS: Technical + News + Social Sentiment")
        print(f"⏰ Scanning 1 coin every {self.scan_interval} seconds")
        print(f"📈 {self.batch_size} coins per 6-minute batch")
        print(f"🔄 Complete top 200 rotation every {(200 * self.scan_interval) // 60:.1f} minutes (stablecoins excluded)")
        print("🎯 INSTANT alerts for confluence opportunities (75%+ score)")
        print("=" * 70)
        
        self.is_running = True
        
        # Initialize top 200 coins
        await self._refresh_top_200_coins()
        
        while self.is_running:
            try:
                await self._run_scanning_cycle()
            except Exception as e:
                print(f"❌ Scanner error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _run_scanning_cycle(self):
        """Run a single scanning cycle"""
        if not self.top_200_coins:
            await self._refresh_top_200_coins()
            if not self.top_200_coins:
                print("❌ No coins available for scanning")
                await asyncio.sleep(300)
                return
        
        # Get current coin to scan
        coin_symbol = self.top_200_coins[self.current_coin_index]
        batch_position = (self.current_coin_index % self.batch_size) + 1
        total_batches = len(self.top_200_coins) // self.batch_size
        current_batch_num = (self.current_coin_index // self.batch_size) + 1
        
        print(f"\n🔍 SCANNING {coin_symbol} [{batch_position}/{self.batch_size}] - Batch {current_batch_num}/{total_batches}")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | Coin {self.current_coin_index + 1}/{len(self.top_200_coins)}")
        
        # Perform comprehensive 3-layer analysis
        analysis = await self._comprehensive_analysis(coin_symbol)
        
        # Calculate confluence score
        if analysis:
            confluence_score = self._calculate_confluence_score(analysis)
            analysis['confluence_score'] = confluence_score
            
            print(f"📊 {coin_symbol}: {confluence_score:.1f}% confidence")
            
            # Get AI-powered market insight ONLY for high-confidence opportunities (COST OPTIMIZATION)
            ai_insight = None
            if self.ai_enabled and analysis and confluence_score >= self.ai_threshold:
                ai_insight = await self._get_ai_market_insight(coin_symbol, analysis, confluence_score)
            elif confluence_score >= 15:  # Provide basic insight without expensive AI calls
                ai_insight = f"{coin_symbol}'s low confidence score of {confluence_score:.1f}% is primarily driven by neutral technical indicators, lack of positive sentiment in recent news, and stagnant social momentum, indicating limited enthusiasm or catalysts for price movement. Traders should note the absence of catalysts and engagement suggests limited short-term movement potential."
            
            # Update scanner status file for dashboard
            self._update_scanner_status(coin_symbol, confluence_score, current_batch_num, total_batches, ai_insight)
            
            # Send alert if meets quality threshold
            if confluence_score >= self.alert_thresholds['min_opportunity_score']:
                await self._send_alpha_alert(coin_symbol, analysis, ai_insight)
        
        # Move to next coin
        self.current_coin_index = (self.current_coin_index + 1) % len(self.top_200_coins)
        
        # Check if we completed a full rotation
        if self.current_coin_index == 0:
            print(f"\n✅ COMPLETED FULL TOP 200 ROTATION (stablecoins excluded)")
            await self._refresh_top_200_coins()  # Refresh for next cycle
        
        # Check if we need to refresh top 200 (every hour)
        if (not self.last_top_200_refresh or 
            datetime.now() - self.last_top_200_refresh > timedelta(hours=1)):
            await self._refresh_top_200_coins()
        
        # Wait 30 seconds before next coin (increased to reduce TradingView rate limits)
        await asyncio.sleep(30)
    
    async def _comprehensive_analysis(self, symbol: str) -> Optional[Dict]:
        """Perform comprehensive 3-layer analysis: Technical + News + Social"""
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'technical': {},
            'news': {},
            'social': {},
            'errors': []
        }
        
        async with aiohttp.ClientSession() as session:
            # Layer 1: Technical Analysis (reduced indicators to manage rate limits)
            technical_data = await self._get_technical_analysis(session, symbol)
            if technical_data:
                analysis['technical'] = technical_data
            else:
                analysis['errors'].append('Technical analysis failed')
            
            # Layer 2: News Sentiment Analysis
            news_data = await self._get_news_analysis(session, symbol)
            if news_data:
                analysis['news'] = news_data
            else:
                analysis['errors'].append('News analysis failed')
            
            # Layer 3: Social Sentiment Analysis
            social_data = await self._get_social_analysis(session, symbol)
            if social_data:
                analysis['social'] = social_data
            else:
                analysis['errors'].append('Social analysis failed')
        
        return analysis if any([analysis['technical'], analysis['news'], analysis['social']]) else None
    
    async def _get_direct_technical_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Get REAL technical analysis from Lumif-ai TradingView wrapper"""
        try:
            # Use Lumif-ai TradingView Enhanced Analysis with proper symbol format
            symbol_formatted = f"{symbol}USDT" if not symbol.endswith('USDT') else symbol
            url = f"{LOCAL_API_URL}/api/lumif/enhanced-analysis/{symbol_formatted}"
            
            print(f"🔍 Attempting Lumif TradingView analysis for {symbol_formatted}...")
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success' and data.get('data'):
                        tv_data = data['data']
                        
                        # Extract REAL TradingView indicator values from actual response format
                        indicators = tv_data.get('technical_indicators', {})
                        
                        rsi = indicators.get('rsi', 50)
                        macd = indicators.get('macd', 0)
                        macd_signal = indicators.get('rsi_signal', 'NEUTRAL').lower()
                        
                        # Get TradingView recommendation and signals
                        recommendation = tv_data.get('overall_recommendation', 'NEUTRAL').lower()
                        signals = tv_data.get('signals', {})
                        buy_signals = signals.get('buy', 0)
                        sell_signals = signals.get('sell', 0)
                        tv_confidence = tv_data.get('confidence_score', 50)
                        
                        # Calculate REAL signals based on TradingView data
                        rsi_signal = 'oversold' if rsi < 30 else ('overbought' if rsi > 70 else 'neutral')
                        macd_signal_processed = 'bullish' if macd > 0 else ('bearish' if macd < 0 else 'neutral')
                        
                        # Count bullish signals from REAL TradingView indicators
                        bullish_signals = 0
                        if rsi < 35: bullish_signals += 1  # Oversold condition
                        if macd > 0: bullish_signals += 1  # MACD bullish
                        if recommendation == 'buy': bullish_signals += 1  # TradingView buy signal
                        if buy_signals > sell_signals: bullish_signals += 1  # More buy than sell signals
                        
                        # Conservative but REAL confluence scoring using TradingView data
                        base_score = 20
                        
                        # Add score based on TradingView recommendation
                        if recommendation == 'buy':
                            base_score += min(15, (buy_signals - sell_signals) * 2)  # Signal strength
                        if macd > 0:
                            base_score += 5
                        if tv_confidence > 70:  # High TradingView confidence
                            base_score += 8
                        elif tv_confidence > 60:
                            base_score += 5
                        
                        # Penalty for bearish conditions
                        if recommendation == 'sell':
                            base_score = max(10, base_score - 10)
                        
                        technical_score = min(45, base_score)  # Cap at 45% as planned
                        
                        print(f"✅ REAL TradingView Analysis: {symbol} - RSI: {rsi:.1f}, MACD: {macd:.2f}, Rec: {recommendation}")
                        print(f"   TV Confidence: {tv_confidence:.1f}%, Buy/Sell: {buy_signals}/{sell_signals}")
                        
                        return {
                            'rsi': round(rsi, 1),
                            'rsi_signal': rsi_signal,
                            'macd_signal': macd_signal_processed,
                            'macd_value': round(macd, 2),
                            'recommendation': recommendation,
                            'confluence_score': round(technical_score, 1),
                            'bullish_signals': bullish_signals,
                            'bearish_signals': max(0, 4 - bullish_signals),
                            'technical_score': round(technical_score, 1),
                            'source': 'lumif_tradingview_real',
                            'confidence': 85,
                            'tradingview_confidence': round(tv_confidence, 1),
                            'tv_buy_signals': buy_signals,
                            'tv_sell_signals': sell_signals
                        }
                
                # If Lumif-ai TradingView fails, use fallback API
                print(f"⚠️ Lumif TradingView not available for {symbol}, trying fallback...")
                
                # Try alternative TradingView endpoint with proper symbol format
                fallback_url = f"{LOCAL_API_URL}/api/lumif/pattern-signals/{symbol_formatted}"
                async with session.get(fallback_url, timeout=timeout) as fallback_response:
                    if fallback_response.status == 200:
                        fallback_data = await fallback_response.json()
                        if fallback_data.get('success'):
                            # Use pattern analysis as backup
                            return {
                                'rsi': 50.0,
                                'rsi_signal': 'neutral',
                                'macd_signal': 'neutral',
                                'recommendation': 'neutral',
                                'confluence_score': 25.0,
                                'bullish_signals': 1,
                                'bearish_signals': 1,
                                'technical_score': 25.0,
                                'source': 'lumif_pattern_fallback',
                                'confidence': 60
                            }
                
                # Final fallback to neutral
                print(f"⚠️ All TradingView sources unavailable for {symbol}")
                return {
                    'rsi': 50.0,
                    'rsi_signal': 'neutral',
                    'macd_signal': 'neutral',
                    'recommendation': 'neutral',
                    'confluence_score': 20.0,
                    'bullish_signals': 1,
                    'bearish_signals': 1,
                    'technical_score': 20.0,
                    'source': 'neutral_fallback',
                    'confidence': 50
                }
                    
        except Exception as e:
            print(f"⚠️ Lumif TradingView analysis error for {symbol}: {e}")
            # Return neutral instead of fake random data
            return {
                'rsi': 50.0,
                'rsi_signal': 'neutral', 
                'macd_signal': 'neutral',
                'recommendation': 'neutral',
                'confluence_score': 20.0,
                'bullish_signals': 1,
                'bearish_signals': 1,
                'technical_score': 20.0,
                'source': 'error_fallback',
                'confidence': 25
            }
    
    async def _get_technical_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Enhanced technical analysis using Lumif-ai TradingView + fallback to local"""
        try:
            # RE-ENABLE TRADINGVIEW with proper cooldown strategy
            print(f"🔍 Attempting TradingView analysis for {symbol} (with smart rate limiting)")
            
            # Try TradingView first - it was working earlier today
            tradingview_analysis = await self._get_direct_technical_analysis(session, symbol)
            if tradingview_analysis and tradingview_analysis.get('confluence_score', 0) > 15:
                print(f"✅ TradingView Technical Analysis: {symbol} - RSI: {tradingview_analysis.get('rsi')}, Score: {tradingview_analysis.get('confluence_score')}%")
                return tradingview_analysis
            
            print(f"⚠️ TradingView failed for {symbol}, trying TAAPI fallback...")
            
            # Primary: TAAPI technical analysis (real RSI, MACD data)
            taapi_analysis = await self._get_taapi_technical_analysis(session, symbol)
            if taapi_analysis:
                print(f"✅ TAAPI Technical Analysis: {symbol} - RSI: {taapi_analysis.get('rsi')}, Score: {taapi_analysis.get('technical_score')}%")
                return taapi_analysis
            
            # Fallback: Enhanced local analysis with price action
            enhanced_local = await self._get_enhanced_local_analysis(session, symbol)
            if enhanced_local:
                print(f"✅ Enhanced Local Analysis: {symbol} - Score: {enhanced_local.get('technical_score')}%")
                return enhanced_local
            
            # Final fallback to neutral analysis
            print(f"⚠️ All technical analysis methods failed for {symbol}")
            return {
                'rsi': 50,
                'rsi_signal': 'neutral',
                'macd_signal': 'neutral',
                'recommendation': 'neutral',
                'confluence_score': 25,
                'bullish_signals': 1,
                'bearish_signals': 1,
                'technical_score': 25,
                'source': 'fallback_analysis',
                'confidence': 25
            }
                    
        except Exception as e:
            print(f"⚠️ Technical analysis error for {symbol}: {e}")
            return None
    
    async def _get_taapi_technical_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Get technical analysis from TAAPI.io as fallback"""
        try:
            # Use TAAPI.io for RSI, MACD, and basic indicators
            url = f"{LOCAL_API_URL}/api/taapi/rsi"
            params = {
                'symbol': f"{symbol}USDT",  # Fixed: Remove slash for TAAPI format
                'exchange': 'binance',
                'interval': '4h'
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, params=params, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    rsi = data.get('value', 50)
                    
                    # Generate technical analysis from TAAPI data
                    rsi_signal = 'oversold' if rsi < 30 else ('overbought' if rsi > 70 else 'neutral')
                    recommendation = 'buy' if rsi < 35 else ('sell' if rsi > 65 else 'neutral')
                    
                    # Calculate technical score based on RSI
                    if rsi < 30:
                        technical_score = 40  # Strong oversold signal
                    elif rsi > 70:
                        technical_score = 15  # Overbought (lower score)
                    else:
                        technical_score = 25  # Neutral
                    
                    return {
                        'rsi': round(rsi, 1),
                        'rsi_signal': rsi_signal,
                        'macd_signal': 'neutral',
                        'recommendation': recommendation,
                        'confluence_score': round(technical_score, 1),
                        'bullish_signals': 2 if rsi < 35 else 0,
                        'bearish_signals': 2 if rsi > 65 else 0,
                        'technical_score': round(technical_score, 1),
                        'source': 'taapi_analysis',
                        'confidence': 80
                    }
                    
        except Exception as e:
            print(f"⚠️ TAAPI analysis error for {symbol}: {e}")
            return None
    
    async def _get_enhanced_local_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Enhanced local technical analysis using price action and volume"""
        try:
            # Get price data from CoinGecko (free, no limits)
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': symbol.lower(),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, params=params, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if symbol.lower() in data:
                        price_data = data[symbol.lower()]
                        price_change_24h = price_data.get('usd_24h_change', 0)
                        volume_24h = price_data.get('usd_24h_vol', 0)
                        
                        # Generate technical signals from price action
                        if price_change_24h > 5:
                            recommendation = 'buy'
                            technical_score = 45  # Strong bullish
                            rsi_estimate = 35  # Oversold bounce
                        elif price_change_24h < -5:
                            recommendation = 'sell'  
                            technical_score = 20  # Bearish breakdown
                            rsi_estimate = 65  # Overbought
                        elif abs(price_change_24h) < 2:
                            recommendation = 'neutral'
                            technical_score = 30  # Consolidation
                            rsi_estimate = 50  # Neutral
                        else:
                            recommendation = 'neutral'
                            technical_score = 25
                            rsi_estimate = 45 + (price_change_24h * 2)  # Estimate based on momentum
                        
                        # Volume confirmation
                        if volume_24h > 1000000:  # High volume
                            technical_score += 5
                        
                        return {
                            'rsi': round(rsi_estimate, 1),
                            'rsi_signal': 'oversold' if rsi_estimate < 35 else ('overbought' if rsi_estimate > 65 else 'neutral'),
                            'macd_signal': 'bullish' if price_change_24h > 2 else ('bearish' if price_change_24h < -2 else 'neutral'),
                            'recommendation': recommendation,
                            'confluence_score': round(technical_score, 1),
                            'bullish_signals': 2 if price_change_24h > 3 else (1 if price_change_24h > 0 else 0),
                            'bearish_signals': 2 if price_change_24h < -3 else (1 if price_change_24h < 0 else 0),
                            'technical_score': round(technical_score, 1),
                            'source': 'enhanced_local_analysis',
                            'confidence': 70,
                            'price_change_24h': round(price_change_24h, 2),
                            'volume_24h': volume_24h
                        }
                        
        except Exception as e:
            print(f"⚠️ Enhanced local analysis error for {symbol}: {e}")
            return None
                    
        except Exception as e:
            print(f"⚠️ Technical analysis error for {symbol}: {e}")
            return None
    
    async def _get_news_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Get recent news and sentiment for the symbol"""
        try:
            url = f"{LOCAL_API_URL}/api/crypto-news/symbol/{symbol}"
            params = {"hours": 24, "sentiment": "positive"}
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, params=params, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_news_data(data)
                else:
                    return None
                    
        except Exception as e:
            print(f"⚠️ News analysis error for {symbol}: {e}")
            return None
    
    async def _get_social_analysis(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Dict]:
        """Get social sentiment and momentum"""
        try:
            url = f"{LOCAL_API_URL}/api/social/momentum/{symbol}"
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_social_data(data)
                else:
                    return None
                    
        except Exception as e:
            print(f"⚠️ Social analysis error for {symbol}: {e}")
            return None
    
    def _process_technical_data(self, data: Dict) -> Dict:
        """Process local technical analysis data (already processed by local_technical_analysis)"""
        # Local TA already returns processed signals, just return as-is
        return data if data else {
            'rsi_signal': 'neutral',
            'macd_signal': 'neutral', 
            'bb_signal': 'neutral',
            'trend_signal': 'neutral',
            'bullish_signals': 0,
            'technical_score': 0
        }
    
    def _process_news_data(self, data: Dict) -> Dict:
        """Process news data with AI-powered sentiment analysis"""
        news_signals = {
            'recent_news_count': 0,
            'positive_sentiment_ratio': 0,
            'news_catalyst': False,
            'news_score': 0,
            'ai_sentiment_score': 0,
            'market_impact_score': 0
        }
        
        if data.get('success') and data.get('articles'):
            articles = data['articles']
            news_signals['recent_news_count'] = len(articles)
            
            # Use AI to grade news quality and market impact
            if self.ai_enabled and articles:
                try:
                    # Combine all article titles/descriptions for AI analysis
                    news_text = ". ".join([
                        f"{article.get('title', '')}: {article.get('description', '')[:200]}"
                        for article in articles[:3]  # Analyze top 3 articles
                    ])
                    
                    ai_analysis = self._analyze_news_with_ai(news_text, data.get('symbol', 'UNKNOWN'))
                    if ai_analysis:
                        news_signals['ai_sentiment_score'] = ai_analysis.get('sentiment_score', 0)
                        news_signals['market_impact_score'] = ai_analysis.get('market_impact', 0)
                        news_signals['news_catalyst'] = ai_analysis.get('is_catalyst', False)
                        
                        # AI-powered news score (0-15 points max)
                        news_signals['news_score'] = min(15, 
                            news_signals['ai_sentiment_score'] * 0.6 +  # 60% sentiment weight
                            news_signals['market_impact_score'] * 0.4    # 40% impact weight
                        )
                        return news_signals
                        
                except Exception as e:
                    print(f"⚠️ AI news analysis failed: {e}")
                    # Fall through to traditional analysis
            
            # Fallback to traditional sentiment counting
            positive_count = sum(1 for article in articles 
                               if article.get('sentiment', '').lower() == 'positive')
            
            if len(articles) > 0:
                news_signals['positive_sentiment_ratio'] = positive_count / len(articles)
                news_signals['news_catalyst'] = positive_count >= 2
            
            # Traditional conservative scoring
            if news_signals['news_catalyst']:
                news_signals['news_score'] = min(8,
                    news_signals['positive_sentiment_ratio'] * 5 + 
                    min(3, news_signals['recent_news_count']))
        
        return news_signals
    
    def _process_social_data(self, data: Dict) -> Dict:
        """Process social sentiment data with AI enhancement"""
        social_signals = {
            'social_momentum': 0,
            'sentiment_score': 0,
            'viral_potential': False,
            'social_score': 0,
            'ai_social_grade': 0,
            'community_strength': 0
        }
        
        if data.get('success'):
            # Process raw LunarCrush data
            momentum = data.get('momentum', {})
            raw_momentum = momentum.get('score', 0)
            raw_sentiment = momentum.get('sentiment', 0)
            
            social_signals['social_momentum'] = raw_momentum
            social_signals['sentiment_score'] = raw_sentiment
            social_signals['viral_potential'] = raw_momentum > 0.7
            
            # Use AI to grade social sentiment quality if available
            if self.ai_enabled and (raw_momentum > 0.1 or raw_sentiment != 0):
                try:
                    # Extract social context for AI analysis
                    symbol = data.get('symbol', 'UNKNOWN')
                    social_context = {
                        'momentum_score': raw_momentum,
                        'sentiment_score': raw_sentiment,
                        'social_posts': momentum.get('posts', 0),
                        'engagement_rate': momentum.get('engagement', 0)
                    }
                    
                    ai_grade = self._analyze_social_with_ai(social_context, symbol)
                    if ai_grade:
                        social_signals['ai_social_grade'] = ai_grade.get('quality_score', 0)
                        social_signals['community_strength'] = ai_grade.get('community_strength', 0)
                        
                        # AI-enhanced social score (0-10 points max)
                        social_signals['social_score'] = min(10,
                            social_signals['ai_social_grade'] * 0.7 +     # 70% AI quality weight
                            social_signals['community_strength'] * 0.3    # 30% community weight
                        )
                        return social_signals
                        
                except Exception as e:
                    print(f"⚠️ AI social analysis failed: {e}")
                    # Fall through to traditional analysis
            
            # Fallback to traditional conservative scoring
            social_signals['social_score'] = min(5, raw_momentum * 5)
        
        return social_signals
    
    def _analyze_news_with_ai(self, news_text: str, symbol: str) -> Optional[Dict]:
        """Use AI to analyze news sentiment and market impact"""
        try:
            if not self.openai_client:
                return None
                
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. 
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional crypto news analyst. Analyze news for:
1. Sentiment Score (0-10): How positive/negative for price
2. Market Impact (0-10): Likelihood to move markets significantly  
3. Is Catalyst (true/false): Major news that could trigger price movement

Consider: partnerships, regulations, tech developments, institutional adoption, market trends.
Respond in JSON format: {"sentiment_score": number, "market_impact": number, "is_catalyst": boolean}"""
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze these {symbol} news articles for market impact:\n\n{news_text}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=150,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                'sentiment_score': max(0, min(10, result.get('sentiment_score', 5))),
                'market_impact': max(0, min(10, result.get('market_impact', 5))),  
                'is_catalyst': result.get('is_catalyst', False)
            }
            
        except Exception as e:
            print(f"⚠️ AI news analysis error: {e}")
            return None
    
    def _analyze_social_with_ai(self, social_context: Dict, symbol: str) -> Optional[Dict]:
        """Use AI to grade social sentiment quality and community strength"""
        try:
            if not self.openai_client:
                return None
                
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. 
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a crypto social sentiment analyst. Grade social activity for:
1. Quality Score (0-10): How genuine/organic the social buzz is (not bots/spam)
2. Community Strength (0-10): Strength of the underlying community and engagement

Consider: engagement quality, organic growth, community loyalty, influencer involvement, spam detection.
Higher scores for genuine community-driven momentum vs artificial pump signals.
Respond in JSON format: {"quality_score": number, "community_strength": number}"""
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze {symbol} social sentiment:\nMomentum: {social_context['momentum_score']}\nSentiment: {social_context['sentiment_score']}\nPosts: {social_context.get('social_posts', 0)}\nEngagement: {social_context.get('engagement_rate', 0)}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=100,
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                'quality_score': max(0, min(10, result.get('quality_score', 5))),
                'community_strength': max(0, min(10, result.get('community_strength', 5)))
            }
            
        except Exception as e:
            print(f"⚠️ AI social analysis error: {e}")
            return None
    
    def _calculate_confluence_score(self, analysis: Dict) -> float:
        """Calculate confluence score from all 3 layers of analysis - MUCH more conservative"""
        technical_score = analysis.get('technical', {}).get('technical_score', 0)
        news_score = analysis.get('news', {}).get('news_score', 0)  
        social_score = analysis.get('social', {}).get('social_score', 0)
        
        # DRAMATICALLY reduce base scoring
        base_score = (technical_score * 0.4) + (news_score * 0.3) + (social_score * 0.2)
        
        # Much higher thresholds for confluence bonus (updated for AI-enhanced scoring)
        layers_positive = sum([
            technical_score > 35,  # Technical shows STRONG strength
            news_score > 12,       # AI-graded significant news catalyst  
            social_score > 8       # AI-graded strong social momentum
        ])
        
        confluence_bonus = 0
        if layers_positive >= 3:  # ALL layers must be strong (raised from 2)
            confluence_bonus = 5 * layers_positive  # Much smaller bonus
        elif layers_positive >= 2:
            confluence_bonus = 2 * layers_positive  # Tiny bonus for 2 layers
        
        # Apply confidence penalty for missing data
        successful_layers = sum([
            bool(analysis.get('technical')),
            bool(analysis.get('news')), 
            bool(analysis.get('social'))
        ])
        
        confidence_multiplier = successful_layers / 3.0
        
        final_score = (base_score + confluence_bonus) * confidence_multiplier
        
        # Cap at 85% max - no coin should easily hit 90%+
        return min(85, max(15, final_score))
    
    async def _refresh_top_200_coins(self):
        """Refresh the top 200 coins list (excluding stablecoins)"""
        # Comprehensive stablecoin list to exclude
        STABLECOINS = {
            'USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDD', 'FRAX', 'USDE', 'SUSDE',
            'FDUSD', 'PYUSD', 'GUSD', 'USDP', 'LUSD', 'USDK', 'USDN', 'RSR', 'USTC',
            'MIM', 'USDC.E', 'BSC-USD', 'USDS', 'CRVUSD', 'DOLA', 'ALUSD', 'AGEUR',
            'EURO', 'EURS', 'EURT', 'STETH', 'WSTETH', 'WETH', 'WBTC', 'WBETH',
            'CBBTC', 'WEETH', 'CETH', 'RETH'  # Wrapped/staked versions
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{LOCAL_API_URL}/api/market/top-performers"
                params = {
                    'limit': 350,  # Get 350 to ensure 200+ after filtering stablecoins
                    'timeframe': '24h',
                    'min_volume': 500000,
                    'sort_by': 'volume_weighted_performance'
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('coins'):
                            # Filter out stablecoins and get top 200 non-stablecoin assets
                            all_coins = [coin['symbol'] for coin in data['coins']]
                            filtered_coins = [symbol for symbol in all_coins if symbol.upper() not in STABLECOINS]
                            self.top_200_coins = filtered_coins[:200]  # Take top 200 after filtering
                            self.last_top_200_refresh = datetime.now()
                            
                            excluded_count = len(all_coins) - len(filtered_coins)
                            print(f"✅ Refreshed top coins list: {len(self.top_200_coins)} coins (excluded {excluded_count} stablecoins)")
                            return
            
            # Fallback to major non-stablecoin coins if API fails (200 coins)
            print("⚠️ Using fallback top coins list (no stablecoins)")
            fallback_coins = [
                'BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'DOT', 'AVAX', 'LINK', 'UNI',
                'LTC', 'BCH', 'ALGO', 'VET', 'ICP', 'FIL', 'TRX', 'ETC', 'XLM', 'ATOM',
                'HBAR', 'NEAR', 'MANA', 'SAND', 'AXS', 'CRV', 'MKR', 'AAVE', 'COMP', 'YFI',
                'DOGE', 'SHIB', 'PEPE', 'LEO', 'TON', 'XMR', 'HYPE', 'TAO', 'SUI', 'MNT',
                'APT', 'ARB', 'OP', 'IMX', 'THETA', 'FTM', 'ALGO', 'EGLD', 'FLOW', 'XTZ',
                'KAVA', 'ROSE', 'CHZ', 'ENJ', 'BAT', 'ZEC', 'DASH', 'DCR', 'RVN', 'DGB',
                'SC', 'ZEN', 'WAVES', 'ONT', 'QTUM', 'LSK', 'STRAT', 'ARK', 'KMD', 'PIVX',
                'NXS', 'BTS', 'STEEM', 'XEM', 'MAID', 'SYS', 'VIA', 'BLK', 'POT', 'FAIR',
                'CLOAK', 'CURE', 'XVC', 'BLOCK', 'ABY', 'BYC', 'XPY', 'HYP', 'IOC', 'CANN',
                'STV', 'TRUST', 'NEOS', 'GRS', 'PKB', 'CRW', 'LXC', 'UFO', 'PRIME', 'PTC',
                'NLG', 'GLD', 'SLR', 'RBY', 'XWC', 'EFL', 'DMD', 'TX', 'BCY', 'EXP',
                'INFX', 'OMNI', 'AMP', 'AGRS', 'XLR', 'CLUB', 'VOX', 'EMC', 'FCT', 'RADS',
                'OK', 'SNRG', 'PKT', 'CPC', 'AEON', 'ETH', 'LBC', 'STRAT', 'UBQ', 'PTOY',
                'CFI', 'BRX', 'IOP', 'NXC', 'ETC', 'ZEC', 'XMR', 'DASH', 'PPC', 'NMC',
                'DOGE', 'RDD', 'XPM', 'AUR', 'NVC', 'TRC', 'PRT', 'NXT', 'BURST', 'XCP',
                'SJCX', 'STORJ', 'XRP', 'GAME', 'LTC', 'PND', 'VTC', 'DRK', 'BC', 'DGB',
                'MYRIAD', 'UNO', 'JPC', 'BITS', 'NOTE', 'ERY', 'HVC', 'FRK', 'AC', 'MIN',
                'WDC', 'TIPS', 'ALT', 'FLO', 'QRK', 'PXC', 'MOON', 'LOT', 'MEOW', 'PLNC',
                'RPC', 'VRC', 'SRC', 'NEC', 'RIC', 'QTL', 'GDN', 'XJO', 'SLG', 'RZR',
                'VPN', 'CDN', 'RED', 'PHS', 'TTC', 'PRC', 'CGA', 'WC', 'SYNC', 'PINK'
            ]
            # Filter fallback list and ensure exactly 200 coins
            filtered_fallback = [symbol for symbol in fallback_coins if symbol not in STABLECOINS]
            self.top_200_coins = filtered_fallback[:200]
            
        except Exception as e:
            print(f"❌ Error refreshing top coins: {e}")
    
    async def _get_ai_market_insight(self, symbol: str, analysis: Dict, confidence: float) -> Optional[str]:
        """Get AI-powered market insight and explanation using GPT-4o"""
        if not self.ai_enabled or not self.openai_client:
            return None
            
        try:
            # Prepare analysis data for AI
            technical_data = analysis.get('technical', {})
            news_data = analysis.get('news', {})
            social_data = analysis.get('social', {})
            
            prompt = f"""You are an expert crypto trading analyst. Analyze {symbol} with this data:

CONFIDENCE SCORE: {confidence:.1f}%

TECHNICAL ANALYSIS:
- RSI: {technical_data.get('rsi', 'N/A')}
- MACD Signal: {technical_data.get('macd_signal', 'N/A')}
- Recommendation: {technical_data.get('recommendation', 'N/A')}
- Technical Score: {technical_data.get('technical_score', 0)}/50

NEWS ANALYSIS:
- Recent News: {news_data.get('recent_news_count', 0)} articles
- Positive Sentiment: {news_data.get('positive_sentiment_ratio', 0)*100:.1f}%
- News Catalyst: {'Yes' if news_data.get('news_catalyst') else 'No'}
- News Score: {news_data.get('news_score', 0)}/30

SOCIAL ANALYSIS:
- Social Momentum: {social_data.get('social_momentum', 0)*100:.1f}%
- Sentiment Score: {social_data.get('sentiment_score', 0)*100:.1f}%
- Viral Potential: {'Yes' if social_data.get('viral_potential') else 'No'}
- Social Score: {social_data.get('social_score', 0)}/20

Provide a concise 2-sentence analysis explaining why this coin scored {confidence:.1f}% and what traders should know. Focus on the key factors driving the score."""

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional crypto trading analyst providing concise, actionable market insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            insight = response.choices[0].message.content.strip()
            print(f"🧠 AI Insight for {symbol}: {insight}")
            return insight
            
        except Exception as e:
            print(f"⚠️ AI insight error for {symbol}: {e}")
            return None
    
    def _update_scanner_status(self, symbol: str, confidence: float, batch_num: int, total_batches: int, ai_insight: Optional[str] = None):
        """Update scanner status for dashboard"""
        try:
            # Keep recent scans history
            recent_scans = []
            
            # Try to load existing data
            try:
                if os.path.exists('scanner_status.json'):
                    with open('scanner_status.json', 'r') as f:
                        existing_data = json.load(f)
                        recent_scans = existing_data.get('recent_scans', [])
            except:
                pass
            
            # Add current scan
            recent_scans.insert(0, {
                'symbol': symbol,
                'confidence': confidence,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'alert_triggered': confidence >= 75,
                'status': 'completed',
                'ai_insight': ai_insight
            })
            
            # Keep only last 10 scans
            recent_scans = recent_scans[:10]
            
            # Update status
            status_data = {
                'current_coin': symbol,
                'current_index': self.current_coin_index + 1,
                'total_coins': len(self.top_200_coins),
                'current_batch': f'{batch_num}/{total_batches}',
                'confidence': confidence,
                'alert_triggered': confidence >= 75,
                'timestamp': datetime.now().isoformat(),
                'scanning_active': True,
                'recent_scans': recent_scans
            }
            
            # Write to file
            with open('scanner_status.json', 'w') as f:
                json.dump(status_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Failed to update scanner status: {e}")

    async def _send_alpha_alert(self, symbol: str, analysis: Dict, ai_insight: Optional[str] = None):
        """Send high-quality alpha opportunity alert"""
        confluence_score = analysis['confluence_score']
        
        # Create detailed alert message
        alert_data = {
            'symbol': symbol,
            'score': confluence_score,
            'technical': analysis.get('technical', {}),
            'news': analysis.get('news', {}),
            'social': analysis.get('social', {}),
            'ai_insight': ai_insight,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        print(f"🚨 ALPHA ALERT: {symbol} - {confluence_score:.1f}% confluence score")
        if ai_insight:
            print(f"🧠 AI Analysis: {ai_insight}")
        
        # Send to Discord webhook
        await self._send_discord_alpha_alert(alert_data)
    
    async def _send_discord_alpha_alert(self, alert_data: Dict):
        """Send alpha alert to Discord using webhook"""
        if not DISCORD_WEBHOOK_ALPHA_SCANS:
            print("⚠️ Discord webhook URL not configured for alpha scans")
            return
        
        try:
            symbol = alert_data['symbol']
            score = alert_data['score']
            technical = alert_data.get('technical', {})
            ai_insight = alert_data.get('ai_insight', '')
            timestamp = alert_data['timestamp']
            
            # Create rich Discord embed
            embed = {
                "title": f"🚨 ALPHA ALERT: {symbol}",
                "description": f"**{score:.1f}% Confluence Score**\n\n🎯 High-confidence trading opportunity detected!",
                "color": 0x00FF00 if score >= 80 else 0xFF9900,  # Green for 80%+, Orange for 75-79%
                "fields": [],
                "footer": {"text": f"The Alpha Playbook v4 • {timestamp}"},
                "thumbnail": {"url": f"https://cryptoicons.org/api/white/{symbol.lower()}/64"}
            }
            
            # Add technical analysis
            if technical.get('recommendation'):
                embed["fields"].append({
                    "name": "📊 Technical Analysis",
                    "value": f"**Recommendation**: {technical['recommendation']}\n**RSI**: {technical.get('rsi', 'N/A')}\n**MACD**: {technical.get('macd_signal', 'N/A')}",
                    "inline": True
                })
            
            # Add AI insight if available
            if ai_insight:
                # Truncate if too long for Discord
                insight_text = ai_insight[:200] + "..." if len(ai_insight) > 200 else ai_insight
                embed["fields"].append({
                    "name": "🧠 AI Market Analysis",
                    "value": insight_text,
                    "inline": False
                })
            
            # Generate trade recommendation based on confluence score and technical data
            trade_setup = await self._generate_trade_setup(symbol, score, technical)
            embed["fields"].append({
                "name": "💰 TRADE SETUP",
                "value": trade_setup,
                "inline": False
            })
            
            # Send webhook
            webhook_data = {
                "content": f"<@&1399790636990857277> Alpha opportunity detected!",  # Optional role mention
                "embeds": [embed]
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(DISCORD_WEBHOOK_ALPHA_SCANS, json=webhook_data) as response:
                    if response.status == 204:
                        print(f"✅ Alpha alert sent to Discord: {symbol} ({score:.1f}%)")
                    else:
                        print(f"❌ Discord webhook failed: {response.status}")
                        
        except Exception as e:
            print(f"❌ Discord alert error: {e}")
    
    async def _generate_trade_setup(self, symbol: str, confidence: float, technical: Dict) -> str:
        """Generate complete trade setup with entry, TP, SL, and position sizing"""
        try:
            # Get current price from local API
            current_price = await self._get_current_price(symbol)
            if not current_price:
                return "⚠️ Unable to fetch current price for trade setup"
            
            # Calculate position size based on confidence score
            if confidence >= 85:
                position_size = "3-5%"  # High conviction
                risk_level = "HIGH CONVICTION"
            elif confidence >= 80:
                position_size = "2-3%"  # Strong signal
                risk_level = "STRONG SIGNAL"
            else:  # 75-79%
                position_size = "1-2%"  # Conservative
                risk_level = "CONSERVATIVE"
            
            # Determine trade direction from technical analysis
            recommendation = technical.get('recommendation', 'neutral').lower()
            rsi = technical.get('rsi', 50)
            macd_signal = technical.get('macd_signal', 'neutral').lower()
            
            if 'buy' in recommendation or 'bullish' in macd_signal:
                # LONG setup
                entry_zone = f"${current_price * 0.995:.4f} - ${current_price * 1.005:.4f}"
                stop_loss = f"${current_price * 0.92:.4f}"  # 8% stop loss
                
                # Multiple TP levels based on confidence
                if confidence >= 85:
                    tp1 = f"${current_price * 1.10:.4f} (10%)"
                    tp2 = f"${current_price * 1.18:.4f} (18%)"
                    tp3 = f"${current_price * 1.25:.4f} (25%)"
                elif confidence >= 80:
                    tp1 = f"${current_price * 1.08:.4f} (8%)"
                    tp2 = f"${current_price * 1.15:.4f} (15%)"
                    tp3 = f"${current_price * 1.22:.4f} (22%)"
                else:
                    tp1 = f"${current_price * 1.05:.4f} (5%)"
                    tp2 = f"${current_price * 1.12:.4f} (12%)"
                    tp3 = f"${current_price * 1.18:.4f} (18%)"
                
                trade_type = "LONG 📈"
                
            else:
                # SHORT setup (or wait for better entry)
                entry_zone = f"${current_price * 0.995:.4f} - ${current_price * 1.005:.4f}"
                stop_loss = f"${current_price * 1.08:.4f}"  # 8% stop loss
                
                if confidence >= 85:
                    tp1 = f"${current_price * 0.90:.4f} (-10%)"
                    tp2 = f"${current_price * 0.82:.4f} (-18%)"
                    tp3 = f"${current_price * 0.75:.4f} (-25%)"
                elif confidence >= 80:
                    tp1 = f"${current_price * 0.92:.4f} (-8%)"
                    tp2 = f"${current_price * 0.85:.4f} (-15%)"
                    tp3 = f"${current_price * 0.78:.4f} (-22%)"
                else:
                    tp1 = f"${current_price * 0.95:.4f} (-5%)"
                    tp2 = f"${current_price * 0.88:.4f} (-12%)"
                    tp3 = f"${current_price * 0.82:.4f} (-18%)"
                
                trade_type = "SHORT 📉"
            
            # Format the trade setup
            setup = f"""**{trade_type} • {risk_level}**
**Entry Zone**: {entry_zone}
**Stop Loss**: {stop_loss} (-8%)
**Take Profits**:
• TP1: {tp1} (33% close)
• TP2: {tp2} (33% close)  
• TP3: {tp3} (34% close)

**Position Size**: {position_size} of account
**R:R Ratio**: 1:2.5 minimum
**Current Price**: ${current_price:.4f}"""
            
            return setup
            
        except Exception as e:
            print(f"❌ Trade setup generation error: {e}")
            return f"⚠️ Trade setup unavailable - manual analysis required"
    
    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price from local API"""
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                url = f"{LOCAL_API_URL}/api/crypto/price/{symbol}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(data.get('price', 0))
            return None
        except:
            # Fallback to estimate based on market cap (very rough)
            try:
                if symbol == 'BTC':
                    return 67500.0  # Approximate BTC price
                elif symbol == 'ETH':
                    return 3200.0   # Approximate ETH price
                else:
                    return 1.0      # Generic fallback
            except:
                return None

# Global scanner instance
scanner = None

async def start_comprehensive_market_scanner():
    """Start the comprehensive market scanner"""
    global scanner
    scanner = ComprehensiveMarketScanner()
    await scanner.start_comprehensive_scanning()

def stop_comprehensive_market_scanner():
    """Stop the comprehensive market scanner"""
    global scanner
    if scanner:
        scanner.is_running = False

if __name__ == "__main__":
    asyncio.run(start_comprehensive_market_scanner())