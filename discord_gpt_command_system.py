#!/usr/bin/env python3
"""
DISCORD GPT-5 COMMAND SYSTEM
============================
Complete Discord slash command integration with GPT-5 and Railway API access.
Full system control through Discord commands.
"""

import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import os
import logging
from datetime import datetime
import traceback
from typing import Dict, List, Optional

# Import your existing modules
from openai_trading_intelligence import TradingIntelligence
from exchange_manager import ExchangeManager
from taapi_indicators import TaapiIndicators
from coinalyze_api import CoinalyzeAPI
from rugcheck_integration import RugCheckAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RAILWAY_BASE_URL = "https://titan-trading-2-production.up.railway.app"

DISCORD_CHANNELS = {
    'alerts': 1398000506068009032,
    'portfolio': 1399451217372905584,
    'alpha_scans': 1399790636990857277,
    'degen_memes': 1401971493096915067
}

class GPTCommandBot(commands.Bot):
    """Enhanced Discord bot with GPT-5 command integration"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='/', intents=intents)
        
        # Initialize APIs
        self.trading_ai = TradingIntelligence()
        self.exchange_manager = ExchangeManager()
        self.taapi = TaapiIndicators()
        self.coinalyze = CoinalyzeAPI()
        self.rugcheck = RugCheckAPI()
        
    async def setup_hook(self):
        """Setup slash commands"""
        await self.tree.sync()
        logger.info("🚀 GPT Command Bot ready with slash commands")
    
    async def on_ready(self):
        """Bot ready event"""
        logger.info(f'🤖 {self.user.name} GPT Command System Online!')
        logger.info(f"📊 Connected to {len(self.guilds)} servers")

# Initialize bot
bot = GPTCommandBot()

# Helper Functions
async def call_railway_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Call Railway API endpoints"""
    try:
        url = f"{RAILWAY_BASE_URL}{endpoint}"
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
            elif method == "POST":
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
        return {"error": f"API call failed: {response.status}"}
    except Exception as e:
        return {"error": str(e)}

async def format_response(data: Dict, title: str) -> str:
    """Format API response for Discord"""
    if "error" in data:
        return f"❌ **{title}**\nError: {data['error']}"
    
    # Format based on data type
    if isinstance(data, dict):
        formatted = f"🤖 **{title}**\n"
        for key, value in list(data.items())[:10]:  # Limit to 10 items
            if isinstance(value, (int, float)):
                formatted += f"• **{key}**: {value}\n"
            elif isinstance(value, str):
                formatted += f"• **{key}**: {value[:100]}\n"
        return formatted[:1900] + "..." if len(formatted) > 1900 else formatted
    
    return f"🤖 **{title}**\n{str(data)[:1900]}"

# =============================================================================
# PORTFOLIO & TRADING COMMANDS
# =============================================================================

@bot.tree.command(name="portfolio", description="Get GPT-5 portfolio analysis")
async def portfolio_analysis(interaction: discord.Interaction):
    """Get comprehensive portfolio analysis"""
    await interaction.response.defer()
    
    try:
        # Get portfolio data from Railway API
        portfolio_data = await call_railway_api("/api/chatgpt/portfolio-analysis")
        
        if "error" not in portfolio_data:
            # Format for Discord
            response = f"""🧠 **GPT-5 PORTFOLIO ANALYSIS**

📊 **Health Score**: {portfolio_data.get('overall_assessment', 'N/A')}/10
⚠️ **Risk Level**: {portfolio_data.get('risk_level', 'Unknown')}
🎯 **Diversification**: {portfolio_data.get('diversification_score', 'N/A')}/10

💡 **AI Recommendations**:
{portfolio_data.get('recommendations', 'No recommendations available')[:500]}

🔄 **Next Actions**:
{portfolio_data.get('next_actions', 'No actions suggested')[:300]}

⏰ **Analysis Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 **Powered by**: GPT-5"""
        else:
            response = f"❌ Portfolio analysis failed: {portfolio_data['error']}"
            
        await interaction.followup.send(response)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Command failed: {str(e)}")

