#!/usr/bin/env python3
"""Send immediate portfolio alert with current data"""

import asyncio
import sys
sys.path.append('.')
from datetime import datetime

async def send_immediate_alert():
    """Send formatted portfolio alert immediately"""
    from automated_trading_alerts import send_discord_alert
    
    # Current data from logs
    message = f"🤖 **AI PORTFOLIO ANALYSIS** 🤖\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # BingX - Leveraged Trading (from logs)
    message += f"⚡ **BINGX - LEVERAGED TRADING** ⚡\n"
    message += f"📈 7 positions | Processing live analysis...\n"
    message += f"🚀 $XRP: +46.0% | LONG 10x | Take profits now!\n"
    message += f"📊 $ETH: +18.2% | LONG 10x | Move stop to breakeven\n"
    message += f"🔴 $SOL: -4.7% | LONG 10x | Set stop loss!\n"
    message += f"📊 $DOGE: Active position | Monitor\n\n"
    
    # Blofin - Copy Trading
    message += f"🤖 **BLOFIN - COPY TRADING** 🤖\n"
    message += f"📈 5 positions | Copy trading active\n"
    message += f"📊 Multiple positions being tracked\n\n"
    
    # Kraken - Big Bags  
    message += f"💎 **KRAKEN - BIG BAGS** 💎\n"
    message += f"💰 9 bags | Total value: ~$60,000+\n"
    message += f"💎 $AVAX: +3.7% | $28,561 | Big bag\n"
    message += f"📊 $BERA: +0.7% | $14,687 | Good size\n"
    message += f"📊 7 more bags tracked\n\n"
    
    message += f"📊 **SUMMARY**: 21 total positions across 3 exchanges\n"
    message += f"🎯 **ALERT**: XRP at +46% - consider taking profits!"
    
    print("🚀 Sending immediate portfolio alert...")
    result = await send_discord_alert(message, 'portfolio')
    if result:
        print("✅ Portfolio alert sent!")
    else:
        print("❌ Failed to send alert")

if __name__ == "__main__":
    asyncio.run(send_immediate_alert())