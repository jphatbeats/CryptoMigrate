#!/usr/bin/env python3
"""
Start ChatGPT Alpha Discord Bot
Simple launcher for the ChatGPT trading bot with Discord alerts
"""

import os
import sys

def main():
    print("🚀 Starting ChatGPT Alpha Discord Bot...")
    print("📊 Integrating ChatGPT's trading strategy with Discord alerts")
    print("⚡ Using your bulletproof TAAPI rate limiting system")
    print("-" * 60)
    
    # Import and run
    try:
        from chatgpt_alpha_discord_bot import ChatGPTAlphaDiscordBot
        
        bot = ChatGPTAlphaDiscordBot()
        print("✅ Bot initialized successfully")
        print("🔄 Starting scheduled scans every 30 minutes...")
        print("💬 Alerts will be sent to Discord callouts channel (1403926917694099496)")
        print("⚠️ Press Ctrl+C to stop")
        print("-" * 60)
        
        bot.start_scheduler()
        
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()