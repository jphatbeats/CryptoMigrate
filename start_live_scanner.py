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
        from hourly_trade_scanner import stop_hourly_trade_scanner
        stop_hourly_trade_scanner()
    except:
        pass
    sys.exit(0)

async def main():
    """Main function to start the live trade scanner"""
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 HOURLY TRADE SCANNER SERVICE")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍 Scanning 20 tokens every 6 minutes (10 batches per hour)")
    print("📊 Complete TOP 200 analysis every hour")
    print("📈 Full TA + News + Sentiment for each coin")
    print("⚡ INSTANT alerts for quality trades (score >70)")
    print("🎯 Get alerts the moment opportunities appear")
    print("⚠️ Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        from hourly_trade_scanner import start_hourly_trade_scanner
        await start_hourly_trade_scanner()
    except KeyboardInterrupt:
        print("\n🛑 Scanner stopped by user")
    except Exception as e:
        print(f"❌ Scanner error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())