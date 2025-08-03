#!/usr/bin/env python3
"""
Multi-Channel Discord Bot - Intelligent Trading Alerts System
Channel-specific alerts with different schedules and content types
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
import schedule
import threading
import time

# Import existing functions
try:
    from automated_trading_alerts import (
        convert_csv_to_json, 
        analyze_trading_conditions, 
        cleanup_old_files
    )
except ImportError:
    print("❌ Could not import from automated_trading_alerts.py")
    sys.exit(1)

# Configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

# Discord Channel Configuration
DISCORD_CHANNELS = {
    'alerts': {
        'id': '1398000506068009032',
        'webhook_url': os.getenv('DISCORD_ALERTS_WEBHOOK'),
        'name': 'alerts',
        'purpose': 'Breaking news, risk alerts, market updates'
    },
    'portfolio': {
        'id': '1399451217372905584', 
        'webhook_url': os.getenv('DISCORD_PORTFOLIO_WEBHOOK'),
        'name': 'portfolio',
        'purpose': 'Portfolio analysis, position alerts, trading signals'
    },
    'alpha_scans': {
        'id': '1399790636990857277',
        'webhook_url': os.getenv('DISCORD_ALPHA_WEBHOOK'),
        'name': 'alpha-scans',
        'purpose': 'Trading opportunities, early entries, market scanning'
    }
}

class DiscordChannelBot:
    """Multi-channel Discord bot with intelligent routing"""
    
    def __init__(self):
        self.session = None
        
    async def start_session(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def send_to_channel(self, channel_name: str, message: str, embed_data: dict = None):
        """Send message to specific Discord channel"""
        if not self.session:
            await self.start_session()
            
        channel = DISCORD_CHANNELS.get(channel_name)
        if not channel or not channel['webhook_url']:
            print(f"❌ No webhook configured for {channel_name}")
            return False
            
        payload = {
            "content": message,
            "username": f"Trading Bot - {channel['name'].title()}"
        }
        
        if embed_data:
            payload["embeds"] = [embed_data]
            
        try:
            async with self.session.post(channel['webhook_url'], json=payload) as response:
                if response.status == 204:
                    print(f"✅ Message sent to #{channel['name']}")
                    return True
                else:
                    print(f"❌ Failed to send to #{channel['name']}: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Error sending to #{channel['name']}: {e}")
            return False

class AlertsChannelManager:
    """Manages alerts channel - breaking news, risk alerts, market updates"""
    
    def __init__(self, bot: DiscordChannelBot):
        self.bot = bot
        
    async def fetch_breaking_news(self):
        """Fetch breaking crypto news"""
        try:
            async with self.bot.session.get(
                f"{RAILWAY_API_URL}/api/crypto-news/breaking-news",
                params={'items': 5, 'hours': 6}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])[:3]
        except Exception as e:
            print(f"❌ Breaking news error: {e}")
        return []
    
    async def fetch_risk_alerts(self):
        """Fetch risk alerts and warnings"""
        try:
            async with self.bot.session.get(f"{RAILWAY_API_URL}/api/crypto-news/risk-alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('alerts', [])[:2]
        except Exception as e:
            print(f"❌ Risk alerts error: {e}")
        return []
    
    async def fetch_pump_dump_alerts(self):
        """Fetch pump/dump detection signals"""
        try:
            async with self.bot.session.get(f"{RAILWAY_API_URL}/api/crypto-news/pump-dump-detector") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('signals', [])[:2]
        except Exception as e:
            print(f"❌ Pump/dump alerts error: {e}")
        return []
    
    async def send_alerts_update(self):
        """Send comprehensive alerts update"""
        print(f"🚨 Sending alerts update to #{DISCORD_CHANNELS['alerts']['name']}")
        
        # Fetch all alert data
        breaking_news, risk_alerts, pump_dump = await asyncio.gather(
            self.fetch_breaking_news(),
            self.fetch_risk_alerts(),
            self.fetch_pump_dump_alerts(),
            return_exceptions=True
        )
        
        # Build alert message
        message_parts = []
        
        # Breaking news section
        if isinstance(breaking_news, list) and breaking_news:
            message_parts.append("🚨 **BREAKING CRYPTO NEWS** 🚨")
            for news in breaking_news:
                sentiment_emoji = "📈" if news.get('sentiment') == 'Positive' else "📉" if news.get('sentiment') == 'Negative' else "📊"
                message_parts.append(f"{sentiment_emoji} **{news.get('title', 'News')[:80]}**")
                message_parts.append(f"   Source: {news.get('source_name', 'Unknown')} | Sentiment: {news.get('sentiment', 'Neutral')}")
            message_parts.append("")
        
        # Risk alerts section
        if isinstance(risk_alerts, list) and risk_alerts:
            message_parts.append("⚠️ **RISK ALERTS** ⚠️")
            for alert in risk_alerts:
                message_parts.append(f"🚨 {alert.get('title', 'Risk detected')[:100]}")
            message_parts.append("")
        
        # Pump/dump detection
        if isinstance(pump_dump, list) and pump_dump:
            message_parts.append("⚡ **PUMP/DUMP DETECTION** ⚡")
            for signal in pump_dump:
                message_parts.append(f"📊 {signal.get('title', 'Signal detected')[:100]}")
            message_parts.append("")
        
        if message_parts:
            message_parts.append(f"🕐 **Alert Time**: {datetime.now().strftime('%I:%M %p CST')}")
            full_message = "\n".join(message_parts)
            await self.bot.send_to_channel('alerts', full_message[:2000])
        else:
            await self.bot.send_to_channel('alerts', "✅ No urgent market alerts at this time")

class PortfolioChannelManager:
    """Manages portfolio channel - positions, trading signals, hourly analysis"""
    
    def __init__(self, bot: DiscordChannelBot):
        self.bot = bot
        
    async def fetch_portfolio_news(self, symbols):
        """Fetch portfolio-specific news"""
        try:
            async with self.bot.session.get(
                f"{RAILWAY_API_URL}/api/crypto-news/portfolio",
                params={'symbols': ','.join(symbols)}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])[:3]
        except Exception as e:
            print(f"❌ Portfolio news error: {e}")
        return []
    
    def get_portfolio_symbols_from_positions(self, positions):
        """Extract symbols from positions data"""
        if not positions:
            return ['BTC', 'ETH', 'SOL', 'XRP', 'ADA']  # Default portfolio
        
        symbols = set()
        for pos in positions:
            symbol = pos.get('symbol', '')
            if symbol:
                clean_symbol = symbol.replace('-USDT', '').replace('/USD', '').replace('-USD', '')
                symbols.add(clean_symbol)
        
        return list(symbols)[:8]  # Max 8 symbols
    
    async def send_portfolio_update(self):
        """Send hourly portfolio analysis"""
        print(f"💼 Sending portfolio update to #{DISCORD_CHANNELS['portfolio']['name']}")
        
        # Get positions data
        positions = convert_csv_to_json()
        if not positions:
            await self.bot.send_to_channel('portfolio', "📭 No position data available for analysis")
            return
        
        # Analyze trading conditions
        trading_alerts = analyze_trading_conditions(positions)
        
        # Get portfolio symbols and fetch news
        portfolio_symbols = self.get_portfolio_symbols_from_positions(positions)
        portfolio_news = await self.fetch_portfolio_news(portfolio_symbols)
        
        # Build portfolio message
        message_parts = []
        message_parts.append("💼 **PORTFOLIO ANALYSIS** 💼")
        message_parts.append(f"📊 **Positions**: {len(positions)} active")
        message_parts.append(f"🎯 **Tracking**: {', '.join(portfolio_symbols[:5])}")
        message_parts.append("")
        
        # Trading alerts summary
        if trading_alerts:
            alert_types = {}
            for alert in trading_alerts:
                alert_type = alert.get('type', 'unknown')
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            message_parts.append("🚨 **Position Alerts**:")
            emoji_map = {
                'oversold': '📉', 'overbought': '📈', 'losing_trade': '⚠️',
                'no_stop_loss': '🛡️', 'high_profit': '💰'
            }
            
            for alert_type, count in alert_types.items():
                emoji = emoji_map.get(alert_type, '📊')
                formatted_type = alert_type.replace('_', ' ').title()
                message_parts.append(f"{emoji} {formatted_type}: {count}")
            
            # Show top 3 critical alerts
            critical_alerts = [a for a in trading_alerts if a.get('type') in ['losing_trade', 'no_stop_loss']][:3]
            if critical_alerts:
                message_parts.append("")
                message_parts.append("🔥 **Critical Alerts**:")
                for alert in critical_alerts:
                    symbol = alert.get('symbol', 'Unknown')
                    message_parts.append(f"• {symbol}: {alert.get('message', 'Alert')[:60]}...")
        else:
            message_parts.append("✅ **All positions within normal parameters**")
        
        # Portfolio news
        if portfolio_news:
            message_parts.append("")
            message_parts.append("📰 **Portfolio News**:")
            for news in portfolio_news:
                message_parts.append(f"• {news.get('title', 'News')[:80]}...")
        
        message_parts.append("")
        message_parts.append(f"🕐 **Analysis Time**: {datetime.now().strftime('%I:%M %p CST')}")
        
        full_message = "\n".join(message_parts)
        await self.bot.send_to_channel('portfolio', full_message[:2000])

class AlphaScansChannelManager:
    """Manages alpha scans channel - trading opportunities, early entries (twice daily)"""
    
    def __init__(self, bot: DiscordChannelBot):
        self.bot = bot
        
    async def fetch_trading_opportunities(self):
        """Fetch trading opportunities"""
        try:
            async with self.bot.session.get(f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('opportunities', [])[:4]
        except Exception as e:
            print(f"❌ Trading opportunities error: {e}")
        return []
    
    async def fetch_bullish_signals(self):
        """Fetch bullish signals"""
        try:
            async with self.bot.session.get(f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('signals', [])[:3]
        except Exception as e:
            print(f"❌ Bullish signals error: {e}")
        return []
    
    async def fetch_market_intelligence(self):
        """Fetch comprehensive market intelligence"""
        try:
            async with self.bot.session.get(f"{RAILWAY_API_URL}/api/crypto-news/market-intelligence") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('intelligence', [])[:2]
        except Exception as e:
            print(f"❌ Market intelligence error: {e}")
        return []
    
    async def send_alpha_scans_update(self):
        """Send twice-daily alpha scans update"""
        print(f"🔍 Sending alpha scans to #{DISCORD_CHANNELS['alpha_scans']['name']}")
        
        # Fetch all opportunity data
        opportunities, bullish_signals, market_intel = await asyncio.gather(
            self.fetch_trading_opportunities(),
            self.fetch_bullish_signals(),
            self.fetch_market_intelligence(),
            return_exceptions=True
        )
        
        # Build alpha scans message
        message_parts = []
        message_parts.append("🔍 **ALPHA OPPORTUNITY SCANS** 🔍")
        message_parts.append(f"🎯 **Scan Time**: {datetime.now().strftime('%I:%M %p CST')}")
        message_parts.append("")
        
        # Trading opportunities
        if isinstance(opportunities, list) and opportunities:
            message_parts.append("📈 **TRADING OPPORTUNITIES**")
            for i, opp in enumerate(opportunities, 1):
                message_parts.append(f"{i}. **{opp.get('title', 'Opportunity')[:70]}**")
                if opp.get('summary'):
                    message_parts.append(f"   {opp['summary'][:100]}...")
            message_parts.append("")
        
        # Bullish signals
        if isinstance(bullish_signals, list) and bullish_signals:
            message_parts.append("🚀 **BULLISH SIGNALS**")
            for signal in bullish_signals:
                message_parts.append(f"📊 {signal.get('title', 'Bullish signal')[:80]}")
            message_parts.append("")
        
        # Market intelligence
        if isinstance(market_intel, list) and market_intel:
            message_parts.append("🧠 **MARKET INTELLIGENCE**")
            for intel in market_intel:
                message_parts.append(f"💡 {intel.get('title', 'Market insight')[:80]}")
            message_parts.append("")
        
        if len(message_parts) <= 3:  # Only header
            message_parts.append("📭 **No alpha opportunities detected in current scan**")
            message_parts.append("🔄 **Next scan in 12 hours**")
        else:
            message_parts.append("⚡ **Take action quickly - alpha opportunities don't last long!**")
        
        full_message = "\n".join(message_parts)
        await self.bot.send_to_channel('alpha_scans', full_message[:2000])

class MultiChannelScheduler:
    """Scheduler for multi-channel Discord bot"""
    
    def __init__(self):
        self.bot = DiscordChannelBot()
        self.alerts_manager = AlertsChannelManager(self.bot)
        self.portfolio_manager = PortfolioChannelManager(self.bot)
        self.alpha_manager = AlphaScansChannelManager(self.bot)
        self.running = False
        
    async def run_alerts_update(self):
        """Run alerts channel update"""
        try:
            await self.bot.start_session()
            await self.alerts_manager.send_alerts_update()
        except Exception as e:
            print(f"❌ Alerts update error: {e}")
    
    async def run_portfolio_update(self):
        """Run portfolio channel update (hourly)"""
        try:
            await self.bot.start_session()
            await self.portfolio_manager.send_portfolio_update()
        except Exception as e:
            print(f"❌ Portfolio update error: {e}")
    
    async def run_alpha_scans_update(self):
        """Run alpha scans update (twice daily)"""
        try:
            await self.bot.start_session()
            await self.alpha_manager.send_alpha_scans_update()
        except Exception as e:
            print(f"❌ Alpha scans error: {e}")
    
    def schedule_updates(self):
        """Schedule all channel updates"""
        # Portfolio updates every hour
        schedule.every().hour.do(lambda: asyncio.run(self.run_portfolio_update()))
        
        # Alpha scans twice daily (9 AM and 9 PM)
        schedule.every().day.at("09:00").do(lambda: asyncio.run(self.run_alpha_scans_update()))
        schedule.every().day.at("21:00").do(lambda: asyncio.run(self.run_alpha_scans_update()))
        
        # Alerts updates every 4 hours
        schedule.every(4).hours.do(lambda: asyncio.run(self.run_alerts_update()))
        
        print("📅 Scheduled updates:")
        print("   💼 Portfolio: Every hour")
        print("   🔍 Alpha Scans: 9 AM & 9 PM daily")
        print("   🚨 Alerts: Every 4 hours")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    async def start(self):
        """Start the multi-channel bot system"""
        self.running = True
        
        print("🚀 MULTI-CHANNEL DISCORD BOT STARTING")
        print("=" * 50)
        
        # Test webhooks
        webhook_count = sum(1 for ch in DISCORD_CHANNELS.values() if ch['webhook_url'])
        if webhook_count == 0:
            print("❌ No Discord webhooks configured!")
            print("Set environment variables:")
            print("   DISCORD_ALERTS_WEBHOOK")
            print("   DISCORD_PORTFOLIO_WEBHOOK") 
            print("   DISCORD_ALPHA_WEBHOOK")
            return
        
        print(f"✅ {webhook_count}/3 Discord webhooks configured")
        
        # Schedule updates
        self.schedule_updates()
        
        # Run initial updates
        print("🔄 Running initial updates...")
        await self.run_portfolio_update()
        await self.run_alerts_update()
        
        # Start scheduler in background
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        
        print("✅ Multi-channel Discord bot is running!")
        print("🔄 All channels will update automatically on schedule")
        
        # Keep running
        try:
            while self.running:
                await asyncio.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("\n🛑 Stopping multi-channel bot...")
        finally:
            self.running = False
            await self.bot.close_session()

async def main():
    """Main entry point"""
    scheduler = MultiChannelScheduler()
    await scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())