"""
Smart Trading Bot - Discord/Telegram Integration
Automated alerts for crypto trading opportunities, portfolio insights, and market intelligence
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartTradingBot:
    def __init__(self, railway_api_url: str):
        self.api_url = railway_api_url.rstrip('/')
        self.session = None
        
        # Alert configuration
        self.alert_intervals = {
            'breaking_news': 300,  # 5 minutes
            'portfolio_check': 3600,  # 1 hour  
            'opportunities': 1800,  # 30 minutes
            'market_intelligence': 7200,  # 2 hours
            'risk_alerts': 600  # 10 minutes
        }
        
        self.portfolio_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']  # User configurable
        
    async def start_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            
    async def api_call(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API call to Railway endpoint"""
        url = f"{self.api_url}{endpoint}"
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"API call failed: {response.status} - {endpoint}")
                    return {}
        except Exception as e:
            logger.error(f"API call error: {e}")
            return {}
    
    async def get_breaking_news_alerts(self) -> Dict:
        """Get breaking crypto news for alerts"""
        return await self.api_call('/api/crypto-news/breaking-news', {'items': 10, 'hours': 6})
    
    async def get_portfolio_insights(self) -> Dict:
        """Get portfolio-specific news and insights"""
        symbols = ','.join(self.portfolio_symbols)
        portfolio_news = await self.api_call('/api/crypto-news/portfolio', {'symbols': symbols})
        
        # Get portfolio performance from exchanges
        portfolio_data = {}
        for exchange in ['bingx', 'kraken', 'blofin']:
            positions = await self.api_call(f'/api/{exchange}/positions')
            if positions.get('success'):
                portfolio_data[exchange] = positions.get('data', {})
        
        return {
            'news': portfolio_news,
            'positions': portfolio_data,
            'symbols': self.portfolio_symbols
        }
    
    async def scan_trading_opportunities(self) -> Dict:
        """Scan for trading opportunities across exchanges"""
        opportunities = await self.api_call('/api/crypto-news/opportunity-scanner')
        bullish_signals = await self.api_call('/api/crypto-news/bullish-signals')
        
        # Get market analysis for key symbols
        market_analysis = {}
        for symbol in ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']:
            bingx_analysis = await self.api_call(f'/api/bingx/market-analysis/{symbol}')
            if bingx_analysis.get('success'):
                market_analysis[symbol] = bingx_analysis.get('data', {})
        
        return {
            'opportunities': opportunities,
            'bullish_signals': bullish_signals,
            'market_analysis': market_analysis
        }
    
    async def get_risk_alerts(self) -> Dict:
        """Get risk alerts and warnings"""
        risk_alerts = await self.api_call('/api/crypto-news/risk-alerts')
        pump_dump = await self.api_call('/api/crypto-news/pump-dump-detector')
        
        return {
            'risk_alerts': risk_alerts,
            'pump_dump_signals': pump_dump
        }
    
    async def get_market_intelligence(self) -> Dict:
        """Get comprehensive market intelligence"""
        intelligence = await self.api_call('/api/crypto-news/market-intelligence')
        ai_summary = await self.api_call('/api/chatgpt/account-summary')
        
        return {
            'market_overview': intelligence,
            'ai_insights': ai_summary
        }
    
    def format_breaking_news_alert(self, news_data: Dict) -> str:
        """Format breaking news for Discord/Telegram"""
        if not news_data.get('success'):
            return "❌ Unable to fetch breaking news"
            
        articles = news_data.get('data', {}).get('articles', [])[:5]  # Top 5
        if not articles:
            return "📰 No breaking crypto news in the last 6 hours"
            
        alert = "🚨 **BREAKING CRYPTO NEWS** 🚨\n\n"
        
        for i, article in enumerate(articles, 1):
            sentiment_emoji = "📈" if article.get('sentiment') == 'Positive' else "📉" if article.get('sentiment') == 'Negative' else "📊"
            alert += f"{sentiment_emoji} **{article.get('title', 'No title')}**\n"
            alert += f"   Source: {article.get('source_name', 'Unknown')}\n"
            alert += f"   Sentiment: {article.get('sentiment', 'Neutral')}\n\n"
            
        return alert[:2000]  # Discord/Telegram message limit
    
    def format_portfolio_alert(self, portfolio_data: Dict) -> str:
        """Format portfolio insights for alerts"""
        news = portfolio_data.get('news', {})
        positions = portfolio_data.get('positions', {})
        
        alert = "💼 **PORTFOLIO CHECK** 💼\n\n"
        
        # Portfolio news
        if news.get('success') and news.get('data', {}).get('articles'):
            articles = news['data']['articles'][:3]
            alert += f"📰 **News affecting your portfolio** ({len(articles)} articles):\n"
            for article in articles:
                alert += f"• {article.get('title', 'No title')[:80]}...\n"
            alert += "\n"
        
        # Position summary
        alert += "📊 **Position Summary**:\n"
        active_exchanges = 0
        for exchange, data in positions.items():
            if data:
                active_exchanges += 1
                alert += f"• {exchange.upper()}: Active positions detected\n"
        
        if active_exchanges == 0:
            alert += "• No active positions detected\n"
            
        alert += f"\n🎯 **Tracking**: {', '.join(self.portfolio_symbols)}"
        
        return alert[:2000]
    
    def format_opportunity_alert(self, opp_data: Dict) -> str:
        """Format trading opportunities for alerts"""
        opportunities = opp_data.get('opportunities', {})
        bullish = opp_data.get('bullish_signals', {})
        analysis = opp_data.get('market_analysis', {})
        
        alert = "🔍 **TRADING OPPORTUNITIES** 🔍\n\n"
        
        # Opportunities from news
        if opportunities.get('success'):
            opps = opportunities.get('data', {}).get('opportunities', [])[:3]
            if opps:
                alert += "📈 **News-Based Opportunities**:\n"
                for opp in opps:
                    alert += f"• {opp.get('title', 'Opportunity detected')[:60]}...\n"
                alert += "\n"
        
        # Bullish signals
        if bullish.get('success'):
            signals = bullish.get('data', {}).get('signals', [])[:2]
            if signals:
                alert += "🚀 **Bullish Signals**:\n"
                for signal in signals:
                    alert += f"• {signal.get('title', 'Bullish signal')[:60]}...\n"
                alert += "\n"
        
        # Technical analysis summary
        if analysis:
            alert += "📊 **Market Analysis**:\n"
            for symbol, data in list(analysis.items())[:3]:
                price = data.get('price_analysis', {}).get('current_price')
                if price:
                    alert += f"• {symbol}: ${price}\n"
        
        return alert[:2000]
    
    def format_risk_alert(self, risk_data: Dict) -> str:
        """Format risk alerts"""
        risk_alerts = risk_data.get('risk_alerts', {})
        pump_dump = risk_data.get('pump_dump_signals', {})
        
        alert = "⚠️ **RISK ALERTS** ⚠️\n\n"
        
        # Risk warnings
        if risk_alerts.get('success'):
            alerts = risk_alerts.get('data', {}).get('alerts', [])[:3]
            if alerts:
                alert += "🚨 **Risk Warnings**:\n"
                for risk in alerts:
                    alert += f"• {risk.get('title', 'Risk detected')[:70]}...\n"
                alert += "\n"
        
        # Pump/dump detection
        if pump_dump.get('success'):
            signals = pump_dump.get('data', {}).get('signals', [])[:2]
            if signals:
                alert += "⚡ **Pump/Dump Signals**:\n"
                for signal in signals:
                    alert += f"• {signal.get('title', 'Signal detected')[:70]}...\n"
        
        if not risk_alerts.get('success') and not pump_dump.get('success'):
            alert += "✅ No immediate risk alerts detected"
        
        return alert[:2000]

