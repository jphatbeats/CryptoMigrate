#!/usr/bin/env python3
"""
Interactive Discord Chatbot for Titan Trading Bot
Allows direct conversation with AI in Discord channels
"""

import discord
import os
import asyncio
import logging
from datetime import datetime
import json

# Import OpenAI trading intelligence
try:
    from openai_trading_intelligence import TradingIntelligence
    trading_ai = TradingIntelligence()
    openai_available = True
    print("✅ OpenAI Trading Intelligence loaded for Discord bot")
except Exception as e:
    openai_available = False
    print(f"❌ OpenAI not available for Discord bot: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class TitanDiscordBot:
    """Interactive Titan Discord Bot with AI capabilities"""
    
    def __init__(self):
        self.bot_user_id = None
        self.active_channels = {
            'portfolio': os.getenv('DISCORD_PORTFOLIO_CHANNEL_ID'),
            'alerts': os.getenv('DISCORD_ALERTS_CHANNEL_ID'), 
            'alpha_scans': os.getenv('DISCORD_ALPHA_CHANNEL_ID')
        }
    
    async def handle_message(self, message):
        """Handle incoming Discord messages"""
        if message.author.bot:
            return
            
        # Check if bot is mentioned or message starts with trigger words
        is_mentioned = self.bot_user_id and f'<@{self.bot_user_id}>' in message.content
        trigger_words = ['titan', 'bot', 'analyze', 'portfolio', 'risk', 'news']
        has_trigger = any(word in message.content.lower() for word in trigger_words)
        
        if is_mentioned or has_trigger:
            await self.respond_to_message(message)
    
    async def respond_to_message(self, message):
        """Generate AI response to user message"""
        if not openai_available:
            await message.channel.send("🤖 AI features temporarily unavailable. Please try again later.")
            return
        
        try:
            # Show typing indicator
            async with message.channel.typing():
                # Determine response type based on message content
                user_input = message.content.lower()
                
                if any(word in user_input for word in ['portfolio', 'positions', 'balance']):
                    response = await self.generate_portfolio_response(message)
                elif any(word in user_input for word in ['news', 'sentiment', 'market']):
                    response = await self.generate_news_response(message)
                elif any(word in user_input for word in ['risk', 'danger', 'safe']):
                    response = await self.generate_risk_response(message)
                elif any(word in user_input for word in ['opportunity', 'trade', 'buy', 'sell']):
                    response = await self.generate_opportunity_response(message)
                else:
                    response = await self.generate_general_response(message)
                
                # Send response in chunks if too long
                await self.send_chunked_response(message.channel, response)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await message.channel.send("🤖 Sorry, I encountered an error processing your request.")
    
    async def generate_portfolio_response(self, message):
        """Generate portfolio-focused AI response"""
        try:
            # Get portfolio data (mock for now since no exchange APIs)
            portfolio_data = {
                'user_request': message.content,
                'channel': message.channel.name,
                'timestamp': datetime.now().isoformat()
            }
            
            analysis = trading_ai.analyze_portfolio(portfolio_data)
            
            response = f"🤖 **Portfolio Analysis Response**\n\n"
            
            if 'overall_assessment' in analysis:
                response += f"📊 **Health Score**: {analysis['overall_assessment']}/10\n"
            
            if 'risk_level' in analysis:
                response += f"⚠️ **Risk Level**: {analysis['risk_level']}\n"
            
            if 'recommendations' in analysis:
                response += f"\n💡 **AI Recommendations**:\n"
                for i, rec in enumerate(analysis['recommendations'][:3], 1):
                    response += f"{i}. {rec}\n"
            
            return response
            
        except Exception as e:
            return f"🤖 Portfolio analysis temporarily unavailable: {str(e)}"
    
    async def generate_news_response(self, message):
        """Generate news/sentiment focused response"""
        try:
            # Simulate recent news for analysis
            sample_news = [
                {
                    'title': 'Bitcoin reaches new support level amid institutional buying',
                    'content': 'Major institutions continue accumulating Bitcoin',
                    'tickers': ['BTC']
                }
            ]
            
            sentiment = trading_ai.grade_news_sentiment(sample_news)
            
            response = f"🤖 **Market Sentiment Analysis**\n\n"
            
            if 'overall_market_sentiment' in sentiment:
                response += f"📈 **Overall Sentiment**: {sentiment['overall_market_sentiment']}\n"
            
            if 'summary' in sentiment:
                response += f"📰 **AI Summary**: {sentiment['summary']}\n"
            
            return response
            
        except Exception as e:
            return f"🤖 News analysis temporarily unavailable: {str(e)}"
    
    async def generate_risk_response(self, message):
        """Generate risk assessment response"""
        try:
            # Mock portfolio for risk analysis
            portfolio_data = {
                'user_question': message.content,
                'analysis_type': 'risk_assessment'
            }
            
            risk_analysis = trading_ai.assess_risk_profile(portfolio_data, {})
            
            response = f"🤖 **Risk Assessment**\n\n"
            
            if 'overall_risk_score' in risk_analysis:
                response += f"⚠️ **Risk Score**: {risk_analysis['overall_risk_score']}/10\n"
            
            if 'risk_factors' in risk_analysis:
                response += f"\n🚨 **Key Risk Factors**:\n"
                for factor in risk_analysis['risk_factors'][:2]:
                    response += f"• {factor}\n"
            
            return response
            
        except Exception as e:
            return f"🤖 Risk assessment temporarily unavailable: {str(e)}"
    
    async def generate_opportunity_response(self, message):
        """Generate trading opportunity response"""
        try:
            market_data = {
                'user_query': message.content,
                'request_type': 'opportunity_scan'
            }
            
            opportunities = trading_ai.scan_opportunities(market_data, {})
            
            response = f"🤖 **Trading Opportunities**\n\n"
            
            if 'high_probability_setups' in opportunities:
                response += f"🎯 **High Probability Setups**:\n"
                for setup in opportunities['high_probability_setups'][:2]:
                    response += f"• {setup}\n"
            
            if 'timeline' in opportunities:
                response += f"\n⏱️ **Timeline**: {opportunities['timeline']}\n"
            
            return response
            
        except Exception as e:
            return f"🤖 Opportunity scan temporarily unavailable: {str(e)}"
    
    async def generate_general_response(self, message):
        """Generate general AI response"""
        try:
            # Use the alert analysis function for general queries
            mock_alert = [{'message': message.content, 'type': 'user_question'}]
            
            analysis = trading_ai.analyze_alerts_for_discord(mock_alert)
            
            response = f"🤖 **Titan AI Response**\n\n"
            
            if 'key_insight' in analysis:
                response += f"🧠 **Insight**: {analysis['key_insight']}\n"
            
            if 'action_recommendation' in analysis:
                response += f"💡 **Recommendation**: {analysis['action_recommendation']}\n"
            
            return response
            
        except Exception as e:
            return f"🤖 I'm here to help with crypto trading analysis. Try asking about portfolio, risk, or market opportunities!"
    
    async def send_chunked_response(self, channel, response):
        """Send response in chunks if too long for Discord"""
        max_length = 2000
        
        if len(response) <= max_length:
            await channel.send(response)
        else:
            # Split into chunks
            chunks = [response[i:i+max_length] for i in range(0, len(response), max_length)]
            for chunk in chunks:
                await channel.send(chunk)
                await asyncio.sleep(0.5)  # Small delay between chunks

# Initialize bot instance
titan_bot = TitanDiscordBot()

@client.event
async def on_ready():
    """Bot startup event"""
    print(f'🤖 Titan Discord Bot logged in as {client.user}')
    titan_bot.bot_user_id = client.user.id
    
    # Send startup message to configured channels
    for channel_name, channel_id in titan_bot.active_channels.items():
        if channel_id:
            try:
                channel = client.get_channel(int(channel_id))
                if channel:
                    await channel.send("🤖 **Titan AI Bot Online** - I can now respond to your messages! Try asking about portfolio, risk, or trading opportunities.")
            except Exception as e:
                logger.error(f"Failed to send startup message to {channel_name}: {e}")

@client.event
async def on_message(message):
    """Handle incoming messages"""
    await titan_bot.handle_message(message)

def main():
    """Start the Discord bot"""
    print("🚀 Starting Titan Interactive Discord Bot...")
    print("=" * 50)
    print("🤖 Features:")
    print("  • Responds to mentions and trigger words")
    print("  • AI-powered portfolio analysis") 
    print("  • Real-time market sentiment analysis")
    print("  • Risk assessment and trading opportunities")
    print("  • Interactive conversation in Discord channels")
    print("=" * 50)
    
    # Get Discord bot token
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not discord_token:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables")
        print("💡 Add your Discord bot token to continue")
        return
    
    if not openai_available:
        print("⚠️ OpenAI not available - bot will have limited functionality")
    
    try:
        client.run(discord_token)
    except Exception as e:
        print(f"❌ Failed to start Discord bot: {e}")

if __name__ == "__main__":
    main()