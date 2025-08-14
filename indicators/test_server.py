#!/usr/bin/env python3
"""
Simple test script to verify server functionality locally
"""

import requests
import json

def test_local_server():
    """Test the indicators server locally"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Technical Indicators Server")
    print("="*50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
    
    # Test enhanced intelligence
    try:
        response = requests.get(f"{base_url}/api/enhanced-intelligence/BTC-USDT", timeout=15)
        if response.status_code == 200:
            print("✅ Enhanced intelligence: PASSED")
        else:
            print(f"❌ Enhanced intelligence: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Enhanced intelligence: ERROR - {e}")
    
    # Test single indicator
    try:
        response = requests.get(f"{base_url}/api/taapi/indicators/BTC/USDT?indicator=rsi", timeout=15)
        if response.status_code == 200:
            print("✅ Single indicator: PASSED")
        else:
            print(f"❌ Single indicator: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Single indicator: ERROR - {e}")
    
    # Test bulk indicators
    try:
        payload = {
            "symbol": "BTC/USDT",
            "indicators": [
                {"indicator": "rsi"},
                {"indicator": "macd"}
            ],
            "interval": "1h"
        }
        response = requests.post(f"{base_url}/api/taapi/bulk", json=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Bulk indicators: PASSED")
        else:
            print(f"❌ Bulk indicators: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Bulk indicators: ERROR - {e}")
    
    print("="*50)
    print("🧪 Testing complete!")

if __name__ == "__main__":
    test_local_server()