class DiscordBot:
    """Discord bot integration"""
    
    def __init__(self, webhook_url: str, trading_bot: SmartTradingBot):
        self.webhook_url = webhook_url
        self.trading_bot = trading_bot
        
    async def send_alert(self, message: str):
        """Send alert to Discord via webhook"""
        if not self.trading_bot.session:
            await self.trading_bot.start_session()
            
        payload = {
            "content": message,
            "username": "Smart Trading Bot"
        }
        
        try:
            async with self.trading_bot.session.post(self.webhook_url, json=payload) as response:
                if response.status == 204:
                    logger.info("Discord alert sent successfully")
                else:
                    logger.error(f"Discord alert failed: {response.status}")
        except Exception as e:
            logger.error(f"Discord send error: {e}")

class TelegramBot:
    """Telegram bot integration"""
    
    def __init__(self, bot_token: str, chat_id: str, trading_bot: SmartTradingBot):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.trading_bot = trading_bot
        
    async def send_alert(self, message: str):
        """Send alert to Telegram"""
        if not self.trading_bot.session:
            await self.trading_bot.start_session()
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            async with self.trading_bot.session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("Telegram alert sent successfully")
                else:
                    logger.error(f"Telegram alert failed: {response.status}")
        except Exception as e:
            logger.error(f"Telegram send error: {e}")

