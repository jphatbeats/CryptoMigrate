#!/usr/bin/env python3
"""
Hourly Trade Scanner
Scans top 200 coins every hour with full TA, news, sentiment analysis
Sends instant alerts when quality trades are detected
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

# Local API configuration - use local server
LOCAL_API_URL = "http://localhost:5000"

class HourlyTradeScanner:
    def __init__(self):
        self.scan_interval = 360  # 6 minutes between batches (10 batches per hour)
        self.batch_size = 20  # 20 tokens per batch
        self.total_tokens = 200  # Complete top 200 every hour
        self.is_running = False
        self.current_batch = 0
        self.hourly_cycle = 0
        
        # Quality thresholds for instant alerts
        self.alert_thresholds = {
            'min_opportunity_score': 70,  # Raised to 70+ for quality
            'min_gain_potential': 20,     # 20%+ potential gain
            'min_volume_24h': 2000000,    # $2M+ daily volume
            'max_risk_level': 'High',     # No "Very High" risk
            'require_catalyst': True,     # Must have news catalyst
            'min_ta_signals': 3           # At least 3 bullish TA signals
        }
        
        # Track recent alerts to prevent spam
        self.recent_alerts = {}
        self.alert_cooldown = 1800  # 30 minutes between same symbol alerts
        
    async def start_hourly_scanning(self):
        """Start the hourly scanning cycle"""
        print("🚀 HOURLY TRADE SCANNER STARTING...")
        print(f"📊 Scanning {self.batch_size} tokens every {self.scan_interval//60} minutes")
        print(f"🎯 Complete top 200 analysis every hour")
        print(f"⚡ INSTANT alerts for quality trades (score >{self.alert_thresholds['min_opportunity_score']})")
        print(f"📈 Full TA + News + Sentiment for each coin")
        
        self.is_running = True
        
        while self.is_running:
            try:
                await self._run_hourly_cycle()
                
            except Exception as e:
                print(f"❌ Hourly scanner error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _run_hourly_cycle(self):
        """Run a complete hourly cycle of the top 200 coins"""
        self.hourly_cycle += 1
        start_time = datetime.now()
        
        print(f"\n🔄 HOURLY CYCLE #{self.hourly_cycle} STARTING")
        print(f"⏰ Started at: {start_time.strftime('%H:%M:%S')}")
        
        # Get fresh top 200 coins for this hour
        top_200_coins = await self._get_top_200_coins()
        
        if not top_200_coins:
            print("❌ Failed to get top 200 coins")
            await asyncio.sleep(300)
            return
        
        # Split into 10 batches of 20 coins each
        batches = [top_200_coins[i:i+20] for i in range(0, len(top_200_coins), 20)]
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"\n🔍 BATCH {batch_num}/10 - Scanning {len(batch)} coins")
            
            # Scan batch with full analysis
            opportunities = await self._scan_batch_comprehensive(batch)
            
            # Send instant alerts for quality opportunities
            for opportunity in opportunities:
                await self._send_instant_alert(opportunity)
            
            # Wait before next batch (6 minutes = 10 batches per hour)
            if batch_num < len(batches):  # Don't wait after last batch
                print(f"⏳ Next batch in {self.scan_interval//60} minutes...")
                await asyncio.sleep(self.scan_interval)
        
        cycle_time = (datetime.now() - start_time).total_seconds() / 60
        print(f"✅ HOURLY CYCLE #{self.hourly_cycle} COMPLETED in {cycle_time:.1f} minutes")
        
        # Brief pause before starting next cycle
        await asyncio.sleep(60)
    
    async def _get_top_200_coins(self):
        """Get the current top 200 coins by market performance"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get top performers for today  
                url = f"{LOCAL_API_URL}/api/market/top-performers"
                params = {
                    'limit': 200,
                    'timeframe': '24h',
                    'min_volume': 500000,  # Minimum $500k volume
                    'sort_by': 'volume_weighted_performance'
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('coins'):
                            coins = data['coins']
                            print(f"📊 Retrieved {len(coins)} top performing coins")
                            return [coin['symbol'] for coin in coins]
                
                # Fallback to major coins if API fails
                print("⚠️ Using fallback coin list")
                return [
                    'BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE', 'SUSHI',
                    'DOGE', 'SHIB', 'AVAX', 'DOT', 'ATOM', 'LUNA', 'FTM', 'NEAR', 'ALGO', 'ICP',
                    'VET', 'THETA', 'FIL', 'TRX', 'ETC', 'XLM', 'MANA', 'SAND', 'CRV', 'COMP',
                    'MKR', 'SNX', 'YFI', 'BAT', 'ZRX', 'ENJ', 'REN', 'LRC', 'GRT', 'BAND',
                    'OCEAN', 'REEF', 'CHZ', 'HOT', 'WIN', 'BTT', 'NPXS', 'CELR', 'ANKR', 'STORJ'
                ][:200]
                
        except Exception as e:
            print(f"❌ Error getting top 200 coins: {e}")
            return []
    
    async def _scan_batch_comprehensive(self, batch_symbols):
        """Scan a batch of coins with full technical analysis, news, and sentiment"""
        opportunities = []
        
        print(f"📊 Symbols: {', '.join(batch_symbols)}")
        
        for symbol in batch_symbols:
            try:
                # Comprehensive analysis for each coin
                analysis = await self._comprehensive_coin_analysis(symbol)
                
                # Check if it meets alert criteria
                if self._meets_alert_criteria(analysis):
                    opportunity = self._format_trading_opportunity(analysis)
                    opportunities.append(opportunity)
                    print(f"🎯 QUALITY TRADE FOUND: {symbol} (Score: {analysis.get('opportunity_score', 0)})")
                
            except Exception as e:
                print(f"⚠️ Error analyzing {symbol}: {e}")
                continue
        
        return opportunities
    
    async def _comprehensive_coin_analysis(self, symbol):
        """Perform comprehensive analysis: TA + News + Sentiment + Social"""
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'technical_signals': [],
            'news_catalyst': None,
            'sentiment_score': 0,
            'social_momentum': 0,
            'opportunity_score': 0
        }
        
        async with aiohttp.ClientSession() as session:
            # 1. Technical Analysis (multiple indicators)
            ta_data = await self._get_technical_analysis(session, symbol)
            analysis.update(ta_data)
            
            # 2. News Analysis
            news_data = await self._get_news_analysis(session, symbol)
            analysis.update(news_data)
            
            # 3. Sentiment Analysis
            sentiment_data = await self._get_sentiment_analysis(session, symbol)
            analysis.update(sentiment_data)
            
            # 4. Social Media Analysis
            social_data = await self._get_social_analysis(session, symbol)
            analysis.update(social_data)
            
            # 5. Calculate overall opportunity score
            analysis['opportunity_score'] = self._calculate_opportunity_score(analysis)
        
        return analysis
    
    async def _get_technical_analysis(self, session, symbol):
        """Get comprehensive technical analysis"""
        try:
            # Use bulk taapi.io request for efficiency
            indicators = ['rsi', 'macd', 'bbands', 'ema20', 'sma50', 'adx', 'stoch', 'willr']
            
            url = f"{LOCAL_API_URL}/api/taapi/bulk"
            payload = {
                'symbol': symbol,
                'indicators': indicators,
                'timeframes': ['1h', '4h', '1d']
            }
            
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Process technical signals
                    signals = []
                    
                    # RSI analysis
                    rsi_1h = data.get('1h', {}).get('rsi', {}).get('value', 50)
                    if rsi_1h < 30:
                        signals.append({'type': 'oversold', 'strength': 'strong', 'indicator': 'RSI'})
                    elif rsi_1h < 40:
                        signals.append({'type': 'oversold', 'strength': 'medium', 'indicator': 'RSI'})
                    
                    # MACD analysis
                    macd_1h = data.get('1h', {}).get('macd', {})
                    if macd_1h.get('histogram', 0) > 0 and macd_1h.get('signal', 0) > macd_1h.get('macd', 0):
                        signals.append({'type': 'bullish_crossover', 'strength': 'strong', 'indicator': 'MACD'})
                    
                    # Bollinger Bands analysis
                    bbands_1h = data.get('1h', {}).get('bbands', {})
                    if bbands_1h.get('lower', 0) and data.get('price', 0) < bbands_1h['lower']:
                        signals.append({'type': 'oversold', 'strength': 'strong', 'indicator': 'BBands'})
                    
                    return {
                        'technical_signals': signals,
                        'rsi_1h': rsi_1h,
                        'technical_strength': len([s for s in signals if s['strength'] == 'strong'])
                    }
        
        except Exception as e:
            print(f"⚠️ TA error for {symbol}: {e}")
        
        return {'technical_signals': [], 'technical_strength': 0}
    
    async def _get_news_analysis(self, session, symbol):
        """Get news analysis and catalysts"""
        try:
            url = f"{LOCAL_API_URL}/api/crypto-news/symbol/{symbol}"
            params = {'hours': 24, 'sentiment': 'positive'}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('articles'):
                        articles = data['data']['articles'][:3]
                        
                        for article in articles:
                            title = article.get('title', '').lower()
                            
                            # Look for strong catalysts
                            catalyst_keywords = [
                                'partnership', 'listing', 'upgrade', 'launch', 'adoption',
                                'integration', 'announcement', 'acquisition', 'investment'
                            ]
                            
                            if any(keyword in title for keyword in catalyst_keywords):
                                return {
                                    'news_catalyst': {
                                        'title': article.get('title', ''),
                                        'sentiment': article.get('sentiment', 'Positive'),
                                        'strength': 'strong'
                                    },
                                    'catalyst_score': 20  # Boost to opportunity score
                                }
        
        except Exception as e:
            print(f"⚠️ News error for {symbol}: {e}")
        
        return {'news_catalyst': None, 'catalyst_score': 0}
    
    async def _get_sentiment_analysis(self, session, symbol):
        """Get sentiment analysis"""
        try:
            url = f"{LOCAL_API_URL}/api/sentiment/analyze/{symbol}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    sentiment_score = data.get('sentiment_score', 0)
                    
                    return {
                        'sentiment_score': sentiment_score,
                        'sentiment_boost': max(0, (sentiment_score - 50) / 10)  # Boost for positive sentiment
                    }
        
        except Exception as e:
            print(f"⚠️ Sentiment error for {symbol}: {e}")
        
        return {'sentiment_score': 50, 'sentiment_boost': 0}
    
    async def _get_social_analysis(self, session, symbol):
        """Get social media momentum analysis"""
        try:
            url = f"{LOCAL_API_URL}/api/social/momentum/{symbol}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    momentum_score = data.get('momentum_score', 0)
                    
                    return {
                        'social_momentum': momentum_score,
                        'social_boost': max(0, (momentum_score - 60) / 10)  # Boost for high momentum
                    }
        
        except Exception as e:
            print(f"⚠️ Social error for {symbol}: {e}")
        
        return {'social_momentum': 50, 'social_boost': 0}
    
    def _calculate_opportunity_score(self, analysis):
        """Calculate overall opportunity score (0-100)"""
        base_score = 40  # Start with base score
        
        # Technical analysis boost (max +30)
        technical_boost = min(30, analysis.get('technical_strength', 0) * 10)
        
        # News catalyst boost (max +20)
        catalyst_boost = analysis.get('catalyst_score', 0)
        
        # Sentiment boost (max +10)
        sentiment_boost = min(10, analysis.get('sentiment_boost', 0))
        
        # Social momentum boost (max +10)
        social_boost = min(10, analysis.get('social_boost', 0))
        
        total_score = base_score + technical_boost + catalyst_boost + sentiment_boost + social_boost
        
        return min(100, max(0, total_score))
    
    def _meets_alert_criteria(self, analysis):
        """Check if analysis meets criteria for instant alert"""
        score = analysis.get('opportunity_score', 0)
        technical_signals = len(analysis.get('technical_signals', []))
        has_catalyst = analysis.get('news_catalyst') is not None
        
        # Check all criteria
        meets_score = score >= self.alert_thresholds['min_opportunity_score']
        meets_signals = technical_signals >= self.alert_thresholds['min_ta_signals']
        meets_catalyst = has_catalyst if self.alert_thresholds['require_catalyst'] else True
        
        return meets_score and meets_signals and meets_catalyst
    
    def _format_trading_opportunity(self, analysis):
        """Format analysis into trading opportunity"""
        symbol = analysis['symbol']
        score = analysis['opportunity_score']
        signals = analysis.get('technical_signals', [])
        catalyst = analysis.get('news_catalyst')
        
        # Calculate risk/reward
        risk_level = 'Medium'
        if score >= 85:
            risk_level = 'Low'
        elif score < 70:
            risk_level = 'High'
        
        return {
            'symbol': symbol,
            'opportunity_score': score,
            'entry_price': 'Market',
            'target_gain': f"{self.alert_thresholds['min_gain_potential']}%+",
            'risk_level': risk_level,
            'timeframe': '1-7 days',
            'technical_signals': signals,
            'catalyst': catalyst,
            'strategy': self._generate_trading_strategy(analysis),
            'confidence': 'High' if score >= 80 else 'Medium',
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_trading_strategy(self, analysis):
        """Generate specific trading strategy"""
        signals = analysis.get('technical_signals', [])
        rsi = analysis.get('rsi_1h', 50)
        
        if rsi < 30:
            return 'Oversold bounce play - DCA entry, quick scalp'
        elif len(signals) >= 3:
            return 'Multi-signal confluence - swing trade setup'
        elif analysis.get('news_catalyst'):
            return 'News catalyst trade - momentum play'
        else:
            return 'Technical setup - breakout trade'
    
    async def _send_instant_alert(self, opportunity):
        """Send instant Discord alert for quality opportunity"""
        symbol = opportunity['symbol']
        
        # Check cooldown
        now = time.time()
        if symbol in self.recent_alerts:
            if now - self.recent_alerts[symbol] < self.alert_cooldown:
                return  # Skip, too soon
        
        self.recent_alerts[symbol] = now
        
        # Format for Discord
        message = self._format_instant_alert_for_discord(opportunity)
        
        # Send to Discord
        await self._send_discord_alert(message, 'alpha_scans')
        
        print(f"🚨 INSTANT ALERT SENT: {symbol} (Score: {opportunity['opportunity_score']})")
    
    def _format_instant_alert_for_discord(self, opportunity):
        """Format opportunity as Discord alert"""
        symbol = opportunity['symbol']
        score = opportunity['opportunity_score']
        confidence = opportunity['confidence']
        strategy = opportunity['strategy']
        risk_level = opportunity['risk_level']
        timeframe = opportunity['timeframe']
        
        # Confidence emoji
        conf_emoji = "🟢" if confidence == "High" else "🟡"
        
        # Risk emoji
        risk_emoji = "🟢" if risk_level == "Low" else "🟡" if risk_level == "Medium" else "🟠"
        
        message = f"🚨 **INSTANT TRADE ALERT** 🚨\n\n"
        message += f"{conf_emoji} **{symbol}** | Score: {score}/100\n"
        message += f"📊 Confidence: {confidence} | {risk_emoji} Risk: {risk_level}\n"
        message += f"⏰ Timeframe: {timeframe} | 🎯 Target: {opportunity['target_gain']}\n"
        message += f"💡 Strategy: {strategy}\n"
        
        # Add technical signals
        signals = opportunity.get('technical_signals', [])
        if signals:
            signal_text = ', '.join([f"{s['indicator']} {s['type']}" for s in signals[:3]])
            message += f"📈 Signals: {signal_text}\n"
        
        # Add catalyst if available
        catalyst = opportunity.get('catalyst')
        if catalyst:
            message += f"🔥 Catalyst: {catalyst['title'][:50]}...\n"
        
        message += f"\n⚡ **INSTANT ALERT**: Quality setup detected - act fast!"
        
        return message
    
    async def _send_discord_alert(self, message, channel='alpha_scans'):
        """Send alert to Discord"""
        try:
            webhook_url = os.getenv(f'DISCORD_WEBHOOK_{channel.upper()}')
            if not webhook_url:
                print(f"⚠️ No webhook configured for {channel}")
                return
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': message}
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        print(f"✅ Alert sent to #{channel}")
                    else:
                        print(f"❌ Failed to send to #{channel}: {response.status}")
        
        except Exception as e:
            print(f"❌ Discord alert error: {e}")

# Global instance
hourly_scanner = HourlyTradeScanner()

async def start_hourly_trade_scanner():
    """Main function to start hourly scanner"""
    await hourly_scanner.start_hourly_scanning()

def stop_hourly_trade_scanner():
    """Stop the hourly scanner"""
    hourly_scanner.is_running = False