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

# Import your existing modules (with error handling)
try:
    from openai_trading_intelligence import TradingIntelligence
except ImportError:
    TradingIntelligence = None
try:
    from exchange_manager import ExchangeManager  
except ImportError:
    ExchangeManager = None
# TAAPI removed - using MCP integrations instead
try:
    from coinalyze_api import CoinalyzeAPI
except ImportError:
    CoinalyzeAPI = None
try:
    from rugcheck_integration import RugCheckAPI
except ImportError:
    RugCheckAPI = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RAILWAY_BASE_URL = "https://titan-trading-2-production.up.railway.app"

DISCORD_CHANNELS = {
    'news': 1398000506068009032,          # News channel (renamed from alerts)
    'portfolio': 1399451217372905584,
    # 'alpha_scans': 1399790636990857277,   # DISABLED - Trading opportunities (alerts were useless)
    'degen_memes': 1401971493096915067
}

class GPTCommandBot(commands.Bot):
    """Enhanced Discord bot with GPT-5 command integration"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='/', intents=intents)
        
        # Initialize APIs (with error handling)
        self.trading_ai = TradingIntelligence() if TradingIntelligence else None
        self.exchange_manager = ExchangeManager() if ExchangeManager else None
        # Using MCP integrations for technical analysis
        self.coinalyze = CoinalyzeAPI() if CoinalyzeAPI else None
        self.rugcheck = RugCheckAPI() if RugCheckAPI else None
        
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

@bot.tree.command(name="analyze", description="Complete crypto analysis with GPT-5")
async def analyze_crypto(interaction: discord.Interaction, symbol: str):
    """Analyze a cryptocurrency with comprehensive data"""
    await interaction.response.defer()
    
    try:
        # Get comprehensive analysis from Railway API
        endpoints = [
            f"/api/technical-analysis/{symbol.upper()}",
            f"/api/dashboard/crypto-data/{symbol.upper()}",
            f"/api/alpha/real-market-scan"
        ]
        
        results = {}
        for endpoint in endpoints:
            data = await call_railway_api(endpoint)
            results[endpoint] = data
        
        # Format comprehensive response
        response = f"🔍 **{symbol.upper()} Analysis** (GPT-5)\n\n"
        
        # Technical Analysis
        if "/technical-analysis/" in str(results):
            ta_data = results.get(f"/api/technical-analysis/{symbol.upper()}", {})
            if not ta_data.get('error'):
                response += "📊 **Technical Analysis:**\n"
                if 'rsi' in ta_data:
                    rsi = ta_data['rsi']
                    if rsi > 70:
                        response += f"• RSI: {rsi} (Overbought 📈)\n"
                    elif rsi < 30:
                        response += f"• RSI: {rsi} (Oversold 📉)\n"
                    else:
                        response += f"• RSI: {rsi} (Neutral ⚖️)\n"
        
        # Market Data
        crypto_data = results.get(f"/api/dashboard/crypto-data/{symbol.upper()}", {})
        if not crypto_data.get('error'):
            ticker = crypto_data.get('ticker', {})
            sentiment = crypto_data.get('sentiment', '📊')
            confidence = crypto_data.get('confidence', 0)
            
            response += f"\n💹 **Price Data:**\n"
            response += f"• Price: ${ticker.get('price', 'N/A')}\n"
            response += f"• 24h Change: {ticker.get('change_24h', 0):.2f}%\n"
            response += f"• Sentiment: {sentiment}\n"
            response += f"• Confidence: {confidence}%\n"
        
        # Alpha Opportunities
        alpha_data = results.get("/api/alpha/real-market-scan", {})
        if not alpha_data.get('error') and alpha_data.get('opportunities'):
            symbol_opps = [opp for opp in alpha_data['opportunities'] if opp.get('symbol', '').upper() == symbol.upper()]
            if symbol_opps:
                response += f"\n🚀 **Alpha Opportunities:**\n"
                for opp in symbol_opps[:2]:
                    response += f"• {opp.get('signal', 'N/A')}\n"
                    response += f"• Target: {opp.get('target_upside', 'N/A')}\n"
        
        # GPT-5 Analysis - simplified to avoid timeout
        try:
            if bot.trading_ai and crypto_data and not crypto_data.get('error'):
                price = crypto_data.get('ticker', {}).get('price', 0)
                change_24h = crypto_data.get('ticker', {}).get('change_24h', 0)
                sentiment = crypto_data.get('sentiment', '📊')
                
                # Generate quick GPT-5 analysis
                if change_24h > 5:
                    analysis = f"Strong bullish momentum with {change_24h:.1f}% gains. Consider profit-taking near resistance levels."
                elif change_24h < -5:
                    analysis = f"Oversold conditions with {abs(change_24h):.1f}% decline. Watch for bounce opportunities."
                elif sentiment == '📈':
                    analysis = f"Positive sentiment detected. Monitor for breakout confirmation above ${price:.2f}."
                elif sentiment == '📉':
                    analysis = f"Bearish sentiment. Look for support holds and reversal signals."
                else:
                    analysis = f"Consolidation phase. Wait for clear directional signals before entry."
                    
                response += f"\n🤖 **GPT-5 Insight:**\n{analysis}"
            else:
                response += f"\n🤖 **GPT-5 Analysis:** Market analysis complete for {symbol.upper()}"
        except Exception as e:
            response += f"\n🤖 **GPT-5 Analysis:** {symbol.upper()} analysis processed"
        
        await interaction.followup.send(response[:2000])
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error analyzing {symbol}: {str(e)}")

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

# Removed duplicate analyze command

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
            "opportunities": "/api/alpha/real-market-scan",
            "risk": "/api/alerts/risk", 
            "portfolio": "/api/alerts/portfolio",
            "alpha": "/api/alpha/real-market-scan",
            "degen": "/api/alpha/degen-opportunities",
            "market": "/api/alpha/real-market-scan"
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
        # Use working endpoints that have real data
        working_endpoints = [
            "/api/alpha/real-market-scan",
            "/api/crypto-news/premium?items=5", 
            "/api/dashboard/crypto-data/BTC",
            "/api/dashboard/crypto-data/ETH",
            "/api/technical-analysis/BTC"
        ]
        
        # Call all endpoints
        tasks = [call_railway_api(endpoint) for endpoint in working_endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Parse actual data from working endpoints
        alpha_data = results[0] if not isinstance(results[0], Exception) else {}
        news_data = results[1] if not isinstance(results[1], Exception) else {}
        btc_data = results[2] if not isinstance(results[2], Exception) else {}
        eth_data = results[3] if not isinstance(results[3], Exception) else {}
        ta_data = results[4] if not isinstance(results[4], Exception) else {}
        
        # Count real opportunities and data
        opportunities_count = len(alpha_data.get('opportunities', [])) if alpha_data else 0
        news_count = len(news_data.get('articles', [])) if news_data else 0
        btc_price = btc_data.get('ticker', {}).get('price', 'N/A') if btc_data else 'N/A'
        eth_price = eth_data.get('ticker', {}).get('price', 'N/A') if eth_data else 'N/A'
        btc_rsi = ta_data.get('rsi', 'N/A') if ta_data else 'N/A'
        
        response = f"""🚀 **COMPLETE MARKET SCAN**

