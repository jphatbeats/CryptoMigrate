#!/usr/bin/env python3
"""
Test BingX pricing endpoint fix directly
"""

import sys
sys.path.append('.')

from exchange_manager import exchange_manager
import trading_functions
import json

def test_pricing_fix():
    """Test the BingX pricing fix"""
    
    print("Testing BingX pricing fix...")
    
    if 'bingx' in exchange_manager.get_available_exchanges():
        # Test spot pricing
        print("\n1. Testing BTC/USDT (spot):")
        try:
            spot_ticker = trading_functions.get_ticker('bingx', 'BTC/USDT')
            print(f"   Spot price: ${spot_ticker.get('last')}")
            print(f"   Bid/Ask: ${spot_ticker.get('bid')} / ${spot_ticker.get('ask')}")
        except Exception as e:
            print(f"   Spot error: {e}")
        
        # Test futures pricing  
        print("\n2. Testing BTC/USDT:USDT (futures):")
        try:
            futures_ticker = trading_functions.get_ticker('bingx', 'BTC/USDT:USDT')
            print(f"   Futures price: ${futures_ticker.get('last')}")
            print(f"   Bid/Ask: ${futures_ticker.get('bid')} / ${futures_ticker.get('ask')}")
        except Exception as e:
            print(f"   Futures error: {e}")
        
        # Show price difference
        print("\n3. Price difference analysis:")
        try:
            spot_price = float(trading_functions.get_ticker('bingx', 'BTC/USDT').get('last', 0))
            futures_price = float(trading_functions.get_ticker('bingx', 'BTC/USDT:USDT').get('last', 0))
            
            difference = spot_price - futures_price
            percentage = (difference / spot_price) * 100 if spot_price > 0 else 0
            
            print(f"   Spot price: ${spot_price:,.2f}")
            print(f"   Futures price: ${futures_price:,.2f}")
            print(f"   Difference: ${difference:,.2f} ({percentage:.3f}%)")
            
            if abs(difference) > 50:
                print(f"   ⚠️  SIGNIFICANT PRICE DIFFERENCE - This could cause ChatGPT confusion!")
            else:
                print(f"   ✅ Prices are close - normal market conditions")
                
        except Exception as e:
            print(f"   Analysis error: {e}")
    else:
        print("BingX not available")

if __name__ == "__main__":
    test_pricing_fix()