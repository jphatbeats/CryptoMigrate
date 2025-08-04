#!/usr/bin/env python3
"""
Test Discord bot functionality
"""

import asyncio
import os
from automated_trading_alerts import send_discord_alert

async def test_discord_alerts():
    """Test Discord bot sending alerts to all channels"""
    print("🤖 Testing Discord Bot Alerts...")
    
    # Test messages for each channel
    test_messages = {
        'portfolio': "🧠 **AI PORTFOLIO TEST** 🧠\n✅ Discord bot is working!\n📊 Health Score: 8/10\n💡 Recommendation: Testing successful",
        'alerts': "🚨 **AI ALERT TEST** 🚨\n✅ Discord bot is working!\n⚠️ Risk Level: LOW\n🎯 This is a test message",
        'alpha_scans': "🎯 **AI ALPHA TEST** 🎯\n✅ Discord bot is working!\n🚀 Opportunity: Test signal detected\n💰 Confidence: HIGH"
    }
    
    # Send test messages to each channel
    for channel, message in test_messages.items():
        print(f"\n📤 Testing {channel} channel...")
        try:
            success = await send_discord_alert(message, channel)
            if success:
                print(f"✅ {channel} channel test successful")
            else:
                print(f"❌ {channel} channel test failed")
        except Exception as e:
            print(f"❌ {channel} channel error: {e}")
    
    print("\n🎯 Discord bot testing completed!")

if __name__ == "__main__":
    asyncio.run(test_discord_alerts())