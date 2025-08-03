#!/usr/bin/env python3
"""
Multi-Channel Discord Bot - Token-Based Version
Alternative to webhook version for users who prefer Discord bot tokens
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

# Discord.py imports
try:
    import discord
    from discord.ext import commands, tasks
except ImportError:
    print("❌ Discord.py not installed. Install with: pip install discord.py")
    sys.exit(1)

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
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Discord Channel IDs
CHANNELS = {
    'alerts': 1398000506068009032,
    'portfolio': 1399451217372905584, 
    'alpha_scans': 1399790636990857277
}

class TradingBot(commands.Bot):
    """Multi-channel Discord trading bot using bot token"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=None
        )
        
        self.session = None
        
    async def setup_hook(self):
        """Initialize HTTP session and start background tasks"""
        self.session = aiohttp.ClientSession()
        
        # Start background tasks
        self.portfolio_updates.start()
        self.alpha_scans.start()  
        self.alerts_updates.start()
        
        print("🚀 Trading bot background tasks started!")
        
    async def close(self):
        """Clean shutdown"""
        if self.session:
            await self.session.close()
        await super().close()
        
    async def on_ready(self):
        """Bot ready event"""
        print(f"✅ {self.user} connected to Discord!")
        print(f"📊 Monitoring {len(CHANNELS)} channels")
        
        # Verify channel access
        for name, channel_id in CHANNELS.items():
            channel = self.get_channel(channel_id)
            if channel:
                print(f"   ✅ #{channel.name} ({name})")
            else:
                print(f"   ❌ Channel {channel_id} not accessible ({name})")
    
    # Portfolio Updates - Every Hour
    @tasks.loop(hours=1)
    async def portfolio_updates(self):
        """Send hourly portfolio analysis to #portfolio"""
        try:
            channel = self.get_channel(CHANNELS['portfolio'])
            if not channel:
                return
                
            print(f"💼 Sending portfolio update to #{channel.name}")
            
            # Get positions data
            positions = convert_csv_to_json()
            if not positions:
                await channel.send("📭 No position data available for analysis")
                return
            
            # Analyze trading conditions
            trading_alerts = analyze_trading_conditions(positions)
            
            # Get portfolio symbols and fetch news
            portfolio_symbols = self.get_portfolio_symbols(positions)
            portfolio_news = await self.fetch_portfolio_news(portfolio_symbols)
            
            # Build portfolio message
            embed = discord.Embed(
                title="💼 Portfolio Analysis",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="📊 Overview",
                value=f"**Positions**: {len(positions)} active\n**Tracking**: {', '.join(portfolio_symbols[:5])}",
                inline=False
            )
            
            # Trading alerts summary
            if trading_alerts:
                alert_types = {}
                for alert in trading_alerts:
                    alert_type = alert.get('type', 'unknown')
                    alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
                
                emoji_map = {
                    'oversold': '📉', 'overbought': '📈', 'losing_trade': '⚠️',
                    'no_stop_loss': '🛡️', 'high_profit': '💰'
                }
                
                alerts_text = []
                for alert_type, count in alert_types.items():
                    emoji = emoji_map.get(alert_type, '📊')
                    formatted_type = alert_type.replace('_', ' ').title()
                    alerts_text.append(f"{emoji} {formatted_type}: {count}")
                
                embed.add_field(
                    name="🚨 Position Alerts",
                    value="\n".join(alerts_text),
                    inline=True
                )
                
                # Show critical alerts
                critical_alerts = [a for a in trading_alerts if a.get('type') in ['losing_trade', 'no_stop_loss']][:3]
                if critical_alerts:
                    critical_text = []
                    for alert in critical_alerts:
                        symbol = alert.get('symbol', 'Unknown')
                        message = alert.get('message', 'Alert')[:50]
                        critical_text.append(f"• {symbol}: {message}...")
                    
                    embed.add_field(
                        name="🔥 Critical Alerts",
                        value="\n".join(critical_text),
                        inline=False
                    )
            else:
                embed.add_field(
                    name="✅ Status",
                    value="All positions within normal parameters",
                    inline=False
                )
            
            # Portfolio news
            if portfolio_news:
                news_text = []
                for news in portfolio_news[:3]:
                    title = news.get('title', 'News')[:60]
                    news_text.append(f"• {title}...")
                
                embed.add_field(
                    name="📰 Portfolio News",
                    value="\n".join(news_text),
                    inline=False
                )
            
            await channel.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Portfolio update error: {e}")
    
    # Alpha Scans - Twice Daily (9 AM & 9 PM)
    @tasks.loop(hours=12)
    async def alpha_scans(self):
        """Send alpha opportunity scans to #alpha-scans"""
        try:
            # Only run at 9 AM and 9 PM
            current_hour = datetime.now().hour
            if current_hour not in [9, 21]:
                return
                
            channel = self.get_channel(CHANNELS['alpha_scans'])
            if not channel:
                return
                
            print(f"🔍 Sending alpha scans to #{channel.name}")
            
            # Fetch opportunity data
            opportunities, bullish_signals, market_intel = await asyncio.gather(
                self.fetch_trading_opportunities(),
                self.fetch_bullish_signals(),
                self.fetch_market_intelligence(),
                return_exceptions=True
            )
            
            # Build alpha scans embed
            embed = discord.Embed(
                title="🔍 Alpha Opportunity Scans",
                color=0xffd700,
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="🎯 Scan Info",
                value=f"**Time**: {datetime.now().strftime('%I:%M %p CST')}\n**Next Scan**: 12 hours",
                inline=False
            )
            
            # Trading opportunities
            if isinstance(opportunities, list) and opportunities:
                opp_text = []
                for i, opp in enumerate(opportunities[:3], 1):
                    title = opp.get('title', 'Opportunity')[:50]
                    opp_text.append(f"{i}. **{title}**")
                    if opp.get('summary'):
                        opp_text.append(f"   {opp['summary'][:80]}...")
                
                embed.add_field(
                    name="📈 Trading Opportunities",
                    value="\n".join(opp_text),
                    inline=False
                )
            
            # Bullish signals
            if isinstance(bullish_signals, list) and bullish_signals:
                signals_text = []
                for signal in bullish_signals[:3]:
                    signals_text.append(f"📊 {signal.get('title', 'Bullish signal')[:60]}")
                
                embed.add_field(
                    name="🚀 Bullish Signals",
                    value="\n".join(signals_text),
                    inline=False
                )
            
            # Market intelligence
            if isinstance(market_intel, list) and market_intel:
                intel_text = []
                for intel in market_intel[:2]:
                    intel_text.append(f"💡 {intel.get('title', 'Market insight')[:60]}")
                
                embed.add_field(
                    name="🧠 Market Intelligence",
                    value="\n".join(intel_text),
                    inline=False
                )
            
            if len(embed.fields) <= 1:  # Only scan info
                embed.add_field(
                    name="📭 Status",
                    value="No alpha opportunities detected in current scan\n🔄 Next scan in 12 hours",
                    inline=False
                )
            else:
                embed.add_field(
                    name="⚡ Action Required",
                    value="Take action quickly - alpha opportunities don't last long!",
                    inline=False
                )
            
            await channel.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Alpha scans error: {e}")
    
    # Alerts Updates - Every 4 Hours
    @tasks.loop(hours=4)
    async def alerts_updates(self):
        """Send market alerts to #alerts"""
        try:
            channel = self.get_channel(CHANNELS['alerts'])
            if not channel:
                return
                
            print(f"🚨 Sending alerts update to #{channel.name}")
            
            # Fetch alert data
            breaking_news, risk_alerts, pump_dump = await asyncio.gather(
                self.fetch_breaking_news(),
                self.fetch_risk_alerts(),
                self.fetch_pump_dump_alerts(),
                return_exceptions=True
            )
            
            # Build alerts embed
            embed = discord.Embed(
                title="🚨 Market Alerts Update",
                color=0xff0000,
                timestamp=datetime.now()
            )
            
            # Breaking news
            if isinstance(breaking_news, list) and breaking_news:
                news_text = []
                for news in breaking_news[:3]:
                    sentiment_emoji = "📈" if news.get('sentiment') == 'Positive' else "📉" if news.get('sentiment') == 'Negative' else "📊"
                    title = news.get('title', 'News')[:60]
                    source = news.get('source_name', 'Unknown')
                    sentiment = news.get('sentiment', 'Neutral')
                    news_text.append(f"{sentiment_emoji} **{title}**")
                    news_text.append(f"   Source: {source} | Sentiment: {sentiment}")
                
                embed.add_field(
                    name="🚨 Breaking Crypto News",
                    value="\n".join(news_text),
                    inline=False
                )
            
            # Risk alerts
            if isinstance(risk_alerts, list) and risk_alerts:
                risk_text = []
                for alert in risk_alerts[:2]:
                    risk_text.append(f"🚨 {alert.get('title', 'Risk detected')[:80]}")
                
                embed.add_field(
                    name="⚠️ Risk Alerts",
                    value="\n".join(risk_text),
                    inline=False
                )
            
            # Pump/dump detection
            if isinstance(pump_dump, list) and pump_dump:
                signals_text = []
                for signal in pump_dump[:2]:
                    signals_text.append(f"📊 {signal.get('title', 'Signal detected')[:80]}")
                
                embed.add_field(
                    name="⚡ Pump/Dump Detection",
                    value="\n".join(signals_text),
                    inline=False
                )
            
            if len(embed.fields) == 0:
                embed.add_field(
                    name="✅ All Clear",
                    value="No urgent market alerts at this time",
                    inline=False
                )
            
            await channel.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Alerts update error: {e}")
    
    # Helper methods for API calls
    async def fetch_breaking_news(self):
        """Fetch breaking crypto news"""
        try:
            async with self.session.get(
                f"{RAILWAY_API_URL}/api/crypto-news/breaking-news",
                params={'items': 5, 'hours': 6}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])
        except Exception as e:
            print(f"❌ Breaking news error: {e}")
        return []
    
    async def fetch_risk_alerts(self):
        """Fetch risk alerts"""
        try:
            async with self.session.get(f"{RAILWAY_API_URL}/api/crypto-news/risk-alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('alerts', [])
        except Exception as e:
            print(f"❌ Risk alerts error: {e}")
        return []
    
    async def fetch_pump_dump_alerts(self):
        """Fetch pump/dump detection"""
        try:
            async with self.session.get(f"{RAILWAY_API_URL}/api/crypto-news/pump-dump-detector") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('signals', [])
        except Exception as e:
            print(f"❌ Pump/dump error: {e}")
        return []
    
    async def fetch_portfolio_news(self, symbols):
        """Fetch portfolio-specific news"""
        try:
            async with self.session.get(
                f"{RAILWAY_API_URL}/api/crypto-news/portfolio",
                params={'symbols': ','.join(symbols)}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])
        except Exception as e:
            print(f"❌ Portfolio news error: {e}")
        return []
    
    async def fetch_trading_opportunities(self):
        """Fetch trading opportunities"""
        try:
            async with self.session.get(f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('opportunities', [])
        except Exception as e:
            print(f"❌ Trading opportunities error: {e}")
        return []
    
    async def fetch_bullish_signals(self):
        """Fetch bullish signals"""
        try:
            async with self.session.get(f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('signals', [])
        except Exception as e:
            print(f"❌ Bullish signals error: {e}")
        return []
    
    async def fetch_market_intelligence(self):
        """Fetch market intelligence"""
        try:
            async with self.session.get(f"{RAILWAY_API_URL}/api/crypto-news/market-intelligence") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('intelligence', [])
        except Exception as e:
            print(f"❌ Market intelligence error: {e}")
        return []
    
    def get_portfolio_symbols(self, positions):
        """Extract symbols from positions data"""
        if not positions:
            return ['BTC', 'ETH', 'SOL', 'XRP', 'ADA']
        
        symbols = set()
        for pos in positions:
            symbol = pos.get('symbol', '')
            if symbol:
                clean_symbol = symbol.replace('-USDT', '').replace('/USD', '').replace('-USD', '')
                symbols.add(clean_symbol)
        
        return list(symbols)[:8]

    # Manual commands for testing
    @commands.command()
    async def portfolio(self, ctx):
        """Manual portfolio check"""
        if ctx.channel.id == CHANNELS['portfolio']:
            await self.portfolio_updates()
    
    @commands.command()  
    async def alpha(self, ctx):
        """Manual alpha scan"""
        if ctx.channel.id == CHANNELS['alpha_scans']:
            await self.alpha_scans()
    
    @commands.command()
    async def alerts(self, ctx):
        """Manual alerts check"""
        if ctx.channel.id == CHANNELS['alerts']:
            await self.alerts_updates()

async def main():
    """Main entry point"""
    if not DISCORD_TOKEN:
        print("❌ DISCORD_BOT_TOKEN environment variable not set!")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a new application and bot")
        print("3. Copy the bot token")
        print("4. Set environment variable: DISCORD_BOT_TOKEN=your_token_here")
        return
    
    bot = TradingBot()
    
    try:
        print("🚀 Starting Discord Trading Bot...")
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
    except Exception as e:
        print(f"❌ Bot error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())