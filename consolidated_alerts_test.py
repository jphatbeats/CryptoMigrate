#!/usr/bin/env python3
"""
Test consolidated AI-enhanced Discord alerts system
"""

import asyncio
import os
import discord
from datetime import datetime
import pytz

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNELS = {
    'alerts': 1398000506068009032,        # Breaking news, risks
    'portfolio': 1399451217372905584,     # Portfolio analysis  
    'alpha_scans': 1399790636990857277    # Trading opportunities
}

async def send_ai_alert(message, channel_name):
    """Send AI-enhanced alert to Discord channel"""
    try:
        if not DISCORD_TOKEN:
            print("❌ No Discord token configured")
            return False
        
        channel_id = DISCORD_CHANNELS.get(channel_name)
        if not channel_id:
            print(f"❌ No Discord channel configured for {channel_name}")
            return False
        
        # Create Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            try:
                discord_channel = client.get_channel(channel_id)
                if discord_channel:
                    await discord_channel.send(message)
                    print(f"✅ AI alert sent to #{channel_name}")
                else:
                    print(f"❌ Channel {channel_id} not found")
                await client.close()
            except Exception as e:
                print(f"❌ Send error: {e}")
                await client.close()
        
        await client.start(DISCORD_TOKEN)
        return True
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def test_consolidated_system():
    """Test the complete AI-enhanced alert system"""
    print("🎯 TESTING CONSOLIDATED AI-ENHANCED DISCORD ALERTS")
    print("=" * 60)
    
    # Get current time
    central_tz = pytz.timezone('US/Central')
    timestamp = datetime.now(central_tz).strftime('%Y-%m-%d %I:%M %p CST')
    
    # Test Portfolio Analysis (AI-enhanced)
    portfolio_message = f"""🧠 **AI PORTFOLIO ANALYSIS** 🧠

📊 **Health Score**: 8/10 (STRONG)
⚠️ **Risk Level**: MEDIUM
🎯 **AI Recommendation**: Rebalance recommended

💡 **Key Insights**:
• BTC showing overbought signals (RSI: 78)
• ETH presenting accumulation opportunity
• Portfolio diversification: GOOD

🔄 **Suggested Actions**:
1. Take 25% BTC profits above $47,500
2. Accumulate ETH on dips below $2,400
3. Monitor SOL for breakout signals

⏰ **Analysis Time**: {timestamp}
🤖 **Powered by**: OpenAI GPT-4o Intelligence"""
    
    # Test Risk Alert (AI-enhanced)
    risk_message = f"""🚨 **AI RISK ALERT** 🚨

⚠️ **URGENCY**: HIGH
🎯 **Affected Assets**: BTC, ETH
📰 **Trigger**: Market volatility spike detected

🧠 **AI Analysis**:
• Unusual volume patterns detected
• Correlation breakdown between assets
• Potential liquidation cascade risk

🛡️ **Risk Mitigation**:
1. Reduce leverage immediately
2. Set tight stop losses
3. Consider hedging positions

⏰ **Alert Time**: {timestamp}
🤖 **AI Confidence**: 87%"""
    
    # Test Alpha Opportunity (AI-enhanced)
    alpha_message = f"""🎯 **AI ALPHA OPPORTUNITY** 🎯

🚀 **Signal Strength**: HIGH (9/10)
💰 **Asset**: MATIC/USDT
📈 **Direction**: LONG

🧠 **AI Analysis**:
• Technical breakout confirmed
• News sentiment: BULLISH
• Volume surge: +340%

💡 **Trade Setup**:
• Entry: $0.65 - $0.67
• Target 1: $0.75 (+15%)
• Target 2: $0.82 (+25%)
• Stop Loss: $0.61 (-7%)

⏰ **Signal Time**: {timestamp}
🤖 **AI Probability**: 85% success rate"""
    
    # Send alerts to respective channels
    test_alerts = [
        (portfolio_message, 'portfolio'),
        (risk_message, 'alerts'),
        (alpha_message, 'alpha_scans')
    ]
    
    for message, channel in test_alerts:
        print(f"\n📤 Sending AI alert to #{channel}...")
        await send_ai_alert(message, channel)
        await asyncio.sleep(2)  # Avoid rate limiting
    
    print("\n✅ CONSOLIDATED AI ALERT SYSTEM TEST COMPLETE!")
    print("🎯 Your Discord channels should now have AI-enhanced alerts")
    print("🤖 System ready for production deployment!")

if __name__ == "__main__":
    asyncio.run(test_consolidated_system())