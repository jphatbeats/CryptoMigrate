#!/usr/bin/env python3
"""
Test script to verify ENA search fix for CryptoNews API
"""

import sys
import os
sys.path.append('.')

from crypto_news_api import CryptoNewsAPI

def test_ena_search():
    """Test ENA search using the fixed API methods"""
    
    print("🧪 Testing ENA Search Fix...")
    
    api = CryptoNewsAPI()
    
    # Test 1: Portfolio news for ENA
    print("\n📰 Test 1: Portfolio news for ENA")
    result = api.get_portfolio_news(['ENA'], limit=5)
    
    if 'data' in result and len(result['data']) > 0:
        print(f"✅ SUCCESS: Found {len(result['data'])} ENA articles")
        print(f"   Sample: {result['data'][0].get('title', 'No title')[:70]}...")
    else:
        print(f"❌ FAILED: {result}")
    
    # Test 2: Symbol search for ENA
    print("\n🔍 Test 2: Symbol search for ENA")  
    result = api.get_news_by_symbols(['ENA'], limit=5, mode='laser')
    
    if 'data' in result and len(result['data']) > 0:
        print(f"✅ SUCCESS: Found {len(result['data'])} ENA articles")
        print(f"   Sample: {result['data'][0].get('title', 'No title')[:70]}...")
    else:
        print(f"❌ FAILED: {result}")
    
    # Test 3: Multi-symbol search
    print("\n🎯 Test 3: Multi-symbol search (ENA + BTC)")
    result = api.get_news_by_symbols(['ENA', 'BTC'], limit=5, mode='broad')
    
    if 'data' in result and len(result['data']) > 0:
        print(f"✅ SUCCESS: Found {len(result['data'])} articles")
        ena_articles = [a for a in result['data'] if 'ENA' in a.get('title', '').upper() or 'ETHENA' in a.get('title', '').upper()]
        print(f"   ENA-specific articles: {len(ena_articles)}")
    else:
        print(f"❌ FAILED: {result}")
    
    print(f"\n🎉 ENA search testing complete!")

if __name__ == "__main__":
    test_ena_search()