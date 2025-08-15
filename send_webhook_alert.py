#!/usr/bin/env python3
"""Send portfolio alert via Discord webhook immediately"""

import requests
import json
from datetime import datetime

def send_webhook_alert():
    """Send formatted portfolio alert via Discord webhook"""
    
    webhook_url = "https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8"
    
    # Current data from logs
    message = f"🤖 **AI PORTFOLIO ANALYSIS** 🤖\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # BingX - Leveraged Trading (from logs)
    message += f"⚡ **BINGX - LEVERAGED TRADING** ⚡\n"
    message += f"📈 7 positions | Live analysis complete\n"
    message += f"🚀 $XRP: +46.0% | LONG 10x | **TAKE PROFITS NOW!**\n"
    message += f"📊 $ETH: +18.2% | LONG 10x | Move stop to breakeven\n"
    message += f"🔴 $SOL: -4.7% | LONG 10x | **Set stop loss!**\n\n"
    
    # Blofin - Copy Trading
    message += f"🤖 **BLOFIN - COPY TRADING** 🤖\n"
    message += f"📈 5 positions | Copy trading active\n"
    message += f"📊 Multiple positions being tracked\n\n"
    
    # Kraken - Big Bags  
    message += f"💎 **KRAKEN - BIG BAGS** 💎\n"
    message += f"💰 9 bags | Total value: ~$60,000+\n"
    message += f"💎 $AVAX: +3.7% | $28,561 | Big bag\n"
    message += f"📊 $BERA: +0.7% | $14,687 | Good size\n"
    message += f"📊 7 more big bags tracked\n\n"
    
    message += f"📊 **SUMMARY**: 21 total positions across 3 exchanges\n"
    message += f"🎯 **URGENT**: XRP at +46% - prime time for profit taking!"
    
    # Prepare webhook payload
    payload = {
        "content": message,
        "username": "TITAN BOT",
        "avatar_url": "https://cdn.discordapp.com/attachments/1234567890/avatar.png"
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Portfolio alert sent successfully to Discord!")
            return True
        else:
            print(f"❌ Discord webhook failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error sending webhook: {e}")
        return False

if __name__ == "__main__":
    send_webhook_alert()