#!/usr/bin/env python3
"""
START DISCORD GPT BOT
====================
Launch script for the Discord GPT-5 command system.
"""

import asyncio
import os
import logging
from discord_gpt_command_system import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check required environment variables"""
    required_vars = ['DISCORD_TOKEN', 'OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ All required environment variables found")
    return True

async def start_bot():
    """Start the Discord GPT command bot"""
    print("🤖 DISCORD GPT-5 COMMAND SYSTEM")
    print("=" * 50)
    print("🚀 Initializing Discord bot with GPT-5 integration...")
    print("📊 Available commands:")
    print("   /portfolio - GPT-5 portfolio analysis")
    print("   /analyze [symbol] - Complete crypto analysis")
    print("   /scan [type] - Trading scans")
    print("   /fullscan - Complete market scan")
    print("   /news [symbol] - AI-filtered news")
    print("   /token [id] - Token research")
    print("   /ask [question] - Direct GPT-5 conversation")
    print("   /opinion [topic] - GPT-5 market opinion")
    print("   /status - System status check")
    print("=" * 50)
    
    if not check_environment():
        print("❌ Environment check failed - cannot start bot")
        return
    
    try:
        await main()
    except KeyboardInterrupt:
        print("\n🛑 Bot shutdown requested")
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(start_bot())