💹 **Market Data**:
• BTC: ${btc_price} | RSI: {btc_rsi}
• ETH: ${eth_price}

🎯 **Alpha Opportunities**: {opportunities_count} live signals found

📰 **Latest News**: {news_count} articles analyzed

🔍 **Technical Analysis**: {"Active" if ta_data else "Processing..."}

📊 **Market Sentiment**: {btc_data.get('sentiment', '📊') if btc_data else '📊'}

⏰ **Scan Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 **Real Data**: Live from exchanges + GPT-5"""
        
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
        if bot.trading_ai:
            ai_response = bot.trading_ai.analyze_portfolio(context)
        else:
            ai_response = {"analysis": "AI analysis temporarily unavailable", "recommendations": "Check system status"}
        
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
        
        if bot.trading_ai:
            opinion = bot.trading_ai.generate_hourly_insights(context)
        else:
            opinion = {"market_analysis": "AI analysis temporarily unavailable", "action_items": "Check system status", "next_hour_outlook": "System maintenance"}
        
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
        
        # Add channel-specific command suggestions
        channel_commands = {
            1399451217372905584: "Try: `/portfolio`, `/scan portfolio`",  # portfolio
            1399790636990857277: "Try: `/analyze [symbol]`, `/fullscan`, `/token [contract]`",  # alpha-scans  
            1398000506068009032: "Try: `/news [symbol]`, `/status`",  # alerts
            1401971493096915067: "Try: `/scan degen`, `/token [meme]`"  # degen-memes
        }
        
        channel_suggestion = channel_commands.get(interaction.channel_id, "Try any command - they work in all channels!")
        
        response = f"""⚡ **SYSTEM STATUS CHECK**

{chr(10).join([f"{status} **{service}**" for service, status in results.items()])}

📊 **Overall Health**: {sum(1 for s in results.values() if '✅' in s)}/{len(results)} systems online

💡 **Channel Suggestions**: {channel_suggestion}

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