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
    print("\n🛑 Shutting down Live Trade Scanner...")
    try:
        from live_trade_scanner import stop_live_trade_scanner
        stop_live_trade_scanner()
    except:
        pass
    sys.exit(0)

async def main():
    """Main function to start the live trade scanner"""
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 LIVE TRADE SCANNER SERVICE")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍 Scanning 20 tokens every 5 minutes")
    print("📊 Complete cycle every ~50 minutes (200 tokens)")
    print("📢 Callouts only for score >65 opportunities")
    print("⚠️ Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        from live_trade_scanner import start_live_trade_scanner
        await start_live_trade_scanner()
    except KeyboardInterrupt:
        print("\n🛑 Scanner stopped by user")
    except Exception as e:
        print(f"❌ Scanner error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())