#!/usr/bin/env python3
"""
Start the Live Trade Scanner as a background service
"""

import asyncio
import signal
import sys
from datetime import datetime

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Shutting down Hourly Trade Scanner...")
    try:
        from comprehensive_market_scanner import stop_comprehensive_market_scanner
        stop_comprehensive_market_scanner()
    except:
        pass
    sys.exit(0)

async def main():
    """Main function to start the live trade scanner"""
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 COMPREHENSIVE MARKET SCANNER - THE ALPHA PLAYBOOK v4")
    print("=" * 70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📊 3-LAYER ANALYSIS: Technical + News + Social Sentiment")
    print("🔍 Scanning 1 coin every 20 seconds (18 coins per 6-minute batch)")
    print("🔄 Complete TOP 200 rotation every 66.7 minutes")
    print("📈 Confluence-based scoring (Technical + News + Social)")
    print("⚡ INSTANT alerts for quality opportunities (75%+ score)")
    print("🎯 No more inflated scores - confidence penalty for missing data")
    print("⚠️ Press Ctrl+C to stop")
    print("=" * 70)
    
    try:
        from comprehensive_market_scanner import start_comprehensive_market_scanner
        await start_comprehensive_market_scanner()
    except KeyboardInterrupt:
        print("\n🛑 Scanner stopped by user")
    except Exception as e:
        print(f"❌ Scanner error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())