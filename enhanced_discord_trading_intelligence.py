#!/usr/bin/env python3
"""
ENHANCED DISCORD TRADING INTELLIGENCE SYSTEM
============================================
Advanced multi-channel crypto trading intelligence with:
- Whale movement tracking
- Liquidation monitoring  
- Market maker analysis
- Social sentiment fusion
- Real-time funding rates
- Performance tracking
- Interactive features
"""

import asyncio
import aiohttp
import json
import os
import pandas as pd
import logging
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional
import requests
import sqlite3
from dataclasses import dataclass
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingAlert:
    """Enhanced trading alert with full metadata"""
    symbol: str
    alert_type: str
    confidence: int  # 1-10 scale
    entry_price: float
    targets: List[float]
    stop_loss: float
    risk_reward: float
    catalyst: str
    timeframe: str
    volume_analysis: str
    whale_activity: bool
    funding_rate: float
    liquidation_level: float
    social_sentiment: float
    timestamp: datetime
    alert_id: str

class AdvancedDiscordTradingBot:
    """Enhanced Discord trading intelligence system"""
    
    def __init__(self):
        self.db_path = "trading_intelligence.db"
        self.init_database()
        self.performance_tracker = {}
        self.watchlists = {}
        
    def init_database(self):
        """Initialize SQLite database for performance tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Alerts performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_performance (
                alert_id TEXT PRIMARY KEY,
                symbol TEXT,
                alert_type TEXT,
                confidence INTEGER,
                entry_price REAL,
                current_price REAL,
                max_gain REAL,
                max_loss REAL,
                status TEXT,
                created_at TIMESTAMP,
                resolved_at TIMESTAMP,
                performance_score REAL
            )
        ''')
        
        # Whale movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whale_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                amount REAL,
                usd_value REAL,
                direction TEXT,
                exchange TEXT,
                timestamp TIMESTAMP,
                price_impact REAL
            )
        ''')
        
        # User interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interactions (
                alert_id TEXT,
                user_id TEXT,
                action TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    async def enhanced_whale_tracker(self):
        """Track large transactions and whale movements"""
        whale_data = []
        
        try:
            # Monitor large transactions across exchanges
            exchanges = ['binance', 'coinbase', 'kraken', 'bybit']
            
            for exchange in exchanges:
                large_trades = await self.fetch_large_trades(exchange)
                for trade in large_trades:
                    if trade['usd_value'] > 1000000:  # $1M+ transactions
                        whale_data.append({
                            'symbol': trade['symbol'],
                            'amount': trade['amount'],
                            'usd_value': trade['usd_value'],
                            'direction': trade['side'],
                            'exchange': exchange,
                            'price_impact': trade.get('price_impact', 0),
                            'timestamp': datetime.now()
                        })
            
            return whale_data
            
        except Exception as e:
            logger.error(f"Whale tracking error: {e}")
            return []
    
    async def real_time_liquidations_monitor(self):
        """Monitor liquidations for reversal opportunities"""
        try:
            # Fetch liquidation data from multiple sources
            liquidation_data = await self.fetch_liquidation_data()
            
            significant_liquidations = []
            for liq in liquidation_data:
                if liq['usd_value'] > 500000:  # $500k+ liquidations
                    significant_liquidations.append({
                        'symbol': liq['symbol'],
                        'side': liq['side'],
                        'amount': liq['amount'],
                        'price': liq['price'],
                        'exchange': liq['exchange'],
                        'cascade_risk': self.calculate_cascade_risk(liq),
                        'reversal_probability': self.calculate_reversal_probability(liq)
                    })
            
            return significant_liquidations
            
        except Exception as e:
            logger.error(f"Liquidations monitoring error: {e}")
            return []
    
    async def funding_rates_analyzer(self):
        """Analyze funding rates for sentiment signals"""
        try:
            funding_data = {}
            top_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'MATIC', 'AVAX', 'DOT']
            
            for symbol in top_symbols:
                rates = await self.fetch_funding_rates(symbol)
                if rates:
                    funding_data[symbol] = {
                        'current_rate': rates['current'],
                        'trend': rates['trend'],
                        'extremity': rates['extremity'],
                        'reversal_signal': abs(rates['current']) > 0.01,  # 1% threshold
                        'sentiment': 'bearish' if rates['current'] > 0.005 else 'bullish' if rates['current'] < -0.005 else 'neutral'
                    }
            
            return funding_data
            
        except Exception as e:
            logger.error(f"Funding rates analysis error: {e}")
            return {}
    
    async def market_structure_analyzer(self):
        """Analyze market structure and order book depth"""
        try:
            structure_analysis = {}
            
            # Analyze order book imbalances
            for symbol in ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']:
                orderbook = await self.fetch_orderbook_depth(symbol)
                if orderbook:
                    bid_strength = sum([order['amount'] for order in orderbook['bids'][:20]])
                    ask_strength = sum([order['amount'] for order in orderbook['asks'][:20]])
                    
                    structure_analysis[symbol] = {
                        'bid_ask_ratio': bid_strength / ask_strength if ask_strength > 0 else 0,
                        'market_bias': 'bullish' if bid_strength > ask_strength * 1.2 else 'bearish' if ask_strength > bid_strength * 1.2 else 'neutral',
                        'liquidity_score': (bid_strength + ask_strength) / 2,
                        'manipulation_risk': self.detect_spoofing(orderbook)
                    }
            
            return structure_analysis
            
        except Exception as e:
            logger.error(f"Market structure analysis error: {e}")
            return {}
    
    async def social_sentiment_fusion(self):
        """Fuse social sentiment from multiple sources"""
        try:
            sentiment_data = {}
            
            # Twitter sentiment
            twitter_sentiment = await self.fetch_twitter_sentiment()
            
            # Reddit sentiment
            reddit_sentiment = await self.fetch_reddit_sentiment()
            
            # Fear & Greed Index
            fear_greed = await self.fetch_fear_greed_index()
            
            # LunarCrush data
            lunarcrush_data = await self.fetch_lunarcrush_sentiment()
            
            # Fusion algorithm
            for symbol in ['BTC', 'ETH', 'SOL']:
                scores = []
                if twitter_sentiment.get(symbol):
                    scores.append(twitter_sentiment[symbol]['score'])
                if reddit_sentiment.get(symbol):
                    scores.append(reddit_sentiment[symbol]['score'])
                if lunarcrush_data.get(symbol):
                    scores.append(lunarcrush_data[symbol]['sentiment_score'])
                
                if scores:
                    sentiment_data[symbol] = {
                        'composite_score': np.mean(scores),
                        'confidence': len(scores) / 3,  # How many sources we have
                        'trend': 'bullish' if np.mean(scores) > 0.6 else 'bearish' if np.mean(scores) < 0.4 else 'neutral',
                        'volatility': np.std(scores) if len(scores) > 1 else 0
                    }
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Social sentiment fusion error: {e}")
            return {}
    
    async def performance_tracker_update(self):
        """Update performance tracking for all active alerts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all active alerts
            cursor.execute('''
                SELECT alert_id, symbol, entry_price, confidence 
                FROM alert_performance 
                WHERE status = 'active'
            ''')
            
            active_alerts = cursor.fetchall()
            
            for alert_id, symbol, entry_price, confidence in active_alerts:
                current_price = await self.get_current_price(symbol)
                if current_price:
                    performance = ((current_price - entry_price) / entry_price) * 100
                    
                    # Update performance
                    cursor.execute('''
                        UPDATE alert_performance 
                        SET current_price = ?, performance_score = ?
                        WHERE alert_id = ?
                    ''', (current_price, performance, alert_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Performance tracking error: {e}")
    
    async def generate_enhanced_discord_alerts(self):
        """Generate comprehensive Discord alerts across all channels"""
        try:
            # Gather all intelligence
            whale_movements = await self.enhanced_whale_tracker()
            liquidations = await self.real_time_liquidations_monitor()
            funding_rates = await self.funding_rates_analyzer()
            market_structure = await self.market_structure_analyzer()
            social_sentiment = await self.social_sentiment_fusion()
            
            # Generate alerts for each channel
            await self.send_whale_alerts(whale_movements)
            await self.send_liquidation_alerts(liquidations)
            await self.send_funding_alerts(funding_rates)
            await self.send_market_structure_alerts(market_structure)
            await self.send_sentiment_alerts(social_sentiment)
            
            # Generate composite intelligence alerts
            await self.send_composite_intelligence_alerts(
                whale_movements, liquidations, funding_rates, 
                market_structure, social_sentiment
            )
            
        except Exception as e:
            logger.error(f"Enhanced alerts generation error: {e}")
    
    async def send_whale_alerts(self, whale_data):
        """Send whale movement alerts to #whale-alerts channel"""
        if not whale_data:
            return
        
        message = "🐋 **WHALE MOVEMENT ALERTS** 🐋\n\n"
        
        for whale in whale_data[:5]:  # Top 5 movements
            direction_emoji = "🟢" if whale['direction'] == 'buy' else "🔴"
            impact_emoji = "⚡" if whale['price_impact'] > 2 else "📊"
            
            message += f"{direction_emoji} **{whale['symbol']}** - ${whale['usd_value']:,.0f}\n"
            message += f"   {impact_emoji} Amount: {whale['amount']:,.2f} | Exchange: {whale['exchange']}\n"
            message += f"   📈 Price Impact: {whale['price_impact']:.2f}%\n"
            message += f"   ⏰ {whale['timestamp'].strftime('%H:%M UTC')}\n\n"
        
        message += "💡 **Strategy**: Watch for follow-through or reversal patterns"
        
        await self.send_discord_message(message, 'whale_alerts')
    
    async def send_liquidation_alerts(self, liquidations):
        """Send liquidation alerts to #liquidations channel"""
        if not liquidations:
            return
        
        message = "💥 **LIQUIDATION ALERTS** 💥\n\n"
        
        for liq in liquidations[:3]:
            side_emoji = "🩸" if liq['side'] == 'long' else "💚" if liq['side'] == 'short' else "⚡"
            cascade_emoji = "🚨" if liq['cascade_risk'] > 0.7 else "⚠️" if liq['cascade_risk'] > 0.4 else "📊"
            
            message += f"{side_emoji} **{liq['symbol']}** {liq['side'].upper()} LIQUIDATION\n"
            message += f"   💰 Amount: ${liq['amount']:,.0f} at ${liq['price']:,.2f}\n"
            message += f"   {cascade_emoji} Cascade Risk: {liq['cascade_risk']:.0%}\n"
            message += f"   🔄 Reversal Probability: {liq['reversal_probability']:.0%}\n"
            message += f"   🏛️ Exchange: {liq['exchange']}\n\n"
        
        message += "🎯 **Strategy**: Look for bounces after heavy liquidations"
        
        await self.send_discord_message(message, 'liquidations')
    
    async def send_funding_alerts(self, funding_data):
        """Send funding rate alerts to #funding-rates channel"""
        if not funding_data:
            return
        
        message = "📊 **FUNDING RATE ANALYSIS** 📊\n\n"
        
        extreme_rates = {k: v for k, v in funding_data.items() if v['reversal_signal']}
        
        if extreme_rates:
            message += "🚨 **EXTREME FUNDING RATES** (Reversal Signals):\n"
            for symbol, data in extreme_rates.items():
                sentiment_emoji = "📈" if data['sentiment'] == 'bullish' else "📉" if data['sentiment'] == 'bearish' else "➡️"
                message += f"{sentiment_emoji} **{symbol}**: {data['current_rate']:.3%} ({data['sentiment']})\n"
            message += "\n"
        
        message += "📈 **ALL FUNDING RATES**:\n"
        for symbol, data in funding_data.items():
            trend_emoji = "🔥" if data['trend'] == 'increasing' else "❄️" if data['trend'] == 'decreasing' else "🔄"
            message += f"{trend_emoji} **{symbol}**: {data['current_rate']:.3%}\n"
        
        message += "\n💡 **Strategy**: Negative rates = bullish, Positive rates = bearish"
        
        await self.send_discord_message(message, 'funding_rates')
    
    async def send_market_structure_alerts(self, structure_data):
        """Send market structure alerts to #market-structure channel"""
        if not structure_data:
            return
        
        message = "🏗️ **MARKET STRUCTURE ANALYSIS** 🏗️\n\n"
        
        for symbol, data in structure_data.items():
            bias_emoji = "🟢" if data['market_bias'] == 'bullish' else "🔴" if data['market_bias'] == 'bearish' else "🟡"
            manipulation_emoji = "⚠️" if data['manipulation_risk'] else "✅"
            
            message += f"{bias_emoji} **{symbol}** - {data['market_bias'].upper()}\n"
            message += f"   📊 Bid/Ask Ratio: {data['bid_ask_ratio']:.2f}\n"
            message += f"   💧 Liquidity Score: {data['liquidity_score']:,.0f}\n"
            message += f"   {manipulation_emoji} Manipulation Risk: {'High' if data['manipulation_risk'] else 'Low'}\n\n"
        
        message += "🎯 **Strategy**: Trade with the structure, avoid manipulated levels"
        
        await self.send_discord_message(message, 'market_structure')
    
    async def send_sentiment_alerts(self, sentiment_data):
        """Send social sentiment alerts to #social-sentiment channel"""
        if not sentiment_data:
            return
        
        message = "🌐 **SOCIAL SENTIMENT FUSION** 🌐\n\n"
        
        for symbol, data in sentiment_data.items():
            trend_emoji = "🚀" if data['trend'] == 'bullish' else "🩸" if data['trend'] == 'bearish' else "🔄"
            confidence_emoji = "🎯" if data['confidence'] > 0.8 else "📊" if data['confidence'] > 0.5 else "❓"
            
            message += f"{trend_emoji} **{symbol}** - {data['trend'].upper()}\n"
            message += f"   {confidence_emoji} Score: {data['composite_score']:.1f}/10 (Confidence: {data['confidence']:.0%})\n"
            message += f"   📈 Volatility: {data['volatility']:.2f}\n\n"
        
        message += "💡 **Strategy**: High confidence sentiment often leads price"
        
        await self.send_discord_message(message, 'social_sentiment')
    
    async def send_composite_intelligence_alerts(self, whales, liquidations, funding, structure, sentiment):
        """Send high-conviction composite signals to #alpha-scans"""
        try:
            composite_signals = []
            
            # Analyze confluence of signals
            symbols = set()
            if whales:
                symbols.update([w['symbol'] for w in whales])
            if funding:
                symbols.update(funding.keys())
            if sentiment:
                symbols.update(sentiment.keys())
            
            for symbol in symbols:
                signal_strength = 0
                reasons = []
                
                # Whale activity
                whale_activity = any(w['symbol'] == symbol for w in whales)
                if whale_activity:
                    signal_strength += 2
                    reasons.append("🐋 Whale activity detected")
                
                # Extreme funding
                if symbol in funding and funding[symbol]['reversal_signal']:
                    signal_strength += 3
                    reasons.append(f"📊 Extreme funding: {funding[symbol]['current_rate']:.3%}")
                
                # Strong sentiment
                if symbol in sentiment and sentiment[symbol]['confidence'] > 0.7:
                    if sentiment[symbol]['trend'] in ['bullish', 'bearish']:
                        signal_strength += 2
                        reasons.append(f"🌐 Strong {sentiment[symbol]['trend']} sentiment")
                
                # Market structure alignment
                symbol_formatted = f"{symbol}/USDT"
                if symbol_formatted in structure:
                    if structure[symbol_formatted]['market_bias'] != 'neutral':
                        signal_strength += 1
                        reasons.append(f"🏗️ {structure[symbol_formatted]['market_bias']} structure")
                
                # Generate alert if signal strength is high
                if signal_strength >= 4:
                    composite_signals.append({
                        'symbol': symbol,
                        'strength': signal_strength,
                        'reasons': reasons
                    })
            
            if composite_signals:
                message = "🎯 **COMPOSITE INTELLIGENCE SIGNALS** 🎯\n\n"
                message += "⚡ **HIGH CONVICTION SETUPS** (4+ confluence factors):\n\n"
                
                for signal in sorted(composite_signals, key=lambda x: x['strength'], reverse=True)[:3]:
                    strength_emoji = "🔥" if signal['strength'] >= 6 else "⚡" if signal['strength'] >= 5 else "📊"
                    
                    message += f"{strength_emoji} **{signal['symbol']}** (Strength: {signal['strength']}/8)\n"
                    for reason in signal['reasons']:
                        message += f"   {reason}\n"
                    message += "\n"
                
                message += "🚨 **STRATEGY**: These setups have multiple confluence factors - monitor for entries!"
                
                await self.send_discord_message(message, 'alpha_scans')
        
        except Exception as e:
            logger.error(f"Composite intelligence error: {e}")
    
    async def send_discord_message(self, message, channel_type):
        """Send message to appropriate Discord channel"""
        try:
            webhook_map = {
                'whale_alerts': 'DISCORD_WEBHOOK_WHALE_ALERTS',
                'liquidations': 'DISCORD_WEBHOOK_LIQUIDATIONS',
                'funding_rates': 'DISCORD_WEBHOOK_FUNDING_RATES',
                'market_structure': 'DISCORD_WEBHOOK_MARKET_STRUCTURE',
                'social_sentiment': 'DISCORD_WEBHOOK_SOCIAL_SENTIMENT',
                'alpha_scans': 'DISCORD_WEBHOOK_ALPHA_SCANS',
                'performance': 'DISCORD_WEBHOOK_PERFORMANCE'
            }
            
            webhook_url = os.getenv(webhook_map.get(channel_type, 'DISCORD_WEBHOOK_ALERTS'))
            
            if not webhook_url:
                # Fallback to main alerts channel
                webhook_url = os.getenv('DISCORD_WEBHOOK_ALERTS')
                if not webhook_url:
                    return
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': message}
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"Alert sent to #{channel_type}")
                    else:
                        logger.error(f"Failed to send to #{channel_type}: {response.status}")
        
        except Exception as e:
            logger.error(f"Discord message error: {e}")
    
    # Placeholder methods for external API calls
    async def fetch_large_trades(self, exchange):
        """Fetch large trades from exchange"""
        # Implementation would connect to exchange APIs
        return []
    
    async def fetch_liquidation_data(self):
        """Fetch liquidation data"""
        # Implementation would connect to liquidation APIs
        return []
    
    async def fetch_funding_rates(self, symbol):
        """Fetch funding rates for symbol"""
        # Implementation would connect to funding rate APIs
        return None
    
    async def fetch_orderbook_depth(self, symbol):
        """Fetch order book depth"""
        # Implementation would connect to exchange APIs
        return None
    
    async def fetch_twitter_sentiment(self):
        """Fetch Twitter sentiment"""
        # Implementation would connect to Twitter API
        return {}
    
    async def fetch_reddit_sentiment(self):
        """Fetch Reddit sentiment"""
        # Implementation would connect to Reddit API
        return {}
    
    async def fetch_fear_greed_index(self):
        """Fetch Fear & Greed Index"""
        # Implementation would connect to Fear & Greed API
        return None
    
    async def fetch_lunarcrush_sentiment(self):
        """Fetch LunarCrush sentiment data"""
        # Implementation would connect to LunarCrush API
        return {}
    
    async def get_current_price(self, symbol):
        """Get current price for symbol"""
        # Implementation would connect to price API
        return None
    
    def calculate_cascade_risk(self, liquidation):
        """Calculate risk of cascade liquidations"""
        # Implementation of cascade risk algorithm
        return 0.5
    
    def calculate_reversal_probability(self, liquidation):
        """Calculate probability of price reversal"""
        # Implementation of reversal probability algorithm
        return 0.6
    
    def detect_spoofing(self, orderbook):
        """Detect order book spoofing/manipulation"""
        # Implementation of spoofing detection
        return False

# Global instance
enhanced_bot = AdvancedDiscordTradingBot()

async def run_enhanced_intelligence_system():
    """Main function to run enhanced Discord trading intelligence"""
    await enhanced_bot.generate_enhanced_discord_alerts()
    await enhanced_bot.performance_tracker_update()

if __name__ == "__main__":
    asyncio.run(run_enhanced_intelligence_system())