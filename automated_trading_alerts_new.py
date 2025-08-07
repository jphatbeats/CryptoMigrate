#!/usr/bin/env python3
"""
Automated Trading Alerts System (REBUILT)
Reads positions CSV, analyzes trading opportunities, and generates Discord alerts
Now uses the new two-part alpha system: Early Alpha + Established Coin News
"""

import asyncio
import aiohttp
import json
import os
import pandas as pd
import logging
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

async def run_alpha_analysis():
    """Generate real alpha opportunities for #alpha-scans channel using new two-part system"""
    try:
        print("\n🔍 ALPHA OPPORTUNITIES - Using new two-part system...")
        
        early_opportunities = []
        established_news = []
        
        # Part 1: Early Alpha Detection (opportunities BEFORE they pump)
        try:
            from early_alpha_detector import detect_early_alpha_opportunities, format_early_alpha_for_discord
            early_opportunities = await detect_early_alpha_opportunities()
            
            if early_opportunities:
                early_message = format_early_alpha_for_discord(early_opportunities)
                await send_discord_alert(early_message, 'alpha_scans')
                print("✅ Early alpha opportunities sent to Discord #alpha-scans")
            
        except Exception as e:
            print(f"⚠️ Early alpha detector error: {e}")
        
        # Part 2: Established Coin News (topping signals, short opportunities)
        try:
            from established_coin_news import monitor_established_coin_news, format_established_news_for_discord
            established_news = await monitor_established_coin_news()
            
            if established_news:
                news_message = format_established_news_for_discord(established_news)
                await send_discord_alert(news_message, 'alpha_scans')
                print("✅ Established coin news sent to Discord #alpha-scans")
            
        except Exception as e:
            print(f"⚠️ Established news monitor error: {e}")
        
        # If both systems found nothing, send status update
        if not early_opportunities and not established_news:
            no_opportunities_message = (
                "🔍 **ALPHA ANALYSIS** 🔍\n\n"
                "⏳ No early alpha signals or topping patterns detected.\n"
                "🔎 Monitoring:\n"
                "• **Early Alpha**: Pre-listing signals, accumulation patterns\n"
                "• **Established Coins**: Topping signals, distribution patterns\n\n"
                "🎯 **Strategy**: Wait for clear setups - don't chase pumps!"
            )
            await send_discord_alert(no_opportunities_message, 'alpha_scans')
            print("✅ No-opportunities status sent to #alpha-scans")
        
        return
        
    except Exception as e:
        print(f"❌ Alpha analysis system error: {e}")
        # Send error message
        error_message = (
            "⚠️ **ALPHA ANALYSIS SYSTEM** ⚠️\n\n"
            "🔧 System temporarily unavailable.\n"
            "🔄 Please wait for next analysis cycle.\n\n"
            "📊 **Hourly Trade Scanner** is still active and monitoring for instant alerts."
        )
        await send_discord_alert(error_message, 'alpha_scans')
        print("⚠️ Alpha system error message sent")
        return

async def send_discord_alert(message, channel_type='alerts'):
    """Send alert to Discord using webhooks"""
    try:
        # Map channel types to webhook environment variables
        webhook_map = {
            'alerts': 'DISCORD_WEBHOOK_ALERTS',
            'portfolio': 'DISCORD_WEBHOOK_PORTFOLIO', 
            'alpha_scans': 'DISCORD_WEBHOOK_ALPHA_SCANS',
            'degen_memes': 'DISCORD_WEBHOOK_DEGEN_MEMES'
        }
        
        webhook_var = webhook_map.get(channel_type, 'DISCORD_WEBHOOK_ALERTS')
        webhook_url = os.getenv(webhook_var)
        
        if not webhook_url:
            print(f"⚠️ No webhook configured for {channel_type}")
            return
        
        # Send message
        async with aiohttp.ClientSession() as session:
            payload = {'content': message}
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    print(f"✅ Alert sent to #{channel_type}")
                else:
                    print(f"❌ Failed to send to #{channel_type}: {response.status}")
                    
    except Exception as e:
        print(f"❌ Discord alert error: {e}")

async def main():
    """Main function to run alpha analysis"""
    await run_alpha_analysis()

if __name__ == "__main__":
    asyncio.run(main())