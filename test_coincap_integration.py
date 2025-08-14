#!/usr/bin/env python3
"""
Test script for CoinCap FREE API integration
"""

import sys
sys.path.append('mcp_servers')

import asyncio
from coincap_mcp_integration import coincap_client, initialize_coincap_mcp, get_market_data, get_top_performers

async def test_coincap():
    print("🚀 Testing CoinCap FREE API Integration...")
    
    # Test initialization
    success = await initialize_coincap_mcp()
    print(f"✅ Initialization: {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        # Test Bitcoin price
        btc_data = get_market_data('BTC')
        print(f"📊 BTC Data: {btc_data}")
        
        # Test top performers
        top_5 = get_top_performers(5)
        print(f"🏆 Top 5 cryptos: {len(top_5)} retrieved")
        if top_5:
            print(f"   - {top_5[0]['symbol']}: ${top_5[0]['price_usd']}")

if __name__ == "__main__":
    asyncio.run(test_coincap())