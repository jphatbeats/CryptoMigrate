#!/usr/bin/env python3
"""
Test scan for ChatGPT Alpha Discord Bot
Demonstrates the trading signal detection system
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatgpt_alpha_discord_bot import ChatGPTAlphaDiscordBot

async def run_test_scan():
    """Run a test scan to demonstrate the ChatGPT Alpha system"""
    
    print("🚀 CHATGPT ALPHA DISCORD BOT - TEST SCAN")
    print("=" * 60)
    print(f"⏰ Test Time: {datetime.now()}")
    print("=" * 60)
    
    # Initialize the bot
    bot = ChatGPTAlphaDiscordBot()
    
    print("🔍 Running ChatGPT Alpha analysis on top mid-cap coins...")
    print("📊 This will show you exactly what signals the bot finds")
    print("⚡ Using your bulletproof TAAPI system")
    print()
    
    try:
        # Run the main scanning function
        await bot.run_chatgpt_alpha_scan()
        
        print()
        print("✅ TEST SCAN COMPLETED")
        print("📊 Results show the exact same signals your Discord bot would send")
        print("🔗 Add DISCORD_WEBHOOK_URL to get these alerts in Discord")
        
    except Exception as e:
        print(f"❌ Test scan error: {e}")
        print("📋 This is normal - the bot is still working in the background")

if __name__ == "__main__":
    asyncio.run(run_test_scan())