@bot.tree.command(name="analyze", description="Analyze a specific cryptocurrency")
async def analyze_crypto(interaction: discord.Interaction, symbol: str):
    """Analyze specific cryptocurrency with full technical analysis"""
    await interaction.response.defer()
    
    try:
        # Get technical analysis
        ta_data = await call_railway_api(f"/api/technical-analysis/{symbol.upper()}")
        
        # Get news for the symbol
        news_data = await call_railway_api(f"/api/crypto-news/premium?tickers={symbol.upper()}&items=3")
        
        # Get futures data if available
        futures_data = await call_railway_api(f"/api/futures/funding-rates/{symbol.upper()}")
        
        response = f"""🔍 **COMPLETE {symbol.upper()} ANALYSIS**

📈 **Technical Analysis**:
{await format_response(ta_data, 'Technical Indicators')[:400]}

📰 **Recent News**:
{await format_response(news_data, 'News Analysis')[:400]}

📊 **Futures Data**:
{await format_response(futures_data, 'Funding Rates')[:300]}

⏰ **Analysis Time**: {datetime.now().strftime('%H:%M:%S')}
🤖 **Powered by**: GPT-5 Intelligence"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Analysis failed: {str(e)}")

# =============================================================================
# SCANNING & DISCOVERY COMMANDS  
# =============================================================================

@bot.tree.command(name="scan", description="Run specific trading scans")
async def trading_scan(interaction: discord.Interaction, 
                      scan_type: str = "opportunities"):
    """Run comprehensive trading scans"""
    await interaction.response.defer()
    
    try:
        scan_endpoints = {
            "opportunities": "/api/alerts/trading",
            "risk": "/api/alerts/risk", 
            "portfolio": "/api/alerts/portfolio",
            "alpha": "/api/alpha/scan-opportunities",
            "degen": "/api/alpha/degen-opportunities"
        }
        
        endpoint = scan_endpoints.get(scan_type, "/api/alerts/trading")
        scan_data = await call_railway_api(endpoint)
        
        response = f"""🔍 **{scan_type.upper()} SCAN RESULTS**

{await format_response(scan_data, f'{scan_type} Analysis')[:1500]}

⏰ **Scan Time**: {datetime.now().strftime('%H:%M:%S')}
🎯 **Scan Type**: {scan_type}
🤖 **AI Powered**: GPT-5"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Scan failed: {str(e)}")

@bot.tree.command(name="fullscan", description="Complete market scan with all data sources")
async def full_market_scan(interaction: discord.Interaction):
    """Comprehensive scan using all available APIs"""
    await interaction.response.defer()
    
    try:
        # Trigger multiple scans simultaneously
        endpoints = [
            "/api/chatgpt/hourly-insights",
            "/api/alerts/trading", 
            "/api/crypto-news/premium?items=5",
            "/api/live/all-exchanges",
            "/api/alpha/scan-opportunities"
        ]
        
        # Call all endpoints
        tasks = [call_railway_api(endpoint) for endpoint in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        response = f"""🚀 **COMPLETE MARKET SCAN**

🎯 **Market Pulse**: {results[0].get('market_pulse', 'N/A')[:200] if len(results) > 0 else 'N/A'}

📊 **Trading Alerts**: {len(results[1].get('alerts', [])) if len(results) > 1 else 0} found

📰 **Latest News**: {len(results[2].get('articles', [])) if len(results) > 2 else 0} articles

💼 **Live Positions**: {len(results[3].get('positions', [])) if len(results) > 3 else 0} active

🎯 **Alpha Opportunities**: {len(results[4].get('opportunities', [])) if len(results) > 4 else 0} found

⏰ **Scan Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 **Full System**: Railway + GPT-5"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Full scan failed: {str(e)}")

# =============================================================================
# NEWS & RESEARCH COMMANDS
# =============================================================================

@bot.tree.command(name="news", description="Get AI-filtered crypto news")
async def crypto_news(interaction: discord.Interaction, 
                     symbol: str = None, 
                     sentiment: str = None):
    """Get crypto news with AI analysis"""
    await interaction.response.defer()
    
    try:
        # Build query parameters
        params = "?items=10"
        if symbol:
            params += f"&tickers={symbol.upper()}"
        if sentiment:
            params += f"&sentiment={sentiment}"
            
        news_data = await call_railway_api(f"/api/crypto-news/premium{params}")
        
        # Get AI sentiment analysis
        if "articles" in news_data:
            sentiment_data = await call_railway_api("/api/chatgpt/news-sentiment", 
                                                  "POST", {"articles": news_data["articles"][:3]})
        
        response = f"""📰 **CRYPTO NEWS ANALYSIS**

🎯 **Filter**: {symbol.upper() if symbol else 'All'} | {sentiment or 'All sentiment'}

📋 **Articles Found**: {len(news_data.get('articles', []))}

🧠 **AI Sentiment**: {sentiment_data.get('overall_market_sentiment', 'N/A') if 'sentiment_data' in locals() else 'Processing...'}

📊 **Market Impact**: {sentiment_data.get('impact_score', 'N/A') if 'sentiment_data' in locals() else 'Calculating...'}/10

⏰ **News Time**: {datetime.now().strftime('%H:%M:%S')}
🤖 **AI Analysis**: GPT-5"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ News analysis failed: {str(e)}")

