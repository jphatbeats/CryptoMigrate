#!/usr/bin/env python3
"""
Test script for taapi.io technical indicators integration
"""

import os
from taapi_indicators import TaapiIndicators

def test_taapi_integration():
    print("🔍 Testing taapi.io technical indicators integration...")
    
    # Initialize indicators
    taapi = TaapiIndicators()
    
    # Check API key
    api_key = os.getenv('TAAPI_API_KEY')
    if api_key:
        print(f"✅ API key configured (length: {len(api_key)})")
    else:
        print("❌ No API key found")
        return
    
    # Test symbols
    test_symbols = ['ETHUSDT', 'BTCUSDT', 'XRPUSDT']
    
    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}...")
        
        # Test RSI
        try:
            rsi_result = taapi.get_rsi(symbol, '1h', 14)
            if 'error' in rsi_result:
                print(f"⚠️ RSI error: {rsi_result['error']}")
            else:
                print(f"✅ RSI: {rsi_result}")
        except Exception as e:
            print(f"❌ RSI exception: {e}")
        
        # Test comprehensive analysis
        try:
            comp_result = taapi.get_comprehensive_analysis(symbol, '1h')
            if 'error' in comp_result:
                print(f"⚠️ Comprehensive analysis error: {comp_result.get('error', 'Unknown error')}")
            else:
                print(f"✅ Comprehensive analysis completed")
                print(f"   Indicators found: {list(comp_result.get('indicators', {}).keys())}")
        except Exception as e:
            print(f"❌ Comprehensive analysis exception: {e}")
        
        break  # Test only first symbol to avoid API rate limits

if __name__ == "__main__":
    test_taapi_integration()