class AlertScheduler:
    """Schedule and manage automated alerts"""
    
    def __init__(self, trading_bot: SmartTradingBot, discord_bot: DiscordBot = None, telegram_bot: TelegramBot = None):
        self.trading_bot = trading_bot
        self.discord_bot = discord_bot
        self.telegram_bot = telegram_bot
        self.running = False
        
    async def send_to_platforms(self, message: str):
        """Send message to all configured platforms"""
        tasks = []
        if self.discord_bot:
            tasks.append(self.discord_bot.send_alert(message))
        if self.telegram_bot:
            tasks.append(self.telegram_bot.send_alert(message))
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def breaking_news_loop(self):
        """Breaking news alert loop"""
        while self.running:
            try:
                news_data = await self.trading_bot.get_breaking_news_alerts()
                alert = self.trading_bot.format_breaking_news_alert(news_data)
                await self.send_to_platforms(alert)
                
                await asyncio.sleep(self.trading_bot.alert_intervals['breaking_news'])
            except Exception as e:
                logger.error(f"Breaking news loop error: {e}")
                await asyncio.sleep(60)
    
    async def portfolio_check_loop(self):
        """Portfolio check alert loop"""
        while self.running:
            try:
                portfolio_data = await self.trading_bot.get_portfolio_insights()
                alert = self.trading_bot.format_portfolio_alert(portfolio_data)
                await self.send_to_platforms(alert)
                
                await asyncio.sleep(self.trading_bot.alert_intervals['portfolio_check'])
            except Exception as e:
                logger.error(f"Portfolio check loop error: {e}")
                await asyncio.sleep(60)
    
    async def opportunity_scan_loop(self):
        """Opportunity scanning alert loop"""
        while self.running:
            try:
                opp_data = await self.trading_bot.scan_trading_opportunities()
                alert = self.trading_bot.format_opportunity_alert(opp_data)
                await self.send_to_platforms(alert)
                
                await asyncio.sleep(self.trading_bot.alert_intervals['opportunities'])
            except Exception as e:
                logger.error(f"Opportunity scan loop error: {e}")
                await asyncio.sleep(60)
    
    async def risk_alert_loop(self):
        """Risk alert loop"""
        while self.running:
            try:
                risk_data = await self.trading_bot.get_risk_alerts()
                alert = self.trading_bot.format_risk_alert(risk_data)
                
                # Only send if there are actual risks
                if "No immediate risk alerts" not in alert:
                    await self.send_to_platforms(alert)
                
                await asyncio.sleep(self.trading_bot.alert_intervals['risk_alerts'])
            except Exception as e:
                logger.error(f"Risk alert loop error: {e}")
                await asyncio.sleep(60)
    
    async def start_all_alerts(self):
        """Start all alert loops"""
        self.running = True
        await self.trading_bot.start_session()
        
        logger.info("Starting smart trading bot alert system...")
        
        # Start all alert loops concurrently
        tasks = [
            self.breaking_news_loop(),
            self.portfolio_check_loop(),
            self.opportunity_scan_loop(),
            self.risk_alert_loop()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("Shutting down alert system...")
        finally:
            self.running = False
            await self.trading_bot.close_session()

# Configuration and startup
async def main():
    """Main entry point"""
    # Configuration - Set these environment variables
    RAILWAY_API_URL = os.getenv('RAILWAY_API_URL', 'https://titan-trading-2-production.up.railway.app')
    DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK_URL')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Initialize trading bot
    trading_bot = SmartTradingBot(RAILWAY_API_URL)
    
    # Initialize platform bots
    discord_bot = DiscordBot(DISCORD_WEBHOOK, trading_bot) if DISCORD_WEBHOOK else None
    telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, trading_bot) if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID else None
    
    if not discord_bot and not telegram_bot:
        logger.error("No Discord or Telegram configuration found. Please set environment variables.")
        return
    
    # Start alert scheduler
    scheduler = AlertScheduler(trading_bot, discord_bot, telegram_bot)
    await scheduler.start_all_alerts()

if __name__ == "__main__":
    asyncio.run(main())