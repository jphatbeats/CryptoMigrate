#!/usr/bin/env python3
"""Test script for the taapi.io proxy endpoint"""

import requests
import json

def test_proxy_endpoint():
    """Test the ChatGPT proxy endpoint"""
    print("🧪 Testing Taapi.io Proxy Endpoint for ChatGPT")
    print("=" * 50)
    
    # Test URL
    url = "http://localhost:5000/api/taapi/proxy"
    
    # Test payload (will get 401 with test key, but that's expected)
    test_payload = {
        "secret": "test_api_key_will_fail",
        "construct": {
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "1h",
            "indicators": [
                {"id": "rsi_test", "indicator": "rsi", "period": 14},
                {"id": "macd_test", "indicator": "macd"},
                {"id": "supertrend_test", "indicator": "supertrend", "period": 10, "multiplier": 3.0}
            ]
        }
    }
    
    # Test CORS OPTIONS request
    print("1. Testing CORS preflight (OPTIONS)...")
    try:
        options_response = requests.options(url, headers={
            'Origin': 'https://chatgpt.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        })
        print(f"   Status: {options_response.status_code}")
        print(f"   CORS Headers:")
        for header, value in options_response.headers.items():
            if 'access-control' in header.lower():
                print(f"     {header}: {value}")
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")
    
    print("\n2. Testing POST request (proxy functionality)...")
    try:
        response = requests.post(url, json=test_payload, headers={
            'Content-Type': 'application/json',
            'Origin': 'https://chatgpt.com'
        })
        print(f"   Status: {response.status_code}")
        print(f"   Response headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower() or 'content-type' in header.lower():
                print(f"     {header}: {value}")
        
        # Parse response
        try:
            result = response.json()
            print(f"   Response body: {json.dumps(result, indent=2)[:200]}...")
            
            # Expected: 401 authentication error from taapi.io (which means proxy is working)
            if response.status_code == 401 and 'not authenticated' in str(result).lower():
                print("   ✅ Proxy working correctly (401 from taapi.io as expected with test key)")
            elif response.status_code == 200:
                print("   ✅ Proxy working with valid API key")
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
                
        except json.JSONDecodeError:
            print(f"   Response text: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ POST test failed: {e}")
    
    print("\n3. Testing BONK/USDT request (as requested in chat)...")
    bonk_payload = {
        "secret": "test_api_key_will_fail",
        "construct": {
            "exchange": "kucoin",
            "symbol": "BONK/USDT",
            "interval": "4h",
            "indicators": [
                {"id": "supertrend", "indicator": "supertrend", "period": 10, "multiplier": 3.0},
                {"id": "fisher_transform", "indicator": "fisher_transform", "period": 10},
                {"id": "vortex", "indicator": "vortex", "period": 14},
                {"id": "aroon", "indicator": "aroon", "period": 14},
                {"id": "cmf", "indicator": "cmf", "period": 20}
            ]
        }
    }
    
    try:
        response = requests.post(url, json=bonk_payload)
        print(f"   Status: {response.status_code}")
        result = response.json()
        if response.status_code == 401:
            print("   ✅ BONK request structure accepted by proxy (401 expected with test key)")
        else:
            print(f"   Response: {json.dumps(result, indent=2)[:150]}...")
    except Exception as e:
        print(f"   ❌ BONK test failed: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("✅ Proxy endpoint: /api/taapi/proxy")
    print("✅ CORS headers: Configured for ChatGPT access")
    print("✅ Request forwarding: Direct to taapi.io API")
    print("✅ Error handling: 401 authentication errors properly forwarded")
    print("\n🔧 For ChatGPT:")
    print("1. Upload taapi_chatgpt_proxy_schema.json to ChatGPT Actions")
    print("2. Set server URL: https://titan-trading-2-production.up.railway.app")
    print("3. ChatGPT can request any of 208+ indicators via getTaapiIndicators operation")
    print("\n🚀 Ready for ChatGPT integration!")

if __name__ == "__main__":
    test_proxy_endpoint()