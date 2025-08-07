#!/usr/bin/env python3
"""
Test crypto news with images functionality
Tests both the CryptoNews API directly and the new Railway endpoints
"""

import requests
import json
from datetime import datetime

def test_direct_cryptonews_api():
    """Test CryptoNews API directly to see image URLs"""
    print("🔍 Testing CryptoNews API directly for image URLs...")
    
    try:
        # Test with BTC ticker
        url = "https://cryptonews-api.com/api/v1"
        params = {
            'tickers': 'BTC',
            'items': 3,
            'token': 'ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('data'):
            print(f"✅ Found {len(data['data'])} articles")
            
            for i, article in enumerate(data['data'], 1):
                print(f"\n📰 Article {i}:")
                print(f"   Title: {article.get('title', 'No title')[:60]}...")
                print(f"   Source: {article.get('source_name', 'Unknown')}")
                print(f"   Image URL: {article.get('image_url', 'No image')}")
                print(f"   Has Image: {'✅' if article.get('image_url') else '❌'}")
                print(f"   Sentiment: {article.get('sentiment', 'Unknown')}")
        else:
            print("❌ No articles found")
            print(f"Response: {data}")
            
    except Exception as e:
        print(f"❌ Error testing direct API: {e}")

def test_railway_image_endpoint():
    """Test the new Railway endpoint for images"""
    print("\n🚀 Testing Railway endpoint for crypto news with images...")
    
    try:
        # Test the new image endpoint
        url = "http://localhost:5000/api/crypto-news-with-images"
        params = {
            'tickers': 'BTC,ETH',
            'items': 3
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and data.get('data'):
                print(f"✅ Railway endpoint working! Found {len(data['data'])} articles with images")
                
                for i, article in enumerate(data['data'], 1):
                    print(f"\n🖼️ Article {i} with Image:")
                    print(f"   Title: {article.get('title', 'No title')[:60]}...")
                    print(f"   Source: {article.get('source', 'Unknown')}")
                    print(f"   Image URL: {article.get('image_url', 'No image')}")
                    print(f"   Sentiment: {article.get('sentiment', 'Unknown')} {article.get('sentiment_emoji', '')}")
                    print(f"   Tickers: {', '.join(article.get('tickers', []))}")
                    
                print(f"\n📊 Summary:")
                print(f"   Total articles processed: {data.get('total_articles_processed', 0)}")
                print(f"   Articles with images: {data.get('count', 0)}")
                print(f"   Images guaranteed: {data.get('images_guaranteed', False)}")
                
            else:
                print("⚠️ No articles with images found")
                print(f"Response: {data}")
        else:
            print(f"❌ Railway endpoint error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Railway endpoint: {e}")

def test_discord_formatted_news():
    """Test how the news would look in Discord format"""
    print("\n💬 Testing Discord formatting with images...")
    
    try:
        from automated_trading_alerts import create_enhanced_breaking_news_alert_with_images
        from crypto_news_api import CryptoNewsAPI
        
        # Get real news data
        crypto_news_api = CryptoNewsAPI()
        result = crypto_news_api.get_breaking_news(limit=3)
        
        if result and result.get('data'):
            articles = result['data']
            discord_message = create_enhanced_breaking_news_alert_with_images(articles)
            
            print("🎯 Discord Message Preview:")
            print("=" * 60)
            print(discord_message)
            print("=" * 60)
            
            # Count images
            image_count = discord_message.count('https://crypto.snapi.dev')
            print(f"\n📸 Images included: {image_count}")
            
        else:
            print("❌ No news data available for Discord test")
            
    except Exception as e:
        print(f"❌ Error testing Discord formatting: {e}")

if __name__ == "__main__":
    print("🧪 CRYPTO NEWS IMAGES TEST")
    print("=" * 50)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_direct_cryptonews_api()
    test_railway_image_endpoint()
    test_discord_formatted_news()
    
    print(f"\n✅ All tests completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")