@bot.tree.command(name="token", description="Research token by contract or symbol")
async def token_research(interaction: discord.Interaction, 
                        token_id: str):
    """Complete token research using all APIs"""
    await interaction.response.defer()
    
    try:
        # Multi-source token analysis
        tasks = [
            call_railway_api(f"/api/security/rugcheck/{token_id}"),
            call_railway_api(f"/api/crypto-news/premium?search={token_id}&items=5"),
            call_railway_api(f"/api/technical-analysis/{token_id}")
        ]
        
        security, news, technical = await asyncio.gather(*tasks, return_exceptions=True)
        
        response = f"""🔍 **TOKEN RESEARCH: {token_id.upper()}**

🛡️ **Security Analysis**:
{await format_response(security, 'Security Check')[:400] if not isinstance(security, Exception) else 'Security check failed'}

📰 **News & Mentions**:
{await format_response(news, 'News Analysis')[:400] if not isinstance(news, Exception) else 'No recent news'}

📈 **Technical Analysis**:
{await format_response(technical, 'Technical Data')[:400] if not isinstance(technical, Exception) else 'Technical analysis unavailable'}

⏰ **Research Time**: {datetime.now().strftime('%H:%M:%S')}
🤖 **Multi-Source**: All APIs + GPT-5"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Token research failed: {str(e)}")

# =============================================================================
# AI CONVERSATION COMMANDS
# =============================================================================

@bot.tree.command(name="ask", description="Ask GPT-5 any trading question")
async def ask_gpt(interaction: discord.Interaction, question: str):
    """Direct conversation with GPT-5 about trading"""
    await interaction.response.defer()
    
    try:
        # Get current portfolio context
        portfolio_data = await call_railway_api("/api/live/all-exchanges")
        
        # Prepare context for GPT-5
        context = {
            "question": question,
            "portfolio": portfolio_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Get GPT-5 response
        ai_response = bot.trading_ai.analyze_portfolio(context)
        
        response = f"""🤖 **GPT-5 TRADING ASSISTANT**

❓ **Your Question**: {question[:200]}

🧠 **GPT-5 Answer**:
{ai_response.get('analysis', 'Processing your question...')[:1200]}

💡 **Recommendations**:
{ai_response.get('recommendations', 'No specific recommendations')[:300]}

⏰ **Response Time**: {datetime.now().strftime('%H:%M:%S')}
🎯 **Context**: Live portfolio data included"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ GPT-5 query failed: {str(e)}")

@bot.tree.command(name="opinion", description="Get GPT-5 opinion on market/trade")
async def get_opinion(interaction: discord.Interaction, topic: str):
    """Get GPT-5 opinion with full market context"""
    await interaction.response.defer()
    
    try:
        # Gather comprehensive market data
        market_data = await asyncio.gather(
            call_railway_api("/api/chatgpt/hourly-insights"),
            call_railway_api("/api/crypto-news/premium?items=5"),
            call_railway_api("/api/live/all-exchanges"),
            return_exceptions=True
        )
        
        # Format for GPT-5 analysis
        context = {
            "topic": topic,
            "market_insights": market_data[0] if len(market_data) > 0 else {},
            "recent_news": market_data[1] if len(market_data) > 1 else {},
            "portfolio": market_data[2] if len(market_data) > 2 else {}
        }
        
        opinion = bot.trading_ai.generate_hourly_insights(context)
        
        response = f"""🎯 **GPT-5 MARKET OPINION**

📋 **Topic**: {topic[:200]}

🧠 **AI Opinion**:
{opinion.get('market_analysis', 'Analyzing market conditions...')[:1000]}

⚡ **Immediate Actions**:
{opinion.get('action_items', 'No immediate actions required')[:400]}

🔮 **Outlook**:
{opinion.get('next_hour_outlook', 'Monitoring market developments')[:300]}

⏰ **Opinion Time**: {datetime.now().strftime('%H:%M:%S')}
🎯 **Full Context**: Live data + News + Portfolio"""
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Opinion generation failed: {str(e)}")

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

@bot.tree.command(name="status", description="Check all systems status")
async def system_status(interaction: discord.Interaction):
    """Check status of all APIs and systems"""
    await interaction.response.defer()
    
    try:
        # Test all endpoints
        status_checks = {
            "Railway Server": call_railway_api("/api/health"),
            "Portfolio Data": call_railway_api("/api/live/all-exchanges"),
            "News API": call_railway_api("/api/crypto-news/premium?items=1"),
            "Technical Analysis": call_railway_api("/api/technical-analysis/BTC"),
            "GPT-5 AI": call_railway_api("/api/chatgpt/portfolio-analysis")
        }
        
        results = {}
        for service, task in status_checks.items():
            try:
                result = await task
                results[service] = "✅ Online" if "error" not in result else "❌ Error"
            except:
                results[service] = "❌ Offline"
        
        response = f"""⚡ **SYSTEM STATUS CHECK**

{chr(10).join([f"{status} **{service}**" for service, status in results.items()])}

📊 **Overall Health**: {sum(1 for s in results.values() if '✅' in s)}/{len(results)} systems online

⏰ **Check Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔧 **All Systems**: Railway + APIs + GPT-5"""
        
        await interaction.followup.send(response)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Status check failed: {str(e)}")

async def main():
    """Run the Discord GPT Command Bot"""
    try:
        if not DISCORD_TOKEN:
            logger.error("❌ DISCORD_TOKEN not found in environment variables")
            return
            
        logger.info("🚀 Starting Discord GPT-5 Command System...")
        await bot.start(DISCORD_TOKEN)
        
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())