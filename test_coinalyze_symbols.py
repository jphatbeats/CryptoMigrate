#!/usr/bin/env python3
"""
Test script to discover correct symbol format for Coinalyze API
"""

import requests
import json

def test_coinalyze_symbols():
    """Test different symbol formats to find the correct one"""
    print("🔍 Testing Coinalyze Symbol Formats")
    print("=" * 50)
    
    api_key = "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
    base_url = "https://api.coinalyze.net/v1"
    
    # Step 1: Get available future markets
    print("1. Getting available future markets...")
    try:
        response = requests.get(f"{base_url}/future-markets", params={'api_key': api_key}, timeout=10)
        if response.status_code == 200:
            markets = response.json()
            print(f"   ✅ Found {len(markets)} future markets")
            
            # Find BTC, ETH, XRP markets
            btc_markets = [m for m in markets if m.get('base_asset', '').upper() == 'BTC'][:3]
            eth_markets = [m for m in markets if m.get('base_asset', '').upper() == 'ETH'][:3]  
            xrp_markets = [m for m in markets if m.get('base_asset', '').upper() == 'XRP'][:3]
            
            print("   📊 BTC Markets:")
            for market in btc_markets:
                print(f"     - {market.get('symbol', 'N/A')} on {market.get('exchange', 'N/A')}")
            
            print("   📊 ETH Markets:")
            for market in eth_markets:
                print(f"     - {market.get('symbol', 'N/A')} on {market.get('exchange', 'N/A')}")
                
            print("   📊 XRP Markets:")
            for market in xrp_markets:
                print(f"     - {market.get('symbol', 'N/A')} on {market.get('exchange', 'N/A')}")
            
            # Step 2: Test funding rates with actual symbols
            if btc_markets:
                test_symbol = btc_markets[0]['symbol']
                print(f"\n2. Testing funding rates with symbol: {test_symbol}")
                
                try:
                    response = requests.get(
                        f"{base_url}/funding-rate", 
                        params={'symbols': test_symbol, 'api_key': api_key}, 
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ Funding rate data: {len(data)} items")
                        if data:
                            print(f"     - Symbol: {data[0].get('symbol', 'N/A')}")
                            print(f"     - Value: {data[0].get('value', 'N/A')}")
                            print(f"     - Update: {data[0].get('update', 'N/A')}")
                    else:
                        print(f"   ❌ Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
            
            # Step 3: Test open interest
            if btc_markets:
                test_symbol = btc_markets[0]['symbol']
                print(f"\n3. Testing open interest with symbol: {test_symbol}")
                
                try:
                    response = requests.get(
                        f"{base_url}/open-interest", 
                        params={'symbols': test_symbol, 'api_key': api_key}, 
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ Open interest data: {len(data)} items")
                        if data:
                            print(f"     - Symbol: {data[0].get('symbol', 'N/A')}")
                            print(f"     - Value: {data[0].get('value', 'N/A')}")
                            print(f"     - Update: {data[0].get('update', 'N/A')}")
                    else:
                        print(f"   ❌ Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
                    
        else:
            print(f"   ❌ Error getting markets: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Symbol discovery complete!")

if __name__ == "__main__":
    test_coinalyze_symbols()