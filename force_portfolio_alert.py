#!/usr/bin/env python3
"""Force send a portfolio alert to Discord now"""

import asyncio
import sys
sys.path.append('.')
from automated_trading_alerts import send_discord_alert
from datetime import datetime

async def force_portfolio_alert():
    """Send a test portfolio alert with the new formatting"""
    
    # Create a formatted portfolio message with the new exchange grouping
    message = f"🤖 **AI PORTFOLIO ANALYSIS** 🤖\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # BingX Section - Based on what we know from logs
    message += f"⚡ **BINGX - LEVERAGED TRADING** ⚡\n"
    message += f"📈 7 positions | Recent activity detected\n"
    message += f"🚀 $XRP: +46.1% | LONG 10x | Take profits!\n"
    message += f"📊 $ETH: +18.3% | LONG 10x | Move SL to breakeven\n"
    message += f"🔴 $SOL: -4.3% | LONG 10x | Set stop loss!\n"
    message += f"📊 $DOGE: -1.6% | LONG 10x | Monitor closely\n\n"
    
    # Blofin Section 
    message += f"🤖 **BLOFIN - COPY TRADING** 🤖\n"
    message += f"📈 5 positions | Copy trading active\n"
    message += f"🤖 $PENDLE: -4.8% | LONG 2x | Monitor trader\n\n"
    
    # Kraken Section
    message += f"💎 **KRAKEN - BIG BAGS** 💎\n"
    message += f"💰 9 bags | Total value: ~$60,000+\n"
    message += f"💎 $AVAX: $28,561 | HODL | Big bag\n"
    message += f"💎 $BERA: $14,687 | HODL | Good size\n\n"
    
    message += f"📊 **SUMMARY**: 21 total positions being monitored"
    
    print("🔥 Sending forced portfolio alert with new formatting...")
    result = await send_discord_alert(message, 'portfolio')
    if result:
        print("✅ Portfolio alert sent successfully!")
    else:
        print("❌ Failed to send portfolio alert")

if __name__ == "__main__":
    asyncio.run(force_portfolio_alert())