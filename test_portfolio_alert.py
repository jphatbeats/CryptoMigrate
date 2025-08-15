#!/usr/bin/env python3
"""Test portfolio alert to show Discord formatting"""

import asyncio
import sys
import os
sys.path.append('.')

# Import the portfolio analysis function
from automated_trading_alerts import run_automated_analysis

async def test_portfolio_alert():
    """Run a single portfolio analysis to test Discord formatting"""
    print("🔍 Running test portfolio analysis...")
    try:
        await run_automated_analysis()
        print("✅ Test portfolio alert completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_portfolio_alert())