#!/usr/bin/env python3
"""
Test script for taapi.io bulk API integration
"""

import requests
import json
import time

def test_bulk_api():
    """Test the bulk API endpoint after 5 minute wait period"""
    print("🔍 Testing taapi.io bulk API integration...")
    print("⏰ Waiting for API key cooldown period...")
    
    # Test bulk endpoint via our server
    bulk_payload = {
        "symbol": "ETHUSDT",
        "interval": "1h", 
        "exchange": "binance",
        "indicators": [
            {"id": "rsi_test", "indicator": "rsi", "period": 14},
            {"id": "ema_test", "indicator": "ema", "period": 20},
            {"id": "macd_test", "indicator": "macd"}
        ]
    }
    
    try:
        print("📡 Testing bulk endpoint...")
        response = requests.post(
            "http://localhost:5000/api/indicators/bulk",
            json=bulk_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Bulk API test error: {e}")
    
    # Test comprehensive endpoint with POST
    try:
        print("\n📡 Testing comprehensive endpoint with POST...")
        comp_payload = {
            "interval": "1h",
            "indicators": [
                {"id": "rsi_comp", "indicator": "rsi"},
                {"id": "bb_comp", "indicator": "bbands"}
            ]
        }
        
        response = requests.post(
            "http://localhost:5000/api/indicators/comprehensive/BTCUSDT",
            json=comp_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        if 'indicators' in result:
            print(f"Indicators found: {list(result['indicators'].keys())}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"❌ Comprehensive API test error: {e}")

if __name__ == "__main__":
    test_bulk_api()